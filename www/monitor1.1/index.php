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
					<li class="currentPage">Monitor</li>
					<li><a href="open_ports.php">Open ports</a></li>
					<li><a href="failed_ssh_logins.php">Failed ssh logs</a></li>
					<li><a href="successful_ssh_logins.php">Successful ssh logs</a></li>
				</ul>
			</nav>
		</header>
		
		<div class="row1">
			<div class="row1col1"><h2>FAIL2BAN</h2></div>
			<div class="row1col2">
				<table align="center">
					<thead>
						<tr>
							<?php foreach($blocked_ips_column_names as $name) echo "<th>". $name ."</th>"; ?>
						</tr>
					</thead>
					<?php
					$col = 1;
					if(count($blocked_ips_array) > $blocked_ips_column_count)
					{
						foreach($blocked_ips_array as $value)
						{
							if($col == 1) echo "<tr>";
							elseif($col > $blocked_ips_column_count) 
							{
								echo "</tr>";
								$col = 1;
							}				
							echo "<td>". $value ."</td>";
							$col++;
						}
					}
					else
					{
						echo "<td>No banned ips</td>";
						echo "<td>No banned ips</td>";
						echo "<td>No banned ips</td>";
					}
					echo "</tr>";
					?>
				</table>
				<div class="row2">
					<div class="row2col">status</div>
					<div class="row2col"> <?php echo get_failtoban_status(); ?></div>	
				</div>
			</div>
		</div>
		
		<div class="row1">
			<div class="row1col1"><h2>CPU</h2></div>
			<div class="row1col2">
				<table class="shortTable" align="center">
					<tr>
						<th>Temperature</th>
						<?php echo  "<td>". $temp_output ."</td>"?></td>
					</tr>
					<tr>
						<th>Voltage</th>
						<?php echo  "<td>". $voltage_output ."</td>"?></td>
					</tr>
					<tr>
						<th>Usage</th>
						<?php echo "<td>\t\t\t". number_format((float)$cpu_usage, 1, '.', ''). "%". "</td>"; ?>
					</tr>
				</table>
					
				<table align="center">
						<thead>
							<tr>
								<?php foreach($top_cpu_column_names as $name) echo "<th>". $name ."</th>"; ?>
							</tr>
						</thead>
						<?php
						$col = 1;
						foreach($top_cpu_array as $value)
						{
							if($col == 1) echo "<tr>";
							elseif($col > $top_cpu_column_count) 
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
					<div class="row2">
						<div class="row2col">status</div>
							<div class="row2col"> 
								<?php 
									if(get_cpu_status() == 'two')
									{
										echo "<font color='FF0000'>HIGH TEMP</font></div>";
										echo "<div class='row2col'><font color='FF0000'>HIGH LOAD</font></div>"; 
									}
									else echo "<div>". get_cpu_status() ."</div>";
								?>
							</div>	
					</div>
			</div>
		</div>
		
		<div class="row1">
			<div class="row1col1"><h2>MEMORY</h2></div>
			<div class="row1col2">
				<table align="center">
					<thead>
						<tr>
							<?php foreach($memory_column_names as $name) echo "<th>". $name ."</th>"; ?>
						</tr>
					</thead>
					<?php
					$col = 1;
					foreach($memory_array as $value)
					{
						if($col == 1) echo "<tr>";
						elseif($col > $memory_column_count) 
						{
							echo "</tr>";
							$col = 1;
						}
						if($col == 1)	echo "<th>". $value ."</th>";
						else echo "<td>". $value. "</td>";
						$col++;
					}
					echo "</tr>";
					?>
					</table>
					<table align="center">
						<thead>
							<tr>
								<?php foreach($top_memory_column_names as $name) echo "<th>". $name ."</th>"; ?>
							</tr>
						</thead>
						<?php
						$col = 1;
						foreach($top_memory_array as $value)
						{
							if($col == 1) echo "<tr>";
							elseif($col > $top_memory_column_count) 
							{
								echo "</tr>";
								$col = 1;
							}
							echo "<td>". $value. "</td>";
							$col++;
						}
						echo "</tr>";
					?>
					</table>
					<div class="row2">
						<div class="row2col">status</div>
						<div class="row2col"> <?php echo get_memory_status(); ?></div>	
					</div>
			</div>
		</div>
		
		<div class="row1">
			<div class="row1col1"><h2>FIREWALL</h2></div>
			<div class="row1col2">
					<table align="center">
					<thead>
						<tr>
							<?php foreach($firewall_column_names as $name) echo "<th>". $name ."</th>"; ?>
						</tr>
					</thead>
					<?php
					$col = 1;
					if(count($firewall_array) > $firewall_column_count)
					{
						foreach($firewall_array as $value)
						{
							if($col == 1) echo "<tr>";
							elseif($col > $firewall_column_count) 
							{
								echo "</tr>";
								$col = 1;
							}
							echo "<td>". $value. "</td>";
							$col++;
						}
					}
					else
					{
						echo "<td>ufw not running</td>";
						echo "<td>ufw not running</td>";
						echo "<td>ufw not running</td>";
					}
					echo "</tr>";
					?>
					</table>
					<div class="row2">
						<div class="row2col">status</div>
						<div class="row2col"> <?php echo get_firewall_status(); ?></div>
					</div>
			</div>
		</div>
		
		<div class="footer">Toni @ 2015</dib>
	</body>
</html>


