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
	/*
	 * Here you can use standard WordPress functions like get_post_meta() and get_post() to
	 * retrieve data, make changes and then save them with update_post() and/or update_post_meta()
	 *
	 * There are two ways to access the data from the current record in your import file:
	 *
	 * 1) Custom fields. For example, you could import a value to a custom field called "_temp" and
	 *  then retrieve it here. Since it's only temporary, you'd probably want to delete it immediately:
	 *
	 *     $my_value = get_post_meta($post_id, "_temp", true);
	 *     delete_post_meta($post_id,"_temp");
	 *
	 * 2) The $xml param (a SimpleXMLElement object). This can be complex to work with if you're nott
	 * used to iterators and/or xpath syntax. It's usually easiest to convert it a nested array using:
	 *
	 *     $record = json_decode(json_encode((array) $xml_node), 1);
	 */

	/*
	 * You can also conditionally run your code based on the import ID:
	 *
	 *     $import_id = ( isset( $_GET['id'] ) ? $_GET['id'] : ( isset( $_GET['import_id'] ) ? $_GET['import_id'] : 'new' ) );
	 *     if ( $import_id == '8' ) {
	 *        // run code
	 *     }
	 */
	$post                 = get_post( $post_id );
	$content              = $post->post_content;
	$record               = json_decode( json_encode( (array) $xml_node ), 1 );
	$old_images_urls      = explode( '|', $record['ImageURL'] );
	$old_attachemnts_urls = explode( '|', $record['AttachmentURL'] );
	global $wpdb;


	foreach ( $old_images_urls as $old_image ) {

		$basename   = basename( $old_image );
		$attachment = $wpdb->get_col( $wpdb->prepare( "SELECT ID FROM $wpdb->posts WHERE guid LIKE '%%%s';", strtolower( $basename ) ) );
		if ( isset( $attachment[0] ) ) {

			$attachment = get_post( $attachment[0] );
			$sm_cloud   = get_post_meta( $attachment->ID, 'sm_cloud', 1 );
			if ( $attachment instanceof \WP_Post ) {

				$temp_attachment = str_replace( 'https://greenpeacearabic.org', 'http://146.148.18.215', $old_image );
				$content         = str_replace( $temp_attachment, $sm_cloud['fileLink'], $content );
				$content         = str_replace( $old_image . '|', $attachment->ID, $content ); // replace urls in galleries shortcodes with new attachment id
				$content         = str_replace( $old_image, $sm_cloud['fileLink'], $content ); // replace urls with wp-stateless url
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
