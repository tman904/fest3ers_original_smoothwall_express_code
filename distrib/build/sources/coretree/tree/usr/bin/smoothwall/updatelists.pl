#!/usr/bin/perl

use IO::Socket;
require '/var/smoothwall/header.pl';
require '/var/smoothwall/updatelists.pl';

my @this;
my $return = &downloadlist();
if ($return =~ m/^HTTP\/\d+\.\d+ 200/) {
	unless(open(LIST, ">${swroot}/patches/available")) {
		die "Could not open available lists database."; }
	flock LIST, 2;
	@this = split(/----START LIST----\n/,$return);
	print LIST $this[1];
	close(LIST);
} else {
	die "Could not download patches list.";
}
