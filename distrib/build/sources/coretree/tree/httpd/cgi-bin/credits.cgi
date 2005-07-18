#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

require '/var/smoothwall/header.pl';

&showhttpheaders();

&openpage($tr{'credits'}, 1, '', 'control');

&showcontrolsection();

&openbigbox('100%', 'CENTER');

# &alertbox($errormessage);

print <<END
<img src="/ui/assets/3.5/img/credits.$version.gif" 
 alt="SmoothWall Express $version"> &nbsp; <img 
 src="/ui/assets/3.5/img/netstatus.connecting.gif" alt=""
 width="100" height="87">
END
;

&openbox('100%', 'CENTER', '');

print <<END

<div align="center"><h2>SmoothWall Express 2.0</h2>
<p>express $version $revision $webuirevision

<table border="0" cellpadding="3" cellspacing="0" width="90%">

<tr><td width="50%" align="left" valign="top">
<center>
SmoothWall Express $version<br>
Copyright &copy; 2000 - 2003 the 
<a href="http://smoothwall.org/team/"
 target="_breakoutWindow">SmoothWall Team</a>
</center>
<p>
A full team listing can be found <a href="http://smoothwall.org/team/"
 target="_breakoutWindow">on our website</a>.
Portions of this software are copyright &copy; the original
authors, the source code of such portions are 
<a href="http://smoothwall.org/sources.html"
 target="_breakoutWindow">available under the terms of the appropriate 
licenses</a>.
</p>
</td>
<td width="50%" align="left" valign="top">
<p>
For more information about SmoothWall Express, 
please visit our website at
<a href="http://smoothwall.org/"
 target="_breakoutWindow">http://smoothwall.org/</a>
</p>
<p>
For more information about SmoothWall products, please visit 
our website at <a href="http://www.smoothwall.net/"
 target="_breakoutWindow">http://www.smoothwall.net/</a>
</p>
</td>
</table>

<p>
SmoothWall&trade; is a trademark of SmoothWall Limited.
Linux&reg; is a registered trademark of Linus Torvalds.
All other trademarks and copyrights are property of their
respective owners.
Stock photography used courtesy of
<a href="http://istockphoto.com/">iStockphoto.com</a>.
</p>
</div>
END
;

&closebox();

&alertbox('add','add');

&closebigbox();

print "</DIV>\n";

&closepage();

