#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

require '/var/smoothwall/header.pl';

my (%cgiparams,%selected,%checked);
my $filename = "${swroot}/portfw/config";

&showhttpheaders();

$cgiparams{'ENABLED'} = 'off';
&getcgihash(\%cgiparams);

my $errormessage = '';

if ($cgiparams{'ACTION'} eq $tr{'add'})
{
	unless($cgiparams{'PROTOCOL'} =~ /^(tcp|udp)$/) { $errormessage = $tr{'invalid input'}; }
	unless(&validipormask($cgiparams{'EXT'}))
	{
		if ($cgiparams{'EXT'} ne '') {
			$errormessage = $tr{'source ip bad'}; }
		else {
			$cgiparams{'EXT'} = '0.0.0.0/0'; }
	}
	unless(&validportrange($cgiparams{'SRC_PORT'})) { $errormessage = $tr{'source port numbers'}; }
	if ($cgiparams{'DEST_PORT'}) {
		unless(&validport($cgiparams{'DEST_PORT'})) { $errormessage = $tr{'destination port numbers'}; } }
	else {
		$cgiparams{'DEST_PORT'} = 0; }
	unless(&validip($cgiparams{'DEST_IP'})) { $errormessage = $tr{'destination ip bad'}; }
	open(FILE, $filename) or die 'Unable to open config file.';
	my @current = <FILE>;
	close(FILE);
	my $line;
	foreach $line (@current)
	{
		my @temp = split(/\,/,$line);
		if($cgiparams{'SRC_PORT'} eq $temp[1] &&
			$cgiparams{'PROTOCOL'} eq $temp[0])
		{
			 $errormessage =  
				"$tr{'source port in use'} $cgiparams{'SRC_PORT'}";
		}
	}
	unless ($errormessage)
	{
		open(FILE,">>$filename") or die 'Unable to open config file.';
		flock FILE, 2;
		print FILE "$cgiparams{'PROTOCOL'},$cgiparams{'EXT'},$cgiparams{'SRC_PORT'},$cgiparams{'DEST_IP'},$cgiparams{'DEST_PORT'},$cgiparams{'ENABLED'}\n";
		close(FILE);
		undef %cgiparams;
		&log($tr{'forwarding rule added'});
		system('/usr/bin/setuids/setportfw');
	}
}
if ($cgiparams{'ACTION'} eq $tr{'remove'} || $cgiparams{'ACTION'} eq $tr{'edit'})
{
	open(FILE, "$filename") or die 'Unable to open config file.';
	my @current = <FILE>;
	close(FILE);

	my $count = 0;
	my $id = 0;
	my $line;
	foreach $line (@current)
	{
		$id++;
		if ($cgiparams{$id} eq "on") {
			$count++; }
	}
	if ($count == 0) {
		$errormessage = $tr{'nothing selected'}; }
	if ($count > 1 && $cgiparams{'ACTION'} eq $tr{'edit'}) {
		$errormessage = $tr{'you can only select one item to edit'}; }
	unless ($errormessage)
	{
		open(FILE, ">$filename") or die 'Unable to open config file.';
		flock FILE, 2;
		$id = 0;
		foreach $line (@current)
		{
			$id++;
			unless ($cgiparams{$id} eq "on") {
				print FILE "$line"; }
			elsif ($cgiparams{'ACTION'} eq $tr{'edit'})
			{
				chomp($line);
				my @temp = split(/\,/,$line);
				$cgiparams{'PROTOCOL'} = $temp[0];
				$cgiparams{'EXT'} = $temp[1];
				$cgiparams{'SRC_PORT'} = $temp[2];
				$cgiparams{'DEST_IP'} = $temp[3];
				$cgiparams{'DEST_PORT'} = $temp[4];
				$cgiparams{'ENABLED'} = $temp[5];
			}
		}
		close(FILE);
		system('/usr/bin/setuids/setportfw');
		&log($tr{'forwarding rule removed'});
	}
}
if ($cgiparams{'ACTION'} eq '')
{
	$cgiparams{'PROTOCOL'} = 'tcp';
	$cgiparams{'ENABLED'} = 'on';
}

$selected{'PROTOCOL'}{'udp'} = '';
$selected{'PROTOCOL'}{'tcp'} = '';
$selected{'PROTOCOL'}{$cgiparams{'PROTOCOL'}} = 'SELECTED';

$checked{'ENABLED'}{'off'} = '';
$checked{'ENABLED'}{'on'} = '';  
$checked{'ENABLED'}{$cgiparams{'ENABLED'}} = 'CHECKED';

&openpage($tr{'port forwarding configuration'}, 1, '', 'networking');

&shownetworkingsection();

&openbigbox('100%', 'LEFT');

&alertbox($errormessage);

print <<END
<!--
<CENTER>
<TABLE BORDER='0' CELLPADDING='0' CELLSPACING='0'>
<TR><TD VALIGN='top' ALIGN='CENTER'>
<A HREF='http://www.smoothwall.co.uk/'><IMG
 SRC='/ui/assets/3.5/img/inlinepromo.smoothhost.png' BORDER='0'
 ALT='Visit smoothwall.co.uk for enhanced commercial SmoothWall products'></A>
</TD></TR>
</TABLE>
</CENTER>
 -->
END
;

print "<FORM METHOD='POST'>\n";

