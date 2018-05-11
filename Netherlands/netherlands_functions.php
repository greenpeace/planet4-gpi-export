<?php

/**
 * Add styling to blockquote.
 *
 * @param $text
 * @param $blockquote1
 * @param $blockquote2
 * @param $blockquote3
 *
 * @return mixed
 */
function add_blockquote_style( $text, $blockquote1, $blockquote2, $blockquote3 ) {

	$new_blockquote1 = str_replace( '<blockquote', '<blockquote style="display: block; margin-top: 1em; margin-bottom: 1em; margin-left: 40px !important; margin-right: 40px !important;"', $blockquote1 );
	$text = str_replace( $blockquote1, $new_blockquote1, $text );

	$new_blockquote2 = str_replace( '<blockquote', '<blockquote style="display: block; margin-top: 1em; margin-bottom: 1em; margin-left: 40px !important; margin-right: 40px !important;"', $blockquote2 );
	$text = str_replace( $blockquote2, $new_blockquote2, $text );

	$new_blockquote3 = str_replace( '<blockquote', '<blockquote style="display: block; margin-top: 1em; margin-bottom: 1em; margin-left: 40px !important; margin-right: 40px !important;"', $blockquote3 );
	$text = str_replace( $blockquote3, $new_blockquote3, $text );

	return $text;
}

/**
 * Align floated images correctly.
 *
 * @param $text
 * @param $image
 *
 * @return mixed
 */
function add_image_class( $text, $image ) {
	if ( strpos( $image, 'float: left;' ) !== false ) {
		$text = str_replace( '<img', '<img class="alignleft"', $text );
	} elseif ( strpos( $image, 'float: right;') !== false ) {
		$text = str_replace( '<img', '<img class="alignright"', $text );
	}

	return $text;
}

/**
 * Fix attachments url.
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
function replace_all_attachments( $text, $pdf, $images1, $images2, $images3, $images4, $images5, $images6, $images7, $images8, $images9, $images10,
	$images11, $images12, $images13, $images14, $images15, $images16, $images17, $images18, $images19, $images20, $images21, $images22, $images23, $images24 ) {

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
	$text = replace_attachment($text, $images24);
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
