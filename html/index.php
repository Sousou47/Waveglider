<?php

include("auth.php"); //include auth.php file on all secure pages ?>
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Home</title>
<link rel="stylesheet" href="css/style.css" />
</head>
<body>

<div class="form">
<p><H1>Welcome <?php echo $_SESSION['username']; ?>!</H1></p>
<p>We are proud to count you in our Nessi Team !</p>
<img src="./css/NESSI.PNG" alt="Simply Easy Learning" width="200"
         height="180">

<p>Choose to redirect :</p> 
<p><a href="dashboard.php">Wave glider status</a></p>
<p><a href="http://waveglidereps.ddns.net:8082">Cameras status</a></p>



<a href="logout.php">Logout</a>


<br /><br /><br /><br />
To see how a wave glider works, please visit: <a href="https://www.liquid-robotics.com/wave-glider/how-it-works/">Liquid robotics !</a></div>
</div>
</body>
</html>
