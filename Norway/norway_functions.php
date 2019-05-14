<?php

// Hooks.
add_action( 'pmxi_saved_post', 'post_saved', 10, 1 );
add_action( 'pmxi_attachment_uploaded', 'fix_attachment_uploaded', 10, 3);

/**
 * Add styling to blockquote.
 *
 * @param string $text
 * @param array  $blockquotes Variable number of params, so that we can fix multiple blockquotes in same post.
 *
 * @return mixed
 */
function add_blockquote_style( $text, ...$blockquotes ) {
	foreach ( $blockquotes as $blockquote ) {
		$new_blockquote = str_replace( '<blockquote', '<blockquote style="display: block; margin-top: 1em; margin-bottom: 1em; margin-left: 40px !important; margin-right: 40px !important;"', $blockquote );
		$text           = str_replace( $blockquote, $new_blockquote, $text );
	}

	return $text;
}

/**
 * Align floated images correctly.
 *
 * @param string $text The post content.
 * @param array  $elements Variable number of params, so that we can align multiple images in same post.
 *
 * @return mixed
 */
function align_images( $text, ...$elements  ) {
	foreach( $elements as $element ) {
		if ( strpos( $element, 'float: left;' ) !== false ) {
			$text = str_replace( '<img', '<img class="alignleft"', $text );
		} elseif ( strpos( $element, 'float: right;' ) !== false ) {
			$text = str_replace( '<img', '<img class="alignright"', $text );
		} elseif ( strpos( $element, 'events-box middle-box left' ) !== false ) {
			$text = str_replace( 'events-box middle-box left', 'events-box middle-box alignleft', $text );
			$text = str_replace( '<img', '<img class="Thumbnail alignleft"', $text );
		} elseif ( strpos( $element, 'events-box middle-box right' ) !== false ) {
			$text = str_replace( 'events-box middle-box right', 'events-box middle-box alignright', $text );
			$text = str_replace( '<img', '<img class="Thumbnail alignright"', $text );
		}
	}

	return $text;
}

/**
 * Fix attachments url.
 *
 * @param string $text
 * @param string $pdf
 * @param array  $images
 *
 * @return mixed
 */
function replace_all_attachments( $text, $pdf, ...$images ) {

	$text = replace_attachment($text, $pdf);
	foreach ( $images as $image ) {
		$text = replace_attachment($text, $image);
	}

	return $text;
}

/**
 * @param $text
 * @param $attachment
 *
 * @return mixed
 */
function replace_attachment( $text, $attachment ) {
	$basename = basename($attachment);
	$basename = preg_replace_callback('/\.\w+$/', function($m){
		return strtolower($m[0]);
	}, $basename);
	$basename = str_replace(' ', '-', urldecode($basename));
	$basename = str_replace('-----', '-', urldecode($basename));
	$basename = str_replace('----', '-', urldecode($basename));
	$basename = str_replace('---', '-', urldecode($basename));
	$basename = str_replace('--', '-', urldecode($basename));
	$basename = str_replace("'", "", urldecode($basename));
	$basename = str_replace('%20', '-', urldecode($basename));
	$basename = str_replace("(", "", urldecode($basename));
	$basename = str_replace(")", "", urldecode($basename));
	$bodytag  = str_replace($attachment, "https://storage.googleapis.com/planet4-norway-stateless/2019/04/". $basename , $text);

	return $bodytag;
}

/**
 * @param $postid
 */
