#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );

$graphcriticalcolour = "#ff0000";
$graphwarningcolour  = "#ff5d00";
$graphnominalcolour  = "#ffa200";
$graphblankcolour    = "#ffffff";

$graphalertcritical = 90;
$graphalertwarning  = 70;

&showhttpheaders();

&openpage($tr{'advanced status information'}, 1, '', 'about your smoothie');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage);

&openbox($tr{'memory'});

@echo = `/usr/bin/free -ot`;
shift(@echo);

# these really should be tr strings

print qq|
<table>
<tr>
	<td>&nbsp;</td>
	<td style='text-align: right; width: 50px'><tt>   $tr{ 'adv total' }</tt></td>
	<td style='text-align: right; width: 50px'><tt>    $tr{ 'adv used' }</tt></td>
	<td style='text-align: right; width: 50px'><tt>    $tr{ 'adv free' }</tt></td>
	<td style='text-align: right;'><tt>&nbsp;</tt></td>
	<td style='text-align: center; width: 150px;'><tt>$tr{ 'adv used%' }</tt></td>
	<td style='text-align: right; width: 50px;' ><tt>  $tr{ 'adv shared' }</tt></td>
	<td style='text-align: right; width: 50px;' ><tt> $tr{ 'adv buffers' }</tt></td>
	<td style='text-align: right; width: 50px;' ><tt>  $tr{ 'adv cached' }</tt></td>
</tr>
|;

foreach $mline (@echo) {
	chomp($mline);

	my ($mdev, $mtotal, $mused, $mfree, $mshared, $mbuffers, $mcached) = split(/\s+/, $mline);

	$mperc = int((($mused/$mtotal)*100));
	if ($mperc > $graphalertcritical) {
		$graphbgcolour = $graphcriticalcolour;
	} elsif ($mperc > $graphalertwarning) {
		$graphbgcolour = $graphwarningcolour;
	} elsif ($mperc > 0) {
		$graphbgcolour = $graphnominalcolour;
	} else {
		$graphbgcolour = $graphblankcolour;
	}
	if ( $mdev eq "Total:" ) {
		print qq|<tr><td colspan="9"><hr></td></tr>|;
	}
	print qq|
<tr>
<td style='text-align: right;'><tt>$mdev</tt></td>
<td style='text-align: right;'><tt>${mtotal}</tt></td>
<td style='text-align: right;'><tt>${mused}K</tt></td>
<td style='text-align: right;'><tt>${mfree}K</tt></td>
<td style='text-align: right;'><tt>&nbsp;</tt></td>
<td style='text-align: right;' width='160px;' nowrap>
	<table class='blank' style='width: 150px; border: 1px #505050 solid;'><tr>|;
	if ($mperc < 1) {
		print "<td style='background-color: $graphbgcolour; width: 1%; text-align: center;'><tt>$mperc%</tt></td>";}
	else {
		print "<td style='background-color: $graphbgcolour; width: $mperc%; text-align: center;'><tt>$mperc%</tt></td>";
	}
	print qq|
<td style='background-color: $graphblankcolour;'>&nbsp;</td></tr></table></td>
|;
	if ( $mshared ne "" ) {
		print qq|
<td style='text-align: right;'><tt>${mshared}K</tt></td>
<td style='text-align: right;'><tt>${mbuffers}K</tt></td>
<td style='text-align: right;'><tt>${mcached}K</tt></td>
|;
	}
	print qq|
</tr>
|;
}

print qq|
</table>|;
&closebox();

&openbox($tr{'disk usage'});

@echo = `df -h`;
shift(@echo);

print qq|
<table>
<tr>
<td style='width: 100px;'><tt>$tr{ 'adv filesystem' }</tt></td>
<td style='width: 75px;'><tt>$tr{ 'adv mount point' }</tt></td>
<td style='width: 40px; text-align: right;'><tt>$tr{ 'adv size'}</tt></td>
<td style='width: 40px; text-align: right;'><tt>$tr{ 'adv used'}</tt></td>
<td style='width: 65px; text-align: right;'><tt>$tr{ 'adv available'}</tt></td>
<td style='width: 5px;' ><tt>&nbsp;</tt></td>
<td style='width: 150px; text-align: center;'><tt>$tr{ 'adv used%' }</tt></td>
</tr>
|;
foreach $mount (@echo) {
   chomp($mount);
   ($dev, $size, $size_used, $size_avail, $size_percentage, $mount_point) = split(/\s+/,$mount);
   if (int($size_percentage) > $graphalertcritical) {
      $graphbgcolour = $graphcriticalcolour;
   } elsif (int($size_percentage) > $graphalertwarning) {
      $graphbgcolour = $graphwarningcolour;
   } elsif (int($size_percentage) > 0) {
      $graphbgcolour = $graphnominalcolour;
   } else {
      $graphbgcolour = $graphblankcolour;
   }
   print qq|
<tr>
	<td><tt>$dev</tt></td>
	<td><tt>$mount_point</tt></td>
	<td style='text-align: right;'><tt>$size</tt></td>
	<td style='text-align: right;'><tt>$size_used</tt></td>
	<td style='text-align: right;'><tt>$size_avail</tt></td>
	<td><tt>&nbsp;</tt></td>
	<td><table class='blank' style='width: 150px; border: 1px #505050 solid;'>
<tr>
|;
   if (int($size_percentage) < 1) {
	print "<td style='background-color: $graphbgcolour; width: 1%; text-align: center;'><tt>$size_percentage</tt></td>";}
   else {
	print "<td style='background-color: $graphbgcolour; width: $size_percentage; text-align: center;'><tt>$size_percentage</tt></td>";
   }
   print qq|
<td style='background-color: $graphblankcolour;'>&nbsp;</td></tr></table></td>
</tr>
|;
}

