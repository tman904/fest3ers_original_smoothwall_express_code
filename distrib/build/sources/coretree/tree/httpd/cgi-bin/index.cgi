#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );

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

&openbigbox('70%', 'CENTER');

&alertbox($errormessage);

&openbox('');

$currentconnection = &connectedstate();
print <<END
<table class='centered'>
	<tr>
		<td valign='top'><img src='/ui/img/netstatus.$currentconnection.gif' alt='$connpick'></td><td align='center' valign='middle'></td>
END
;

if ($pppsettings{'COMPORT'} ne '')
{
	if ($pppsettings{'VALID'} eq 'yes')
	{
		print <<END
<td style='vertical-align: top;'>
<table>
	<tr>
		<form method='post' action='/cgi-bin/dial.cgi'>
		<td style='text-align: center;'><input type='submit' name='ACTION' value='$tr{'dial'}'></td>
		<td>&nbsp;&nbsp;</td>
		<td style='text-align: center;'><input type='submit' name='ACTION' value='$tr{'hangup'}'></td>
		<td>&nbsp;&nbsp;</td>
		</form>
		<form method='post'>
		<td style='text-align: center;'><input type='submit' name='ACTION' value='$tr{'refresh'}'></td>
		</form>
	</tr>
</table>
</td>
END
		;
	}
	elsif (-e "${swroot}/red/active" )
	{
		print <<END
<td style='vertical-align: top;'>
<form method='post' action='/cgi-bin/dial.cgi'>
	<input type='submit' name='ACTION' value='$tr{'hangup'}'>
</form>
</td>
END
		;
	}

	print "<td><strong>$tr{'current profile'} $pppsettings{'PROFILENAME'}</strong><br/>\n";
	
	if ($pppsettings{'VALID'} eq 'yes' && $modemsettings{'VALID'} eq 'yes')
	{
		print $connstate;
	}
	elsif ($modemsettings{'VALID'} eq 'no') {
		print "$tr{'modem settings have errors'}\n"; }
	else {
		print "$tr{'profile has errors'}\n"; }

	print "</td>";

}
else
{
	print <<END
<td style='vertical-align: top;'>
<form method='post'>
	<input type='submit' name='ACTION' value='$tr{'refresh'}'>
</form>
</td>
END
	;
}
	print <<END
	</tr>
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

print "<br/><table class='blank'><tr><td class='note'>";

system('/usr/bin/uptime');

print "</td></tr></table>\n";

&closebigbox();

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

