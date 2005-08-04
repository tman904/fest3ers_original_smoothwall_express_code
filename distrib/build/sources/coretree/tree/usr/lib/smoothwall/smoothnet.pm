# (c) 2004-2005 SmoothWall Ltd

package smoothnet;
require Exporter;
@ISA = qw(Exporter);

# define the Exportlists.

@EXPORT       = qw();
@EXPORT_OK    = qw( download $downloadstore );
%EXPORT_TAGS  = (
		standard   => [qw( download $downloadstore)],
		);

our $server        = "downloads.smoothwall.org";
our $basever       = "2.0";
our $uri           = "/updates/$basever/";
our $extension     = ".tar.gz";

my $default_port   = "80";
my $protocol       = "http";

my $retries       = 3;	# number of retries for downloads
my $proxyserver   = "";
my $proxyport     = "";
my $agent         = "SmoothWall Download Agent V1.1";
my $basestore     = "/var/patches";
my $downloadstore = "$basestore/downloads";
my $pendingstore  = "$basestore/pending";

# HTTP / HTTPS download mechanism to download the latest updates.
use LWP::Simple;
use LWP::UserAgent;
use HTTP::Request;

# modules
use IO::Socket;

sub download
{
	my ( $filename, $size, $md5, $status ) = @_;

	my $url = "$protocol://$server/$uri/$basever-$filename$extension"; 

	my $destination = "$downloadstore/$filename";

	$url =~s/ /%20/g;
	$filename =~s/ /%20/g;

        for my $retryno (1..$retries) {
		if ( &safedownload( "$url", $size, $destination, $proxyserver, $proxyport, $status, $filename ) == 1) {

			my $gotsize = ( stat( "$destination") )[7];

			if($gotsize != $size) {
				system('/usr/bin/logger', '-t', 'SmoothDownload', "Download failed (read $gotsize bytes instead of $size) | $retryno" );
				sleep(3*$retryno);
                                next;
                        }       
			
			# calculate the MD5 of the file we just downloaded
                        my $md5sum;

			open(PIPE, '-|') || exec('/usr/bin/md5sum', "$destination");
			
                        while (<PIPE>) { $md5sum = $md5sum.$_; }
                        close (PIPE);
                        
			chomp $md5sum;
                        $md5sum =~ /^([\da-fA-F]+)/;
                        $md5sum = $1;
                        if ($md5sum eq $md5) {
                        	# file is ok, it has the correct md5
				system('/usr/bin/logger', '-t', 'SmoothDownload', "Complete $destination" );
				return $destination;
                        } else {
				# failed;
				system('/usr/bin/logger', '-t', 'SmoothDownload', "Download failed MD5 mistmatch $md5 vs $md5sum" );
				return undef;
                        }
		} else {
			system('/usr/bin/logger', '-t', 'SmoothDownload', "Download failed, Retry $retryno" );
		}
	}

	system('/usr/bin/logger', '-t', 'SmoothDownload', "Unable to download update ($destination from $url)" );

	open ( my $out, ">$destination.failure" ) or return undef;
	print $out "too many retries";

	close $out;

	unlink "$destination";
	unlink "$destination.abort";
	
	system('/usr/bin/logger', '-t', 'SmoothDownload', "end $destination" );

	return undef;
}

