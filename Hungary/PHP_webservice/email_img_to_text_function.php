<?php
/*
 * Below script is use to manully call OCR API and save parse results in DB, for manual review purpose.
*/

require_once "connection.php";

$url_list = array(
	"https://www.greenpeace.org/hungary/Global/hungary/kepek/43196556620_25ca5e1223_z.jpg",
	"https://www.greenpeace.org/hungary/PageFiles/762795/37031050990_53306b49bd_k.jpg",
);

foreach ( $url_list as $url) {
	process_request($url);
	sleep(5);
}


function process_request( $img_url ) {
	
	global $conn;
	$email_text = "";

	$sql = "SELECT email_text FROM email_img_to_text WHERE email_img_url = '".$img_url."'";
	$result = $conn->query($sql);

	if ($result->num_rows > 0) {
		// output data of each row.
		while($row = $result->fetch_assoc()) {
			$email_text = $row["email_text"];
			break;
		}
	} else {
		if ( $img_url ) {
			$email_text = api_call( $img_url );

			// Validate the email id.
			if ( !filter_var( $email_text, FILTER_VALIDATE_EMAIL )) {
				$email_text = str_replace(".or.;",".org",$email_text );
			}

			// Insert it into DB.
			$sql = "INSERT INTO email_img_to_text (email_img_url, email_text) VALUES ('".$img_url."', '".$email_text."')";
			$conn->query($sql);
		}
	}

	echo $email_text;

	if ($email_text == "")
		$email_text = "Email field is blank";

	// Log request
	$sql = "INSERT INTO api_request_logs (url, email_text) VALUES ('".$img_url."', '".$email_text."')";
	$conn->query($sql);

	$conn->close();

}

/**
 * Call OCR API and return the text from image.
 *
 * @param string $image_url The p3 email image url.
 *
 * @return string
 */
function api_call( $image_url ) {

	//$api_key   = "2777dc471788957";
	//$api_url   = "https://api.ocr.space/parse/imageurl";
	//$image_url = "http://www.greenpeace.org/canada/Templates/Planet3/Styles/Images/emailimages/0644d173c2da766215d59d6dfa12235b.png";
	global $api_key, $api_url;

	$end_point_url = $api_url."?apikey=".$api_key."&url=".$image_url;

	$responce = file_get_contents( $end_point_url );

	$result = json_decode($responce, true);

	if ( isset ($result['ParsedResults'][0]['ParsedText']) )
		return $result['ParsedResults'][0]['ParsedText'];
	else
		return '';
}

?>

