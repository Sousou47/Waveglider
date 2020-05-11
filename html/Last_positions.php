<?php

 
require('db.php');
include("auth.php");
?>
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Wave glider : Last positions</title>
<link rel="stylesheet" href="css/style.css" />
</head>
<body>
	<body style='background-color:#98C1D9'>;

<div class="form">
<p><a href="dashboard.php">Home</a> | <a href="logout.php">Logout</a></p>
<h2>Boat's last positions</h2>
<table width="100%" border="1" style="border-collapse:collapse;">
<thead>
<tr><th><strong>Date</strong></th><th><strong>Latitude</strong></th><th><strong>Longitude</strong></th><th><strong>Delete</strong></th></tr>
</thead>
<tbody>
<?php
$count=1;
$sel_query="Select * from last_locations ORDER BY date desc;";
$result = mysqli_query($con,$sel_query);
while($row = mysqli_fetch_assoc($result)) { ?>
<tr><td align="center"><?php echo $row["dat2"]; ?></td><td align="center"><?php echo $row["latitude"]; ?></td><td align="center"><?php echo $row["longitude"]; ?></td><td align="center"><a href="delete.php?id=<?php echo $row["date"]; ?>">Delete</a></td></tr>
<?php $count++; } ?>
</tbody>
</table>

<br /><br /><br /><br />


</div>












<html lang="en">
<head>
<meta charset="utf-8" />
<style type="text/css">
#sidebar { float: right; width: 30%; }
#main { padding-right: 15px; }
.infoWindow { width: 220px; }
</style>
<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
<script type="text/javascript">
//<![CDATA[

var map;

// Center of mer du nord
var center = new google.maps.LatLng(56.521581, 3.111592);



function init() {

var mapOptions = {
zoom: 5,
center: center,
mapTypeId: google.maps.MapTypeId.ROADMAP
}

map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);


<?php
$count2=1;
$sel_query="Select * from last_locations ORDER BY date desc;";
$result = mysqli_query($con,$sel_query);
while($row = mysqli_fetch_assoc($result)) { ?>


	var last = new google.maps.LatLng(<?php echo $row["latitude"];?>, <?php echo $row["longitude"];?>);

	var window = new google.maps.InfoWindow({
	content : '<?php echo $row["date"];?>'});
	
	var marker = new google.maps.Marker({
	map: map,
	position: last,
	label : {text : '<?php echo $row["date"];?>'},
	});
	

	
	
<?php $count2++; } ?>


var Oslo = new google.maps.LatLng(59.4111, 10.714131);

var infowindow = new google.maps.InfoWindow({
	content : 'Place where we designed the glider'});

var marker = new google.maps.Marker({
map: map,
position: Oslo, 
label : {text : "Oslo"},

});

marker.addListener('click', function(){
	infowindow.open(map,marker);
});

}
//]]>
</script>
</head>
<body onload="init();">


<section id="sidebar">
<div id="directions_panel"></div>
</section>

<section id="main">
<div id="map_canvas" style="width: 100%; height: 600px;"></div>
</section>






</body>
</html>