sub safedownload {
        my ( $url, $expectedbytes, $saveasfile, $proxyserver, $proxyport, $status, $filename ) = @_;
	
        my $bytesdown = 1;
        my $data;
        my $req = new HTTP::Request( GET => $url );
        my $ua = new LWP::UserAgent;
        
	$ua->agent("$agent" . $ua->agent);
        $ua->timeout(300);
	$ua->env_proxy;

        $start_t = time;
        $last_time = $start_t;

	unlink( "$saveasfile" );
	unlink "$saveasfile.failure";
	unlink "$saveasfile.timestamp";	
	
        if ($proxyserver) {
                $ua->proxy(['http', 'https'], 'http://$proxyserver:$proxyport/');
        }
        unless ( open(FILE, ">$saveasfile") ){
		warn "Unable to open updates file ($saveasfile)\n";
		return ( 0 );
	};
        if ( open(TSFILE, ">$saveasfile.timestamp") ){
		print TSFILE $start_t;
		close TSFILE;
	} else {
		warn "Unable to open updates file ($saveasfile)\n";
	};

        binmode FILE;

	&{$status}( 0,0,0,0,$expectedbytes, $filename );

        my $res = $ua->request($req, 
                sub {
	    		my ($d, $res) = @_;
                        if (!($res->is_success)) {
                                close(FILE);
                                return 0;
                        }
			if ( -e "$saveasfile.abort" ){
				close FILE;
				unlink "$saveasfile";
				unlink "$saveasfile.abort";
				unlink "$saveasfile.failure";
				unlink "$saveasfile.timestamp";
				exit -1;
			}
                        print FILE $d;
                        $bytesdown += length($d);
                        if ( (time - $last_time) > 1) {
                                $last_time = time;
				size_callback( $bytesdown, $expectedbytes, $status, $start_t, $filename);	
                        }
                }
        , 4096 );
        close(FILE);
	unlink "$saveasfile.timestamp";
     
	if ($res->is_success) {
                return 1;
        }

        return 0;
}

sub size_callback
{
	my ( $bytesdown, $expectedbytes, $status, $start_t, $filename ) = @_;

	my $perc = 0;
	$perc = int(($bytesdown / $expectedbytes) * 100) if ( $expectedbytes != 0 );
        my $speed = 0;
	$speed = $bytesdown/((time - $start_t)) if ( ((time - $start_t) > 0) and  (defined $start_t and $start_t ne 0) );
        my $secs_left = "n/a";
	$secs_left = int((($expectedbytes - $bytesdown) / $speed) + .5) if ( $speed ne "0" );
        $speed = int($speed/1024);
	# status is a function reference, call it.
	&{$status}( $perc, $speed, $secs_left, $bytesdown, $expectedbytes, $filename);
}

# The following functions provide the basis for offline (non interactive) downloading.
# i.e. the files are downloaded without being attached to a front end (such as perl etc)

sub checkstatus
{
	my ( $url, $filename, $size, $md5, $status ) = @_;

	my $destination = "$downloadstore/$filename";

	# check for a "failure"
	if ( -e "$destination.failure" ){
		size_callback( -1, -1, $status, -1, $filename );	
		return -3;
	}

	unless ( -e $destination ){
		return 1;
	}

	my $gotsize = ( stat( "$destination") )[7];

	my $date = (stat( "$destination" ))[9];
	
	if ( ((time() - $date) > 60 ) and ( $gotsize != $size ) ){
		# the download has probably stalled...
		size_callback( -1, $size, $status, -1, $filename );	
		return -2;
	}

	if ( $gotsize == $size ){
		# file is complete, check it's md5
		if ( not checkmd5( $filename, $md5 ) ){
			size_callback( -1, $size, $status, -1, $filename );	
			return -1;
		}
	}

	my $start_t = 0;

	# get the timestamp for this file...
        if ( open(TSFILE, "<$destination.timestamp") ){
		$start_t = <TSFILE>;
		chomp $start_t;
		close TSFILE;
	};
	

	size_callback( $gotsize, $size, $status, $start_t, $filename );	
	
	return 0;
}

sub checkmd5
{
	my ( $filename , $md5 ) = @_;

	my $destination = "$downloadstore/$filename";
	# calculate the MD5 of the file we just downloaded
        my $md5sum;

	open(PIPE, '-|') || exec('/usr/bin/md5sum', "$destination");
	
	while (<PIPE>) { $md5sum = $md5sum.$_; }
	close (PIPE);
	
	chomp $md5sum;
	$md5sum =~ /^([\da-fA-F]+)/;
	$md5sum = $1;
	if ($md5sum eq $md5) {
		# file is ok, it has the correct md5
		return 1;
	} else {
		# failed;
		warn "Failed $md5sum\n";
		return 0;
	}
}


1;
