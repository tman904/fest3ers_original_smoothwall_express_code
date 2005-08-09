#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );

&showhttpheaders();

&openpage($tr{'msecure shell'}, 1, '', 'tools');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage);

&openbox($tr{'secure shellc'}, '');
print <<END
<DIV ALIGN='CENTER'>
<!-- 
<APPLET ARCHIVE='/mindtermfull.jar' CODE='mindbright.application.MindTerm.class'
WIDTH='580' HEIGHT='400'>
<PARAM NAME='te' VALUE='xterm-color'>
<PARAM NAME='fg' VALUE='white'>
<PARAM NAME='bg' VALUE='black'>
<PARAM NAME='port' VALUE='222'>
<PARAM NAME='username' VALUE='setup'>
<PARAM NAME='autoprops' VALUE='both'>
<PARAM NAME='quiet' VALUE='false'>
</APPLET>
 -->


<applet codebase="/"
 archive="jta20_o.jar"
 code="de.mud.jta.Applet" 
 width="590" height="360">
<param name="config" value="applet.conf">
You require <a href="http://java.sun.com/">Java</a> to use the shell applet
</applet>



</DIV>
END
;

&closebox();

print "</FORM>\n";

&alertbox('add','add');

&closebigbox();

&closepage();
