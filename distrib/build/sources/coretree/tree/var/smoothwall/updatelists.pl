sub downloadlist
{
	my %proxy;
	&readhash("${swroot}/main/proxy", \%proxy);

	my $host; my $port;
        unless ($proxy{'SERVER'})
        {
                $host = 'www.smoothwall.org';
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
	print STDERR "GET http://www.smoothwall.org/updates/$version/info HTTP/1.1\r\nHost: www.smoothwall.org\r\nConnection: close\r\n\r\n";
	print $sock "GET http://www.smoothwall.org/updates/$version/info HTTP/1.1\r\nHost: www.smoothwall.org\r\nConnection: close\r\n\r\n";
	my $ret = '';
	while (<$sock>) {
		$ret .= $_; }
	close($sock);
	return $ret;
}

1;
