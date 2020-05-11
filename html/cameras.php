<!DOCTYPE html>
<html lang="fr">

<head>
	<meta charset="utf-8">
	<title>Camera board</title>
	<meta name="viewport" content="width=device-width,initial-scale=1" />
	<link href="A-style.css" rel="stylesheet" media="all" type="text/css"> 
</head>

<body class="pi-dashboard">

	<H1>Board table house - Olivier</h1>
	 
	<section class="video-surveillance">

		<img name="Entrance" class="stream" src="http://192.168.1.27:8082/?action=stream" width="600" height="450" alt="Live Feed" title="Entrance" />

		<img name="Garden" class="stream" src= "http://192.168.1.27:8082/?action=stream" width="600" height="450" title="Garden"/>
		
	</section>
	
	<section class="capteurs">


		
	</section>
 
</body>
</html>
sudo service motion start
pi@Olivier:~ $ sudo motion
