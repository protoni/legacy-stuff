#!/usr/bin/env python
# script to view terminal commands
import subprocess
import time
import argparse


system = {'uname -a' : 'Display linux system information',
			'uname -r' : 'Display kernel release information',
			'uptime' : 'Show how long the system has been running + load',
			'hostname' : 'Show system hostname',
			'hostname -i' : 'Display the IP address of the host',
			'last reboot' : 'Show system reboot history',
			'date' : 'Show the current date and time',
			'cal' : 'Show this month calendar',
			'w' : 'Display who is online',
			'whoami' : 'Who you are logged in as',
			'finger user' : 'Display information about user',
			'Recovery' : 'Type the phrase "REISUB" while holding down Alt and SysRq(PrintScrn) with about 1 second between each letter. Your system will reboot.',
			'lsb_release -a' : 'Get Ubuntu version',
			'uname -r' : 'Get kernel version',
			'uname -a' : 'Get all kernel information',
			'title' : 'SYSTEM'}

hardware = {'dmesg' : 'Detected hardware and boot messages',
			'cat /proc/cpuinfo' : 'CPU model',
			'cat /proc/meminfo' : 'Hardware memory',
			'cat /proc/interrupts' : 'Lists the number of interrupts per CPU per I/O device',
			'lshw' : 'Displays information on hardware configuration of the system',
			'lsblk' : 'Displays block device related information in Linux',
			'free -m' : 'Used and free memory (-m for MB)',
			'lspci -tv' : 'Show PCI devices',
			'lsusb -tv' : 'Show USB devices',
			'dmidecode' : 'Show hardware info from the BIOS',
			'hdparm -i /dev/sda' : 'Show info about disk sda',
			'hdparm -tT /dev/sda' : 'Do a read speed test on disk sda',
			'badblocks -s /dev/sda' : 'Test for unreadable blocks on disk sda',
			'title' : 'HARDWARE'}
			
users = {'id' : 'Show the active user id with login and group',
		'last' : 'Show last logins on the system',
		'who' : 'Show who is logged on the system',
		'groupadd admin' : 'Add group "admin"',
		'useradd -c "Toni"' : 'g admin -m ton #Create user "ton',
		'userdel ton' : 'Delete user ton',
		'adduser ton' : 'Add user "ton"',
		'usermod' : 'Modify user information',
		'title' : 'USERS'}
		
file_commands = {'ls -al' : 'Display all information about files / directories',
				'pwd' : 'Show the path of current directory',
				'mkdir directory-name' : 'Create a directory',
				'rm file-name' : 'Delete file',
				'rm -r directory-name' : 'Delete directory recursively',
				'rm -f file-name' : 'Forcefully remove directory recursively',
				'rm -rf directory-name' : 'Forcefully remove directory recursively',
				'cp file1 file2' : 'Copy file1 to file2',
				'cp -r dir1 dir2' : "Copy dir1 to dir2, create dir2 if it doesn't esists",
				'mv file1 file2' : 'Rename source to dest / move source to directory',
				'ln -s /path/to/file-name link-name' : 'Create symbolic link to file-name',
				'touch file' : 'Create or update file',
				'cat > file' : 'Place standard input into file',
				'more file' : 'Output contents of file',
				'head file' : 'Output first 10 lines of file',
				'tail file' : 'Output last 10 lines of file',
				'tail -f file' : 'Output contents of file as it grows starting with the last 10 lines',
				'gpg -c file' : 'Encrypt file',
				'gpg file.gpg' : 'Decrypt file',
				'wc' : 'Print the number of bytes, words, and lines in files',
				'xargs' : 'Execute command lines from standard input',
				'xdg-open' : 'The way to "double-click" on a file from the command line',
				'title' : 'FILE COMMANDS'}
				
process_related = {'ps' : 'Display your currently active processes',
					"ps aux | grep 'telnet'" : 'Find all process id related to telnet process',
					'pmap' : 'Memory map of process',
					'top' : 'Display all running processes',
					'killpid' : 'Kill process with mentioned pid id',
					'killall proc' : 'Kill all processes named proc',
					'pkill process-name' : 'Send signal to a process with its name',
					'bg' : 'Lists stopped or background jobs',
					'fg' : 'Brings the most recent job to foreground',
					'fg n' : 'Brings job n to the foreground',
					'title' : 'PROCESS RELATED'}

