<!DOCTYPE html>
<?php include 'data.php' ?> 
<html>
	<head>
		<title>Raspberry pi monitor</title>
		<link href="main.css" rel="stylesheet" type="text/css" />
	</head>
	<body>
		<header>
			<nav>
				<h1>Raspberry pi system monitor</h1>
				<ul>
					<li><a href="index.php">Monitor</a></li>
					<li><a href="open_ports.php">Open ports</a></li>
					<li><a href="failed_ssh_logins.php">Failed ssh logs</a></li>
					<li class="currentPage">Successful ssh logs</li>
				</ul>
			</nav>
		</header>

		<div class="row1">
			<div class="row1col1"><h2>Successful ssh client sessions</h2></div>
			<div class="row1col2">
				<center>
					<table align="center">
						<thead>
							<tr>
								<?php foreach($successful_ssh_sessions_column_names as $name) echo "<th>". $name ."</th>"; ?>
							</tr>
						</thead>
						<?php
						$col = 1;
						
						foreach($successful_ssh_sessions_array as $value)
						{
							if($col == 1) echo "<tr>";
							elseif($col > $successful_ssh_sessions_column_count) 
							{
								echo "</tr>";
								$col = 1;
							}				
							echo "<td>". $value ."</td>";
							$col++;
						}
						echo "</tr>";
						?>
					</table>
				</center>
			</div>
		</div>

		<div class="row1">
			<div class="row1col1"><h2>Successful ssh connections</h2></div>
			<div class="row1col2">
					<table align="center">
						<thead>
							<tr>
								<?php foreach($successful_ssh_connections_column_names as $name) echo "<th>". $name ."</th>"; ?>
							</tr>
						</thead>
						<?php
						$col = 1;
						
						foreach($successful_ssh_connections_array as $value)
						{
							if($col == 1) echo "<tr>";
							elseif($col > $successful_ssh_connections_column_count) 
							{
								echo "</tr>";
								$col = 1;
							}				
							echo "<td>". $value ."</td>";
							$col++;
						}
						echo "</tr>";
						?>
					</table>
			</div>
		</div>

		<div class="footer">Toni @ 2015</dib>
	</body>
</html>