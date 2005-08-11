#!/usr/bin/perl
#
# SmoothWall CGIs
#
# (c) SmoothWall Ltd, 2002-2003

use lib "/usr/lib/smoothwall";
use header qw( :standard );

my (%cgiparams,%selected);
my $filename = "${swroot}/hosts/config";

&showhttpheaders();

$cgiparams{'ENABLED'} = 'off';
&getcgihash(\%cgiparams);

my $errormessage = '';

if ($cgiparams{'ACTION'} eq $tr{'add'})
{
	unless(&validip($cgiparams{'IP'})) { $errormessage = $tr{'ip address not valid'}; }
	unless(&validhostname($cgiparams{'HOSTNAME'})) { $errormessage = $tr{'invalid hostname'}; }

	unless ($errormessage)
	{
		open(FILE,">>$filename") or die 'Unable to open config file.';
		flock FILE, 2;
		print FILE "$cgiparams{'IP'},$cgiparams{'HOSTNAME'},$cgiparams{'ENABLED'},$cgiparams{'COMMENT'}\n";
		close(FILE);
		undef %cgiparams;
		&log($tr{'host added to hosts list.'});
		system('/usr/bin/writehosts.pl');
                system('/usr/bin/setuids/restartdnsproxy', 'HUP');
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
				$cgiparams{'IP'} = $temp[0];
				$cgiparams{'HOSTNAME'} = $temp[1];
				$cgiparams{'ENABLED'} = $temp[2];
				$cgiparams{'COMMENT'} = $temp[3];
			}
		}
		close(FILE);
 		system('/usr/bin/writehosts.pl');
                system('/usr/bin/setuids/restartdnsproxy', 'HUP');
		&log($tr{'host removed from host list'});
	}
}
if ($cgiparams{'ACTION'} eq '')
{
	$cgiparams{'ENABLED'} = 'on';
}

$checked{'ENABLED'}{'off'} = '';
$checked{'ENABLED'}{'on'} = '';  
$checked{'ENABLED'}{$cgiparams{'ENABLED'}} = 'CHECKED';

&openpage($tr{'static dns configuration'}, 1, '', 'services');

&openbigbox('100%', 'LEFT');

&alertbox( $errormessage );

print "<FORM METHOD='POST'>\n";

&openbox($tr{'add a host'});
print <<END
<TABLE WIDTH='100%'>
<TR>
<TD WIDTH='20%' CLASS='base'>$tr{'ip addressc'}</TD>
<TD WIDTH='30%'><INPUT TYPE='TEXT' NAME='IP' VALUE='$cgiparams{'IP'}' SIZE='15'></TD>
<TD WIDTH='20%' CLASS='base'>$tr{'hostnamec'}</TD>
<TD WIDTH='30%'><INPUT TYPE='TEXT' NAME='HOSTNAME' VALUE='$cgiparams{'HOSTNAME'}' SIZE='15'></TD>
</TR>
<TR>
<TD WIDTH='10%' CLASS='base'>$tr{'commentc'}</TD>
<TD WIDTH='40%'><INPUT TYPE='TEXT' NAME='COMMENT' VALUE='$cgiparams{'COMMENT'}' SIZE='50'></TD>
<TD WIDTH='25%' CLASS='base' ALIGN='CENTER'>$tr{'enabled'}<INPUT TYPE='CHECKBOX' NAME='ENABLED' $checked{'ENABLED'}{'on'}></TD>
<TD WIDTH='25%' ALIGN='CENTER'><INPUT TYPE='SUBMIT' NAME='ACTION' VALUE='$tr{'add'}'></TD>
</TR>
</TABLE>
END
;
&closebox();

&openbox($tr{'current hosts'});
print <<END
<table class='centered'>
<tr>
<th style='width: 40%; text-align: center;'>$tr{'ip address'}</th>
<th style='width: 40%; text-align: center;'>$tr{'hostname'}</th>
<th style='width: 10%; text-align: center;'>$tr{'enabledtitle'}</th>
<th style='width: 10%; text-align: center;'>$tr{'mark'}</th>
</tr>
<tr>
<th colspan='4' style='text-align: center;'>$tr{'comment'}</th>
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

	if ($temp[2] eq 'on') {
		$gif = 'on.gif'; }
	else {
		$gif = 'off.gif'; }
	if ($id % 2) {
		$colour = 'light'; }
	else {
		$colour = 'dark'; }
print <<END
<tr class='$colour'>
<td style='text-align: center;'>$temp[0]</td>
<td style='text-align: center;'>$temp[1]</td>
<td style='text-align: center;'><img src='/ui/img/$gif'></td>
<td style='text-align: center;'><input type='checkbox' name='$id'></td>
</tr>
END
	;
	if ($temp[3])
	{
		print <<END
<tr class='$colour'>
<td colspan='4' style='text-align: center;'>$temp[3]</td>
</tr>
END
		;
	}
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

&alertbox( "add", "add" );

&closebigbox();

&closepage();
