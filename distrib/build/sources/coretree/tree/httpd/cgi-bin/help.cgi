#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

require '/var/smoothwall/header.pl';

my $needhelpwith = $ENV{'QUERY_STRING'};

&showhttpheaders();

&openpage($tr{'help'}, 1, '', 'help');

&openbigbox();

&openbox('');

open (FILE, "/httpd/html/help/$needhelpwith.html.$language");
my @content = <FILE>;
close (FILE);
print <<END
<table>
<tr>
	<td class='helpheader'>
		<a href="javascript:window.close();"><img src="/ui/img/help.footer.png" alt="SmoothWall Express Online Help - click to close window"></a>
	</td>
</tr>
<tr>
	<td>
END
;

print "@content";
print <<END
	</td>
</tr>
<tr>
	<td class='helpfooter'>
		<a href="javascript:window.close();"><img alt="Close this window" src="/ui/img/help.footer.png" border="0"></a>
	</td>
</tr>
</table>
END
;

&closebox();

&closebigbox();

&closepage('blank');