file_permissions = {'chmod octal file-name' : 'Change the permissions of file to octal',
					'chmod 777 /data/test.c' : 'Set rwx permission for owner, group, world',
					'chmod 755 /data/test.c' : 'Set rwx permission for owner, rw for group and world',
					'chown owhen-user file' : 'Change owner of the file',
					'chown owner-user:owner-group file-name' : 'Change owner and group owner of the file',
					'chown owner-user:owner-group directory' : 'Change owner and group owner of the directory',
					'title' : 'FILE PERMISSIONS'}
					
network = {'ifconfig -a' : 'Display all network ports and ip address',
			'ifconfig' : 'Show network information',
			'iwconfig' : 'Show wireless information',
			'sudo iwlist scan' : 'Scan for wireless networks',
			'sudo /etc/init.d/networking restart' : 'Reset network for manual configurations',
			'(file) /etc/network/interfaces' : 'Manual configuration',
			'ifup interface' : 'Bring interface online',
			'ifdown interface' : 'Disable interface',
			'ifconfig eth0' : 'Display specific ethernet port',
			'ethtool eth0' : 'Linux tool to show ethernet status',
			'mii-tool eth0' : 'Linux tool to show ethernet status',
			'ping host' : 'Send echo request to test connection',
			'whois domain' : 'Get information of domain',
			'dig domain' : 'Get DNS information for domain',
			'dig -x host' : 'Reverse lookup host',
			'host google.com' : 'Lookup DNS ip address for the name',
			'hostname -i' : 'Lookup local ip address',
			'wget file' : 'Download file',
			'netstat -tupl' : 'List active connections to / from system',
			'nslookup server' : 'Display default gateway',
			'title' : 'NETWORK'}
			
compression = {'tar cf home.tar home' : 'Create tar named home.tar containing home/',
				'tar xf file.tar' : 'Extract the files from file.tar',
				'tar czf.tar.gz files' : 'Create a tar with gzip compression',
				'gzip file' : 'Compress file and renames it to file.gz',
				'title' : 'COMPRESSION'}

install_package = {'rpm -i pkgname.rpm' : 'Install rpm based package',
					'rpm -e pkgname' : 'Remove package',
					'title' : 'INSTALL PACKAGE'}

install_from_source = {'./configure' : ' ',
						'make' : ' ',
						'make install' : ' ',
						'title' : 'INSTALL FROM SOURCE'}
						
search = {'grep pattern files' : 'Search for pattern in files',
		'grep -r pattern dir' : 'Search recursively for pattern in dir',
		'locate file' : 'Find all instances of file',
		'find /home/ton -name "index*"' : 'Find files names that start with "index"',
		'find /home -size +10000k' : 'Find files larger than 10000k in /home',
		'title' : 'SEARCH'}
			
login = {'ssh user@host' : 'Connect to host as user',
		'ssh -p port user@host' : 'Connect to host using specific port',
		'telnet host' : 'Connect to the system using telnet port',
		'title' : 'LOGIN'}
			
file_transfer = {'scp file.txt server2:/tmp' : 'Secure copy file.txt to remote host /tmp folder',
				'rsync -a /home/apps /backup/' : 'Synchronize source to destination',
				'title' : 'FILE TRANSFER'}
				
disk_usage = {'df -h' : 'Show free space on mounted filesystems',
			'df -i' : 'Show free inodes on mounted filesystems',
			'fdisk -l' : 'Show disks partitions, sizes and types',
			'du -ah' : 'Display disk usage in human readable form',
			'du -sh' : 'Display total disk usage on the current directory',
			'title' : 'DISK USAGE'}
			
directory_tranverse = {'cd ..' : 'To go up one level of the directory tree',
						'cd' : 'Go to $HOME directory',
						'cd /test' : 'Change to /test directory',
						'title' : 'DIRECTORY TRANVERSE'}
						
privileges = {'sudo command' : 'Run command as root',
			'sudo -s' : 'Open a root shell',
			'sudo -s -u user' : 'Open a shell as user',
			'sudo -k' : 'Forget sudo passwords',
			'gksudo command' : 'Visual sudo dialog (GNOME)',
			'kdesudo command' : 'Visual sudo dialog (KDE)',
			'sudo visudo' : 'Edit /etc/sudoers',
			'gksudo nautilus' : 'Root file manager (GNOME)',
			'kdesudo konqueror' : 'Root file manager (KDE)',
			'passwd' : 'Change your password',
			'title' : 'PRIVILEGES'}

