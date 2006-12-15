#!/usr/bin/perl
use lib "/usr/lib/smoothwall";
use header qw(:standard);
print "Pragma: no-cache\n";
print "Cache-control: no-cache\n";
print "Connection: close\n";
print "content-type: text/html\n\n";
open INPUT, "</var/log/quicktrafficstats";
while ( my $line = <INPUT> ){
	next if ( not $line =~ /^cur_/ );
	print "$line\n";
}
print "\n";
close INPUT;
