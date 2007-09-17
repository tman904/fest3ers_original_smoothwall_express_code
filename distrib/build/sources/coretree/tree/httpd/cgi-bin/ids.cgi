#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use smoothd qw( message );
use smoothtype qw( :standard );

use Cwd;

my (%snortsettings, %checked);

&showhttpheaders();

$snortsettings{'ENABLE_SNORT'} = 'off';
$snortsettings{'ACTION'} = '';
&getcgihash(\%snortsettings);

$errormessage = '';
if ($snortsettings{'ACTION'} eq $tr{'save and update rules'})
{
	if ($snortsettings{'OINK'} !~ /^([\da-f]){40}$/i)
	{
		$errormessage = $tr{'oink code must be 40 hex digits'};
		goto EXIT;
	}

EXIT:
	my $curdir = getcwd;
	my $url = 'http://www.snort.org/pub-bin/oinkmaster.cgi/' . $snortsettings{'OINK'} . '/snortrules-snapshot-CURRENT.tar.gz';
	chdir "${swroot}/snort/";

	if (open(FD, '-|') || exec('/usr/bin/oinkmaster.pl', '-v', '-C',
		'/usr/lib/smoothwall/oinkmaster.conf', '-o', 'rules', '-u', $url))
	{
		$errormessage = $tr{'rules not available'};
		while(<FD>)
		{
			$errormessage = '';
			print STDERR $_;
		}
		close(FD);
		if ($?) {
			$errormessage = $tr{'unable to fetch rules'}; } 
		else
		{
			open (FILE, ">${swroot}/snort/ruleage");
			close (FILE);
		}
	}
	else {
		$errormessage = $tr{'unable to fetch rules'}; }

	chdir $curdir;
}
if ($snortsettings{'ACTION'} eq $tr{'save'} || $snortsettings{'ACTION'} eq $tr{'save and update rules'})
{
	&writehash("${swroot}/snort/settings", \%snortsettings);

	if ($snortsettings{'ENABLE_SNORT'} eq 'on') {
		&log($tr{'snort is enabled'}); }
	else {
		&log($tr{'snort is disabled'}); }

	my $success = message('snortrestart');

	if (not defined $success) {
		$errormessage = $tr{'smoothd failure'}; }
}

&readhash("${swroot}/snort/settings", \%snortsettings);

$checked{'ENABLE_SNORT'}{'off'} = '';
$checked{'ENABLE_SNORT'}{'on'} = '';
$checked{'ENABLE_SNORT'}{$snortsettings{'ENABLE_SNORT'}} = 'CHECKED';

my $ruleage = 'N/A';
if (-e "${swroot}/snort/ruleage")
{
	my $days = int(-M "${swroot}/snort/ruleage");
	$ruleage = "$days $tr{'days'}";
}

&openpage($tr{'intrusion detection system'}, 1, '', 'services');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage);

print "<FORM METHOD='POST'>\n";

&openbox($tr{'intrusion detection system2'});
print <<END
<TABLE WIDTH='100%'>
<TR>
	<TD WIDTH='25%' CLASS='base'>Snort:</TD>
	<TD WIDTH='25%'><INPUT TYPE='checkbox' NAME='ENABLE_SNORT' $checked{'ENABLE_SNORT'}{'on'}></TD>
	<TD WIDTH='25%'>&nbsp;</TD>
	<TD WIDTH='35%'>&nbsp;</TD>
</TR>
</TABLE>
END
;
&closebox();

print <<END
<DIV ALIGN='CENTER'>
<TABLE WIDTH='60%'>
<TR>
	<TD ALIGN='CENTER'><INPUT TYPE='submit' NAME='ACTION' VALUE='$tr{'save'}'></TD> 
</TR>
</TABLE>
</DIV>
END
;


&openbox($tr{'rule retreval'});
print <<END
<TABLE WIDTH='100%'>
<TR>
	<TD WIDTH='25%'>$tr{'oink code'}</TD>
	<TD WIDTH='75%'><INPUT TYPE='text' NAME='OINK' SIZE='42' MAXLENGTH='40' VALUE='$snortsettings{OINK}' id='OINK' @{[jsvalidregex('OINK','^([0-9a-fA-F]){40}$')]}></TD>
</TR>
<TR>
	<TD>$tr{'rule age'}</TD><TD>$ruleage</TD>
</TR>
</TABLE>
END
;

&closebox();

print <<END
<DIV ALIGN='CENTER'>
<TABLE WIDTH='60%'>
<TR>
	<TD ALIGN='CENTER'><INPUT TYPE='submit' NAME='ACTION' VALUE='$tr{'save and update rules'}'></TD> 
</TR>
</TABLE>
</DIV>
END
;

print "</FORM>\n";

&alertbox('add', 'add');

&closebigbox();

&closepage();

