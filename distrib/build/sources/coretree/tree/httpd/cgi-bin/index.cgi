#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

require '/var/smoothwall/header.pl';

my %pppsettings;
my %modemsettings;
my %netsettings;

&showhttpheaders();

$pppsettings{'VALID'} = '';
$pppsettings{'PROFILENAME'} = 'None';
&readhash("${swroot}/ppp/settings", \%pppsettings);
&readhash("${swroot}/modem/settings", \%modemsettings);
&readhash("${swroot}/ethernet/settings", \%netsettings);

if ($pppsettings{'COMPORT'} =~ /^tty/)
{
	if (-e "/var/run/ppp-smooth.pid")
	{
		if (-e "${swroot}/red/active")
		{
			$timestr = &age("${swroot}/red/active");
			$connstate = "$tr{'connected'} (<FONT COLOR='#b04040'>$timestr</FONT>)"; 
		}
		else
		{
			if (-e "${swroot}/red/dial-on-demand")
			{
				$refresh = "<META HTTP-EQUIV='refresh' CONTENT='30;'>";
				$connstate = $tr{'modem dod waiting'};
			}
			else
			{
				$refresh = "<META HTTP-EQUIV='refresh' CONTENT='5;'>";
				$connstate = $tr{'dialing'};
			}
		}
	}
	else {
		$connstate = $tr{'modem idle'};
	 }
}
elsif ($pppsettings{'COMPORT'} =~ /^isdn/) 
{
	$channels = &countisdnchannels();
	if ($channels == 0) {
		$number = 'none!'; }
	elsif ($channels == 1) {
		$number = 'single'; }
	else {
		$number = 'dual'; }
		
	if (-e "${swroot}/red/active")
	{
		$timestr = &age("${swroot}/red/active");
		$connstate = "$tr{'connected'} - $number channel (<FONT COLOR='#b04040'>$timestr</FONT>)";
 	}
	else 
	{
		if ($channels == 0)
		{
			if (-e "${swroot}/red/dial-on-demand")
			{
				$connstate = $tr{'isdn dod waiting'};
				$refresh = "<META HTTP-EQUIV='refresh' CONTENT='30;'>"
			} else {
				$connstate = $tr{'isdn idle'};
			}
		}
		else
		{
			$connstate = $tr{'dialing'};
                 	$refresh = "<META HTTP-EQUIV='refresh' CONTENT='5;'>";
		}
	}
}
elsif ($pppsettings{'COMPORT'} eq 'pppoe')
{
	if (-e "${swroot}/red/active" )
	{
		$timestr = &age("${swroot}/red/active");
		$connstate = "$tr{'connected'} (<FONT COLOR='#b04040'>$timestr</FONT>)";
	}
	else
	{
		if (-e "/var/run/ppp-smooth.pid")
		{
			$connstate = $tr{'dialing'};
			$refresh = "<META HTTP-EQUIV='refresh' CONTENT='5;'>"
		}
		else
		{
			$connstate = $tr{'pppoe idle'};
		}
	}
}
else
{
	if (-e "${swroot}/red/active" )
	{
		$timestr = &age("${swroot}/red/active");
		$connstate = "$tr{'connected'} (<FONT COLOR='#b04040'>$timestr</FONT>)";
	}
	else
	{
		if (-e "/var/run/ppp-smooth.pid")
		{
			$connstate = $tr{'dialing'};
			$refresh = "<META HTTP-EQUIV='refresh' CONTENT='5;'>"
		}
		else
		{
			$connstate = $tr{'adsl idle'};
		}
	}
}

&openpage($tr{'main page'}, 1, $refresh, 'control');

print <<END
<CENTER>
<DIV ALIGN='CENTER'>
END
;

&openbigbox('70%', 'CENTER');

&alertbox($errormessage);

print <<END
<DIV ALIGN='CENTER'>
<TABLE BORDER='0' CELLPADDING='0' CELLSPACING='0'>
<TR><TD>
</TD></TR>
</TABLE>
</DIV>
END
;

print <<END
<DIV ALIGN='CENTER'>
<!-- <A HREF='$adurl'><IMG SRC='$adimg' BORDER='0' HEIGHT='40' WIDTH='600'
 ALT='$adalt'></A><BR><BR> -->
<TABLE WIDTH='100%' BORDER='0' CELLPADDING='0' CELLSPACING='0'>
<TR><!-- <TD VALIGN='top' ALIGN='CENTER' WIDTH='200'>
<A HREF='http://www.smoothwall.co.uk/'><IMG 
 SRC='/ui/assets/3.5/img/gpl.index.left.corpresell.gif' BORDER='0'
 ALT='Visit smoothwall.co.uk for enhanced commercial SmoothWall products'></A><br>
