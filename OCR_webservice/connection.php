<?php
/*
 * Database configuration.
 */


$servername  = "localhost";
$username    = "root";
$password    = "";
$dbname      = "email_img_to_text";

// API credentials.
$api_key     = "2777dc471788957";
$api_url     = "https://api.ocr.space/parse/imageurl";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
	die("Connection failed: " . $conn->connect_error);
}

