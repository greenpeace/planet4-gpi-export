<?php
/*
 * Below script is use to display the original email image and parsed email id text for review purpose.
 */

require_once "connection.php";

$sql = "SELECT * FROM email_img_to_text";
$result = $conn->query($sql);


echo "<h2>test images and text results</h2>";

if ($result->num_rows > 0) {
	// output data of each row.
	while($row = $result->fetch_assoc()) {
		$email_text = $row["email_text"];
		echo "<BR>";
		echo "<BR>".$row["email_img_url"];
		echo "<BR><img src='".$row["email_img_url"]."'>";
		echo "<br>".$email_text;
		echo "<BR>";
	}
}

?>

