#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

require '/var/smoothwall/header.pl';

my %cgiparams;
# Maps a nice printable name to the changing part of the pid file, which
# is also the name of the program

my $iface = '';
if (open(FILE, "${swroot}/red/iface"))
{
	$iface = <FILE>;
	close FILE;
}


# build the list of services.

my %servicenames;

opendir(DIR, "/var/smoothwall/services/");
my @files = grep {!/\./} readdir(DIR);

foreach my $file ( sort @files ){
	print STDERR "checking $file\n";;
	open ( my $line, "</var/smoothwall/services/$file" ) or next;
	my $name = <$line>;
	close $line;
	chomp $name;
	my $servicename = $file;
	$servicename =~s/\[RED\]/$iface/ig;
	
	$servicenames{ $tr{ $name } } = $servicename;
}

#my %servicenames =
#(
#	$tr{'dhcp server'} => 'dhcpd',
#	$tr{'web server'} => 'httpd',
#	$tr{'cron server'} => 'crond',
#	$tr{'dns proxy server'} => 'dnsmasq',
#	$tr{'logging server'} => 'syslogd',
#	$tr{'kernel logging server'} => 'klogd',
#	$tr{'secure shell server'} => 'sshd',
#	$tr{'vpn'} => 'pluto',
#	$tr{'web proxy'} => 'squid'
#);
#
#$servicenames{$tr{'intrusion detection system'}} = "snort_${iface}";

&showhttpheaders();

&getcgihash(\%cgiparams);

&openpage($tr{'status information'}, 1, '', 'about your smoothie');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage);

&openbox($tr{'services'});

print <<END
<DIV ALIGN='CENTER'>
<TABLE WIDTH='60%'>
END
;

my $lines = 0;
my $key = '';
foreach $key (keys %servicenames)
{
	if ($lines % 2) {
		print "<TR BGCOLOR='$table1colour'>\n"; }
	else {
		print "<TR BGCOLOR='$table2colour'>\n"; }
	print "<TD WIDTH='70%' ALIGN='CENTER'>$key</TD>\n";
	my $shortname = $servicenames{$key};
	my $status = &isrunning($shortname);
	print "<TD WIDTH='30%' ALIGN='CENTER'>$status</TD>\n";
	print "</TR>\n";
	$lines++;
}


print "</TABLE>\n";

&closebox();

&alertbox('add','add');

&closebigbox();

&closepage();

sub isrunning
{
	my $cmd = $_[0];
	my $status = "<TABLE CELLPADDING='2' CELLSPACING='0' BGCOLOR='$colourlightred'><TR><TD><B>$tr{'stopped'}</B></TD></TR></TABLE>";
	my $pid = '';
	my $testcmd = '';
	my $exename;

	$cmd =~ /(^[a-z]+)/;
	$exename = $1;

	if (open(FILE, "/var/run/${cmd}.pid"))
	{
 		$pid = <FILE>; chop $pid;
		close FILE;
		if (open(FILE, "/proc/${pid}/status"))
		{
			while (<FILE>)
			{
				if (/^Name:\W+(.*)/) {
					$testcmd = $1; }
			}
			close FILE;
			if ($testcmd =~ /$exename/)
			{
				$status = "<TABLE CELLPADDING='2' CELLSPACING='0' BGCOLOR='$colourlightgreen'><TR><TD><B>$tr{'running'}</B></TD></TR></TABLE>";
				if (open(FILE, "/proc/${pid}/cmdline"))
				{
					my $cmdline = <FILE>;
					if (!$cmdline) {
						$status = "$status ($tr{'swapped'})"; }
				}
			}
		}
	}

	return $status;
}
