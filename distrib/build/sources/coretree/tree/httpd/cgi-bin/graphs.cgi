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
use POSIX qw(strftime);

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

&openpage($tr{'network traffic graphs'}."$title", 1, ' <META HTTP-EQUIV="Refresh" CONTENT="300"> <META HTTP-EQUIV="Cache-Control" content="no-cache"> <META HTTP-EQUIV="Pragma" CONTENT="no-cache"> ', 'about your smoothie');
&openbigbox('100%', 'LEFT');
&alertbox($errormessage);

my @message;

my @details;
	
my %stats;

&readhash('/var/log/trafficstats', \%stats);
	
my $timestamp = 'N/A';
if ($stats{'last_update'}) {
	$timestamp = strftime "%a %b %e %H:%M:%S %Y", localtime($stats{'last_update'}); }
   
foreach my $iface ('eth0', 'eth1', 'eth2', 'ppp0', 'ippp0')
{
	my %ifacestats;
		
	foreach my $stat (keys %stats)
	{
		if ($stat =~ /_${iface}$/)
		{
			my $field = "$`";
			my $value = $stats{$stat};
			my $units;
			if ($field =~ /^cur/)
			{
				$units = "bit/s";
				if ($value > 1000)
				{
					$value /= 1000;
					$units = 'Kbits/s';
				}
				if ($value > 1000)
				{
					$value /= 1000;
					$units = 'Mbits/s';
				}
			}
			else
			{
				$units = 'KB';
				if ($value > 1024)
				{
					$value /= 1024;
					$units = 'MB';
				}
				if ($value > 1024)
				{
					$value /= 1024;
					$units = 'GB';
				}
			}
			$value = sprintf("%0.1f", $value);
			$ifacestats{$field} = "$value $units";
		}
	}
	
	if ($ifacestats{'this_month_inc_total'} > 0)
	{
		my $printableiface;
		if ($iface eq $netsettings{'GREEN_DEV'}) {
			$printableiface = 'Green'; }
		elsif ($iface eq $netsettings{'ORANGE_DEV'}) {
			$printableiface = 'Orange'; }
		elsif ($iface eq $netsettings{'RED_DEV'}) {
			$printableiface = 'Red'; }
		elsif ($iface eq 'ppp0') {
			$printableiface = 'Modem'; }
		elsif ($iface eq 'ippp0') {
			$printableiface = 'ISDN'; }
			
		push @details, { Interface => $printableiface, 
			%ifacestats
		};
	}
}

close(PIPE);

&openbox("Traffic statistics - $timestamp");

print <<END
<TABLE WIDTH='100%'>
<TR>
<TD WIDTH='15%'>$tr{'traffic stats interface'}</TD>
<TD WIDTH='15%'>$tr{'traffic stats period'}</TD>
<TD WIDTH='15%'>$tr{'traffic stats direction'}</TD>
<TD WIDTH='15%'>$tr{'traffic stats current rate'}</TD>
<TD WIDTH='10%'>$tr{'traffic stats hour'}</TD>
<TD WIDTH='10%'>$tr{'traffic stats day'}</TD>
<TD WIDTH='10%'>$tr{'traffic stats week'}</TD>
<TD WIDTH='10%'>$tr{'traffic stats month'}</TD>
</TR>
END
;

foreach my $row ( sort { $a->{'Interface'} cmp $b->{'Interface'} } @details )
{
	print <<END
<TR>
<TD>$row->{ 'Interface' }</TD>
<TD>$tr{'traffic stats current'}</TD>
<TD>$tr{'traffic stats in'}</TD>
<TD>$row->{ 'cur_inc_rate' }</TD>
<TD>$row->{ 'this_hour_inc_total' }</TD>
<TD>$row->{ 'this_day_inc_total' }</TD>
<TD>$row->{ 'this_week_inc_total' }</TD>
<TD>$row->{ 'this_month_inc_total' }</TD>
</TR>
<TR>
<TD>&nbsp;</TD>
<TD>&nbsp;</TD>
<TD>$tr{'traffic stats out'}</TD>
<TD>$row->{ 'cur_out_rate' }</TD>
<TD>$row->{ 'this_hour_out_total' }</TD>
<TD>$row->{ 'this_day_out_total' }</TD>
<TD>$row->{ 'this_week_out_total' }</TD>
<TD>$row->{ 'this_month_out_total' }</TD>
</TR>
<TR>
<TD>&nbsp;</TD>
<TD>$tr{'traffic stats previous'}</TD>
<TD>$tr{'traffic stats in'}</TD>
<TD>&nbsp;</TD>
<TD>$row->{ 'prev_hour_inc_total' }</TD>
<TD>$row->{ 'prev_day_inc_total' }</TD>
<TD>$row->{ 'prev_week_inc_total' }</TD>
<TD>$row->{ 'prev_month_inc_total' }</TD>
</TR>
<TR>
<TD>&nbsp;</TD>
<TD>&nbsp;</TD>
<TD>$tr{'traffic stats out'}</TD>
<TD>&nbsp;</TD>
<TD>$row->{ 'prev_hour_out_total' }</TD>
<TD>$row->{ 'prev_day_out_total' }</TD>
<TD>$row->{ 'prev_week_out_total' }</TD>
<TD>$row->{ 'prev_month_out_total' }</TD>
</TR>
END
	;
}

print "</TABLE>";

&closebox();

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
