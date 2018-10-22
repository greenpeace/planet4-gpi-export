<?php
/*
 * Below script is use to manully call OCR API and save parse results in DB, for manual review purpose.
*/

require_once "connection.php";

$url_list = array(
	# Hungary
	"http://www.greenpeace.org/hungary/Templates/Planet3/Styles/Images/emailimages/cdd24241662884c667a3c9af8b634930.png",
	"http://www.greenpeace.org/hungary/Templates/Planet3/Styles/Images/emailimages/f7316b2e2ab0b1de6312713175270b8f.png",
	"http://www.greenpeace.org/hungary/Global/hungary/kampanyok/atomenergia/p2-180309.jpg",
);

global $conn;

foreach ( $url_list as $url) {
	process_request($url);
}
$conn->close();

echo '<a href="review_parsed_email_id.php">Review results</a><br />' .
     '<br /><a href="index.php">Back</a>';

function process_request( $img_url ) {
	global $conn;

	if ( $img_url ) {
		$email_text = api_call( $img_url );

		if ( $email_text ) {
			$email_text = str_replace( ' ', '', $email_text );
			$email_text = str_replace( 'qreenpeace', 'greenpeace', $email_text );
			$email_text = str_replace( 'aqreenpeace', '@greenpeace', $email_text );
			$email_text = str_replace( '@qreenpeace', '@greenpeace', $email_text );
			$email_text = str_replace( 'agreenpeace', '@greenpeace', $email_text );
		}

		// Validate the email id.
		if ( $email_text && ! filter_var( $email_text, FILTER_VALIDATE_EMAIL ) ) {
			$email_parts = explode( '.', $email_text );
			$email_parts[ count( $email_parts ) - 1 ] = 'org';
			$email_text = implode( '.', $email_parts );
		}
		echo $email_text . '<br />';

		// Insert it into DB.
		if ( 'org' !== $email_text ) {
			$sql  = "INSERT INTO email_img_to_text (email_img_url, email_text) VALUES (?, ?)";
			$stmt = $conn->prepare( $sql );
			$stmt->bind_param( 'ss', $img_url, $email_text );
			$stmt->execute();
		}
	}
}

/**
 * Call OCR API and return the text from image.
 *
 * @param string $image_url The p3 email image url.
 *
 * @return string
 */
function api_call( $image_url ) {
	global $api_key, $api_url;

	$end_point_url = $api_url."?apikey=".$api_key."&url=".$image_url;
	$response      = file_get_contents( $end_point_url );
	$result        = json_decode( $response, true );

	if ( isset ( $result['ParsedResults'][0]['ParsedText'] ) )
		return $result['ParsedResults'][0]['ParsedText'];
	return '';
}
