<?php

 
require('db.php');
include("auth.php");

?>
<!DOCTYPE html>

<html>
<head>
<meta charset="utf-8">
<title>Wave glider : Direction</title>
<link rel="stylesheet" href="css/style.css" />
</head>
<body>
<body style='background-color:#98C1D9'>;

<div class="form">
<p><a href="dashboard.php">Home</a> | <a href="logout.php">Logout</a></p>
<h2>Boat's next directions</h2>
<table width="100%" border="1" style="border-collapse:collapse;">
<thead>
<tr><th><strong>n°</strong></th><th><strong>Latitude</strong></th><th><strong>Longitude</strong></th><th><strong>Edit</strong></th></tr>
</thead>
<tbody>
<?php
$count=1;
$sel_query="Select * from new_record ORDER BY id asc;";
$result = mysqli_query($con,$sel_query);
while($row = mysqli_fetch_assoc($result)) { ?>
<tr><td align="center"><?php echo $count; ?></td><td align="center"><?php echo $row["latitude"]; ?></td><td align="center"><?php echo $row["longitude"]; ?></td><td align="center"><a href="edit.php?id=<?php echo $row["id"]; ?>">Edit</a></td></tr>
<?php $count++; } ?>
</tbody>
</table>

<td align="center"><a href="update_positions_to_be_reached.php?id=1">Click here to send these new positions to the boat. ! Payant function ! </a></td>



<br /><br /><br /><br />
To see how a wave glider works, please visit: <a href="https://www.liquid-robotics.com/wave-glider/how-it-works/">Liquid robotics !</a></div>
</div>
</body>
</html>
