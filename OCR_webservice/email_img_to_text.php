<?php
/*
 * Below script is accept the image url as a param and consume OCR API and return back the email id in text.
*/

require_once "connection.php";

global $conn;

$img_url = $_GET['url'] ?? '';

if ( $img_url ) {
	$sql    = "SELECT email_text FROM email_img_to_text WHERE email_img_url = '" . $img_url . "'";
	$result = $conn->query( $sql );

	if ( 0 === $result->num_rows ) {
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
			$email_parts                              = explode( '.', $email_text );
			$email_parts[ count( $email_parts ) - 1 ] = 'org';
			$email_text                               = implode( '.', $email_parts );
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
$conn->close();

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
