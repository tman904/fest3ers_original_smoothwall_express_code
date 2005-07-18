# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

$|=1; # line buffering

$version = '2.0';
$revision = 'p0';
$webuirevision = 'ui-3.6.1';
$swroot = '/var/smoothwall';
$pagecolour = '#ffffff';
#$tablecolour = '#a0a0a0';
$tablecolour = '#ffffff';
$bigboxcolour = '#ffffff';
$boxcolour = '#ffcc66';
$bordercolour = '#000000';
$table1colour = '#ff9900';
$table2colour = '#ffee88';
$colourred = '#a01010';
$colourorange = '#ff9900';
$colourgreen = '#10a010';
$colourlightred = '#ff6060';
$colourlightgreen = '#60ff60';
$primarynavsel = '#ff9900';
$primarynavdesel = '#ffee99';
$secondarynav = '#ff9900';
$graphblankcolour = '#ffee99';
$graphnominalcolour = '#ffaa00';
$graphwarningcolour = "#ff6600";
$graphcriticalcolour = "#ff0000";
$graphalertwarning = 70;
$graphalertcritical = 90;
$bevel = 1;
$bevellight = '#c0c0c0';
$bevelshadow = '#404040';
$bevelmiddle = '#808080';
$thisscript = basename($ENV{'SCRIPT_NAME'});
%alertbox = (
	bgerror => $pagecolour,
	fonterror => '#FF0000',
	texterror => 'error',
	bgok => $pagecolour,
	fontok => '#000000',
	textok => 'ok',
	bgadd => '#009933',
	fontadd => '#FFFFFF',
	textadd => 'add'
);
$pagewidth = 760;
$helpwidth = 125;
$pagewidthlesshelp = $pagewidth - $helpwidth;
$viewsize = 150;

&readhash("${swroot}/main/settings", \%settings);
$language = $settings{'LANGUAGE'};

if ($language =~ /^(\w+)$/) {$language = $1;}
require "${swroot}/langs/base.pl";
require "${swroot}/langs/${language}.pl";
# text for alertboxen is only available in en, so hardcode it for now
require "${swroot}/main/ui/alertboxes.en.pl";

sub showhttpheaders
{
	print "Pragma: no-cache\n";
	print "Cache-control: no-cache\n";
	print "Connection: close\n";
	print "Content-type: text/html\n\n";
}

