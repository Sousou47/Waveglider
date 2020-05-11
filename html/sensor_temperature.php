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
 
var chart = new CanvasJS.Chart("chartContainer", {
	animationEnabled: true,
	theme: "dark1",
	zoomEnabled: true,
	title: {
		text: "Temperature over time"
	},
	axisY: {
		title: "Temperature *C",
		titleFontSize: 24,
		sufix: " °C"
	},
	data: [{
		type: "spline",
		yValueFormatString: "#,##0.00 *C",
		dataPoints: dataPoints
	}]
});




 
function addData(data) {
	var dps = data.price_usd;
	for (var i = 0; i < dps.length; i++) {
		dataPoints.push({
			x: new Date(dps[i][0]),
			y: dps[i][1]
		});
	}
	chart.render();
	setTimeout(function(){updateChart()},1000);
}


 
$.getJSON("./releves_temperatures.json", addData);

}



</script>
</head>
<body>
<body style='background-color:#98C1D9'>;

<div id="chartContainer" style="height: 370px; width: 100%;"></div>


   ---






<script src="https://canvasjs.com/assets/script/jquery-1.11.1.min.js"></script>
<script src="https://canvasjs.com/assets/script/jquery.canvasjs.min.js"></script>
</body>
</html>
