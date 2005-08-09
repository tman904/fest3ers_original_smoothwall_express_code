#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );

my (%cgiparams,%checked);
my $filename = "${swroot}/vpn/config";

$cgiparams{'ENABLED'} = 'off';
&getcgihash(\%cgiparams);

my $errormessage = '';

if ($cgiparams{'ACTION'} eq $tr{'save'})
{
	if ($cgiparams{'VPN_IP'})
	{
		unless (&validip($cgiparams{'VPN_IP'})) {
			$errormessage = $tr{'invalid input'}; }
	}
	if ($errormessage) {
		$cgiparams{'VALID'} = 'no'; }
	else {
		$cgiparams{'VALID'} = 'yes'; }

	&writehash("${swroot}/vpn/settings", \%cgiparams);
}
&readhash("${swroot}/vpn/settings", \%cgiparams);

if ($cgiparams{'ACTION'} eq $tr{'restart'})
{
	system('/usr/bin/setuids/ipsecctrl', 'R');
}
if ($cgiparams{'ACTION'} eq $tr{'stop'})
{
	system('/usr/bin/setuids/ipsecctrl', 'S');
}

if ($cgiparams{'VALID'} eq '')
{
        $cgiparams{'ENABLE'} = 'off';
}

$checked{'ENABLED'}{'off'} = '';
$checked{'ENABLED'}{'on'} = '';
$checked{'ENABLED'}{$cgiparams{'ENABLED'}} = 'CHECKED';

&showhttpheaders();

&openpage($tr{'vpn configuration main'}, 1, '', 'vpn');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage);

print <<END
<!-- 
<CENTER>
<TABLE BORDER='0' CELLPADDING='0' CELLSPACING='0'>
<TR><TD VALIGN='top' ALIGN='CENTER'>
<A HREF='http://www.smoothwall.co.uk/'><IMG
 SRC='/ui/assets/3.5/img/inlinepromo.smoothtunnel.png' BORDER='0'
 ALT='Visit smoothwall.co.uk for enhanced commercial SmoothWall products'></A>
</TD></TR>
</TABLE>
</CENTER>
 -->
END
;


print "<FORM METHOD='POST'>\n";

&openbox($tr{'global settingsc'});
print <<END
<TABLE WIDTH='100%'>
<TR>
<TD WIDTH='25%' CLASS='base'>$tr{'local vpn ip'}&nbsp;<IMG SRC='/ui/assets/3.5/img/blob.gif'></TD>
<TD WIDTH='25%' ><INPUT TYPE='TEXT' NAME='VPN_IP' VALUE='$cgiparams{'VPN_IP'}' SIZE='15'></TD>
<TD WIDTH='25%' CLASS='base'>$tr{'enabled'}<INPUT TYPE='CHECKBOX' NAME='ENABLED' $checked{'ENABLED'}{'on'}></TD>
<TD WIDTH='25%' ALIGN='CENTER'><INPUT TYPE='SUBMIT' NAME='ACTION' VALUE='$tr{'save'}'></TD>
</TR>
</TABLE>
<BR>
<IMG SRC='/ui/assets/3.5/img/blob.gif' VALIGN='top'>&nbsp;
<FONT CLASS='base'>$tr{'if blank the currently configured ethernet red address will be used'}</FONT>
END
;
&closebox();

&openbox($tr{'manual control and status'});
print <<END
<DIV ALIGN='CENTER'>
<TABLE WIDTH='80%'>
<TR>
<TD ALIGN='LEFT'><INPUT TYPE='SUBMIT' NAME='ACTION' VALUE='$tr{'restart'}'></TD>
<TD ALIGN='RIGHT'><INPUT TYPE='SUBMIT' NAME='ACTION' VALUE='$tr{'stop'}'></TD>
</TR>
</TABLE>
END
;
open (FILE, "$filename");
my @current = <FILE>;
close (FILE);

open (ACTIVE, "/proc/net/ipsec_eroute");
my @active = <ACTIVE>;
close (ACTIVE);

print <<END
<TABLE WIDTH='60%'>
<TR>
<TD ALIGN='CENTER'><B>$tr{'connection name'}</B></TD><TD
ALIGN='CENTER'><B>$tr{'connection status'}</B></TD>
</TR>
END
;

my $id = 0;
my $line;

foreach $line (@current)
{
	$id++;
	chomp($line);
	my @temp = split(/\,/,$line);
	my $name = $temp[0];
	my $netmaskl = $temp[2];
	$netmaskl =~ /\//; $netmaskl = $`;
	my $netmaskr = $temp[4];
	$netmaskr =~ /\//; $netmaskr = $`;
	my $active = "<TABLE CELLPADDING='2' CELLSPACING='0' BGCOLOR='$colourlightred''><TR><TD><B>$tr{'capsclosed'}</B></TD></TR></TABLE>";
	if ($temp[8] eq 'off') {
		$active = "<TABLE CELLPADDING='2' CELLSPACING='0' BGCOLOR='#000000'><TR><TD><B>$tr{'capsdisabled'}</B></TD></TR></TABLE>"; }

	foreach $line (@active)
	{
		@temp = split(/[\t ]+/,$line);
		$d = 0;
		$targetl = $temp[1];
		$targetl =~ /\//; $targetl = $`;
		$targetr = $temp[3];
		$targetr =~ /\//; $targetr = $`;
		if (($targetl eq $netmaskl && $targetr eq $netmaskr) ||
			($targetl eq $netmaskr && $targetr eq $netmaskl))
		 {
			$active = "<TABLE CELLPADDING='2' CELLSPACING='0' BGCOLOR='$colourlightgreen'><TR><TD><B>$tr{'capsopen'}</B></TD></TR></TABLE>";
		}
	}
	if ($id % 2) {
		print "<TR BGCOLOR='$table1colour'>\n"; }
	else {
		print "<TR BGCOLOR='$table2colour'>\n"; }
	print "<TD ALIGN='CENTER'>$name</TD><TD ALIGN='CENTER'>$active</TD>\n";
	print "</TR>\n";
}
print "</TABLE>\n";

print "</DIV>\n";

&closebox();

&alertbox('add','add');

&closebigbox();

&closepage();
