<?php

/**
 * Fix attachments urls.
 *
 * @param $text
 * @param $pdf
 * @param $images1
 * @param $images2
 * @param $images3
 * @param $images4
 * @param $images5
 * @param $images6
 * @param $images7
 * @param $images8
 * @param $images9
 * @param $images10
 * @param $images11
 * @param $images12
 * @param $images13
 * @param $images14
 * @param $images15
 * @param $images16
 * @param $images17
 * @param $images18
 * @param $images19
 * @param $images20
 * @param $images21
 * @param $images22
 * @param $images23
 * @param $images24
 *
 * @return mixed
 */
function replace_all_attachments($text, $pdf, $images1, $images2, $images3, $images4, $images5, $images6, $images7, $images8, $images9, $images10,
$images11, $images12, $images13, $images14, $images15, $images16, $images17, $images18, $images19, $images20, $images21, $images22, $images23 ) {

	$text = replace_attachment($text, $pdf);
	$text = replace_attachment($text, $images1);
	$text = replace_attachment($text, $images2);
	$text = replace_attachment($text, $images3);
	$text = replace_attachment($text, $images4);
	$text = replace_attachment($text, $images5);
	$text = replace_attachment($text, $images6);
	$text = replace_attachment($text, $images7);
	$text = replace_attachment($text, $images8);
	$text = replace_attachment($text, $images9);
	$text = replace_attachment($text, $images10);
	$text = replace_attachment($text, $images11);
	$text = replace_attachment($text, $images12);
	$text = replace_attachment($text, $images13);
	$text = replace_attachment($text, $images14);
	$text = replace_attachment($text, $images15);
	$text = replace_attachment($text, $images16);
	$text = replace_attachment($text, $images17);
	$text = replace_attachment($text, $images18);
	$text = replace_attachment($text, $images19);
	$text = replace_attachment($text, $images20);
	$text = replace_attachment($text, $images21);
	$text = replace_attachment($text, $images22);
	$text = replace_attachment($text, $images23);

	return $text;

}

/**
 * Fix attachments url.
 *
 * @param $text
 * @param $attachment
 *
 * @return mixed
 */
function replace_attachment($text, $attachment) {
	$basename = basename($attachment);

	$basename = preg_replace_callback('/\.\w+$/', function($m){
	   return strtolower($m[0]);
	}, $basename);
	
	$basename = str_replace(' ', '-', urldecode($basename));
	$bodytag = str_replace($attachment, get_site_url(). "/wp-content/uploads/2018/05/". $basename , $text);

	return $bodytag;
}

?>
