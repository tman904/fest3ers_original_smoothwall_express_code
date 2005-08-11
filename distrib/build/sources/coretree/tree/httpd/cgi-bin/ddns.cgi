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
my $filename = "${swroot}/ddns/config";

&showhttpheaders();

$cgiparams{'ENABLED'} = 'off';
$cgiparams{'PROXY'} = 'off';
$cgiparams{'WILDCARDS'} = 'off';
&getcgihash(\%cgiparams);

my $errormessage = '';
my @service = ();

if ($cgiparams{'ACTION'} eq $tr{'add'})
{
	unless ($cgiparams{'SERVICE'} =~ /^(dhs|dyndns-custom|dyndns|dyns|hn|no-ip|zoneedit|easydns|ods)$/) { $errormessage = $tr{'invalid input'}; }
	unless ($cgiparams{'LOGIN'} ne '') { $errormessage = $tr{'username not set'}; }
	unless ($cgiparams{'PASSWORD'} ne '') { $errormessage = $tr{'password not set'}; }
	unless ($cgiparams{'HOSTNAME'} ne '') { $errormessage = $tr{'hostname not set'}; }
	unless ($cgiparams{'HOSTNAME'} =~ /^[a-zA-Z_0-9-]+$/) { $errormessage = $tr{'invalid hostname'}; }
	unless ($cgiparams{'DOMAIN'} ne '') { $errormessage = $tr{'domain not set'}; }
	unless ($cgiparams{'DOMAIN'} =~ /^[a-zA-Z_0-9.-]+$/) { $errormessage = $tr{'invalid domain name'}; }
	unless ($cgiparams{'DOMAIN'} =~ /[.]/) { $errormessage = $tr{'invalid domain name'}; }
	open(FILE, $filename) or die 'Unable to open config file.';
	my @current = <FILE>;
	close(FILE);
	my $line;
	foreach $line (@current)
	{
		my @temp = split(/\,/,$line);
		if($cgiparams{'HOSTNAME'} eq $temp[1] &&
			$cgiparams{'DOMAIN'} eq $temp[2])
		{
			 $errormessage = $tr{'hostname and domain already in use'};
		}
	}
	unless ($errormessage)
	{
		open(FILE,">>$filename") or die 'Unable to open config file.';
		flock FILE, 2;
		print FILE "$cgiparams{'SERVICE'},$cgiparams{'HOSTNAME'},$cgiparams{'DOMAIN'},$cgiparams{'PROXY'},$cgiparams{'WILDCARDS'},$cgiparams{'LOGIN'},$cgiparams{'PASSWORD'},$cgiparams{'ENABLED'}\n";
		close(FILE);
		undef %cgiparams;
		&log($tr{'ddns hostname added'});
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
		my $id = 0;
		foreach $line (@current)
		{
			$id++;
			unless ($cgiparams{$id} eq "on") {
				print FILE "$line"; }
			elsif ($cgiparams{'ACTION'} eq $tr{'edit'})
			{
				chomp($line);
				my @temp = split(/\,/,$line);
				$cgiparams{'SERVICE'} = $temp[0];
				$cgiparams{'HOSTNAME'} = $temp[1];
				$cgiparams{'DOMAIN'} = $temp[2];
				$cgiparams{'PROXY'} = $temp[3];
				$cgiparams{'WILDCARDS'} = $temp[4];
				$cgiparams{'LOGIN'} = $temp[5];
				$cgiparams{'PASSWORD'} = $temp[6];
				$cgiparams{'ENABLED'} = $temp[7];
			}
		}
		close(FILE);
		&log($tr{'ddns hostname removed'});
	}
}

if ($cgiparams{'ACTION'} eq $tr{'force update'})
{
	system('/usr/bin/smoothwall/setddns.pl', '-f');
}

if ($cgiparams{'ACTION'} eq '')
{
	$cgiparams{'ENABLED'} = 'on';
}

$selected{'SERVICE'}{'dhs'} = '';
$selected{'SERVICE'}{'dyndns'} = '';
$selected{'SERVICE'}{'dyndns-custom'} = '';
$selected{'SERVICE'}{'dyns'} = '';
$selected{'SERVICE'}{'hn'} = '';
$selected{'SERVICE'}{'no-ip'} = '';
$selected{'SERVICE'}{'zoneedit'} = '';
$selected{'SERVICE'}{'easydns'} = '';
$selected{'SERIVCE'}{'ods'} = '';
$selected{'SERVICE'}{$cgiparams{'SERVICE'}} = 'SELECTED';

$checked{'PROXY'}{'off'} = '';
$checked{'PROXY'}{'on'} = '';
$checked{'PROXY'}{$cgiparams{'PROXY'}} = 'CHECKED';

$checked{'WILDCARDS'}{'off'} = '';
$checked{'WILDCARDS'}{'on'} = '';
$checked{'WILDCARDS'}{$cgiparams{'WILDCARDS'}} = 'CHECKED';

$checked{'ENABLED'}{'off'} = '';
$checked{'ENABLED'}{'on'} = '';  
$checked{'ENABLED'}{$cgiparams{'ENABLED'}} = 'CHECKED';

&openpage($tr{'dynamic dns'}, 1, '', 'services');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage);

print "<FORM METHOD='POST'>\n";

&openbox($tr{'add a host'});

