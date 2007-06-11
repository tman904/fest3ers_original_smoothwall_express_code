# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

%baseglossary = (
	'De-Militarized Zone'  => "<strong>De-Militarized Zone</strong> A common term for a logically isolated network used to house machines which expose services to the internet (such as HTTP or mail servers) and are therefor isolated from the locally protected network.",
	'DMZ'  => "<strong>De-Militarized Zone</strong> A common term for a logically isolated network used to house machines which expose services to the internet (such as HTTP or mail servers) and are therefor isolated from the locally protected network.",
	'ORANGE' => "<strong>ORANGE</strong> The name usually given for the interface on a SmoothWall system which provides the De-Militarized Zone.",
	'GREEN' => "<strong>GREEN</strong> The local network usually reserved for desktop machines and servers.",
	'PURPLE' => "<strong>PURPLE</strong> An optional additional network intended to be used for wireless laptops and other devices.",
	'PPP' => "<strong>Point to Point Protocol</strong> A protocol used for connecting to an ISP over a serial-like conection, such a analogue modem or ADSL.",
	'ADSL' => "<strong>Asymmetric Digital Subscriber Line</strong> A mechanism for connecting to the Internet at broadband speeds over conventional copper phone lines.",
	'ISDN' => "<strong>Integrated Standards Digital Network</strong> A moderate-speed (64Kbit/sec usually) method for connecting to the Internet.",
	'Port' => "<strong>Port</strong> Each Internet service, such HTTP or SMTP is assigned a unique number which uniquely identifies the service.",
	'IP' => "<strong>Internet Protocol (address)</strong> Each host on an IP network is assigned a numberical address in the form 1.2.3.4. These addresses can either be external (on the wider Internet) or local (on the local network).",
	'TCP' => "<strong>Transmission Control Protocol</strong> A network protocol that guarantees reliable and in-order delivery of data between Internet hosts",
	'UDP' => "<strong>User Datagram Protocol</strong> A network protocol that provides a connection-less data exchange. Delivery of data is not guaranteed.",
	'MSN' => "<strong>Microsoft Messenger</strong> A program for talking to your mates and sending them pictures, videos and the like.",
	'IRC' => "<strong>Internet Relay Chat</strong> A realtime communications network and protocol developed in 1988. The first widespread Internet chat system.",
	'Snort' => "<strong>Snort</strong> 'grep for tcpdump'. A program for monitoring a network interface for suspicous traffic using a clever form of pattern matching. Can be used to identify suspicous activity on your Internet connection.",
	'VOIP' => "<strong>Voice over Internet Protocol</strong> A catch-all term for any protocol or program that provides voice and/or data calls over the public Internet. VOIP calls are effectivly free, but can suffer from quality problems.",
	'SYN cookie' => "<strong>SYN cookie</strong> A mechanism for avoiding DOS attacks.",
	'UPnP' => "<strong>Universal Plug n Play</strong> A collection of mechanisms and protocols for automating network setup, and other tasks. In SmoothWall UPnP support is used to allow programs such as MSN to work better when connecting through a NATed Internet connection.",
	'Traceroute' => "<strong>Traceroute</strong> A program that can be used to determine the path a packet will take on its way to an Inernet host.",
	'Ping' => "<strong>Ping</strong> A program for determining wether a machine is up and running, and also for measuring the time it takes to reach it.",
	'SSH' => "<strong>Secure Shell</strong> A program that can be used to gain command-line access to another machine, with the ability to encrypt the session. It also has strong authentication.",
	'HTTP' => "<strong>Hyper-Text Trasfer Protocol</strong> The protcol used to transfer webpages and simular content between webservers and browsers.",
	'HTTPS' => "<strong>Typer-Text Trasfer Protcol (Secure)</strong> An extention to HTTP to provide security in the form of encryption and identification.",
	'FTP' => "<strong>File Transfer Protocol</strong> An antiquated protocol for use in file transfer between Internet hosts. It provides little in the way of authentication and encryption.",
	'POP3' => "<strong>Post Office Protocol 3</strong> A simple protocol used in the downloading of Emails between a server and a client. Extensions exist for secure authentication and encryption.",
	'NAT' => "<strong>Network Address Translation</strong> Any form of IP address munging, but in a SmoothWall context it is the mechanism by which an internal host on GREEN or any other interface access the Internet with only a single real external IP address.",
);

1;
