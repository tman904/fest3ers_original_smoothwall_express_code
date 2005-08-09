#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );

my (%modemsettings,$errormessage);

&showhttpheaders();

$modemsettings{'ACTION'} = '';
$modemsettings{'VALID'} = '';

&getcgihash(\%modemsettings);

$errormessage = '';
if ($modemsettings{'ACTION'} eq $tr{'save'})
{ 
        if (!($modemsettings{'TIMEOUT'} =~ /^\d+$/))
        {
      	 	$errormessage = $tr{'timeout must be a number'};
	 	goto ERROR;
        }
ERROR:   
        if ($errormessage) {
                $modemsettings{'VALID'} = 'no'; }
        else {
                $modemsettings{'VALID'} = 'yes'; }

	&writehash("${swroot}/modem/settings", \%modemsettings);
}

if ($modemsettings{'ACTION'} eq $tr{'restore defaults'})
{
	system('/bin/cp', "${swroot}/modem/defaults", "${swroot}/modem/settings", '-f');
}

&readhash("${swroot}/modem/settings", \%modemsettings);

&openpage($tr{'modem configuration'}, 1, '', 'maintenance');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage);

print "<FORM METHOD='POST'>\n";

&openbox($tr{'modem configurationc'});
print <<END
<TABLE WIDTH='100%'>
<TR>
	<TD WIDTH='25%' CLASS='base'>$tr{'init string'}&nbsp;<IMG SRC='/ui/assets/3.5/img/blob.gif'></TD>
	<TD WIDTH='25%'><INPUT TYPE='text' NAME='INIT' VALUE='$modemsettings{'INIT'}'></TD>
	<TD WIDTH='25%' CLASS='base'>$tr{'hangup string'}&nbsp;<IMG SRC='/ui/assets/3.5/img/blob.gif'></TD>
	<TD WIDTH='25%'><INPUT TYPE='text' NAME='HANGUP' VALUE='$modemsettings{'HANGUP'}'></TD>
</TR>
<TR>
	<TD CLASS='base'>$tr{'speaker on'}&nbsp;<IMG SRC='/ui/assets/3.5/img/blob.gif'></TD>
	<TD><INPUT TYPE='text' NAME='SPEAKER_ON' VALUE='$modemsettings{'SPEAKER_ON'}'></TD>
	<TD CLASS='base'>$tr{'speaker off'}&nbsp;<IMG SRC='/ui/assets/3.5/img/blob.gif'></TD>
	<TD><INPUT TYPE='text' NAME='SPEAKER_OFF' VALUE='$modemsettings{'SPEAKER_OFF'}'></TD>
</TR>
<TR>
	<TD CLASS='base'>$tr{'tone dial'}&nbsp;<IMG SRC='/ui/assets/3.5/img/blob.gif'></TD>
	<TD><INPUT TYPE='text' NAME='TONE_DIAL' VALUE='$modemsettings{'TONE_DIAL'}'></TD>
	<TD CLASS='base'>$tr{'pulse dial'}&nbsp;<IMG SRC='/ui/assets/3.5/img/blob.gif'></TD>
	<TD><INPUT TYPE='text' NAME='PULSE_DIAL' VALUE='$modemsettings{'PULSE_DIAL'}'></TD>
</TR>
<TR>
	<TD CLASS='base'>$tr{'connect timeout'}</TD>
	<TD><INPUT TYPE='text' NAME='TIMEOUT' VALUE='$modemsettings{'TIMEOUT'}'></TD>
	<TD CLASS='base'>&nbsp;</TD>
	<TD>&nbsp;</TD>
</TR>

</TABLE>
<BR>
<IMG SRC='/ui/assets/3.5/img/blob.gif' VALIGN='top'>&nbsp;
<FONT CLASS='base'>$tr{'these fields may be blank'}</FONT>
END
;
&closebox();

print <<END
<DIV ALIGN='CENTER'>
<TABLE WIDTH='80%'>
<TR>
	<TD ALIGN='CENTER'><INPUT TYPE='submit' NAME='ACTION' VALUE='$tr{'restore defaults'}'></TD>
	<TD ALIGN='CENTER'><INPUT TYPE='submit' NAME='ACTION' VALUE='$tr{'save'}'></TD>
</TR>
</TABLE>
</DIV>
END
;

print "</FORM>\n";

&alertbox('add','add');

&closebigbox();

&closepage();
