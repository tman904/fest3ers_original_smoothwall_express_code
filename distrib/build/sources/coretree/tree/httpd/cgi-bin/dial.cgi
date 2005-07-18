#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

require '/var/smoothwall/header.pl';

my %cgiparams;

$cgiparams{'ACTION'} = '';
&getcgihash(\%cgiparams);

if ($cgiparams{'ACTION'} eq $tr{'dial'}) {
	system('/etc/ppp/ppp-on') == 0
	or &log("Dial failed: $?"); }
elsif ($cgiparams{'ACTION'} eq $tr{'hangup'}) {
	system('/etc/ppp/ppp-off') == 0
	or &log("Hangup failed: $?"); }
sleep 1;

print "Status: 302 Moved\nLocation: /cgi-bin/index.cgi\n\n";
