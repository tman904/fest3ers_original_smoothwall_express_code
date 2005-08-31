sub downloadlist
{
	my %proxy;
	&readhash("${swroot}/main/proxy", \%proxy);

	my $host; my $port;
        unless ($proxy{'SERVER'})
        {
                $host = 'updates.smoothwall.org';
                $port = 80;
        }
        else
        {
                $host = $proxy{'SERVER'};
                $port = $proxy{'PORT'};
        }
	my $sock;
	unless ($sock = new IO::Socket::INET (PeerAddr => $host, PeerPort => $port,
		Proto => 'tcp', Timeout => 5))
	{
		print STDERR "unable to connect\n";
		$errormessage = $tr{'could not connect to smoothwall org'};
		return 0;
	}
	print $sock "GET http://updates.smoothwall.org/express/$version HTTP/1.1\r\nHost: updates.smoothwall.org\r\nConnection: close\r\n\r\n";
	my $ret = '';
	while (<$sock>) {
		$ret .= $_; }
	close($sock);
	return $ret;
}

1;