<IMG SRC='/ui/assets/3.5/img/null.gif' ALT='' width='200' height='5'><BR>
<A HREF='http://www.smoothwall.co.uk/store/'><IMG 
 SRC='/ui/assets/3.5/img/gpl.index.left.store.png' BORDER='0' ALT=''></A><BR>
<IMG SRC='/ui/assets/3.5/img/null.gif' ALT='' width='200' height='5'><BR>
<A HREF='http://www.smoothwall.org/'><IMG 
 SRC='/ui/assets/3.5/img/gpl.index.left.community.png' BORDER='0' ALT=''></A><BR>
</TD>
<td>&nbsp;</td> -->
<TD VALIGN='TOP'>
<CENTER>
END
;

&openbox('');

$currentconnection = &connectedstate();
print <<END
<table border='0' cellpadding='5' cellspacing='0'>
<tr><td valign='top'><img src='/ui/assets/3.5/img/netstatus.$currentconnection.gif'
 alt='$connpick'></td><td align='center' valign='middle'>
END
;

if ($pppsettings{'COMPORT'} ne '')
{
	if ($pppsettings{'VALID'} eq 'yes')
	{
		print <<END
<TABLE BORDER='0'>
<FORM METHOD='POST' ACTION='/cgi-bin/dial.cgi'>
<TR>
	<TD ALIGN='CENTER'><INPUT TYPE='submit' NAME='ACTION' VALUE='$tr{'dial'}'></TD>
	<td>&nbsp;&nbsp;</td>
	<TD ALIGN='CENTER'><INPUT TYPE='submit' NAME='ACTION' VALUE='$tr{'hangup'}'></TD>
	<td>&nbsp;&nbsp;</td>
</FORM>
<FORM METHOD='POST'>
	<TD ALIGN='CENTER'><INPUT TYPE='submit' NAME='ACTION' VALUE='$tr{'refresh'}'></TD>
</FORM>
</TR>
</TABLE>
END
		;
	}
	elsif (-e "${swroot}/red/active" )
	{
		print <<END
<FORM METHOD='POST' ACTION='/cgi-bin/dial.cgi'>
<INPUT TYPE='submit' NAME='ACTION' VALUE='$tr{'hangup'}'>
</FORM>
END
		;
	}

	print "<FONT FACE='Helvetica' SIZE='4'><B>";
	print "<U>$tr{'current profile'} $pppsettings{'PROFILENAME'}</U><BR>\n";
	
	if ($pppsettings{'VALID'} eq 'yes' && $modemsettings{'VALID'} eq 'yes')
	{
		print $connstate;
	}
	elsif ($modemsettings{'VALID'} eq 'no') {
		print "$tr{'modem settings have errors'}\n"; }
	else {
		print "$tr{'profile has errors'}\n"; }

	print "</B></FONT>\n";
	print "</CENTER>\n";
}
else
{
	print <<END
<FORM METHOD='POST'>
<INPUT TYPE='submit' NAME='ACTION' VALUE='$tr{'refresh'}'>
</FORM>
END
	;
}
	print <<END
</td></tr>
</table>
END
;

&closebox();

open(AV, "${swroot}/patches/available") or die "Could not open available patches database ($!)";
@av = <AV>;
close(AV);
open(PF, "${swroot}/patches/installed") or die "Could not open installed patches file. ($!)<br>";
while(<PF>)
{
        next if $_ =~ m/^#/;
        @temp = split(/\|/,$_);
        @av = grep(!/^$temp[0]/, @av);
}
close(PF);

if ($#av != -1)
{
	&pageinfo($alertbox{"texterror"}, "$tr{'there are updates'}");
}
$age = &age("/${swroot}/patches/available");
if ($age =~ m/(\d{1,3})d/)
{
	if ($1 >= 7)
	{
		&pageinfo($alertbox{"texterror"}, "$tr{'updates is old1'} $age $tr{'updates is old2'}");
	}
}
system('/usr/bin/uptime');

print <<END
</CENTER>
</TD>
</TR>
</TABLE>
</DIV>
END
;

&alertbox('add','add');

&closebigbox();

print <<END
</CENTER>
</DIV>
END
;

&closepage();

sub countisdnchannels
{
	my ($idmap, $chmap, $drmap, $usage, $flags, $phone);
	my @phonenumbers;
	my $count;

	open (FILE, "/dev/isdninfo");

	$idmap = <FILE>; chop $idmap;
	$chmap = <FILE>; chop $chmap;
	$drmap = <FILE>; chop $drmap;
	$usage = <FILE>; chop $usage;
	$flags = <FILE>; chop $flags;
	$phone = <FILE>; chop $phone;

	$phone =~ s/^phone(\s*):(\s*)//;

	@phonenumbers = split / /, $phone;

	$count = 0;
	foreach (@phonenumbers)
	{
 		if ($_ ne '???') {
			$count++; }
	}
	
	return $count;
}

