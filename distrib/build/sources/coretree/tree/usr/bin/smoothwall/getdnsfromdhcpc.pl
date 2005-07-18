#!/usr/bin/perl
#
# Helper program to get DNS info from dhcpc .info file.
#
# (c) Lawrence Manning, 2001

require '/var/smoothwall/header.pl';

my $count = $ARGV[0];
my (%settings, $dhcp, $dns, @alldns, %dhcp);

if ($count eq "" || $count < 1) {
	die "Bad DNS number given"; }

readhash("${swroot}/ethernet/settings", \%settings);

if (!($settings{'CONFIG_TYPE'} == 2 || $settings{'CONFIG_TYPE'} == 3)) {
	die "RED is not a nic"; }
if ($settings{'RED_DHCP'} != 'on') {
	die "RED is not on DHCP"; }
if (!&readhash("/etc/dhcpc/dhcpcd-$settings{'RED_DEV'}.info", \%dhcpc)) {
	die "Could not open dhcpc info file"; }

$dns = $dhcpc{'DNS'};

@alldns = split(',', $dns);

print "$alldns[$count - 1]\n";
