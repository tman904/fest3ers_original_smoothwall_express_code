#!/usr/bin/perl

use lib "/usr/lib/smoothwall/";
use header qw( :standard );
use POSIX qw(strftime);

my %cgiparams;
&getcgihash(\%cgiparams);
&showhttpheaders();

# Configuration options  -----  Mostly colours and suchlike

my $protocol_colour     = '#06264d';
my $local_colour        = '#1d398b';
my $remote_colour       = '#2149c1';
my $conversation_colour = '#335ebe';

my $local_user_colour   = 'blue';
my $remote_user_colour  = 'green';

my %smilies = (  
	':)' => 'icon_smile.gif',
	':-)' => 'icon_smile.gif',
	':(' => 'icon_sad.gif',
	':-(' => 'icon_sad.gif',
	';)' => 'icon_wink.gif',
	';-)' => 'icon_wink.gif',
	':o' => 'icon_surprised.gif',
	':-o' => 'icon_surprised.gif',
	':d' => 'icon_biggrin.gif',
	':-d' => 'icon_biggrin.gif',
	':-?' => 'icon_confused.gif',
	':?' => 'icon_confused.gif',
	':roll:' => 'icon_rolleyes.gif',
	'lol' => 'icon_lol.gif',
	':shock:' => 'icon_eek.gif',
	':x'	=> 'icon_mad.gif',
	':evil:' => 'icon_evil.gif',
	':twisted:' => 'icon_twisted.gif',
);


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
					my $protocol_img = "";
					if ( -e "/httpd/html/ui/img/im/$protocol.png" ){
						$protocol_img = "/ui/img/im/$protocol.png";
					}
					print "$protocol_img|$protocol|$localuser|$remoteuser|$conversation\n";
				}
				closedir CONVERSATIONS;
			}
			closedir RUSER;
		}
		closedir LUSER;
	}
	closedir DIR;

	print "--END--\n";

	# now check the log file ...
	
	if ( $cgiparams{'section'} ne "none" ){
		my ( $protocol, $localuser, $remoteuser, $conversation ) = split /\|/, $cgiparams{'section'};
		
		print "$protocol, $localuser, $remoteuser, $conversation\n";
		print "--END--\n";
		
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
				$user = "&lt;<span style='color: $remote_user_colour;'>$u</span>&gt;";
			} elsif ( $type eq "2" ){
				# outgoing message
				my $u = $localuser;
				$u =~ s/\@.*//g;
				$user = "&lt;<span style='color: $local_user_colour;'>$u</span>&gt;";
			}
			foreach my $smiley ( keys %smilies ){
				my $smile = quotemeta $smiley;
				$data =~s/$smile/<img src='\/ui\/img\/im\/smiles\/$smilies{$smiley}' alt='$smiley'\/>/igm;
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
var moveit = 1;
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

	var parts = str.split( "--END--\\n" );

	var lines = parts[0].split( "\\n" );
			
	for ( var line = 0 ; line < lines.length ; line ++ ){
		var a = lines[line].split("|");

		if ( !a[1] || !a[2] || !a[3] ){
			continue;
		}

		/* create titling information if needed */
		if ( !document.getElementById( a[1] ) ){
			document.getElementById('conversations').innerHTML += "<div id='" + a[1] + "_t' style='width: 100%; background-color: #d9d9f3; color: $protocol_colour;'>" + a[1] + "</div><div id='" + a[1] + "' style='width: 100%; background-color: #e5e5f3;'></div>";
		 }

		if ( !document.getElementById( a[1] + "_" + a[2] ) ){
			var imageref = "";
			if ( a[0] ){
				imageref = "<img src='" + a[0] + "' alt='" + a[1] + "'/>";
			}
			document.getElementById( a[1] ).innerHTML += "<div id='" + a[1] + "_" + a[2] + "_t' style='width: 100%; color: $local_colour; padding-left: 5px;'>" + imageref + a[2] + "</div><div id='" + a[1] + "_" + a[2] + "' style='width: 100%; background-color: #efeffa; border-bottom: solid 1px #d9d9f3;'></div>";
		}

		if ( !document.getElementById( a[1] + "_" + a[2] + "_" + a[3] ) ){
			document.getElementById( a[1] + "_" + a[2] ).innerHTML += "<div id='" + a[1] + "_" + a[2] + "_" + a[3] + "_t' style='width: 100%; color: $remote_colour; padding-left: 10px;'>" + a[3] + "</div><div id='" + a[1] + "_" + a[2] + "_" + a[3] + "' style='width: 100%;'></div>";
		}

		if ( !document.getElementById( a[1] + "_" + a[2] + "_" + a[3] + "_" + a[4] ) ){
			document.getElementById( a[1] + "_" + a[2] + "_" + a[3] ).innerHTML += "<div id='" + a[1] + "_" + a[2] + "_" + a[3] + "_" + a[4] + "' style='width: 100%; color: $conversation_colour; cursor: pointer; padding-left: 15px;' onClick=" + '"' + "setsection('" + a[1] + "|" + a[2] + "|" + a[3] + "|" + a[4] + "');" + '"' + "' + >&raquo;" + a[4] + "</div>";
		}
	}

	/* determine the title of this conversation */
	var details = parts[1].split(",");
	var title = details[0] + " conversation between <span style='color: $local_user_colour;'>" + details[ 1 ] + "</span> and <span style='color: $remote_user_colour;'>" + details[2] + "</span>";
	if ( !details[1] ){
		title = "&nbsp;";
	}
	if ( !parts[2] ){
		parts[2] = "&nbsp;";
	}

	document.getElementById('status').style.display = "none";
	
	var bottom  = parseInt( document.getElementById('content').scrollTop );
	var bottom2 = parseInt( document.getElementById('content').style.height );
	var absheight = parseInt( bottom + bottom2 );
	if ( absheight == document.getElementById('content').scrollHeight ){	
		moveit = 1;
	} else {
		moveit = 0;
	}
	document.getElementById('content').innerHTML = parts[2];
	if (moveit == 1 ){
		document.getElementById('content').scrollTop = 0;
		document.getElementById('content').scrollTop = document.getElementById('content').scrollHeight;
	}
	document.getElementById('content_title').innerHTML = title;
	the_timeout = setTimeout( "xmlhttpPost();", 5000 );
}

function setsection( value )
{
	section = value;
	clearTimeout(the_timeout);
	xmlhttpPost();
	document.getElementById('content').scrollTop = 0;
	document.getElementById('content').scrollTop = document.getElementById('content').scrollHeight;
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
			<td style='width: 170px; text-align: left; vertical-align: top; overflow: auto; font-size: 8pt; border: solid 1px #c0c0c0;'><div id='conversations' style='height: 400px; overflow: auto; font-size: 9px; overflow-x: hidden;'></div></td>
			<td style='border: solid 1px #c0c0c0;'>
				<div id='content_title' style='height: 20px; overflow: auto; vertical-align: top; background-color: #E6E8FA; border-bottom: solid 1px #c0c0c0;'></div>
				<div id='content' style='height: 380px; overflow: auto; vertical-align: bottom; border-bottom: solid 1px #c0c0c0; overflow-x: hidden;'></div>
			</td>
		</tr>
	</table>
	<script>xmlhttpPost();</script>
};

&closebigbox();

&closepage();

