#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );

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

&openbigbox('100%', 'LEFT');

&alertbox($errormessage);

print "<FORM METHOD='POST'>\n";

&openbox($tr{'add a new rule'});
print <<END
<table>
<tr>
	<td style='width: 35%;'>$tr{'sourcec'}</td>
	<td style='width: 20%;'><input type='text' name='EXT' value='$cgiparams{'EXT'}' size=18'></td>
	<td style='width: 15%;'>$tr{'source port or rangec'}</td>
	<td style='width: 15%;'><input type='text' name='SRC_PORT' value='$cgiparams{'SRC_PORT'}' size='10'></td>
</tr>
<tr>
	<td>$tr{'destination ipc'}</td>
	<td><input type='text' name='DEST_IP' value='$cgiparams{'DEST_IP'}' size='18'></td>
	<td>$tr{'destination portc'}<img src='/ui/img/blob.gif'>&nbsp;</td>
	<td><input type='text' name='DEST_PORT' value='$cgiparams{'DEST_PORT'}' size='8'></td>
</tr>
<tr>
	<td>$tr{'protocol'}</td>
	<td>
		<select name='PROTOCOL'>
			<option value='udp' $selected{'PROTOCOL'}{'udp'}>UDP
			<option value='tcp' $selected{'PROTOCOL'}{'tcp'}>TCP
		</select>
	</td>
	<td>$tr{'enabled'}<input type='checkbox' name='ENABLED' $checked{'ENABLED'}{'on'}></td>
	<td><input type='submit' name='ACTION' value='$tr{'add'}'></td>
</tr>
</table>
<br/>
<img src='/ui/img/blob.gif'>&nbsp;$tr{'portfw destination port'}
END
;
&closebox();

&openbox($tr{'current rules'});
print <<END
<table class='centered'>
<tr>
	<th style='width: 10%;'>$tr{'protocol'}</th>
	<th style='width: 15%;'>External source IP</th>
	<th style='width: 20%;'>$tr{'source port'}</th>
	<th style='width: 20%;'>$tr{'destination ip'}</th>
	<th style='width: 15%;'>$tr{'destination port'}</th>
	<th style='width: 10%;'>$tr{'enabledtitle'}</th>
	<th style='width: 10%;'>$tr{'mark'}</th>
</tr>
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
		print "<tr class='dark'>\n"; }
	else {
              	print "<tr class='light'>\n"; }
	if ($temp[5] eq 'on') { $gif = 'on.gif'; }
		else { $gif = 'off.gif'; }
print <<END
<td>$protocol</td>
<td>$external</td>
<td>$temp[2]</td>
<td>$temp[3]</td>
<td>$destport</td>
<td><img src='/ui/img/$gif'></td>
<td><input type='checkbox' name='$id'></td>
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

