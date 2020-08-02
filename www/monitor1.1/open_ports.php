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
					<li class="currentPage">Open ports</li>
					<li><a href="failed_ssh_logins.php">Failed ssh logs</a></li>
					<li><a href="successful_ssh_logins.php">Successful ssh logs</a></li>
				</ul>
			</nav>
		</header>
		
		<div class="row1">
			<div class="row1col1">
				<h2>Open ports</h2>
					<div class="row1col2">
						<table align="center">
							<thead>
								<tr>
									<?php foreach($open_ports_column_names as $name) echo "<th>". $name ."</th>"; ?>
								</tr>
							</thead>
							<?php
							$col = 1;
							foreach($open_ports_array as $value)
							{
								if($col == 1) echo "<tr>";
								elseif($col > $open_ports_column_count) 
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
		</div>
		
		<div class="footer">Toni @ 2015</dib>
	</body>
</html>