sub showmenu
{
	$scriptname = $_[0];

	# scriptlist and sectionlist are tied together and are in order
	# with each other
	@scriptlist = ("/cgi-bin/index.cgi", "/cgi-bin/status.cgi", "/cgi-bin/proxy.cgi", "/cgi-bin/portfw.cgi", "/cgi-bin/vpnmain.cgi", "/cgi-bin/logs.cgi/log.dat", "/cgi-bin/ipinfo.cgi", "/cgi-bin/updates.cgi");
	@sectionlist = ( "control", "about your smoothie", "services", "networking", "vpn", "logs", "tools", "maintenance" );

	$read = 0;

	print <<END
<table border=0 cellpadding=0 cellspacing=0 cellmargin=0>
<tr>
END
	;

	while ( $read lt scalar($#sectionlist) + 1 ) { 
		if ( $scriptname eq $sectionlist[$read] ) {
			$tabcolour = $primarynavsel;
		} else { 
			$tabcolour = $primarynavdesel;
		}
		$sectionname = $sectionlist[$read];
		$scriptlink = $scriptlist[$read];
		print <<END
	<td width=7><img src="/ui/assets/3.5/img/null.gif" width="7" height="1" alt="&nbsp;"></td>

	<td bgcolor="$tabcolour" align="center"><img
 src="/ui/assets/3.5/img/null.gif" width="50" height="3" alt=""><br>&nbsp; <a href="$scriptlink">$sectionname</a> &nbsp;<br><img src="/ui/assets/3.5/img/null.gif" width="50" height="3" alt=""></td>
END
		;
		$read = $read + 1;
	}

	print <<END
</tr></table>
END
	;

}

sub subsectionstart
{
	print <<END
<tr><td colspan="2">
<table width="100%" border="0" cellpadding="0" cellspacing="0">
<tr><td align="left" bgcolor="$secondarynav" colspan="2">
<table border="0" cellpadding="0" cellspacing="0">
<tr>
END
	;
}

sub subsectionend
{
	print <<END
</table>
<img src="/ui/assets/3.5/img/null.gif" width="50" height="5" alt=""></td>
<tr><td valign="top" align="left"><img
 src="/ui/assets/3.5/img/nav.fadedown.gif" width="$pagewidthlesshelp"
 height="20" alt=""></td>
<td width="$helpwidth" bgcolor="#FF9900" align="center" valign="middle">&nbsp;
<a href="/cgi-bin/shutdown.cgi">$tr{'ssshutdown'}</a>
<FONT COLOR='$secondarynavdesel'>|</FONT>
<a href="javascript:displayHelp('$thisscript');"
 title="This will popup a new window with the requested help file">help</a> <img 
 src="/ui/assets/3.5/img/help.gif" alt="">&nbsp;
</td>
</table>
END
	;
}

sub subsectiontab
{
	$href = $_[0];
	$linktext = $_[1];
	$end = $_[2];
	$scriptname = $ENV{'SCRIPT_NAME'};

	$basehref = $href;
	$basehref =~ s/\?.*$//g;

	if ($scriptname eq $basehref) {
		$startlink="<STRONG><FONT COLOR='#EEEEEE'>";
		$endlink="</FONT></STRONG>"; }
	else {
		$startlink="<A HREF='$href'>";
		$endlink="</A>"; }

	$thislink = $startlink . $linktext . $endlink;

	print <<END
<td align="left" bgcolor="$secondarynav"><img 
 src="/ui/assets/3.5/img/null.gif" width="50" height="5" alt=""><br>&nbsp;&nbsp;
$thislink&nbsp;&nbsp;
END
	;

	if ($end eq '0') {
		print " <FONT COLOR='$secondarynavdesel'>|</FONT> "; }

	print <<END
</td>
END
	;
}	

sub showcontrolsection
{
        &subsectionstart();
	&subsectiontab('/cgi-bin/index.cgi', $tr{'sshome'}, 0);
        &subsectiontab('/cgi-bin/credits.cgi', $tr{'sscredits'}, 1);
        &subsectionend();
}

sub showaboutsection
{
	&subsectionstart();
	&subsectiontab('/cgi-bin/status.cgi', $tr{'ssstatus'}, 0);
	&subsectiontab('/cgi-bin/advstatus.cgi', $tr{'ssadvstatus'}, 0);
        &subsectiontab('/cgi-bin/graphs.cgi', $tr{'sstraffic graphs'}, 1);
	&subsectionend();
}

sub showservicessection
{
	&subsectionstart();
	&subsectiontab('/cgi-bin/proxy.cgi', $tr{'ssweb proxy'}, 0);
	&subsectiontab('/cgi-bin/dhcp.cgi', $tr{'ssdhcp'}, 0);
	&subsectiontab('/cgi-bin/ddns.cgi', $tr{'ssdynamic dns'}, 0);
	&subsectiontab('/cgi-bin/ids.cgi', $tr{'ssids'}, 0);
	&subsectiontab('/cgi-bin/remote.cgi', $tr{'ssremote access'}, 0);
	&subsectiontab('/cgi-bin/time.cgi', $tr{'sstime'}, 1);
	&subsectionend();
}

sub shownetworkingsection
{
	&subsectionstart();
	&subsectiontab('/cgi-bin/portfw.cgi', $tr{'ssport forwarding'}, 0);
	&subsectiontab('/cgi-bin/xtaccess.cgi', $tr{'ssexternal service access'}, 0);
	&subsectiontab('/cgi-bin/dmzholes.cgi', $tr{'ssdmz pinholes'}, 0);
	&subsectiontab('/cgi-bin/pppsetup.cgi', $tr{'ssppp settings'}, 0);
	&subsectiontab('/cgi-bin/ipblock.cgi', $tr{'ssip block'}, 0);
	&subsectiontab('/cgi-bin/advnet.cgi', $tr{'ssadvanced'}, 1);
	&subsectionend();
}

sub showvpnsection
{
	&subsectionstart();
	&subsectiontab('/cgi-bin/vpnmain.cgi', $tr{'sscontrol'}, 0);
	&subsectiontab('/cgi-bin/vpn.cgi/vpnconfig.dat', $tr{'ssconnections'}, 1);
	&subsectionend();
}

sub showlogssection
{
	&subsectionstart();
	&subsectiontab('/cgi-bin/logs.cgi/log.dat', $tr{'ssother'}, 0);
	&subsectiontab('/cgi-bin/logs.cgi/proxylog.dat', $tr{'ssweb proxy'}, 0);
	&subsectiontab('/cgi-bin/logs.cgi/firewalllog.dat', $tr{'ssfirewall'}, 0);
	&subsectiontab('/cgi-bin/logs.cgi/ids.dat', $tr{'ssids'}, 1);
	&subsectionend();
}

sub showshutdownsection
{
	&subsectionstart();
	&subsectiontab('','&nbsp;',1);
	&subsectionend();
}

sub showtoolssection
{
	&subsectionstart();
	&subsectiontab('/cgi-bin/ipinfo.cgi', $tr{'ssip info'}, 0);
	&subsectiontab('/cgi-bin/iptools.cgi', $tr{'ssip tools'}, 0);
	&subsectiontab('/cgi-bin/shell.cgi', $tr{'ssshell'}, 1);
	&subsectionend();
}

sub showmaintenancesection
{
	&subsectionstart();
	&subsectiontab('/cgi-bin/updates.cgi', $tr{'ssupdates'}, 0);
	&subsectiontab('/cgi-bin/modem.cgi', $tr{'ssmodem'}, 0);
	&subsectiontab('/cgi-bin/alcateladslfw.cgi', $tr{'ssusb adsl firmware upload'}, 0);
	&subsectiontab('/cgi-bin/changepw.cgi', $tr{'sspasswords'}, 0);
	&subsectiontab('/cgi-bin/backup.img', $tr{'ssbackup'}, 0);
	&subsectiontab('/cgi-bin/shutdown.cgi', $tr{'ssshutdown'}, 1);
	&subsectionend();
}

sub openpage
{
	$title = $_[0];
	$menu = $_[1];
	$extrahead = $_[2];
	$thissection = $_[3];

	if ($menu == 1) { $colspan = 2; } else { $colspan = 1; }

	print <<END
<HTML>
<HEAD>
$extrahead
<TITLE>$title - SmoothWall Express</TITLE>
<SCRIPT LANGUAGE='javascript' SRC='/ui/assets/3.5/js/script.js'></SCRIPT>
<LINK HREF='/ui/assets/3.5/css/style.css' REL='STYLESHEET' TYPE='text/css'>
</HEAD>
END
	;

	if ( $thissection ne "help" ) {
		$currentconnection = &connectedstate();
		$cellwidth = $pagewidth / 2;
		print <<END
<BODY BGCOLOR='$pagecolour' TEXT='#000000' LINK='#000000' VLINK='#000000'>
<DIV ALIGN='CENTER'>
<table width="$pagewidth" border="0" cellpadding="0" cellspacing="0">
<TR HEIGHT='$bevel'>
<TD COLSPAN='2' BGCOLOR='$bevellight'></TD>
</TR>
<tr><td width="$cellwidth" height="30" bgcolor="$boxcolour"><a href="/cgi-bin/credits.cgi"><img 
 src="/ui/assets/3.5/img/topleft.logo.${version}.gif"
 border="0" alt="SmoothWall Express 2.0" title="SmoothWall Express 2.0"></td>
<td width="$cellwidth" height="30" align="right" bgcolor="$boxcolour">

<table border='0' cellpadding='0' cellspacing='0'>
<tr><td><img src="/ui/assets/3.5/img/netstatus.label.gif"
 alt="current connection status" title="current connection status"></td>
<td><a href="/cgi-bin/index.cgi"><img 
 src="/ui/assets/3.5/img/netstatus-wee.${currentconnection}.gif"
 border="0" alt="$currentconnection" title="$currentconnection"></td></tr>
</table>

</td></tr>
<tr><td bgcolor="#FFCC66" colspan="2">
<img src="/ui/assets/3.5/img/null.gif" width="$pagewidth" height="5" alt=""><br>
END
		;
		&showmenu($thissection);
		print <<END
</td>
END
		;
	} else { 
		print <<END
<BODY BGCOLOR='$pagecolour' TEXT='#000000' LINK='#000000' VLINK='#000000'
 onLoad="window.focus()">
<DIV ALIGN='CENTER'>


END
		;
	}

}

sub closepage
{
	$thissection = $_[0];

	# if (-e "${swroot}/red/active") {
	#	if ( $ENV{'HTTPS'} eq "on" ) {
	#		$sflogoproto = "https";
	#	} else {
	#		$sflogoproto = "http";
	#	}
	#	 $sflogoimg = $sflogoproto . "://sourceforge.net/sflogo.php?group_id=10366&type=1";
	#} else {
		$sflogoimg = "/ui/assets/3.5/img/sflogo.png";
	#}

	if ( $thissection ne "blank" ) {
		print <<END
</TD>
</TR>
</TABLE>
</TD>
</TR>
</TABLE>
</DIV>
<DIV ALIGN='center'>
<table width='$pagewidth' border=0 cellpadding=0 cellspacing=0 BGCOLOR='$boxcolour'>
<tr><td valign="top" align="left" colspan="5"><img
 src="/ui/assets/3.5/img/nav.fadeup.gif" width="$pagewidth"
 height="20" alt=""></td>
<tr><td class='headerfooterStandard' width='10' valign='top'><img src='/ui/assets/3.5/img/null.gif' height='1' width='10' alt=''></td>
    <td align='left' colspan='3' valign='middle' nowrap>

<table border=0 cellpadding=0 cellspacing=0>
<tr><td>Produced in association with</td>
<td>&nbsp;<a href="http://sf.net/projects/smoothwall/"><img 
    src="$sflogoimg" width="44" height="16" border="0" valign="center"
    alt="SourceForge.net"></a></td>
<td>&nbsp;<a href='http://www.usr.com/'><img src='/ui/assets/3.5/img/corp/usr.png' alt='U.S. Robotics' valign='center' width="63" height="15" border='0'></a></td>
<td>&nbsp;<a href='http://www.ftel.co.uk/'><img src='/ui/assets/3.5/img/corp/fuji.gif' alt='Fujitsu' valign='center' width="32" height="15" border='0'></td>
</table>

    </td>
    <td class='headerfooterStandard' width='10' valign='top'><img src='/ui/assets/3.5/img/null.gif' height='1' width='10' alt=''></td>
<tr><td class='headerfooterStandard' width='10' valign='top'><img src='/ui/assets/3.5/img/null.gif' height='1' width='10' alt=''></td>
    <td class='headerfooterStandard' align='left' valign='bottom' nowrap>
    <font class='smallnote'>
    express $version $revision $webuirevision<br>
    SmoothWall&trade; is a trademark of 
    <A HREF='http://www.smoothwall.net/'>SmoothWall Limited</A>.
    </font>
    </td>
    <td class='headerfooterStandard'>&nbsp;</td>
    <td valign=bottom class='headerfooterStandard' align=right nowrap>
    <font class='smallnote'>

    &copy; 2000 - 2003 <a href='http://smoothwall.org/team/'>The SmoothWall Team</a><br>
<A HREF='/cgi-bin/credits.cgi'>$tr{'credits'}</A> - 
    Portions &copy; <a href='http://smoothwall.org/sources.html'>original authors</a>
    </font>
    </td>
    <td class='headerfooterStandard' width='10' valign='top'><img src='/ui/assets/3.5/img/null.gif' height='1' width='10' alt=''></td>
<tr><td class='headerfooterStandard' width='10' valign='top'><img src='/ui/assets/3.5/img/null.gif' height='5' width='10' alt=''></td>
<TR HEIGHT='$bevel'><TD COLSPAN='5' BGCOLOR='$bevelshadow'></TD>
</TR>
</table>

</DIV>
END
		;
	}

	print <<END
</BODY>
</HTML>
END
	;
}

sub openbigbox
{
	$width = $_[0];
	$align = $_[1];

	print <<END
<TABLE WIDTH='$width' CELLSPACING='0' CELLPADDING='0' BORDER='0'>
<TR>
<TD BGCOLOR='$bigboxcolour' COLSPAN="3" ALIGN='LEFT' VALIGN='TOP'>&nbsp;</TD>
</TD>
</TR>
<TR>
<TD WIDTH='10' BGCOLOR='$bigboxcolour'>&nbsp;</TD>
<TD BGCOLOR='$bigboxcolour' ALIGN='$align'>
END
	;
}

sub closebigbox
{
	print <<END
</TD><TD WIDTH='10' BGCOLOR='$bigboxcolour'>&nbsp;</TD></TR>
<TR>
<TD BGCOLOR='$bigboxcolour' COLSPAN="3" ALIGN='LEFT' VALIGN='TOP'>&nbsp;</TD>
</TR>
</TABLE>
END
	;
}

sub openbox
{
	$width = $_[0];
	$align = $_[1];
	$caption = $_[2];
	$cellcolour = $_[3];
	if ( $cellcolour eq "" ) { $cellcolour = $boxcolour; }

	print <<END
<TABLE WIDTH='$width' CELLSPACING='0' CELLPADDING='0'>
<TR HEIGHT='$bevel'>
<TD WIDTH='100%' BGCOLOR='$bevellight'></TD>
</TR>
<TR>
<TD BGCOLOR='$cellcolour'>
<TABLE WIDTH='100%' CELLPADDING='2'>
<TR><TD ALIGN='$align'>
END
	;
	if ($caption) { print "<B><DIV CLASS='boldbase'>$caption</DIV></B>\n"; }
}

sub closebox
{
	print <<END
</TD></TR>
</TABLE>
</TD>
</TR>
<TR HEIGHT='$bevel'>
<TD BGCOLOR='$bevelshadow'></TD>
</TR>
</TABLE>
<BR>
END
	;
}

sub alertbox
{
	my $thiserror = $_[0];
	my $additional = $_[1];
	if ( $thiserror ne '' && $additional eq '' ) {
		&pageinfo($alertbox{"texterror"}, "<font class='pagetitle'>" . $tr{'error messages'} . "</font><br>" . $thiserror);
	} elsif ( $thiserror eq 'add' && $additional eq 'add' && $abouttext{$thisscript . "-additional"} ne '' ) {
		&pageinfo($alertbox{"textadd"}, $abouttext{$thisscript . "-additional"});
	} elsif ( $thiserror eq 'add' && $additional eq 'add' && $abouttext{$thisscript . "-additional"} eq '' ) {
		# deliberately do nothing
	} else {
		&pageinfo($alertbox{"textok"}, $abouttext{$thisscript});
	}
}

sub pageinfo 
{
	my $thisalerttype = $_[0];
	my $thisboxmessage = $_[1];
	my $localgraphic;
	if ( $thisalerttype ne "error" ) {
		$localgraphic = $thisscript;
	}  else { 
		$localgraphic = "error";
	}
	$localgraphic =~ s/\.cgi//g;
	my $thisbgcolour = $alertbox{"bg" . $thisalerttype};
	my $thisfontcolour = $alertbox{"font" . $thisalerttype};

	print qq|
<table border='0' cellpadding='3' cellspacing='0' width="100%">
<tr><td valign='top' bgcolor='$thisbgcolour' width='100'><img src='/ui/assets/3.6/img/pagetitles/page-$localgraphic.png' width='100'></td>
<td valign='top' align='left' bgcolor='$thisbgcolour'>
<font color='$thisfontcolour'>$thisboxmessage</font>
|;
	print qq|</font></td></tr></table>|;

# 	&openbox('100%','LEFT','',$thisbgcolour);
# 	print <<END
# <table border='0' cellpadding='3' cellspacing='0'>
# <tr><td valign='top'><img src='/ui/assets/3.5/img/alert-$thisalerttype.gif'></td>
# <td valign='top' align='left'><font color='$thisfontcolour'>
# END
# 	;
# 	print $thisboxmessage;
# 	print "</font></td></tr></table>";
#	&closebox;
}

sub writehash
{
	my $filename = $_[0];
	my $hash = $_[1];
	
	# write cgi vars to the file.
	open(FILE, ">${filename}") or die "Unable to write file $filename";
	flock FILE, 2;
	foreach $var (keys %$hash) 
	{
		$val = $hash->{$var};
		if ($val =~ / /) {
			$val = "\'$val\'"; }
		if (!($var =~ /^ACTION/)) {
			print FILE "${var}=${val}\n"; }
	}
	close FILE;
}

sub readhash
{
	my $filename = $_[0];
	my $hash = $_[1];
	my ($var, $val);

	open(FILE, $filename) or die "Unable to read file $filename";
	
	while (<FILE>)
	{
		chop;
		($var, $val) = split /=/, $_, 2;
		if ($var)
		{
			$val =~ s/^\'//g;
			$val =~ s/\'$//g;
			$hash->{$var} = $val;
		}
	}
	close FILE;
}

sub getcgihash
{
	my $hash = $_[0];
	my $buffer = '';
	my $length = $ENV{'CONTENT_LENGTH'};
	my ($name, $value); 
	my ($pair, @pairs, $read);
	my %hash;
	my $boundary;
	my %remotesettings;
	my %main;
	my %netsettings;
	my $redip = '0.0.0.0';
	my $referer;
	my $shorthostname;
	my @hostnameelements;
	
	if ($ENV{'REQUEST_METHOD'} ne 'POST') {
		return; }

	$ENV{'HTTP_REFERER'} =~ m/^(http|https)\:\/\/(.*?)[\:|\/]/;
	$referer = $2;

	&readhash("${swroot}/remote/settings", \%remotesettings);
	&readhash("${swroot}/main/settings", \%main);
	&readhash("${swroot}/ethernet/settings", \%netsettings);

	@hostnameelements = split(/\./, $main{'HOSTNAME'});
	$shorthostname = $hostnameelements[0];

	if (open(FILE, "${swroot}/red/local-ipaddress"))
	{
		$redip = <FILE>; chomp $redip;
		close(FILE);
	}

	if ($remotesettings{'ENABLE_SECURE_ADMIN'} eq 'on')
	{
		unless ($referer eq $main{'HOSTNAME'} ||
			$referer eq $shorthostname ||
			$referer eq $netsettings{'GREEN_ADDRESS'} ||
			$referer eq $redip)
		{
			&log("Referral $ENV{'HTTP_REFERER'} is not a SmoothWall page.");
			return;
		}
	}        
	
	$read = 0;
	$buffer = "";
	while($read < $length){
		$read = $read + (read(STDIN, $buf, 1024) or die "Could not read buffer:$read: $@");
		$buffer .= $buf;
	}
	unless($read == $length) {
		die "Could not read buffer: $!";
	}

	if($ENV{'CONTENT_TYPE'} =~ m/multipart\/form-data; boundary=(.*)/) {
		$boundary = $1;
		chomp $boundary;
		$boundary =~ s/\+/ /g;
		foreach (split(/$boundary/,$buffer)) {
			s!--$!!so;
			if(m/Content-Disposition: form-data; name="(.*?)"/is) {
				$name = $1;
			}
			if(m/Content-Disposition: form-data; name="$name".*?\015\012\015\012(.*)$/is) {
				$value = $1;
				$value =~ s!\015\012$!!so;
				$hash->{$name} = $value;
			}
			else { next; }
		}
	} else {
		@pairs = split(/&/, $buffer);

		foreach $pair (@pairs)
		{
			$pair =~ s/\+/ /g;
			($name, $value) = split(/=/, $pair);
			next unless $name; # fields MUST BE named!
			$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack('C', hex($1))/eg;
			$value =~s/[^\w\013\n!@#\$%\^\*()_\-\+=\{\}\[\]\\|;:\'\"<,>\.?\/`~\& ]//g;
			$hash->{$name} = $value;
    		}
    	}
	return %hash;
}

sub log
{
	system('/usr/bin/logger', '-t', 'smoothwall', $_[0]);
}

sub age
{
	my ($dev, $ino, $mode, $nlink, $uid, $gid, $rdev, $size,
	        $atime, $mtime, $ctime, $blksize, $blocks) = stat $_[0];
	my $now = time;

	my $totalsecs = $now - $mtime;
	my $days = int($totalsecs / 86400);
	my $totalhours = int($totalsecs / 3600);
	my $hours = $totalhours % 24;
	my $totalmins = int($totalsecs / 60);
	my $mins = $totalmins % 60;
	my $secs = $totalsecs % 60;

 	return "${days}d ${hours}h ${mins}m ${secs}s";
}

sub validip
{
	my $ip = $_[0];

	if (!($ip =~ /^(\d+)\.(\d+)\.(\d+)\.(\d+)$/)) {
		return 0; }
	else 
	{
		@octets = ($1, $2, $3, $4);
		foreach $_ (@octets)
		{
			if (/^0./) {
				return 0; }
			if ($_ < 0 || $_ > 255) {
				return 0; }
		}
		return 1;
	}
}

sub validmask
{
	my $mask = $_[0];

	# secord part an ip?
	if (&validip($mask)) {
		return 1; }
	# second part a number?
	if (/^0/) {
		return 0; }
	if (!($mask =~ /^\d+$/)) {
		return 0; }
	if ($mask >= 0 && $mask <= 32) {
		return 1; }
	return 0;
}

sub validipormask
{
	my $ipormask = $_[0];

	# see if it is a IP only.
	if (&validip($ipormask)) {
		return 1; }
	# split it into number and mask.
	if (!($ipormask =~ /^(.*?)\/(.*?)$/)) {
		return 0; }
	$ip = $1;
	$mask = $2;
	# first part not a ip?
	if (!(&validip($ip))) {
		return 0; }
	return &validmask($mask);
}

sub validipandmask
{
	my $ipandmask = $_[0];

	# split it into number and mask.
	if (!($ipandmask =~ /^(.*?)\/(.*?)$/)) {
		return 0; }
	$ip = $1;
	$mask = $2;
	# first part not a ip?
	if (!(&validip($ip))) {
		return 0; }
	return &validmask($mask);
}

sub validport
{
	$_ = $_[0];

	if (!/^\d+$/) {
		return 0; }
	if (/^0./) {
		return 0; }
	if ($_ >= 1 && $_ <= 65535) {
		return 1; }
	return 0;
}

sub validportrange
{
        my $ports = $_[0];
        my $left; my $right;    

        if (&validport($ports)) {
                return 1; }
        if ($ports =~ /:/)
        {
                $left = $`;
                $right = $';
                if (&validport($left) && &validport($right))
                {
                        if ($right > $left) {
                                return 1; }
                }
        }
        return 0;
}

sub validmac
{
	$_ = $_[0];

	if (/^[0-9a-fA-F]{2}[\:\-][0-9a-fA-F]{2}[\:\-][0-9a-fA-F]{2}[\:\-][0-9a-fA-F]{2}[\:\-][0-9a-fA-F]{2}[\:\-][0-9a-fA-F]{2}$/) {
		return 1; }
	return 0;
}

sub basename {
	my ($filename) = @_;
	$filename =~ m!.*/(.*)!;
	if ($1) {
		return $1;
	} else {
		return $filename;
	}
}

sub connectedstate {
	my $theconnstate;
	if ( -e "${swroot}/red/active" ) {
		$theconnstate = "connected";
	} elsif ( -e "/var/run/ppp-smooth.pid" ) {
		$theconnstate = "connecting";
	} else {
		$theconnstate = "idle";
	}
	return $theconnstate;
}


1;