function post_saved( $postid ) {
	$local_path   = 'https://master.k8s.p4.greenpeace.org/norway/wp-content/uploads/';
	$gcs_path     = 'https://storage.googleapis.com/planet4-norway-stateless/';
	$attachments  = get_attached_media( '', $postid );
	$content_post = get_post( $postid );
	$content      = $content_post->post_content;
	$content      = apply_filters( 'the_content', $content );
	$content      = str_replace( ']]>', ']]&gt;', $content );

	preg_match_all( '@src="([^"]+)"@' , $content, $match_img );
	$img_files = array_pop( $match_img );
	preg_match_all( '@href="([^"]+\.pdf|PDF)"@' , $content, $match_pdf );
	$pdf_files = array_pop( $match_pdf );

	/*foreach ( $img_files as $image_file ) {
		$basename = basename( $image_file );
		foreach ( $attachments as $attachment ) {
			if ( preg_match( '/'.$basename.'$/i', $attachment->guid ) ) {
				//if ( preg_match( '/^'.$local_path.'/i', $attachment->guid ) ) {
				if (strpos($attachment->guid, $local_path) !== false) {
					$gcs_file_name = str_replace($local_path, $gcs_path, $attachment->guid);
					$random_str = explode('-', basename( $gcs_file_name ));
					$first_str = $random_str[0];
					if ( 2 !== substr_count( basename( $gcs_file_name ), $first_str ) ) {
						//$gcs_file_name = $first_str . '-' . $gcs_file_name;
						$gcs_file_name = str_replace( $first_str , $first_str.'-'.$first_str, $gcs_file_name );
					}
					wp_update_post(array('ID' => $attachment->ID, 'guid' => $gcs_file_name));
					$content = str_replace( $image_file, $gcs_file_name, $content );
				}
				else
				{
					$content = str_replace( $image_file, $attachment->guid, $content );
				}
			}
		}
	}*/

	foreach ( $img_files as $image_file ) {
		$basename = basename( $image_file );
		$attachement_obj = get_attachment_url_by_name( $basename );
		if ( $attachement_obj ) {
			$attachement_path = $attachement_obj[0]->guid;
			if (strpos($attachement_path, $local_path) !== false) {
				$gcs_file_name = str_replace($local_path, $gcs_path, $attachement_path);
				$gcs_file_name = strtolower($gcs_file_name); // Caps image ext import issue fix.
				$random_str = explode('-', basename( $gcs_file_name ));
				$first_str = $random_str[0];
				if ( 2 !== substr_count( basename( $gcs_file_name ), $first_str ) ) {
					//$gcs_file_name = $first_str . '-' . $gcs_file_name;
					$gcs_file_name = str_replace( $first_str , $first_str.'-'.$first_str, $gcs_file_name );
				}
				wp_update_post(array('ID' => $attachement_obj->ID, 'guid' => $gcs_file_name));
				$content = str_replace( $image_file, $gcs_file_name, $content );
			} else {
				$content = str_replace( $image_file, $attachement_path, $content );
			}
		} else {
			echo "<BR>>>>>>> Attachement not found error...".$basename;
		}
	}

	foreach ( $pdf_files as $image_file ) {
		$basename = basename( $image_file );
		$basename = str_replace(' ', '-', $basename);
		$basename = str_replace('%20', '-', $basename);
		foreach ( $attachments as $attachment ) {
			if ( preg_match( '/'.$basename.'$/i', $attachment->guid ) ) {
				//if ( preg_match( '/^'.$local_path.'/i', $attachment->guid ) ) {
				if (strpos($attachment->guid, $local_path) !== false) {
					$gcs_file_name = str_replace($local_path, $gcs_path, $attachment->guid);
					wp_update_post(array('ID' => $attachment->ID, 'guid' => $gcs_file_name));
					$content = str_replace( $image_file, $gcs_file_name, $content );
				} else {
					$content = str_replace( $image_file, $attachment->guid, $content );
				}
			}
		}
	}
	$updated_post = array();
	$updated_post['ID'] = $postid;
	$updated_post['post_content'] = $content;
	wp_update_post( $updated_post );
}

/**
 * @param $pid
 * @param $attid
 * @param $filepath
 */
function fix_attachment_uploaded( $pid, $attid, $filepath ) {
  $attachment = get_post( $attid );
  $local_path = 'https://master.k8s.p4.greenpeace.org/norway/wp-content/uploads/';
  $gcs_path   = 'https://storage.googleapis.com/planet4-norway-stateless/';

  if ( preg_match( '/^'.$local_path.'/i', $attachment->guid ) ) {
		wp_update_post(
			[
				'ID' => $attid,
				'guid' => str_replace($local_path, $gcs_path, $attachment->guid)
			]
		);
  }
}

/**
 * @param $name
 *
 * @return string
 */
function get_attachment_url_by_name( $name ) {
    global $wpdb;

    $name        = strtolower( $name );
    $attachments = $wpdb->get_results( "SELECT guid FROM $wpdb->posts WHERE guid like '%$name' AND post_type = 'attachment' ", OBJECT );

    if ( $attachments ) {
		return $attachments;
    } else {
        return '';
    }
}
?>
