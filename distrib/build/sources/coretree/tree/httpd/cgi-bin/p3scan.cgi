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

my %p3scansettings;

&showhttpheaders();

$p3scansettings{'ACTION'} = '';
$p3scansettings{'VALID'} = '';

&getcgihash(\%p3scansettings);

my $errormessage = '';

if ($p3scansettings{'ACTION'} eq $tr{'save'})
{ 
ERROR:
	if ($errormessage) {
		$p3scansettings{'VALID'} = 'no'; }
	else {
		$p3scansettings{'VALID'} = 'yes'; }

	&writehash("${swroot}/p3scan/settings", \%p3scansettings);

	if ($p3scansettings{'VALID'} eq 'yes')
	{
		system('/usr/bin/smoothwall/writep3scan.pl');
		
		my $success = message('p3scanrestart');
		
		if (not defined $success) {
			$errormessage = $tr{'smoothd failure'}; }
	}
}

if ($p3scansettings{'ACTION'} eq '')
{
	$p3scansettings{'MSN'} = 'on';
	$p3scansettings{'ICQ'} = 'on';
	$p3scansettings{'YAHOO'} = 'on';
}

&readhash("${swroot}/p3scan/settings", \%p3scansettings);

my %checked;

$checked{'MSN'}{'off'} = '';
$checked{'MSN'}{'on'} = '';
$checked{'MSN'}{$p3scansettings{'MSN'}} = 'CHECKED';

$checked{'ICQ'}{'off'} = '';
$checked{'ICQ'}{'on'} = '';
$checked{'ICQ'}{$p3scansettings{'ICQ'}} = 'CHECKED';

$checked{'YAHOO'}{'off'} = '';
$checked{'YAHOO'}{'on'} = '';
$checked{'YAHOO'}{$p3scansettings{'YAHOO'}} = 'CHECKED';

$checked{'IRC'}{'off'} = '';
$checked{'IRC'}{'on'} = '';
$checked{'IRC'}{$p3scansettings{'IRC'}} = 'CHECKED';

$checked{'FILTERING'}{'off'} = '';
$checked{'FILTERING'}{'on'} = '';
$checked{'FILTERING'}{$p3scansettings{'FILTERING'}} = 'CHECKED';

$checked{'ENABLE'}{'off'} = '';
$checked{'ENABLE'}{'on'} = '';
$checked{'ENABLE'}{$p3scansettings{'ENABLE'}} = 'CHECKED';

&openpage('POP3 proxy configuration', 1, '', 'services');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage);

print "<form method='post'>\n";

&openbox('POP3 proxy:');
print <<END
<table width='100%'>
<tr>
	<td width='25%' class='base'>$tr{'enabled'}</td>
	<td width='25%'><input type='checkbox' name='ENABLE' $checked{'ENABLE'}{'on'}></td>
	<td width='25%'>&nbsp;</td>
	<td width='25%'>&nbsp;</td>
</tr>
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

&alertbox('add', 'add');

&closebigbox();

&closepage();
