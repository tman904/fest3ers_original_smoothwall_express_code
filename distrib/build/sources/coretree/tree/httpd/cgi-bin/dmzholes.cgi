#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );

my (%cgiparams,%checked,%selected);
my $filename = "${swroot}/dmzholes/config";

&showhttpheaders();

$cgiparams{'ENABLED'} = 'off';
&getcgihash(\%cgiparams);

my $errormessage = '';

if ($cgiparams{'ACTION'} eq $tr{'add'})
{
	unless($cgiparams{'PROTOCOL'} =~ /^(tcp|udp)$/) { $errormessage = $tr{'invalid input'}; }
	unless(&validip($cgiparams{'SRC_IP'})) { $errormessage = $tr{'source ip bad'}; }
	unless(&validport($cgiparams{'DEST_PORT'})) { $errormessage = $tr{'destination port numbers'}; }
	unless(&validip($cgiparams{'DEST_IP'})) { $errormessage = $tr{'destination ip bad'}; }
	open(FILE, $filename) or die 'Unable to open config file.';
	my @current = <FILE>;
	close(FILE);
	unless ($errormessage)
	{
		open(FILE,">>$filename") or die 'Unable to open config file.';
		flock FILE, 2;
		print FILE "$cgiparams{'PROTOCOL'},$cgiparams{'SRC_IP'},$cgiparams{'DEST_IP'},$cgiparams{'DEST_PORT'},$cgiparams{'ENABLED'}\n";
		close(FILE);
		undef %cgiparams;
		&log($tr{'dmz pinhole rule added'});
		system('/usr/bin/setuids/setdmzholes');
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
				$cgiparams{'SRC_IP'} = $temp[1];
				$cgiparams{'DEST_IP'} = $temp[2];
				$cgiparams{'DEST_PORT'} = $temp[3];
				$cgiparams{'ENABLED'} = $temp[4];
			}
		}
		close(FILE);
		system('/usr/bin/setuids/setdmzholes');
		&log($tr{'dmz pinhole rule removed'});
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

&openpage($tr{'dmz pinhole configuration'}, 1, '', 'networking');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage);

print "<FORM METHOD='POST'>\n";

&openbox($tr{'add a new rule'});
print <<END
<TABLE WIDTH='100%'>
<TR>
<TD>
<SELECT NAME='PROTOCOL'>
<OPTION VALUE='udp' $selected{'PROTOCOL'}{'udp'}>UDP
<OPTION VALUE='tcp' $selected{'PROTOCOL'}{'tcp'}>TCP
</SELECT>
</TD>
<TD CLASS='base'><FONT COLOR='$colourorange'>$tr{'source ipc'}</FONT></TD>
<TD><INPUT TYPE='TEXT' NAME='SRC_IP' VALUE='$cgiparams{'SRC_IP'}' SIZE='15'></TD>
<TD CLASS='base'><FONT COLOR='$colourgreen'>$tr{'destination ipc'}</FONT></TD>
<TD><INPUT TYPE='TEXT' NAME='DEST_IP' VALUE='$cgiparams{'DEST_IP'}' SIZE='15'></TD>
<TD CLASS='base'><FONT COLOR='$colourgreen'>$tr{'destination portc'}</FONT></TD>
<TD><INPUT TYPE='TEXT' NAME='DEST_PORT' VALUE='$cgiparams{'DEST_PORT'}' SIZE='5'></TD>
</TR>
</TABLE>
<TABLE WIDTH='100%'>
<TR>
<TD CLASS='base' WIDTH='50%' ALIGN='CENTER'>$tr{'enabled'}<INPUT TYPE='CHECKBOX' NAME='ENABLED' $checked{'ENABLED'}{'on'}></TD>
<TD WIDTH='50%' ALIGN='CENTER'><INPUT TYPE='SUBMIT' NAME='ACTION' VALUE='$tr{'add'}'></TD>
</TR>
</TABLE>
END
;
&closebox();

&openbox($tr{'current rules'});
print <<END
<table class='centered'>
<tr>
<th style='width: 15%; text-align: center;'>$tr{'protocol'}</th>
<th style='width: 20%; text-align: center;'>$tr{'source ip'}</th>
<th style='width: 20%; text-align: center;'>$tr{'destination ip'}</th>
<th style='width: 15%; text-align: center;'>$tr{'destination port'}</th>
<th style='width: 10%; text-align: center;'>$tr{'enabledtitle'}</th>
<th style='width: 10%; text-align: center;'>$tr{'mark'}</th>
</tr>
END
;

my $id = 0;
open(RULES, "$filename") or die 'Unable to open config file.';
while (<RULES>)
{
	my ($protocol, $gif);
	$id++;
	chomp($_);
	my @temp = split(/\,/,$_);
	if ($temp[0] eq 'udp') {
		$protocol = 'UDP'; }
	else {
		$protocol = 'TCP' }
	if ($id % 2) {
		print "<tr class='dark'>\n"; }
	else {
              	print "<tr class='light'>\n"; }
	if ($temp[4] eq 'on') { $gif = 'on.gif'; }
		else { $gif = 'off.gif'; }
print <<END
<td style='text-align: center;'>$protocol</td>
<td style='text-align: center;'>$temp[1]</td>
<td style='text-align: center;'>$temp[2]</td>
<td style='text-align: center;'>$temp[3]</td>
<td style='text-align: center;'><IMG SRC='/ui/img/$gif'></td>
<td style='text-align: center;'><input type='checkbox' name='$id'></td>
</tr>
END
	;
}
close(RULES);

print <<END
</table>
<table class='blank'>
<tr>
<td style='width: 50%; text-align: center;'><input type='submit' name='ACTION' value='$tr{'remove'}'></td>
<td style='width: 50%; text-align: center;'><input type='submit' name='ACTION' value='$tr{'edit'}'></td>
</tr>
</table>
END
;
&closebox();

&alertbox('add','add');

&closebigbox();

&closepage();

