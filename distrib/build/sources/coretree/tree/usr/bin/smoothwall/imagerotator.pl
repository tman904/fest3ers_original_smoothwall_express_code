#!/usr/bin/perl

use lib "/usr/lib/smoothwall";
use header qw(:standard );

use IO::Socket;

my %proxy;

&readhash("${swroot}/main/proxy", \%proxy);

my $host; my $port;
unless ($proxy{'SERVER'})
{
	$host = 'www.smoothwall.org';
        $port = 80;
} else {
	$host = $proxy{'SERVER'};
	$port = $proxy{'PORT'};
}

my $sock;

unless ($sock = new IO::Socket::INET (PeerAddr => $host, PeerPort => $port, Proto => 'tcp', Timeout => 5)) {
	print STDERR "unable to connect\n";
	$errormessage = $tr{'could not connect to smoothwall org'};
	return 0;
}

print $sock "GET http://www.smoothwall.org/updates/$version/banners HTTP/1.1\r\nHost: www.smoothwall.org\r\nConnection: close\r\n\r\n";

my $return = '';

while (<$sock>) {
	$return .= $_; 
}
close($sock);

if ($return =~ m/^HTTP\/\d+\.\d+ 200/) {
	unless(open(LIST, ">${swroot}/banners/available")) {
		die "Could not open available lists database."; 
	}

	flock LIST, 2;
	@this = split(/----START LIST----\n/,$return);
	print LIST $this[1];
	close(LIST);
} else {
	die "Could not download banner list. $return";
}


unless(open(LIST, "<${swroot}/banners/available")) {
	die "Could not open available lists database."; 
}

my %seen = ( 'frontpage' => 'true' );

while ( my $input = <LIST> ){
	my ( $url, $md5, $link, $alt ) = ( $input =~/([^,]*),([^,]*),([^,]*),(.*)/ );
	
	$seen{$md5} = 'true';

	if ( !-e "/httpd/html/ui/img/frontpage/$md5.jpg" ){
		# we need to download this file 
		print STDERR "getting missing banner\n";
		my @commands = ( "/usr/bin/wget", "-O", "/httpd/html/ui/img/frontpage/$md5.jpg", "$url" );
		my ( $status, $pid_out );
		open(PIPE, '-|') || exec( @commands );
	        while (<PIPE>) { 
			$status .= $_; 
		}
		close(PIPE);
		print STDERR $status;
	}
}


foreach my $filename ( glob "/httpd/html/ui/img/frontpage/*" ){
	my ($image) = ( $filename =~ /\/httpd\/html\/ui\/img\/frontpage\/(.*)\.jpg/i );
	if ( not defined $seen{$image} ){
		unlink "/httpd/html/ui/img/frontpage/$image.jpg";
	}
}
