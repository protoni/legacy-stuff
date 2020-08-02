<?php

//-------------------------------------------------------------------------------------------------------------------------
//---------------------------------- Fetch fail2ban data from the shell and parse it. -------------------------------------
//-------------------------------------------------------------------------------------------------------------------------

$failtoban_running = shell_exec("sudo /etc/init.d/fail2ban status");

$blocked_ips = shell_exec("sudo iptables -L fail2ban-ssh | sed 1,2d | awk -v OFS='\t\t' '{print $1, $4, $5}' | sed -i '$ d'");
$blocked_ips_array = preg_split('/\s+/', trim($blocked_ips));
$blocked_ips_column_names = array("Target", "Source", "Destination");
$blocked_ips_column_count = count($blocked_ips_column_names);

function get_failtoban_status()
{
	global $failtoban_running;
	if(strpos($failtoban_running, 'fail2ban is running')) return "<font color='#006600'>OK</font>";	
	else return "<font color='FF0000'>FAIL2BAN STOPPED</font>";
}


//-------------------------------------------------------------------------------------------------------------------------
//---------------------------------- Fetch cpu data from the shell and parse it. ------------------------------------------
//-------------------------------------------------------------------------------------------------------------------------

$temp_raw_output = shell_exec("vcgencmd measure_temp");
$temp_output = substr($temp_raw_output, 5, 7);
$temperature = substr($temp_output, 0, 4);
$voltage_raw_output = shell_exec("vcgencmd measure_volts core");
$voltage_output = substr($voltage_raw_output, 5, 9);
$cpu_usage = shell_exec("top -bn 1 | awk '{print $9}' | tail -n +8 | awk '{s+=$1} END {print s}'");	$cpu_usage = substr($cpu_usage, 0, 4);

$top_cpu = shell_exec("top -bn 1 | sed -e '1, 7d' | sed -n '1,10p' | awk -v OFS='\t\t' '{print $1, $2, $9, $12}'");
$top_cpu_array = preg_split('/\s+/', trim($top_cpu));
$top_cpu_column_names = array("PID", "User", "%CPU", "Command");
$top_cpu_column_count = count($top_cpu_column_names);

if($cpu_usage > 100.0) $cpu_usage = 99.9;

function get_cpu_status()
{
	global $cpu_usage, $temperature;
	if($cpu_usage > 90.0 and $temperature > 50.0) return "two";
	elseif($temperature > 50.0) return "<font color='FF0000'>HIGH TEMP</font>";
	elseif($cpu_usage > 90.0) return "<font color='FF0000'>HIGH LOAD</font>";
	else return "<font color='#006600'>OK</font>";
}

//-------------------------------------------------------------------------------------------------------------------------
//----------------------------------Fetch open ports data from the shell and parse it.-------------------------------------
//-------------------------------------------------------------------------------------------------------------------------

$open_ports = shell_exec("sudo netstat -ntlp | grep LISTEN | awk -v OFS='\t\t' '{print $1, $4, $6, $7}'");
$open_ports_array = preg_split('/\s+/', trim($open_ports));
$open_ports_column_names = array("Protocol", "Port", "State", "PID");
$open_ports_column_count = count($open_ports_column_names);


//-------------------------------------------------------------------------------------------------------------------------
//----------------------------------Fetch failed ssh logins data from the shell and parse it.------------------------------
//-------------------------------------------------------------------------------------------------------------------------

$failed_ssh_passwords = shell_exec("sudo cat /var/log/auth.log | sed '/invalid/d' | grep 'Failed password' | awk -v OFS='\t' '{print $1, $2, $3, $5, $11, $9}'");
$failed_ssh_passwords_array = preg_split('/\s+/', trim($failed_ssh_passwords));
$failed_ssh_passwords_column_names = array("Month", "Day", "Time", "PID", "IP", "User");
$failed_ssh_passwords_column_count = count($failed_ssh_passwords_column_names);

