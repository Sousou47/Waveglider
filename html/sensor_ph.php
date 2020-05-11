<!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8">
<title>Sensors values</title>
<link rel="stylesheet" href="css/style.css" />
</head>
<p><a href="dashboard.php">Home</a> | <a href="logout.php">Logout</a></p>


<script>
window.onload = function() {
 
var dataPoints = [];
 
var chart2 = new CanvasJS.Chart("chartContainer2", {
	animationEnabled: true,
	theme: "dark1",
	zoomEnabled: true,
	title: {
		text: "pH over time"
	},
	axisY: {
		title: "pH",
		titleFontSize: 24,
		sufix: " pH"
	},
	data: [{
		type: "spline",
		yValueFormatString: "#,##0.00 ",
		dataPoints: dataPoints
	}]
});

 


function addData2(data) {
	var dps = data.ph;
	for (var i = 0; i < dps.length; i++) {
		dataPoints.push({
			x: new Date(dps[i][0]),
			y: dps[i][1]
		});
	}
	chart2.render();
}
 
$.getJSON("./Sensors_pH.json", addData2);

}




</script>
</head>
<body>
<body style='background-color:#98C1D9'>;



<div id="chartContainer2" style="height: 370px; width: 100%;"></div>



<script src="https://canvasjs.com/assets/script/jquery-1.11.1.min.js"></script>
<script src="https://canvasjs.com/assets/script/jquery.canvasjs.min.js"></script>
</body>
</html>
