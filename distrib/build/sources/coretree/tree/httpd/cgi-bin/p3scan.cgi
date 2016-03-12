#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use smoothd qw( message );
use App::Control;
use strict;
use warnings;

my (%p3scansettings, %clamavsettings, %checked);

my $refresh = '';
my $errormessage = '';
my $success = '';

&showhttpheaders();

$p3scansettings{'ACTION'} = '';

$p3scansettings{"ENABLE"} = '';

&readhash("${swroot}/clamav/settings", \%clamavsettings);

&getcgihash(\%p3scansettings);

if ($p3scansettings{'ACTION'} eq $tr{'save'}) { 

	$clamavsettings{'ENABLE_ZAP'} = $p3scansettings{'ENABLE'};

	&writehash("${swroot}/clamav/settings", \%clamavsettings);
	&writehash("${swroot}/p3scan/settings", \%p3scansettings);
	system('/usr/bin/smoothwall/writep3scan.pl');

	if ($p3scansettings{"ENABLE"} eq 'on') {
		$success = message('p3scanrestart');
		$errormessage .= $success."<br />";
		$errormessage .= $tr{'smoothd failure'}."<br />" unless ($success);

		# Check if ClamAV is already running
		my $avstatus = isclamrunning("clamd");
		if ($avstatus eq 'running') {
			# ClamAV is running - Don't restart it - It takes ages.
			$errormessage .= "ClamAV already running!<br />";
		}
		else {
			$success = message('clamavrestart');
			$success = "TIMEOUT: ClamAV Still Restarting" if ($success =~ /TIMEOUT/i);
			$errormessage .= $success."<br />";
			$errormessage .= $tr{'smoothd failure'}."<br />" unless ($success);
		}
		$refresh = "<meta http-equiv='refresh' content='2; URL=p3scan.cgi'>";
	}
	else {
		$success = message('p3scanstop');
		$errormessage .= $success."<br />";
		$errormessage .= $tr{'smoothd failure'}."<br />" unless ($success);

		# Check if anything else has ClamAV turned on, if not - turn it off.
		open (CLAM, "${swroot}/clamav/settings") || die "Unable to open $!"; 
		my @clamsettings = (<CLAM>); 
		close (CLAM);
		my $clamused = grep { /\=on$/ } @clamsettings;

		if ($clamused == 0) {
			$success = message('clamavstop');
			$errormessage .= $success."<br />";
			$errormessage .= $tr{'smoothd failure'}."<br />" unless ($success);
		}
		else {
			$errormessage .= "ClamAV is being used by another Application - Not Terminated<br />";
		}
		$refresh = "<meta http-equiv='refresh' content='2; URL=p3scan.cgi'>";
	}
}

&readhash("${swroot}/p3scan/settings", \%p3scansettings);

$checked{'ENABLE'}{'off'} = '';
$checked{'ENABLE'}{'on'} = '';
$checked{'ENABLE'}{$p3scansettings{'ENABLE'}} = 'CHECKED';

&openpage('POP3 proxy configuration', 1, $refresh, 'services');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage);

print "<form method='post' action='?'><div>\n";

&openbox('POP3 proxy:');
print <<END
<table style='width:100%;'>
<tr>
	<td style='width:25%;' class='base'>$tr{'enabled'}</td>
	<td style='width:75%;'><input type='checkbox' name='ENABLE' $checked{'ENABLE'}{'on'}></td>
</tr>
</table>
END
;
&closebox();

print <<END
<table style='width: 60%; border: none; margin-left:auto; margin-right:auto'>
<tr>
        <td style='text-align:center;'><input type='submit' name='ACTION' value='$tr{'save'}'></td>
</tr>
</table>
END
;

print "</div></form>\n";

&alertbox('add', 'add');

&closebigbox();

&closepage();

sub isclamrunning {
	my $cmd = $_[0];
	my $pid = '';
	my $testcmd = '';
	my $exename;

	$cmd =~ /(^[a-z]+)/;
	$exename = $1;
	my $status = "stopped";

	if (open(FILE, "/var/run/${cmd}.pid")) {
		$pid = <FILE>;
		chomp $pid;
		close FILE;
		if (open(FILE, "/proc/${pid}/status")) {
			while (<FILE>) {
				if (/^Name:\W+(.*)/) {
					$testcmd = $1;
				}
			}
			close FILE;
			if ($testcmd =~ /$exename/) {
				$status = "running"; 
			}
		}
	}
	else {
		$pid = `ps -C $cmd -o pid=`;
		chomp ($pid);
		if ($pid) {
			$status = "starting";
		}
	}
	return ( $status );
}
