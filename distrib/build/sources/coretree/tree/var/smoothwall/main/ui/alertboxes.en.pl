# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

%abouttext = (

'index.cgi' => '
Welcome to <strong>SmoothWall Express</strong> ' . $version . '<br>
This is your gateway to configuring and administering your SmoothWall
firewall.  Please make sure you read the Administration Guide before
reconfiguring your SmoothWall &mdash; the guide is available with our
other documentation from <a href=\'http://smoothwall.org/docs/\'
 title=\'smoothwall.org - external link\'>our website</a>.
',

'credits.cgi' => '<font class=\'pagetitle\'>SmoothWall Express</font><br>' . $tr{'version'} . ' ' . $version . '-' . $revision . ' ' . $webuirevision,

'status.cgi' => '<font class=\'pagetitle\'>About Your SmoothWall</font><br>Active service status of your Smoothie.',

'advstatus.cgi' => '<font class=\'pagetitle\'>Advanced Status</font><br>Pertinent information about your Smoothie, current configuration and resource usage.',

'graphs.cgi' => '<font class=\'pagetitle\'>Traffic Graphs</font><br>Statistical graphs based upon traffic usage across your SmoothWall\'s network interfaces.',

'proxy.cgi' => '<font class=\'pagetitle\'>Web Proxy</font><br>Configure and enable your SmoothWall\'s integrated caching web proxy service.',

'dhcp.cgi' => '<font class=\'pagetitle\'>DHCP</font><br>Configure and enable your SmoothWall\'s DHCP service, to automatically allocate LAN IP addresses to your network clients.',

'ddns.cgi' => '<font class=\'pagetitle\'>Dynamic DNS</font><br>Especially suited when your ISP assigned you a different IP address every time you connect, you can configure your SmoothWall to manage and update your dynamic DNS names from several popular services.',

'ids.cgi' => '<font class=\'pagetitle\'>Intrusion Detection System</font> (IDS)<br>Enable the Snort IDS service to detect potential security breach attempts from outside your network.  Note that Snort <strong>does not</strong> prevent these attempts &mdash; your port forwarding and access rules are used to allow and deny inbound access from the outside.',

'remote.cgi' => '<font class=\'pagetitle\'>Remote Access</font><br>Enable Secure Shell access to your SmoothWall, and restrict access based upon referral URL to ignore external links to your SmoothWall.',

'portfw.cgi' => '<font class=\'pagetitle\'>Port Forwarding</font><br>Forward ports from your external IP address to ports on machines inside your LAN or DMZ.',

'xtaccess.cgi' => '<font class=\'pagetitle\'>External Service Access</font><br>Allow access to admin services running on the SmoothWall to external hosts.',

'dmzholes.cgi' => '<font class=\'pagetitle\'>DMZ Pinholes</font><br>Enable access from a host on your DMZ to a port on a host on your LAN.',

'pppsetup.cgi' => '<font class=\'pagetitle\'>PPP Settings</font><br>Configure username, password and other details for up to five PPP, PPPoA or PPPoE connections.',

'vpnmain.cgi' => '<font class=\'pagetitle\'>VPN Control</font><br>Control and manage your VPN connections.',

'vpnconfig.dat' => '<font class=\'pagetitle\'>VPN Connections</font><br>Create connections to other SmoothWalls or IPSec-compliant hosts which have static IP addresses.',

'log.dat' => '<font class=\'pagetitle\'>Log Viewer</font><br>Check activity logs for services operating on your SmoothWall, such as DHCP, IPSec, updates and core kernel activity',

'proxylog.dat' => '<font class=\'pagetitle\'>Web Proxy Log Viewer</font><br>Check logs for the web proxy service.',

'firewalllog.dat' => '<font class=\'pagetitle\'>Firewall Log Viewer</font><br>Check logs for attempted access to your network from outside hosts.  Connections listed here <strong>have</strong> been blocked.',

'ids.dat' => '<font class=\'pagetitle\'>IDS Log Viewer</font><br>Check logs for potentially malicious attempted access to your network from outside hosts.  Connections listed here <strong>have not necessarily</strong> been blocked &mdash; use the Firewall Log Viewer to confirm blocked access.',

'ipinfo.cgi' => '<font class=\'pagetitle\'>IP Information</font><br>Perform a \'whois\' lookup on an ip address or domain name.',

'iptools.cgi' => '<font class=\'pagetitle\'>IP Tools</font><br>Perform \'ping\' and \'traceroute\' network diagnostics.',

'shell.cgi' => '<font class=\'pagetitle\'>Secure Shell</font><br>Connect to your SmoothWall using a Java SSH applet (requires SSH to be <a href="/cgi-bin/remote.cgi">enabled</a>).',

'updates.cgi' => '<font class=\'pagetitle\'>Updates</font><br>See the latest updates and fixes available for your SmoothWall, and an installation history of updates previously applied.',

'modem.cgi' => '<font class=\'pagetitle\'>Modem Configuration</font><br>Apply specific AT string settings for your PSTN modem or ISDN TA.',

'alcateladslfw.cgi' => '<font class=\'pagetitle\'>USB ADSL Firmware Upload</font><br>Upload firmware to enable use of an Alcatel/Thomson Speedtouch Home USB ADSL modem, nicknamed the \'frog\' or \'stingray\'.  <a href="http://smoothwall.org/get/" target="_breakFromUI">Download the \'Speedtouch USB Firmware\' tarball</a>, unpack it, and upload the mgmt.o file using this form.',

'changepw.cgi' => '<font class=\'pagetitle\'>Change Passwords</font><br>Change passwords for the \'admin\' and \'dial\' management interface users.  This does not affect access by SSH.',

'shutdown.cgi' => '<font class=\'pagetitle\'>Shutdown / Restart</font><br>Shutdown or restart your SmoothWall &mdash; restarts are sometimes mandated by update installation.',

'time.cgi' => '<font class=\'pagetitle\'>Time settings</font><br>Change timezone, manually set the time and date, and configure time syncronisation.',

'advnet.cgi' => '<font class=\'pagetitle\'>Advanced networking features</font><br>Configure ICMP settings, and other advanced features.',

'ipblock.cgi' => '<font class=\'pagetitle\'>IP block configuration</font><br>Add blocking rules to prevent access from specified IP addresses or networks.',

'backup.img' => '<font class=\'pagetitle\'>Backup</font><br>Use this page to create a backup floppy disk or floppy disk image file.',

);