&openbox('100%', 'LEFT', $tr{'add a new rule'});
print <<END
<TABLE WIDTH='100%'>
<TR>
<TD WIDTH='35%' CLASS='base'><FONT COLOR='$colourred'>$tr{'sourcec'}</FONT></TD>
<TD WIDTH='20%'><INPUT TYPE='TEXT' NAME='EXT' VALUE='$cgiparams{'EXT'}' SIZE=18'></TD>
<TD WIDTH='15%'CLASS='base'><FONT COLOR='$colourred'>$tr{'source port or rangec'}</FONT></TD>
<TD WIDTH='15%'><INPUT TYPE='TEXT' NAME='SRC_PORT' VALUE='$cgiparams{'SRC_PORT'}' SIZE='10'></TD>
<TD CLASS='base'>$tr{'destination ipc'}</TD>
<TD><INPUT TYPE='TEXT' NAME='DEST_IP' VALUE='$cgiparams{'DEST_IP'}' SIZE='18'></TD>
<TD CLASS='base'>$tr{'destination portc'}<IMG SRC='/ui/assets/3.5/img/blob.gif' VALIGN='top'>&nbsp;</TD>
<TD><INPUT TYPE='TEXT' NAME='DEST_PORT' VALUE='$cgiparams{'DEST_PORT'}' SIZE='8'></TD>
</TR>
</TABLE>
<TABLE WIDTH='100%'>
<TR>
<TD WIDTH='20%' ALIGN='CENTER'>
<SELECT NAME='PROTOCOL'>
<OPTION VALUE='udp' $selected{'PROTOCOL'}{'udp'}>UDP
<OPTION VALUE='tcp' $selected{'PROTOCOL'}{'tcp'}>TCP
</SELECT>
</TD>
<TD CLASS='base' WIDTH='40%' ALIGN='CENTER'>$tr{'enabled'}<INPUT TYPE='CHECKBOX' NAME='ENABLED' $checked{'ENABLED'}{'on'}></TD>
<TD WIDTH='40%' ALIGN='CENTER'><INPUT TYPE='SUBMIT' NAME='ACTION' VALUE='$tr{'add'}'></TD>
</TR>
</TABLE>
<BR>
<IMG SRC='/ui/assets/3.5/img/blob.gif' VALIGN='top'>&nbsp;
<FONT CLASS='base'>$tr{'portfw destination port'}</FONT>
END
;
&closebox();

&openbox('100%', 'LEFT', $tr{'current rules'});
print <<END
<TABLE WIDTH='100%'>
<TR>
<TD WIDTH='10%' CLASS='boldbase' ALIGN='CENTER'><B>$tr{'protocol'}</B></TD>
<TD WIDTH='15%' CLASS='boldbase' ALIGN='CENTER'><B>External source IP</B></TD>
<TD WIDTH='20%' CLASS='boldbase' ALIGN='CENTER'><B>$tr{'source port'}</B></TD>
<TD WIDTH='20%' CLASS='boldbase' ALIGN='CENTER'><B>$tr{'destination ip'}</B></TD>
<TD WIDTH='15%' CLASS='boldbase' ALIGN='CENTER'><B>$tr{'destination port'}</B></TD>
<TD WIDTH='10%' CLASS='boldbase' ALIGN='CENTER'><B>$tr{'enabledtitle'}</B></TD>
<TD WIDTH='10%' CLASS='boldbase' ALIGN='CENTER'><B>$tr{'mark'}</B></TD>
</TR>
END
;

my $id = 0;
open(RULES, "$filename") or die 'Unable to open config file.';
while (<RULES>)
{
	my $protocol = '';
	my $gif = '';
	$id++;
	chomp($_);
	my @temp = split(/\,/,$_);
	if ($temp[0] eq 'udp') {
		$protocol = 'UDP'; }
	else {
		$protocol = 'TCP' }
	if ($temp[1] eq '0.0.0.0/0') {
		$external = $tr{'all'}; }
	else {
		$external = $temp[1]; }
	if ($temp[4] eq '0') {
		$destport = 'N/A'; }
	else {
		$destport = $temp[4]; }

	if ($id % 2) {
		print "<TR BGCOLOR='$table1colour'>\n"; }
	else {
              	print "<TR BGCOLOR='$table2colour'>\n"; }
	if ($temp[5] eq 'on') { $gif = 'on.gif'; }
		else { $gif = 'off.gif'; }
print <<END
<TD ALIGN='CENTER'>$protocol</TD>
<TD ALIGN='CENTER'>$external</TD>
<TD ALIGN='CENTER'>$temp[2]</TD>
<TD ALIGN='CENTER'>$temp[3]</TD>
<TD ALIGN='CENTER'>$destport</TD>
<TD ALIGN='CENTER'><IMG SRC='/ui/assets/3.5/img/$gif'></TD>
<TD ALIGN='CENTER'><INPUT TYPE='CHECKBOX' NAME='$id'></TD>
</TR>
END
	;
}
close(RULES);

print <<END
</TABLE>
<TABLE WIDTH='100%'>
<TR>
<TD WIDTH='50%' ALIGN='CENTER'><INPUT TYPE='SUBMIT' NAME='ACTION' VALUE='$tr{'remove'}'></TD>
<TD WIDTH='50%' ALIGN='CENTER'><INPUT TYPE='SUBMIT' NAME='ACTION' VALUE='$tr{'edit'}'></TD>
</TR>
</TABLE>
END
;
&closebox();

&alertbox('add','add');

&closebigbox();

&closepage();

