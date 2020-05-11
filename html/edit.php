<?php

 
require('db.php');
include("auth.php");
$id=$_REQUEST['id'];
$query = "SELECT * from new_record where id='".$id."'"; 
$result = mysqli_query($con, $query) or die ( mysqli_error());
$row = mysqli_fetch_assoc($result);
?>
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Update Record</title>
<link rel="stylesheet" href="css/style.css" />
</head>
<body>
<div class="form">
<p><a href="dashboard.php">Dashboard</a> | <a href="insert.php">Insert New Record</a> | <a href="logout.php">Logout</a></p>
<h1>Update Record</h1>
<?php
$status = "";
if(isset($_POST['new']) && $_POST['new']==1)
{
$id=$_REQUEST['id'];
$trn_date = date("Y-m-d H:i:s");
$latitude =$_REQUEST['latitude'];
$longitude =$_REQUEST['longitude'];
$submittedby = $_SESSION["username"];
$update="update new_record set trn_date='".$trn_date."', latitude='".$latitude."', longitude='".$longitude."', submittedby='".$submittedby."' where id='".$id."'";
mysqli_query($con, $update) or die(mysqli_error());
$status = "Record Updated Successfully. </br></br><a href='view.php'>View Updated Record</a>";
echo '<p style="color:#FF0000;">'.$status.'</p>';
}else {
?>
<div>
<form name="form" method="post" action=""> 
<input type="hidden" name="new" value="1" />
<input name="id" type="hidden" value="<?php echo $row['id'];?>" />
<p><input type="text" name="latitude" placeholder="Enter East coordinates" required value="<?php echo $row['latitude'];?>" /></p>
<p><input type="text" name="longitude" placeholder="Enter North coordinates" required value="<?php echo $row['longitude'];?>" /></p>
<p><input name="submit" type="submit" value="Update" /></p>
</form>
<?php } ?>

<br /><br /><br /><br />
To see how a wave glider works, please visit: <a href="https://www.liquid-robotics.com/wave-glider/how-it-works/">Liquid robotics !</a></div>

</div>
</div>
</body>
</html>
