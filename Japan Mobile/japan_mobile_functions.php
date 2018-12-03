<?php

/**
 * ==================================
 * Action: pmxi_saved_post
 * ==================================
 *
 * Called after a post is created/updated by WP All Import.
 *
 * @param $post_id int               - The id of the post just created/updated
 * @param $xml_node SimpleXMLElement - An object holding values for the current record
 * @param $is_update - Boolean showing whether the post is created or updated
 *
 */
function my_saved_post( $post_id, $xml_node, $is_update ) {

	$post    = get_post( $post_id );
	$content = $post->post_content;
	$record  = json_decode( json_encode( (array) $xml_node ), 1 );


	$old_images_urls = [];
	if ( ! empty( $record['images'] ) ) {
		$old_images_urls_temp = explode( '|', $record['images'] );
		$old_images_urls      = array_merge( $old_images_urls, $old_images_urls_temp );
	}
	if ( ! empty( [ 'featured_image' ] ) ) {
		$old_images_urls_temp = explode( '|', $record['featured_image'] );
		$old_images_urls      = array_merge( $old_images_urls, $old_images_urls_temp );
	}

	$old_attachemnts_urls = explode( '|', $record['pdfs'] );
	global $wpdb;


	foreach ( $old_images_urls as $old_image ) {

		$basename = basename( trim( $old_image ) );
		$filename = substr( $old_image, strrpos( $old_image, '/' ) + 1 );

		$urlencoded_basename = urlencode( $filename );
		$old_image_encoded   = str_replace( $filename, $urlencoded_basename, $old_image );

		$attachment = $wpdb->get_col( $wpdb->prepare( "SELECT ID FROM $wpdb->posts WHERE LCASE(guid) LIKE '%%%s';", strtolower( $basename ) ) );
		if ( isset( $attachment[0] ) ) {

			$attachment = get_post( $attachment[0] );
			$sm_cloud   = get_post_meta( $attachment->ID, 'sm_cloud', 1 );
			if ( $attachment instanceof \WP_Post ) {

				$content = str_replace( $old_image, $sm_cloud['fileLink'], $content ); // replace urls with wp-stateless url
				$content = str_replace( $old_image_encoded, $sm_cloud['fileLink'], $content ); // replace urls with wp-stateless url
				$content = str_replace( str_replace( 'http://greenpeace.jp/', '/', $old_image ), $sm_cloud['fileLink'], $content ); // replace urls with wp-stateless url
			}
		}
	}

	foreach ( $old_attachemnts_urls as $old_att ) {
		$basename   = basename( $old_att );
		$attachment = $wpdb->get_col( $wpdb->prepare( "SELECT ID FROM $wpdb->posts WHERE guid LIKE '%%%s';", strtolower( $basename ) ) );
		if ( isset( $attachment[0] ) ) {
			$attachment = get_post( $attachment[0] );
			if ( $attachment instanceof \WP_Post ) {
				$sm_cloud = get_post_meta( $attachment->ID, 'sm_cloud', 1 );
				$content  = str_replace( $old_att, $sm_cloud['fileLink'], $content );
			}
		}
	}
	$updated_post                 = array();
	$updated_post['ID']           = $post_id;
	$updated_post['post_content'] = $content;
	wp_update_post( $updated_post );

}

add_action( 'pmxi_saved_post', 'my_saved_post', 10, 3 );


?>
