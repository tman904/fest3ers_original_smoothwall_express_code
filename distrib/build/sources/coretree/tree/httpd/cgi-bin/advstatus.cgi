#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

require '/var/smoothwall/header.pl';

&showhttpheaders();

&openpage($tr{'advanced status information'}, 1, '', 'about your smoothie');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage);

&openbox($tr{'memory'});

@echo = `/usr/bin/free -ot`;
shift(@echo);

# these really should be tr strings

print qq|
<table border='0' cellspacing='0' cellpadding='2'>
<tr><td>&nbsp;</td>
<td align="right" width="50" ><tt>   $tr{ 'adv total' }</tt></td>
<td align="right" width="50" ><tt>    $tr{ 'adv used' }</tt></td>
<td align="right" width="50" ><tt>    $tr{ 'adv free' }</tt></td>
<td align="right" ><tt>&nbsp;</tt></td>
<td align="center" width="150"><tt>$tr{ 'adv used%' }</tt></td>
<td align="right" width="50" ><tt>  $tr{ 'adv shared' }</tt></td>
<td align="right" width="50" ><tt> $tr{ 'adv buffers' }</tt></td>
<td align="right" width="50" ><tt>  $tr{ 'adv cached' }</tt></td>
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
<td align="right"><tt>$mdev</tt></td>
<td align="right"><tt>${mtotal}</tt></td>
<td align="right"><tt>${mused}K</tt></td>
<td align="right"><tt>${mfree}K</tt></td>
<td align="right"><tt>&nbsp;</tt></td>
<td align="right" width='150' nowrap><table width='100%' border='0' cellspacing='0' cellpadding='0'><tr>|;
	if ($mperc < 1) {
		print "<td bgcolor='$graphbgcolour' width='1%' align='center'><tt>$mperc%</tt></td>";}
	else {
		print "<td bgcolor='$graphbgcolour' width='$mperc%' align='center'><tt>$mperc%</tt></td>";
	}
	print qq|
<td bgcolor='$graphblankcolour'>&nbsp;</td></tr></table></td>
|;
	if ( $mshared ne "" ) {
		print qq|
<td align="right"><tt>${mshared}K</tt></td>
<td align="right"><tt>${mbuffers}K</tt></td>
<td align="right"><tt>${mcached}K</tt></td>
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
<table border='0' cellspacing='0' cellpadding='2'>
<tr>
<td width="100"><tt>$tr{ 'adv filesystem' }</tt></td>
<td width="75" ><tt>$tr{ 'adv mount point' }</tt></td>
<td width="40" align="right"><tt>$tr{ 'adv size'}</tt></td>
<td width="40" align="right"><tt>$tr{ 'adv used'}</tt></td>
<td width="65" align="right"><tt>$tr{ 'adv available'}</tt></td>
<td width="5" ><tt>&nbsp;</tt></td>
<td width="150" align="center"><tt>$tr{ 'adv used%' }</tt></td>
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
<td align='right'><tt>$size</tt></td>
<td align='right'><tt>$size_used</tt></td>
<td align='right'><tt>$size_avail</tt></td>
<td><tt>&nbsp;</tt></td>
<td><table width='100%' border='0' cellspacing='0' cellpadding='0'>
<tr>
|;
   if (int($size_percentage) < 1) {
      print "<td bgcolor='$graphbgcolour' width='1%' align='center'><tt>$size_percentage</tt></td>";}
   else {
      print "<td bgcolor='$graphbgcolour' width='$size_percentage' align='center'><tt>$size_percentage</tt></td>";
   }
   print qq|
<td bgcolor='$graphblankcolour'>&nbsp;</td>
</tr></table></td>
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
<table border='0' cellspacing='0' cellpadding='2'>
<tr>
<td width="100"><tt>$tr{ 'adv filesystem' }</tt></td>
<td width="75" ><tt>$tr{ 'adv mount point' }</tt></td>
<td width="40" align="right" ><tt>$tr{ 'adv inodes' }</tt></td>
<td width="40" align="right" ><tt>$tr{ 'adv used' }</tt></td>
<td width="65" align="right" ><tt>$tr{ 'adv free' }</tt></td>
<td width="5" ><tt>&nbsp;</tt></td>
<td width="150" align="center"><tt>$tr{ 'adv used%' }</tt></td>
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
<td align='right' ><tt>$size</tt></td>
<td align='right' ><tt>$size_used</tt></td>
<td align='right' ><tt>$size_avail</tt></td>
<td><tt>&nbsp;</tt></td>
<td><table width='100%' border='0' cellspacing='0' cellpadding='0'>
<tr>
|;
   if (int($size_percentage) < 1) {
      print "<td bgcolor='$graphbgcolour' width='1%' align='center'><tt>$size_percentage</tt></td>";}
   else {
      print "<td bgcolor='$graphbgcolour' width='$size_percentage' align='center'><tt>$size_percentage</tt></td>";
   }
   print qq|
<td bgcolor='$graphblankcolour'>&nbsp;</td>
</tr></table></td>
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
print "<PRE>";
system '/sbin/lsmod';
print "</PRE>\n";
&closebox();

&openbox($tr{'kernel version'});
print "<PRE>";
system ('/bin/uname', '-a');
print "</PRE>\n";
&closebox();

&alertbox('add','add');

&closebigbox();

&closepage();

