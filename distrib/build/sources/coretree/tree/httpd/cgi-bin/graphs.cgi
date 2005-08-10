#!/usr/bin/perl
#
# coded by Martin Pot 2003
# http://martybugs.net/smoothwall/rrdtool.cgi
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team
# rrdtool.cgi

use lib "/usr/lib/smoothwall";
use header qw( :standard );

my %cgiparams;
my @graphs;

my $title = "";

my %netsettings;

&readhash("${swroot}/ethernet/settings", \%netsettings);

# get url parameters
my @values = split(/&/, $ENV{'QUERY_STRING'});
foreach my $i (@values)
{
        ($varname, $mydata) = split(/=/, $i);
        if ($varname eq 'i')
        {
                $name = $mydata;
        }
}
# check if viewing one interface only 
if ($name ne "") { $title = " for $name interface"; }

&showhttpheaders();

my $rrddir = "/httpd/html/rrdtool";

# check if viewing summary graphs
if ($name eq "")
{
	push (@graphs, ('green-day'));
	if ($netsettings{'ORANGE_DEV'}) {
		push (@graphs, ('orange-day')); }
	push (@graphs, ('red-day'));
}
else
{
	push (@graphs, ("$name-day"));
	push (@graphs, ("$name-week"));
	push (@graphs, ("$name-month"));
	push (@graphs, ("$name-year"));
}

&openpage($tr{'network traffic graphs'}."$title", 1, ' <META HTTP-EQUIV="Refresh" CONTENT="300"> <META HTTP-EQUIV="Cache-Control" content="no-cache"> <META HTTP-EQUIV="Pragma" CONTENT="no-cache"> ', 'about your smoothie');
&openbigbox('100%', 'LEFT');
&alertbox($errormessage);

&openbox($tr{'network traffic graphsc'});

my $lastdata = scalar localtime(`rrdtool last /var/lib/rrd/green.rrd`);
my $lastupdate = scalar localtime((stat("/var/lib/rrd/green.rrd"))[9]);
print "last updated $lastupdate<br>with data to $lastdata";

&closebox();

&openbox('');
if ($name eq "") { print "<b>Summary network traffic graphs:</b><br><br>\n"; }
else { print "<b>Network traffic graphs for $name interface:</b><br><br>\n"; }

print qq|
<div align="center">
|;

my $found = 0;
my $graphname;

if ( $name ne "" ) {
	print qq|&laquo; <a href="?">return to graph summary</a><br><br>|;
}

foreach $graphname (@graphs)
{
	if (-e "$rrddir/$graphname.png")
	{
		# check if displaying summary graphs
		my $graphinterface = (substr($graphname,0,index($graphname,"-")));
		if ($name eq "") 
		{ 
			print "<a href='".$ENV{'SCRIPT_NAME'}."?i=".(substr($graphname,0,index($graphname,"-")))."'";
			print " title='click for detailed graphs for the ".$name." interface'>";
			print "<img";
		}
		else
		{
			print "<img alt='$graphname'";
		}
		print " border='0' src='/rrdtool/$graphname.png'>";
		if ($name eq "") { 
			print qq|</a><br><a href="?i=$graphinterface|;
			print qq|">click for detailed graphs for the $graphinterface interface</a> &raquo;|;
		}
		print "<br><br>\n";
		$found = 1;
	}
}

if (!$found) {
	print "<B><CLASS='boldbase'>$tr{'no graphs available'}</CLASS></B>"; }

print "<br>\n";

print qq|
</div>
|;

&closebox();
&alertbox('add','add');
&closebigbox();
&closepage();
