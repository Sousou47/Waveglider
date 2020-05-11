<?php


require('db.php');

$query = "DELETE FROM update_positions"; 
$result = mysqli_query($con,$query) or die ( mysqli_error());

header("Location: view.php"); 
?>
