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

print qq|
<a href="javascript:window.close();"><img 
 src="/ui/assets/3.5/img/help.header.png" border="0"
 alt="SmoothWall Express Online Help - click to close window"></a>
|;

&openbigbox('100%', 'LEFT');

&openbox('100%', 'LEFT', '');

# my $htmlfilename = $helpfiles{$needhelpwith};
# if ($htmlfilename eq '') {
# 	print "Invalid section name."; }
# else
# {
	open (FILE, "/home/httpd/html/help/$needhelpwith.html.$language");
	my @content = <FILE>;
	close (FILE);
	print "<TABLE WIDTH='100%' CELLPADDING='8' CELLSPACING='0'><TR><TD>\n";
	print "@content";
	print "</TD></TR></TABLE>\n";
# }
&closebox();

&alertbox('add','add');

&closebigbox();

print qq|
<a href="javascript:window.close();"><img alt="Close this window"
 src="/ui/assets/3.5/img/help.footer.png" border="0"></a>
|;

&closepage('blank');