$failed_ssh_login_names = shell_exec("sudo cat /var/log/auth.log | grep 'sshd.*Invalid' | awk -v OFS='\t' '{print $1, $2, $3, $5, $10, $8}'");
$failed_ssh_login_names_array = preg_split('/\s+/', trim($failed_ssh_login_names));
$failed_ssh_login_names_column_names = array("Month", "Day", "Time", "PID", "IP", "User");
$failed_ssh_login_names_column_count = count($failed_ssh_login_names_column_names);

//-------------------------------------------------------------------------------------------------------------------------
//----------------------------------Fetch successful ssh logins data from the shell and parse it.--------------------------
//-------------------------------------------------------------------------------------------------------------------------

$successful_ssh_connections = shell_exec("sudo cat /var/log/auth.log | grep 'Accepted password' | awk -v OFS='\t' '{print $1, $2, $3, $5, $11, $9}'");
$successful_ssh_connections_array = preg_split('/\s+/', trim($successful_ssh_connections));
$successful_ssh_connections_column_names = array("Month", "Day", "Time", "PID", "IP", "User");
$successful_ssh_connections_column_count = count($successful_ssh_connections_column_names);

$successful_ssh_sessions = shell_exec("last -n -a pitoni root | awk -v OFS='\t' '{print $1, $3, $4, $5, $6, $7, $8, $9, $10}'");
$successful_ssh_sessions = strtr($successful_ssh_sessions, array('in' => '', '-' => ''));
$successful_ssh_sessions_array = preg_split('/\s+/', trim($successful_ssh_sessions));
$successful_ssh_sessions_column_names = array("User", "From", "Day", "Month", "Number", "Started", "Stopped", "Time");
$successful_ssh_sessions_column_count = count($successful_ssh_sessions_column_names);

//-------------------------------------------------------------------------------------------------------------------------
//----------------------------------Fetch memory data from the shell and parse it.-----------------------------------------
//-------------------------------------------------------------------------------------------------------------------------


$memory = shell_exec("free -t -h -o | awk -v OFS='\t\t' '{print $1, $2, $3, $4}' | sed 1d");
$memory = strtr($memory, array(':' => ''));
$memory_array = preg_split('/\s+/', trim($memory));
$memory_column_names = array(" ", "Total", "Used", "Free");
$memory_column_count = count($memory_column_names);


$free_memory_raw = shell_exec("vmstat -s | grep 'free memory'");
$free_memory = substr($free_memory_raw, 0, -14);

$top_memory = shell_exec("top -bn 1 | sed -e '1,7d'| sort -r -k10 | awk '!x[$10]++' | sed -n '1,10p' | awk -v OFS='\t\t' '{print $1, $2, $10, $12}'");
$top_memory_array = preg_split('/\s+/', trim($top_memory));
$top_memory_column_names = array("PID", "User", "%MEM", "Command");
$top_memory_column_count = count($top_memory_column_names);

function get_memory_status()
{
	global $free_memory;
	if($free_memory > 30000) return "<font color='#006600'>OK</font>";
	else return "<font color='FF0000'>LOW MEMORY</font>";
}

//-------------------------------------------------------------------------------------------------------------------------
//----------------------------------Fetch firewall data from the shell and parse it.-----------------------------------------
//-------------------------------------------------------------------------------------------------------------------------

$firewall_status = shell_exec("sudo ufw status");
$firewall = shell_exec("sudo ufw status | sed 1,4d");
$firewall_array = preg_split('/\s+/', trim($firewall));
$firewall_column_names = array("To", "Action", "From");
$firewall_column_count = count($firewall_column_names);

function get_firewall_status()
{
	global $firewall_status;
	if(strpos($firewall_status, 'inactive')) return "<font color='FF0000'>UFW DISABLED</font>";
	else return "<font color='#006600'>OK</font>";
}

?>