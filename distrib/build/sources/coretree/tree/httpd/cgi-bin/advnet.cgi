#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) SmoothWall Ltd, 2002-2003

require '/var/smoothwall/header.pl';

my (%advnetsettings,%checked);

&showhttpheaders();

$advnetsettings{'ENABLE_NOPING'} = 'off';
$advnetsettings{'ENABLE_COOKIES'} = 'off';
$advnetsettings{'ENABLE_NOIGMP'} = 'off';
$advnetsettings{'ENABLE_NOMULTICAST'} = 'off';
$advnetsettings{'ENABLE_UPNP'} = 'off';
$advnetsettings{'ACTION'} = '';
&getcgihash(\%advnetsettings);

$errormessage = '';
if ($advnetsettings{'ACTION'} eq $tr{'save'})
{
	&writehash("${swroot}/advnet/settings", \%advnetsettings);
        if ($advnetsettings{'ENABLE_NOPING'} eq 'on') {
                system ('/bin/touch', "${swroot}/advnet/noping"); }
        else {
                unlink "${swroot}/advnet/noping"; } 
        if ($advnetsettings{'ENABLE_COOKIES'} eq 'on') {
                system ('/bin/touch', "${swroot}/advnet/cookies"); }
        else {
                unlink "${swroot}/advnet/cookies"; } 
        if ($advnetsettings{'ENABLE_NOIGMP'} eq 'on') {
                system ('/bin/touch', "${swroot}/advnet/noigmp"); }
        else {
                unlink "${swroot}/advnet/noigmp"; } 
        if ($advnetsettings{'ENABLE_NOMULTICAST'} eq 'on') {
                system ('/bin/touch', "${swroot}/advnet/nomulticast"); }
        else {
                unlink "${swroot}/advnet/nomulticast"; } 
        if ($advnetsettings{'ENABLE_UPNP'} eq 'on') {
                system ('/bin/touch', "${swroot}/advnet/upnp"); }
        else {
                unlink "${swroot}/advnet/upnp"; } 

	&log($tr{'restarting advanced networking features'});
	system '/usr/bin/setuids/setadvnet';
	system '/usr/bin/setuids/restartupnp';
}

&readhash("${swroot}/advnet/settings", \%advnetsettings);

$checked{'ENABLE_NOPING'}{'off'} = '';
$checked{'ENABLE_NOPING'}{'on'} = '';
$checked{'ENABLE_NOPING'}{$advnetsettings{'ENABLE_NOPING'}} = 'CHECKED';

$checked{'ENABLE_COOKIES'}{'off'} = '';
$checked{'ENABLE_COOKIES'}{'on'} = '';
$checked{'ENABLE_COOKIES'}{$advnetsettings{'ENABLE_COOKIES'}} = 'CHECKED';

$checked{'ENABLE_NOIGMP'}{'off'} = '';
$checked{'ENABLE_NOIGMP'}{'on'} = '';
$checked{'ENABLE_NOIGMP'}{$advnetsettings{'ENABLE_NOIGMP'}} = 'CHECKED';

$checked{'ENABLE_NOMULTICAST'}{'off'} = '';
$checked{'ENABLE_NOMULTICAST'}{'on'} = '';
$checked{'ENABLE_NOMULTICAST'}{$advnetsettings{'ENABLE_NOMULTICAST'}} = 'CHECKED';

$checked{'ENABLE_UPNP'}{'off'} = '';
$checked{'ENABLE_UPNP'}{'on'} = '';
$checked{'ENABLE_UPNP'}{$advnetsettings{'ENABLE_UPNP'}} = 'CHECKED';

&openpage($tr{'advanced networking features'}, 1, '', 'networking');

&shownetworkingsection();

&openbigbox('100%', 'LEFT');

&alertbox($errormessage);

print "<FORM METHOD='POST'>\n";

&openbox('100%', 'LEFT', $tr{'advanced networking featuresc'});
print <<END
<TABLE WIDTH='100%'>
<TR>
	<TD WIDTH='25%' CLASS='base'>$tr{'block icmp ping'}</TD>
	<TD WIDTH='25%'><INPUT TYPE='checkbox' NAME='ENABLE_NOPING' $checked{'ENABLE_NOPING'}{'on'}></TD>
	<TD WIDTH='25%' CLASS='base'>$tr{'enable syn cookies'}</TD>
	<TD WIDTH='25%'><INPUT TYPE='checkbox' NAME='ENABLE_COOKIES' $checked{'ENABLE_COOKIES'}{'on'}></TD>
</TR>
<TR>
	<TD WIDTH='25%' CLASS='base'>$tr{'block and ignore igmp packets'}</TD>
	<TD WIDTH='25%'><INPUT TYPE='checkbox' NAME='ENABLE_NOIGMP' $checked{'ENABLE_NOIGMP'}{'on'}></TD>
	<TD WIDTH='25%' CLASS='base'>$tr{'block and ignore multicast traffic'}</TD>
	<TD WIDTH='25%'><INPUT TYPE='checkbox' NAME='ENABLE_NOMULTICAST' $checked{'ENABLE_NOMULTICAST'}{'on'}></TD>
</TR>
<TR>
	<TD WIDTH='25%' CLASS='base'>$tr{'upnp support'}</TD>
	<TD WIDTH='25%'><INPUT TYPE='checkbox' NAME='ENABLE_UPNP' $checked{'ENABLE_UPNP'}{'on'}></TD>
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

&closepage($errormessage);