print <<END
<TABLE WIDTH='100%'>
<TR>
	<TD WIDTH='25%' CLASS='base'>$tr{'servicec'}</TD>
	<TD WIDTH='25%'>
	<SELECT SIZE='1' NAME='SERVICE'>
	<OPTION VALUE='dhs' $selected{'SERVICE'}{'dhs'}>dhs.org
	<OPTION VALUE='dyndns' $selected{'SERVICE'}{'dyndns'}>dyndns.org
	<OPTION VALUE='dyndns-custom' $selected{'SERVICE'}{'dyndns-custom'}>dyndns.org (Custom)
	<OPTION VALUE='dyns' $selected{'SERVICE'}{'dyns'}>dyns.cx
	<OPTION VALUE='hn' $selected{'SERVICE'}{'hn'}>hn.org
	<OPTION VALUE='no-ip' $selected{'SERVICE'}{'no-ip'}>no-ip.com
	<OPTION VALUE='zoneedit' $selected{'SERVICE'}{'zoneedit'}>zonedit.com
	<OPTION VALUE='easydns' $selected{'SERVICE'}{'easydns'}>easydns.com
	<OPTION VALUE='ods' $selected{'SERVICE'}{'ods'}>ods.org
	</SELECT>
	</TD>
	<TD WIDTH='25%' CLASS='base'>$tr{'behind a proxy'} <INPUT TYPE='checkbox' NAME='PROXY' VALUE='on' $checked{'PROXY'}{'on'}></TD>
	<TD WIDTH='25%' CLASS='base'>$tr{'enable wildcards'} <INPUT TYPE='checkbox' NAME='WILDCARDS' VALUE='on' $checked{'WILDCARDS'}{'on'}></TD>
</TR>
<TR>
	<TD CLASS='base'>$tr{'hostnamec'}</TD>
	<TD><INPUT TYPE='text' NAME='HOSTNAME' VALUE='$cgiparams{'HOSTNAME'}'></TD>
	<TD CLASS='base'>$tr{'domainc'}</TD>
	<TD><INPUT TYPE='text' NAME='DOMAIN' VALUE='$cgiparams{'DOMAIN'}'></TD>
</TR>
<TR>
	<TD CLASS='base'>$tr{'username'}</TD>
	<TD><INPUT TYPE='text' NAME='LOGIN' VALUE='$cgiparams{'LOGIN'}'></TD>
	<TD CLASS='base'>$tr{'password'}</TD>
	<TD><INPUT TYPE='PASSWORD' NAME='PASSWORD' VALUE='$cgiparams{'PASSWORD'}'></TD>
</TR>
</TABLE>
<TABLE WIDTH='100%'>
<TR>
	<TD CLASS='base' WIDTH='50%' ALIGN='CENTER'>$tr{'enabled'}<INPUT TYPE='checkbox' NAME='ENABLED' VALUE='on' $checked{'ENABLED'}{'on'}></TD>
	<TD WIDTH='50%' ALIGN='CENTER'><INPUT TYPE='SUBMIT' NAME='ACTION' VALUE='$tr{'add'}'></TD>
</TR>
</TABLE>
END
;
&closebox();

&openbox($tr{'current hosts'});
print <<END
<table class='centered'>
<tr>
	<th style='width: 15%;'>$tr{'service'}</th>
	<th style='width: 20%;'>$tr{'hostname'}</th>
	<th style='width: 25%;'>$tr{'domain'}</th>
	<th style='width: 10%;'>$tr{'proxy'}</th>
	<th style='width: 10%;'>$tr{'wildcards'}</th>
	<th style='width: 10%;'>$tr{'enabledtitle'}</th>
	<th style='width: 10%;'>$tr{'mark'}</th>
</tr>
END
;

my $id = 0;
open(SETTINGS, "$filename") or die 'Unable to open config file.';
while (<SETTINGS>)
{
	my ($gifproxy,$gifwildcards,$gifenabled);
	$id++;
	chomp($_);
	my @temp = split(/\,/,$_);
	if ($id % 2) { 
		print "<tr class='light'>\n"; 
	}
	else { 
		print "<tr class='dark'>\n"; 
	}
	if ($temp[3] eq 'on') { $gifproxy = 'on.gif'; }
		else { $gifproxy = 'off.gif'; }
	if ($temp[4] eq 'on') { $gifwildcards = 'on.gif'; }
		else { $gifwildcards = 'off.gif'; }
	if ($temp[7] eq 'on') { $gifenabled = 'on.gif'; }
		else { $gifenabled = 'off.gif'; }

print <<END
<td style='text-align: center;'>$temp[0]</td>
<td style='text-align: center;'>$temp[1]</td>
<td style='text-align: center;'>$temp[2]</td>
<td style='text-align: center;'><img src='/ui/img/$gifproxy'></td>
<td style='text-align: center;'><img src='/ui/img/$gifwildcards'></td>
<td style='text-align: center;'><img src='/ui/img/$gifenabled'></td>
<td style='text-align: center;'><input type='checkbox' name='$id'></td>
</tr>
END
	;
}
close(SETTINGS);
print <<END
</table>
<table class='blank'>
<tr>
<td style='width: 50%; text-align:center;'><input type='submit' name='ACTION' value='$tr{'remove'}'></td>
<td style='width: 50%; text-align:center;'><input type='submit' name='ACTION' value='$tr{'edit'}'></td>
</tr>
</table>
<table class='blank'>
<tr>
<td style='text-align: center;'><input type='submit' name='ACTION' value='$tr{'force update'}'></td>
</tr>
</table>
END
;
&closebox();

&alertbox('add','add');

&closebigbox();

&closepage();


