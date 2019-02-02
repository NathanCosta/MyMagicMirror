<!DOCTYPE html>
<html>
	<head>
		<title>PiApp</title>
		<link rel="shortcut icon" href="resources/favicon.webp">

		<script src='/resources/lib/JQuery/3.3.1/jquery-3.3.1.min.js'></script>

		<script src='/resources/lib/iro/3.5.3/iro.min.js'></script>
	</head>
	<body>
		<div id="color-picker-container"></div>
		<label>
			User: <input type="text" name="user" id="user" />
		</label>
		<input type="button" id="capture" value="Capture" />
		

		<script type="text/javascript">
			var conn = new WebSocket('ws://<?= $_SERVER['SERVER_ADDR'] ?>:8080');

			var colorPicker = new iro.ColorPicker("#color-picker-container", {
				width: 320,
				height: 320,
				color: "#000"
			});

			colorPicker.on("color:change", function(color, changes){
				send("setLightsColor", {color : color.hexString});
			});

			$("#capture").click(function(){
				var user = $("#user").val();
				if(user && user.trim())
					send("capture", {user : user});
			});

			conn.onopen = function(e) {
			    console.log("Connection established!");
			};

			conn.onmessage = function(e) {
			    console.log(e.data);
			};

			function send(command, additionalParams)
			{
				var request = {
					command : command
				};

				if(additionalParams)
					$.extend(request, additionalParams);

				conn.send(JSON.stringify(request));
			}
		</script>
	</body>
</html>