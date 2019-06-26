<?php

function p4_wrap_log_message( $message ) {
	$template = "<div class='progress-msg'> [" . date( "H:i:s" ) . "] message</div>";
	echo str_replace( 'message', $message, $template );
}


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


	p4_wrap_log_message( "Running saved post p4 action" );

	$updated_post = array();

	$post    = get_post( $post_id );
	$content = $post->post_content;
	$record  = json_decode( json_encode( (array) $xml_node ), 1 );
	$categories = $record['Categories'];
	$nro_domain = 'https://www.greenpeace.ch/';


	$old_images_urls = [];
	if ( ! empty( $record['ImageURL'] ) ) {
		$old_images_urls_temp = explode( '|', trim($record['ImageURL']) );
		$old_images_urls      = array_merge( $old_images_urls, $old_images_urls_temp );
	}
	if ( ! empty( [ 'featured_image' ] ) ) {
		$old_images_urls_temp = explode( '|', $record['featured_image'] );
		$old_images_urls      = array_merge( $old_images_urls, $old_images_urls_temp );
	}

	$old_attachemnts_urls = explode( '|', $record['AttachmentURL'] );
	global $wpdb;


	p4_wrap_log_message( "Old images" );
	p4_wrap_log_message( var_export($old_images_urls, true) );
	p4_wrap_log_message( "Loop over images" );
	foreach ( $old_images_urls as $old_image ) {

		p4_wrap_log_message( "Old image: ".$old_image );

		// old image (wp all export)
		// https://www.greenpeace.ch/wp-content/uploads/2016/06/Website_Rapports_Image_Couverture_Fraise.jpg
		// old image in source
		// https://www.greenpeace.ch/wp-content/uploads/2016/06/Website_Rapports_Image_Couverture_Fraise-225x300.jpg

		// basename
		// Website_Rapports_Image_Couverture_Fraise.jpg
		$basename = basename( trim( $old_image ) );

		// filename
		// Website_Rapports_Image_Couverture_Fraise
		$filename = pathinfo( $basename, PATHINFO_FILENAME );

		// dirname
		// https://www.greenpeace.ch/wp-content/uploads/2016/06
		$dirname = pathinfo( $old_image, PATHINFO_DIRNAME );

		$urlencoded_basename = urlencode( $filename );
		$old_image_encoded   = str_replace( $filename, $urlencoded_basename, $old_image );

		p4_wrap_log_message( "Searching for old image in the posts table");
		$attachment_id = $wpdb->get_col( $wpdb->prepare( "SELECT ID FROM $wpdb->posts WHERE LCASE(guid) LIKE '%%%s';", strtolower( $basename ) ) );
		if ( isset( $attachment_id[0] ) ) {

			p4_wrap_log_message( "Old image found in the posts table");
			$attachment = get_post( $attachment_id[0] );
			p4_wrap_log_message( "Get wp stateless post meta");
			$sm_cloud   = get_post_meta( $attachment->ID, 'sm_cloud', 1 );
			if ( $attachment instanceof \WP_Post ) {

				$matches=[];
				$attachment_meta = wp_get_attachment_metadata($attachment_id[0]);
				preg_match( "/$filename-([0-9]{1,3})x([0-9]{1,3})\.(JPEG|jpeg|JPG|jpg|PNG|png)/", $content, $matches );


				// If matches found then a thumbnail of the image is used in source.
				if ( ! empty( $matches ) ) {

					// Loop over image thumbnails to find an exact match on image size between old image and imported image.
					foreach ( $attachment_meta['sizes'] as $size ) {

						if ( intval( $matches[1] ) == $size['width'] && intval( $matches[2] ) == $size['height'] ) {

							$old_image_thumbnail_full_path = $dirname . '/' . $matches[0];
							$content                       = str_replace( $old_image_thumbnail_full_path, $size['gs_link'], $content ); // replace urls with wp-stateless url
						}
					}
				}

				$content = str_replace( $old_image, $sm_cloud['fileLink'], $content ); // replace urls with wp-stateless url
				$content = str_replace( $old_image_encoded, $sm_cloud['fileLink'], $content ); // replace urls with wp-stateless url
				$content = str_replace( str_replace( $nro_domain, '/', $old_image ), $sm_cloud['fileLink'], $content ); // replace urls with wp-stateless url
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


	/*
	 * Categories to tags mapping
	 */
	$categories_map = [

		// German categories to Tags
		'Amazonas Riff'       => [ 'Meer' ],
		'Antarktis'           => [ 'Antarktis' ],
		'Arktis'              => [ 'Arktis' ],
		'Arctic30'            => [ 'Arktis' ],
		'Chemie'              => [ 'Chemie' ],
		'Detox'               => [ 'Chemie' ],
		'Detox Outdoor'       => [ 'Chemie' ],
		'Elektroschrott'      => [ 'Chemie' ],
		'Giftmüll'            => [ 'Chemie' ],
		'Luft'                => [ 'Chemie' ],
		'Verschmutzung'       => [ 'Chemie' ],
		'Wasser'              => [ 'Chemie' ],
		'Energie'             => [ 'Energie' ],
		'Atom'                => [ 'Energie' ],
		'Beznau I'            => [ 'Energie' ],
		'Fukushima'           => [ 'Energie' ],
		'Erneuerbare'         => [ 'Energie' ],
		'Fossile Brennstoffe' => [ 'Energie' ],
		'Suffizienz'          => [ 'Energie' ],
		'Finanzen'            => [ 'FinanzplatzSchweiz' ],
		'Fleisch und Milch'   => [ 'Landwirtschaft' ],
		'Jugendsolar'         => [ 'Jugendsolar' ],
		'Klima'               => [ 'Klima' ],
		'Dürre'               => [ 'Klima' ],
		'Klimawandel'         => [ 'Klima' ],
		'Klimagerechtigkeit'  => [ 'ClimateJustice' ],
		'Klimaseniorinnen'    => [ 'ClimateJustice' ],
		'Landwirtschaft'      => [ 'Landwirtschaft' ],
		'Bienen'              => [ 'Landwirtschaft' ],
		'Bioproduktion'       => [ 'Landwirtschaft' ],

		'Ernährung' => [ 'Ernährung', 'Landwirtschaft' ],

		'Gentechnik'    => [ 'Landwirtschaft' ],
		'Pestizide'     => [ 'Landwirtschaft' ],
		'Wasser'        => [ 'Landwirtschaft' ],
		'Meer'          => [ 'Meer' ],
		'Amazonas-Riff' => [ 'Meer' ],
		'Fischerei'     => [ 'Meer' ],

		'Plastik' => [ 'Meer', 'Verpackung' ],

		'Verschmutzung'        => [ 'Meer' ],
		'Walfang'              => [ 'Meer' ],
		'Wald'                 => [ 'Wald' ],
		'Abholzung'            => [ 'Wald' ],
		'Amazonas'             => [ 'Wald' ],
		'Asien'                => [ 'Wald' ],
		'Borealer Wald'        => [ 'Wald' ],
		'Kongo'                => [ 'Wald' ],
		'Munduruku / Tapajos'  => [ 'Wald' ],
		'Palmöl'               => [ 'Wald' ],
		'Regenwald'            => [ 'Wald' ],
		'Urwald'               => [ 'Wald' ],
		'Konzernverantwortung' => [ 'Konzernverantwortung' ],
		'NoDAPL'               => [ 'FinanzplatzSchweiz' ],
		'Organisation'         => [ 'ÜberUns' ],
		'Flotte'               => [ 'Flotte' ],
		'Greenpeace'           => [ 'ÜberUns' ],
		'Über uns'             => [ 'ÜberUns' ],
		'Public Eye'           => [ 'FinanzplatzSchweiz' ],
		'Resolute'             => [ 'Wald' ],


		// French categories to Tags
		'Animaux'        => [ '' ],
		'Consommation'   => [ '' ],
		'Divers'         => [ '' ],
		'Plastique'      => [ 'Plastique' ],
		'Société'        => [ '' ],
		'Thèmes'         => [ '' ],
		'Agriculture'    => [ 'Agriculture' ],
		'OGM'            => [ 'Agriculture' ],
		'Pesticides'     => [ 'Agriculture' ],
		'Climat'         => [ 'Climat' ],
		'COP21'          => [ 'Climat' ],
		'DAPL'           => [ 'Climat' ],
		'Justice'        => [ 'JusticeClimatique' ],
		'Transports'     => [ '' ],
		'Énergie'        => [ 'Energie' ],
		'Fossiles'       => [ 'Energie' ],
		'Nucléaire'      => [ 'Energie' ],
		'Fukushima'      => [ 'Energie' ],
		'Tchernobyl'     => [ 'Energie' ],
		'Renouvelables'  => [ 'Energie' ],
		'Forêts'         => [ 'Fôrets' ],
		'Forêt boréale'  => [ 'Fôrets' ],
		'Huile de palme' => [ 'Fôrets' ],
		'Résolu'         => [ 'Fôrets' ],
		'Greenpeace'     => [ 'Fôrets' ],
		'Océans'         => [ 'Océans' ],
		'Arctique'       => [ 'Arctique' ],
		'Baleines'       => [ 'Océans' ],
		'Corail'         => [ 'Océans' ],
		'Surpêche'       => [ 'Océans' ],
		'Science'        => [ '' ],
		'Société'        => [ 'Anotresujet' ],
		'Toxiques'       => [ 'Chimie' ],
		'Detox'          => [ 'Chimie' ],
		'Électronique'   => [ 'Chimie' ],

	];

	// Get post's categories.
	$post_categories = explode('|',$categories);


	// Consommation | Thèmes > Océans | Plastique
	// Loop over categories and assign mapped/relevant tags.
	if ( ! empty( $post_categories ) ) {

		foreach ( $post_categories as $category ) {
			$subcategories = explode( '>', $category);
			foreach ( $subcategories as $subcategory ) {

				if (array_key_exists($subcategory, $categories_map)) {
					$mapped_tags = $categories_map[$subcategory];
					wp_set_post_tags( $post_id, $mapped_tags ); // Set tags to Post
				}
			}
		}
	}


	/**
	 * Users mapping
	 */
	$users_mapping = [
		'gadmin'              => 'stduerre',
		's.kerkhof'           => '-',
		'd.schaefler'         => '-',
		'a.rid'               => 'arid',
		'johannes'            => '-',
		'mmueller'            => '-',
		'nfojtu'              => '-',
		's.duerrenberger'     => 'stduerre',
		'c.conradin'          => '-',
		'i.ruet'              => '-',
		'j.vonniederhaeusern' => '-',
		'agehring'            => 'agehring',
		'c.guerber'           => '-',
		'b.bommer'            => 'bbommer',
		'l.lukacs'            => '-',
		'y.zenger'            => 'yzenger',
		'm.faehndrich'        => '-',
		't.maeder'            => '-',
		'webstyle'            => '-',
		'm.hophan'            => 'mhophan',
		'c.sager'             => '-',
		'h.struever'          => 'hstrueve',
		'm.schlegel'          => 'mschlege',
		'f.minarro'           => '-',
		't.meier'             => '-',
		'nvalderr'            => '-',
		's.pion'              => 'spion',
		'y.anliker'           => 'yanliker',
		'r.arnold'            => 'rarnold',
		'xch'                 => '-',
		'm.erhart'            => 'merhart',
		'r.pejic'             => 'rpejic',
		's.wuethrich'         => '-',
		'd.walker'            => '-',
		'e.buechler'          => 'ebuechle',
		'p.good'              => '-',
		'd.mueller'           => 'dmueller',
		'r.stucki'            => 'rstucki',
		'nfischer'            => '-',
		'alban-feinheit'      => '-',
		'm.oesch'             => 'moesch',
		'm.decosterd'         => '-',
		'b.eigenmann'         => '-',
		'j.beyer'             => 'jbeyer',
		's.canetta'           => '-',
		'GPIGlobalCounter'    => '-',
		'e.schleiffenbaum'    => 'eschleif',
		'm.eck'               => 'meck',
	];

	/**
	 * Set post author based on users mapping.
	 */
	$old_author = $record['AuthorUsername'];
	if (array_key_exists( $old_author, $users_mapping) && '-' !== $users_mapping[$old_author]) {

		$mapped_user = get_user_by( 'login', $users_mapping[$old_author] );
		if ( $mapped_user ) {
			$updated_post['post_author'] = $mapped_user->ID;
		}

	}

	$updated_post['ID']           = $post_id;
	$updated_post['post_content'] = $content;

	wp_update_post( $updated_post );

	// Set custom p4_author_override meta field from 'Autor' custom meta.
	if (isset( $record['Autor']) && ! empty( $record['Autor'])) {
		update_post_meta( $post_id, 'p4_author_override', $record['Autor'] );
	}

}

add_action( 'pmxi_saved_post', 'my_saved_post', 10, 3 );


?>
