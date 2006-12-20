#!/usr/bin/perl

use lib "/usr/lib/smoothwall/";
use header qw( :standard );
use POSIX qw(strftime);

my %cgiparams;
&getcgihash(\%cgiparams);
&showhttpheaders();

# Configuration options  -----  Mostly colours and suchlike

my $protocol_colour     = 'blue';
my $local_colour        = 'green';
my $remote_colour       = 'red';
my $conversation_colour = 'darkgreen';

# and now back with things that shouldn't be changed :)

my $oururl = '/cgi-bin/logs.cgi/imviewer.cgi';

if ($ENV{'QUERY_STRING'})
{
        my @vars = split('\&', $ENV{'QUERY_STRING'});
	foreach $_ (@vars)
	{
		my ($var, $val) = split(/\=/);
		$cgiparams{$var} = $val;
	}
}

# Act in Tail mode (as in just generate the raw logs and pass back to the other CGI

if ( defined $cgiparams{'mode'} and $cgiparams{'mode'} eq "render" ){
	# render the user list ...

	# browse for the available protocols
	unless ( opendir DIR, "/var/log/imspector/" ){
		print STDERR "no logs\n";
		exit;
	}

	my @protocols = grep {!/^\./} readdir(DIR);		

	foreach my $protocol ( @protocols ){
		unless ( opendir LUSER, "/var/log/imspector/$protocol" ){
			print STDERR "no localusers\n";
			next;
		}
	
		my @localusers = grep {!/^\./} readdir(LUSER);		
		foreach my $localuser ( @localusers ){
			unless ( opendir RUSER, "/var/log/imspector/$protocol/$localuser/" ){
				print STDERR "no remote users ($protocol)\n";
				next;
			}
			my @remoteusers = grep {!/^\./} readdir( RUSER );
			foreach my $remoteuser ( @remoteusers ){
				unless ( opendir CONVERSATIONS, "/var/log/imspector/$protocol/$localuser/$remoteuser/" ){
					print STDERR "no dates\n";
					next;
				}
				my @conversations = grep {!/^\./} readdir( CONVERSATIONS );
				foreach my $conversation ( @conversations ){
					print "$protocol|$localuser|$remoteuser|$conversation\n";
				}
				closedir CONVERSATIONS;
			}
			closedir RUSER;
		}
		closedir LUSER;
	}
	closedir DIR;

	print "--END--";

	# now check the log file ...
	
	if ( $cgiparams{'section'} ne "none" ){
		my ( $protocol, $localuser, $remoteuser, $conversation ) = split /\|/, $cgiparams{'section'};
		my $filename = "/var/log/imspector/$protocol/$localuser/$remoteuser/$conversation";
		print STDERR "looking at $filename\n";
		
		unless ( open(FD, "$filename" ) ){
			print STDERR "Unable to do that $!\n";
			exit;
		};

		# perform some *reasonably* complicated file hopping and stuff of that ilk.
		# it's not beyond reason that logs *could* be extremely large, so what we
		# should do to speed up their processing is to jump to the end of the file,
		# then backtrack a little (say a meg, which is a reasonably amount of logs)
		# and parse from that point onwards.  This, *post* filtering might of course
		# not leave us with the desired resolution for the tail.  If this is the case,
		# we keep that array and jump back another meg and have another go, concatinating
		# the logs as we go.... <wheh>

		my $jumpback = 100000; # not quite a meg, but hey ho	
		my $goneback = 0;
		my $gonebacklimit = 1000000000;  # don't go back more than 100MB

		# firstly jump to the end of the file.
		seek( FD, 0, 2 );

		my $log_position = tell( FD );
		my $end = $log_position;
		my $end_position = $log_position;

		my $lines;
		my @content;

		my $TAILSIZE = 100;

		do {
			$end_position = $log_position;
			$log_position -= $jumpback;
	
			$goneback += $jumpback;

			last if ( $goneback > $gonebacklimit );

			if ( $log_position > 0 ){
				seek( FD, $log_position, 0 );
			} else {
				seek( FD, 0, 0 );
			}
	
			my @newcontent;

			while ( my $line = <FD> and ( tell( FD ) <= $end_position ) ){
				chomp $line;
				push @content, $line;
			}
			shift @content if $#content >= $TAILSIZE;
		} while ( $#content < $TAILSIZE and $log_position > 0 );

		# trim the content down as we may have more entries than we should.
	
		while ( $#content > $TAILSIZE ){ shift @content; };
		close FD;

		print "<table style='width: 100%;'>";
		foreach my $line ( @content ){
			my ( $address, $timestamp, $type, $data ) = ( $line =~ /([^,]*),([^,]*),([^,]*),(.*)/ );
			my $user = "";
			if ( $type eq "1" ){
				# incoming message (from remote user)
				my $u = $remoteuser;
				$u =~ s/\@.*//g;
				$user = "&lt;<span style='color: green;'>$u</span>&gt;";
			} elsif ( $type eq "2" ){
				# outgoing message
				my $u = $localuser;
				$u =~ s/\@.*//g;
				$user = "&lt;<span style='color: blue;'>$u</span>&gt;";
			}
			my $t = strftime "%H:%M:%S", localtime($timestamp);
			print "<tr><td style='width: 30px; vertical-align: top;'>[$t]</td><td style=' width: 60px; vertical-align: top;'>$user</td><td style='vertical-align: top;'>$data</td></tr>";
		}
		print "</table>";
	}

	exit;
}

my $script = qq {
<script language="Javascript">
var section='none';
var the_timeout;

function xmlhttpPost()
{
	var xmlHttpReq = false;
    	var self = this;

    	if (window.XMLHttpRequest) {
		// Mozilla/Safari
        	self.xmlHttpReq = new XMLHttpRequest();
    	} else if (window.ActiveXObject) {
    		// IE
        	self.xmlHttpReq = new ActiveXObject("Microsoft.XMLHTTP");
    	}

    	self.xmlHttpReq.open('POST', "$oururl", true);
	self.xmlHttpReq.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

    	self.xmlHttpReq.onreadystatechange = function() {
	        if ( self.xmlHttpReq && self.xmlHttpReq.readyState == 4) {
        		updatepage(self.xmlHttpReq.responseText);
		}
    	}

	document.getElementById('status').style.display = "inline";

    	self.xmlHttpReq.send( "mode=render&section=" + section );
}

function updatepage(str){
	/* update the list of conversations ( if we need to ) */

	var parts = str.split( "--END--" );

	var lines = parts[0].split( "\\n" );
			
	for ( var line = 0 ; line < lines.length ; line ++ ){
		var a = lines[line].split("|");

		if ( !a[0] || !a[1] || !a[2] ){
			continue;
		}

		/* create titling information if needed */
		if ( !document.getElementById( a[0] ) ){
			document.getElementById('conversations').innerHTML += "<div id='" + a[0] + "_t' style='width: 100%; color: $protocol_colour;'>" + a[0] + "</div><div id='" + a[0] + "' style='width: 100%;'></div>";
		 }

		if ( !document.getElementById( a[0] + "_" + a[1] ) ){
			document.getElementById( a[0] ).innerHTML += "<div id='" + a[0] + "_" + a[1] + "_t' style='width: 100%; color: $local_colour; margin-left: 10px;'>" + a[1] + "</div><div id='" + a[0] + "_" + a[1] + "' style='width: 100%;'></div>";
		}

		if ( !document.getElementById( a[0] + "_" + a[1] + "_" + a[2] ) ){
			document.getElementById( a[0] + "_" + a[1] ).innerHTML += "<div id='" + a[0] + "_" + a[1] + "_" + a[2] + "_t' style='width: 100%; color: $remote_colour; margin-left: 20px;'>" + a[2] + "</div><div id='" + a[0] + "_" + a[1] + "_" + a[2] + "' style='width: 100%;'></div>";
		}

		if ( !document.getElementById( a[0] + "_" + a[1] + "_" + a[2] + "_" + a[3] ) ){
			document.getElementById( a[0] + "_" + a[1] + "_" + a[2] ).innerHTML += "<div id='" + a[0] + "_" + a[1] + "_" + a[2] + "_" + a[3] + "' style='width: 100%; color: $conversation_colour; margin-left: 30px; cursor: pointer;' onClick=" + '"' + "setsection('" + a[0] + "|" + a[1] + "|" + a[2] + "|" + a[3] + "');" + '"' + "' + >" + a[3] + "</div>";
		}
	}

	document.getElementById('status').style.display = "none";
	document.getElementById('content').innerHTML = parts[1];
	the_timeout = setTimeout( "xmlhttpPost();", 5000 );
}

function setsection( value )
{
	section = value;
	clearTimeout(the_timeout);
	xmlhttpPost();
}

</script>
};

&openpage('Instant Messenger proxy logs', 1, $script, 'logs');
&openbigbox('100%', 'LEFT');

my $options = qq{
};

print qq{
	<div style='width: 100%; text-align: right;'><span id='status' style='background-color: #fef1b5; display: none;'>Updating</span>&nbsp;</div>
	<table style='width: 100%;'>
		<tr>
			<td style='width: 14%; text-align: left; vertical-align: top; overflow: auto; font-size: 8pt; border: solid 1px #c0c0c0;'><div id='conversations'></div></td>
			<td style='border: solid 1px #c0c0c0;'>
				<div id='content_title' style='height: 20px; overflow: auto; vertical-align: top; border-bottom: solid 1px #c0c0c0;'></div>
				<div id='content' style='height: 380px; overflow: auto; vertical-align: top; border: solid 1px #c0c0c0;'></div>
			</td>
		</tr>
	</table>
	<script>xmlhttpPost();</script>
};

&closebigbox();

&closepage();

