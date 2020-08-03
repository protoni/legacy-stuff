<?php
	if(isset($_POST['play']))
	{
		if(!file_exists('/tmp/omx')) exec('mkfifo /tmp/omx');
		exec('php run.php > /dev/null &');
		exec("echo . > /tmp/omx");
	}
	
	if(isset($_POST['pause']))
	{
		shell_exec('echo -n p > /tmp/omx');
	}
	
	if(isset($_POST['stop']))
	{
		shell_exec('echo -n q > /tmp/omx');
	}
	
	if(isset($_POST['volUp']))
	{
		shell_exec('echo -n + > /tmp/omx');
	}
	
	if(isset($_POST['volDown']))
	{
		shell_exec('echo -n - > /tmp/omx');
	}
	
	
	
?>


<html>
	<body>
		<form action="" method="post">
			<p>Play fuel.mp3 with omxplayer</p>
			<button type="submit" name="play">Play</button>
		</form>
		<form action="" method="post">
			<button type="submit" name="pause">Pause</button>
		</form>
		<form action="" method="post">
			<button type="submit" name="stop">Stop</button>
		</form>
		<form action="" method="post">
			<button type="submit" name="volUp">Vol up</button>
		</form>
		<form action="" method="post">
			<button type="submit" name="volDown">Vol down</button>
		</form>
	</body>
</html>