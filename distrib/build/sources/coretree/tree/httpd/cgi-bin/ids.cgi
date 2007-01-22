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

my (%snortsettings, %checked);

&showhttpheaders();

$snortsettings{'ENABLE_SNORT'} = 'off';
$snortsettings{'ACTION'} = '';
&getcgihash(\%snortsettings);

$errormessage = '';
if ($snortsettings{'ACTION'} eq $tr{'save'})
{
	&writehash("${swroot}/snort/settings", \%snortsettings);
	if ($snortsettings{'ENABLE_SNORT'} eq 'on')
	{
		&log($tr{'snort is enabled'});
		system ('/bin/touch', "${swroot}/snort/enable");
	}
	else
	{
		&log($tr{'snort is disabled'});
		unlink "${swroot}/snort/enable";
	} 

	my $success = message('snortrestart');
	
	if (not defined $success) {
		$errormessage = $tr{'smoothd failure'}; }
}

&readhash("${swroot}/snort/settings", \%snortsettings);

$checked{'ENABLE_SNORT'}{'off'} = '';
$checked{'ENABLE_SNORT'}{'on'} = '';
$checked{'ENABLE_SNORT'}{$snortsettings{'ENABLE_SNORT'}} = 'CHECKED';

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
	<TD WIDTH='25%'>&nbsp;</TD>
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

print "</FORM>\n";

&alertbox('add', 'add');

&closebigbox();

&closepage();
