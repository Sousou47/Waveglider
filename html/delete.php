<?php


require('db.php');
$id=$_REQUEST['id'];
$query = "DELETE FROM last_locations WHERE date=$id"; 
$result = mysqli_query($con,$query) or die ( mysqli_error());
header("Location: Last_positions.php"); 
?>