display = {'sudo /etc/init.d/gdm restart' : 'Restart X and return to login (GNOME)',
			'sudo /etc/init.d/kdm restart' : 'restart X and return to login (KDE)',
			'(file) /etc/X11/xorg.conf' : 'Display configuration',
			'sudo dexconf' : 'Reset xorg.conf configuration',
			'Ctrl+Alt+Bksp' : 'Reset X display if frozen',
			'Ctrl+Alt+FN' : 'Switch to tty N',
			'Ctrl+Alt+F7' : 'Switch back to X display',
			'title' : 'DISPLAY'}
			
system_services = {'start service' : 'Start job service (Upstart)',
					'stop service' : 'Stop job service (Upstart)',
					'status service' : 'Check if service is running (Upstart)',
					'/etc/init.d/service start' : 'Start service (SysV)',
					'/etc/init.d/service stop' : 'Stop service (SysV)',
					'/etc/init.d/service status' : 'Check service (SysV)',
					'/etc/init.d/service restart' : 'Restart service (SysV)',
					'runlevel' : 'Get current runlevel',
					'title' : 'SYSTEM SERVICES'}
					
package_management = {'apt-get update' : 'Refresh available updates',
						'apt-get upgrade' : 'Upgrade all packages',
						'apt-get dist-upgrade' : 'Upgrade with package replacements; upgrade Ubuntu version',
						'apt-get install pkg' : 'Install pkg',
						'apt-get purge pkg' : 'Uninstall pkg',
						'apt-get autoremove' : 'Remove obsolete packages',
						'apt-get -f install' : 'Try to fix broken packages',
						'dpkg --configure -a' : 'Try to fix broken packages',
						'dpkg -i pkg.deb' : 'Install file pkg.deb',
						'(file) /etc/apt/sources.list' : 'APT repository list',
						'title' : 'PACKAGE MANAGEMENT'}
				
firewall = {'ufw enable' : 'Turn on the firewall',
			'ufw disable' : 'Turn off the firewall',
			'ufw default allow' : 'Allow all connections by default',
			'ufw default deny' : 'Drop all connections by default',
			'ufw status' : 'Current status and rules',
			'ufw allow port' : 'Allow traffic on port',
			'ufw deny port' : 'Block port',
			'ufw deny from ip' : 'Block ip address',
			'title' : 'FIREWALL'}

sections = {'a' : system, 'b' : hardware, 'c' : users, 'd' : file_commands,
			'e' : process_related, 'f' : file_permissions, 'g' : network,
			'h' : compression, 'i' : install_package, 'j' : install_from_source,
			'k' : search, 'l' : login, 'm' : file_transfer, 'n' : disk_usage,
			'o' : directory_tranverse, 'p' : privileges, 'q' : display,
			'r' : system_services, 's' : package_management, 't' : firewall}

all_sections = [system, hardware, users, file_commands, process_related, file_permissions, network, compression,
				install_package, install_from_source, search, login, file_transfer, disk_usage, directory_tranverse, privileges,
				display, system_services, package_management, firewall]

# this prints out the command sections
def write(dictionary, title, speed):	
	subprocess.call(['echo', '-e', "\033[0m \n \t %s \n" % title])
	for command, description in dictionary.iteritems():
		if command != 'title':
			subprocess.call(['echo', '-e', "\033[31m %s \033[0m- %s" % (command, description)])
			time.sleep(float(speed))

# if option is 'all', this iterates through all of the sections
def iterate_dictionarys(commands, speed):
	for dictionary in all_sections:
		title = dictionary['title']
		write(dictionary, title, speed)

# if option is 'help', this prints out a help text
def help():
	subprocess.call(['echo', '-e', "\033[0m \n \t give the letter as an argument"])
	subprocess.call(['echo', '-e', "\033[0m \t (type -s [seconds] to set print speed) \n"])
	subprocess.call(['echo', '-e', "\033[31m %s \033[0m- %s" % ('all', 'SHOW ALL')])
	for prefix, dictionary in sorted(sections.iteritems()):
		subprocess.call(['echo', '-e', "\033[31m %s \033[0m- %s" % (prefix, dictionary['title'])])

# handle system arguments
parser = argparse.ArgumentParser()
parser.add_argument('option', nargs = '?')
parser.add_argument('-s', '--speed')
parser.add_argument('second', nargs = '?')
args = parser.parse_args()
dictionary = None
if args.speed == None:
	speed = 0
else:
	speed = args.speed
if args.option in sections.keys():
	dictionary = sections[args.option]
	title = dictionary['title']
	write(dictionary, title, speed)
elif args.option == 'all':
	iterate_dictionarys(all_sections, speed)
elif args.option == 'help':
	help()
else:
	subprocess.call(['echo', '-e', "\033[0m You must give an argument, type help to see the options"])
	

