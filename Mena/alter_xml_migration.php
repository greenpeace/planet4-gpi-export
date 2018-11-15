<?php
/**
 * Created by PhpStorm.
 * Date: 2/11/2018
 */

$file     = 'Posts-Export-2018-November-09-1254.xml';
$output   = 'Posts-Export-2018-November.xml';
$csv_file = 'content_review_MENA.csv';

$doc = new DOMDocument();
$doc->load( $file );

$posts = $doc->getElementsByTagName( "post" );


$i               = 0;
$j               = 0;
$found           = false;

$data = $doc->documentElement;


for ( $i = $posts->length; --$i >= 0; ) {
	$post = $posts[ $i ];


	$file = fopen( $csv_file, 'r' );
	while ( ( $line = fgetcsv( $file ) ) !== false ) {

		if ( strtolower( $line[0] ) == $post->getElementsByTagName( 'Permalink' )->item( 0 )->nodeValue ) {

			$j++;
			$post->appendChild( $doc->createElement( 'Category', $line[3] ) );
			$post->appendChild( $doc->createElement( 'Type', $line[4] ) );
			$post->appendChild( $doc->createElement( 'Tag1', str_replace( '#', '', $line[5] ) ) );
			$post->appendChild( $doc->createElement( 'Tag2', str_replace( '#', '', $line[6] ) ) );
			$post->appendChild( $doc->createElement( 'author_override', $line[10] ) );
			$post->replaceChild( $doc->createElement( 'Title', $line[7] ), $post->getElementsByTagName( 'Title' )->item( 0 ) );
			$found = true;
			break;
		}

	}
	if ( $found === false ) {
		echo "\n" . $post->getElementsByTagName( 'ID' )->item( 0 )->nodeValue;
		$post->replaceChild( $doc->createElement( 'Status', 'draft' ), $post->getElementsByTagName( 'Status' )->item( 0 ) );
	}
	$found = false;

}

file_put_contents( $output, $doc->saveXML() );
