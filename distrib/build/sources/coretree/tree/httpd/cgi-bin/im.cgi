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

my %imsettings;
my %netsettings;
my %mainsettings;

&readhash("${swroot}/ethernet/settings", \%netsettings);
&readhash("${swroot}/main/settings", \%mainsettings);

&showhttpheaders();

$imsettings{'ACTION'} = '';
$imsettings{'VALID'} = '';

$imsettings{'ENABLE'} = 'off';
$imsettings{'FILTERING'} = 'off';
$imsettings{'MSN'} = 'off';
$imsettings{'ICQ'} = 'off';
$imsettings{'YAHOO'} = 'off';
$imsettings{'IRC'} = 'off';

&getcgihash(\%imsettings);

my $errormessage = '';

if ($imsettings{'ACTION'} eq $tr{'save'})
{ 
ERROR:
	if ($errormessage) {
		$imsettings{'VALID'} = 'no'; }
	else {
              	$imsettings{'VALID'} = 'yes'; }

	&writehash("${swroot}/im/settings", \%imsettings);

	if ($imsettings{'VALID'} eq 'yes')
	{
		system('/usr/bin/smoothwall/writeim.pl');
		
		my $success = message('imrestart');
		
		if (not defined $success) {
			$errormessage = $tr{'smoothd failure'}; }
	}
}

if ($imsettings{'ACTION'} eq '')
{
	$imsettings{'MSN'} = 'on';
	$imsettings{'ICQ'} = 'on';
	$imsettings{'YAHOO'} = 'on';
}

&readhash("${swroot}/im/settings", \%imsettings);

my %checked;

$checked{'MSN'}{'off'} = '';
$checked{'MSN'}{'on'} = '';
$checked{'MSN'}{$imsettings{'MSN'}} = 'CHECKED';

$checked{'ICQ'}{'off'} = '';
$checked{'ICQ'}{'on'} = '';
$checked{'ICQ'}{$imsettings{'ICQ'}} = 'CHECKED';

$checked{'YAHOO'}{'off'} = '';
$checked{'YAHOO'}{'on'} = '';
$checked{'YAHOO'}{$imsettings{'YAHOO'}} = 'CHECKED';

$checked{'IRC'}{'off'} = '';
$checked{'IRC'}{'on'} = '';
$checked{'IRC'}{$imsettings{'IRC'}} = 'CHECKED';

$checked{'FILTERING'}{'off'} = '';
$checked{'FILTERING'}{'on'} = '';
$checked{'FILTERING'}{$imsettings{'FILTERING'}} = 'CHECKED';

$checked{'ENABLE'}{'off'} = '';
$checked{'ENABLE'}{'on'} = '';
$checked{'ENABLE'}{$imsettings{'ENABLE'}} = 'CHECKED';

&openpage('IM proxy configuration', 1, '', 'services');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage);

print "<FORM METHOD='POST'>\n";

&openbox('IM proxy:');
print <<END
<table width='100%'>
<tr>
	<td width='25%' class='base'>$tr{'enabled'}</TD>
	<td width='25%'><input type='checkbox' name='ENABLE' $checked{'ENABLE'}{'on'}></TD>
	<td width='25%' class='base'>Swear-word filtering:</TD>
	<td width='25%'><input type='checkbox' name='FILTERING' $checked{'FILTERING'}{'on'}></TD>
</tr>
<tr>
	<td class='base'>MSN:</td>
	<td><input type='checkbox' name='MSN' $checked{'MSN'}{'on'}></td>
	<td class='base'>ICQ and AIM:</td>
	<td><input type='checkbox' name='ICQ' $checked{'ICQ'}{'on'}></td>
</tr>
<tr>
	<td class='base'>Yahoo:</td>
	<td><input type='checkbox' name='YAHOO' $checked{'YAHOO'}{'on'}></td>
	<td class='base'>IRC:</td>
	<td><input type='checkbox' name='IRC' $checked{'IRC'}{'on'}></td>
</table>
END
;
&closebox();

print <<END
<DIV ALIGN='CENTER'>
<TABLE WIDTH='60%'>
<TR>
        <TD WIDTH='100%' ALIGN='CENTER'><INPUT TYPE='submit' NAME='ACTION' VALUE='$tr{'save'}'></TD>
</TR>
</TABLE>
</DIV>
END
;

print "</FORM>\n";

&alertbox('add','add');

&closebigbox();

&closepage();
