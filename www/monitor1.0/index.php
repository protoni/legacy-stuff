<!DOCTYPE html>
<html>
<head>
<title>Raspberry pi monitor</title>
</head>
<body>
<?php

function draw_space()
{
	echo "<table>";
		echo "<td bgcolor='#BFE2F9' width='500' height='500'>";
		echo "</td>";
	echo "</table>";
}

function draw_cpu()
{
	$temp_raw_output = shell_exec("vcgencmd measure_temp");
	$temp_output = substr($temp_raw_output, 5, 7);
	$temperature = substr($temp_output, 0, 4);
	$voltage_raw_output = shell_exec("vcgencmd measure_volts core");
	$voltage_output = substr($voltage_raw_output, 5, 9);
	$cpu_usage = shell_exec("top -bn 1 | awk '{print $9}' | tail -n +8 | awk '{s+=$1} END {print s}'");
	$cpu_usage = substr($cpu_usage, 0, 4);
	if($cpu_usage > 100.0) $cpu_usage = 99.9;
	echo "<center>";
		echo "<table>";
			echo "<td bgcolor='#aaa' width='600'>";
				echo "<center>";
					echo "CPU";
				echo "</center>";
				echo "<pre>temperature\t\t". $temp_output. "</pre>";
				echo "<pre>voltage\t\t\t". $voltage_output. "</pre>";
				echo "<pre>usage\t\t\t". number_format((float)$cpu_usage, 1, '.', ''). "%". "</pre>";
				echo "<center>";
					echo "<table>";
						echo "<td>STATUS</td>";
						if($cpu_usage > 90.0 and $temperature > 50.0) echo "<td>". "<font color='FF0000'>HIGH LOAD, HIGH TEMP</font>" ."</td>";
						elseif($temperature > 50.0) echo "<td>". "<font color='FF0000'>HIGH TEMP</font>" ."</td>";
						elseif($cpu_usage > 90.0) echo "<td>". "<font color='FF0000'>HIGH LOAD</font>" ."</td>";
						else echo "<td>". "<font color='00FF00'>OK</font>" ."</td>";
					echo "</table>";
				echo "</center>";
		echo "</table>";
	echo "</center>";
		
}

function draw_fail2ban()
{
	$failtoban_running = shell_exec("sudo /etc/init.d/fail2ban status");
	$blocked_ips = shell_exec("sudo iptables -L fail2ban-ssh | sed 1d | awk -v OFS='\t' '{print $1, $4, $5}'");
	echo "<center>";
		echo "<table>";
			echo "<td bgcolor='#aaa' width='600'>";
			echo "<center>";
				echo "FAIL2BAN";
			echo "</center>";
			echo "<pre>blocked ips:</pre>";
			echo "<pre>". $blocked_ips. "</pre>";
			echo "<center>";
				echo "<table>";
					echo "<td>STATUS</td>";
					if(strpos($failtoban_running, 'fail2ban is running')) echo "<td>". "<font color='00FF00'>OK</font>" ."</td>";
					else echo "<td><font color='FF0000'>FAIL2BAN STOPPED</font>" ."</td>";
				echo "</table>";
			echo "</center>";
		echo "</table>";
	echo "</center>";
}

function draw_firewall()
{
	$raw_firewall_output = shell_exec("sudo ufw status");
	echo "<center>";
		echo "<table>";
			echo "<td bgcolor='#aaa' width='600'>";
			echo "<center>";
				echo "FIREWALL";
			echo "</center>";
			echo "<pre>". $raw_firewall_output. "</pre>";
			echo "<center>";
				echo "<table>";
					echo "<td>STATUS</td>";
					if(strpos($raw_firewall_output, 'inactive')) echo "<td><font color='FF0000'>UFW DISABLED</font></td>";
					else echo "<td><font color='00FF00'>OK</font></td>";
				echo "</table>";
			echo "</center>";
		echo "</table>";
	echo "</center>";
}

function draw_memory()
{
	$column_names = shell_exec("free -t -h -o | awk -v OFS='\t\t' '{print $1, $2, $3}' | sed -e '2, 4d'");
	$memory_output = shell_exec("free -t -h -o | awk -v OFS='\t\t' '{print $1, $2, $3, $4}' | sed 1d");
	$free_memory_raw = shell_exec("vmstat -s | grep 'free memory'");
	$free_memory = substr($free_memory_raw, 0, -14);
	echo "<center>";
		echo "<table>";
			echo "<td bgcolor='#aaa' width='600'>";
				echo "<center>";
					echo "MEMORY";
				echo "</center>";
				echo "<pre>\t\t". $column_names. "</pre>";
				echo "<pre>". $memory_output. "</pre>";
				echo "<center>";
					echo "<table>";
						echo "<td>STATUS</td>";
						if($free_memory > 30000) echo "<td>". "<font color='00FF00'>OK</font>" ."</td>";
						else echo "<td><font color='FF0000'>LOW MEMORY</font>" ."</td>";
					echo "</table>";
				echo "</center>";
		echo "</table>";
	echo "</center>";
}

function draw_open_ports()
{
	$open_ports_output = shell_exec("sudo netstat -ntlp | grep LISTEN | awk -v OFS='\t' '{print $1, $4, $6, $7}'");
	echo "<center>";
		echo "<table>";
			echo "<td bgcolor='#aaa' width='600'>";
			echo "<center>";
				echo "OPEN PORTS";
			echo "</center>";
			echo "<pre>". $open_ports_output. "</pre>";
		echo "</table>";
	echo "</center>";
}
/*
function get_date()
{
	$date = date("d");
	if($date[0] == '0')
	{
		$date = substr($date, 1, 1);
	}
	return $date;
}
*/
function draw_failed_logins()
{
	//$date = get_date();
	$invalid_login_output = shell_exec("sudo cat /var/log/auth.log | grep 'sshd.*Invalid' | awk -v OFS='\t' '{print $1, $2, $3, $5, $8}' | tail -10");
	echo "<center>";
		echo "<table>";
			echo "<td bgcolor='#aaa' width='600'>";
			echo "<center>";
				echo "FAILED LOGIN ATTEMPTS";
			echo "</center>";
			echo "<pre>". $invalid_login_output. "</pre>";
		echo "</table>";
	echo "</center>";
}

function draw_page_layout()
{
	echo "<table width='100%' border='0'>";
	 echo "<tr>";
    echo "<td colspan='4' bgcolor='#1F5C99'>";
    	echo "<center>";
      	echo "<h1>Raspberry pi system monitor</h1>";
      echo "</center>";
    echo "</td>";
  echo "</tr>";
	echo "<tr>";
		echo "<tr valign='top'>";
			echo "<td bgcolor='#aaa' width='5%'>";
			echo "</td>";
			echo "<td bgcolor='#BFE2F9' height='300' width='600'>"; // left side of the page
				draw_cpu();
				draw_firewall();
				draw_open_ports();
			echo "</td>";
			echo "<td bgcolor='#BFE2F9' height='300' width='600'>";	// right side of the page
				draw_fail2ban();
				draw_memory();
				draw_failed_logins();
			echo "</td>";
			echo "<td bgcolor='#aaa' width='5%'>";
			echo "</td>";
	echo "</tr>";
	echo "<tr>";
    echo "<td colspan='4' bgcolor='#1F5C99'>";
      echo "<center>";
      	echo "Copyright @ Toni";
      echo "</center>";
    echo "</td>";
  echo "</tr>";
	echo "</table>";
}

draw_page_layout();
?>

</body>
</html>


