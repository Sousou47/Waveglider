<?php


 
require('db.php');
include("auth.php"); //include auth.php file on all secure pages ?>
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Dashboard - Secured Page</title>
<link rel="stylesheet" href="css/style.css" />
</head>
<body>
<body style='background-color:#98C1D9'>;

<div class="form">
<H1>Team Nessy</H1>
<p>Welcome Home !</p>

<p><a href="view.php">View Boat's future trajectory</a><p>
<p><a href="Last_positions.php">View Boat's last positions</a><p>
<p><a href="sensor_temperature.php">Temperature sensor</a><p>
<p><a href="sensor_ph.php">pH sensor</a><p>

<p><a href="logout.php">Logout</a></p>


<br /><br /><br /><br />
To see how a wave glider works, please visit: <a href="https://www.liquid-robotics.com/wave-glider/how-it-works/">Liquid robotics !</a></div>
</div>
</body>
</html>