print qq|
</table>|;
&closebox();

&openbox($tr{'inode usage'});
@echo = `df -i`;
shift(@echo);
print qq|
<table>
<tr>
<td style='width: 100px;'><tt>$tr{ 'adv filesystem' }</tt></td>
<td style='width: 75px;'><tt>$tr{ 'adv mount point' }</tt></td>
<td style='width: 40; text-align: right;'><tt>$tr{ 'adv inodes' }</tt></td>
<td style='width: 40; text-align: right;'><tt>$tr{ 'adv used' }</tt></td>
<td style='width: 65; text-align: right;'><tt>$tr{ 'adv free' }</tt></td>
<td style='width: 5px;'><tt>&nbsp;</tt></td>
<td style='width: 150px; text-align: center;'><tt>$tr{ 'adv used%' }</tt></td>
</tr>
|;
foreach $mount (@echo) {
   chomp($mount);
   ($dev, $size, $size_used, $size_avail, $size_percentage, $mount_point) = split(/\s+/,$mount);
   if (int($size_percentage) > $graphalertcritical) {
      $graphbgcolour = $graphcriticalcolour;
   } elsif (int($size_percentage) > $graphalertwarning) {
      $graphbgcolour = $graphwarningcolour;
   } elsif (int($size_percentage) > 0) {
      $graphbgcolour = $graphnominalcolour;
   } else {
      $graphbgcolour = $graphblankcolour;
   }
   print qq|
<tr>
	<td ><tt>$dev</tt></td>
	<td ><tt>$mount_point</tt></td>
	<td style='text-align: right;'><tt>$size</tt></td>
	<td style='text-align: right;'><tt>$size_used</tt></td>
	<td style='text-align: right;'><tt>$size_avail</tt></td>
	<td><tt>&nbsp;</tt></td>
	<td><table class='blank' style='width: 150px; border: 1px #505050 solid;'>
<tr>
|;
   if (int($size_percentage) < 1) {
	print "<td style='background-color: $graphbgcolour; width: 1%; text-align: center;'><tt>$size_percentage</tt></td>";}
   else {
	print "<td style='background-color: $graphbgcolour; width: $size_percentage; text-align: center;'><tt>$size_percentage</tt></td>";
   }
   print qq|
<td style='background-color: $graphblankcolour;'>&nbsp;</td></tr></table></td>
</tr>
|;
}
print qq|
</table>|;
&closebox();


&openbox($tr{'uptime and users'});
print "<PRE>";
system '/usr/bin/w';
print "</PRE>\n";
&closebox();

&openbox($tr{'interfaces'});
print "<PRE>";
system ('/sbin/ifconfig', '-a');
print "</PRE>\n";
&closebox();

&openbox($tr{'routing'});
print "<PRE>";
system ('/sbin/route', '-n');
print "</PRE>\n";
&closebox();

&openbox($tr{'loaded modules'});
my $modules;
open(PIPE, '-|') || exec('/bin/lsmod');
<PIPE>;
while (<PIPE>) { 
	$modules .= $_; 
}
close (PIPE);

my @modules = split /\n/, $modules;

print <<END
<style type="text/css">
table.modules td {
	font-family:monospace;
}
</style>
<table class="modules">
	<tr>
	<td>Module</td>
	<td>Size</td>
	<td>Used by</td>
	</tr>
END
;

foreach my $module ( @modules ){
	my ( $mod, $size, $used ) = ( $module =~ /([^\s]*)\s+(\d+)\s+(.*)/ );
	$used =~ s/\,/\ /g;
	print "<tr>\n";
	print "<td style='vertical-align: top;'>$mod</td>\n";
	print "<td style='vertical-align: top;'>$size</td>\n";
	print "<td style='vertical-align: top;'>$used</td>\n";
	print "</tr>\n";
}

print "</table>\n";
&closebox();

&openbox($tr{'kernel version'});
print "<PRE>";
system ('/bin/uname', '-a');
print "</PRE>\n";
&closebox();

&alertbox('add','add');

&closebigbox();

&closepage();

