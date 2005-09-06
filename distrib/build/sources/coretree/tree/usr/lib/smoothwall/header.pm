# SmoothWall Express "Header" Module
#
# This code is distributed under the terms of the GPL
#
# (c) 2004-2005 SmoothWall Ltd

package header;
require Exporter;
@ISA = qw(Exporter);

# define the Exportlists.

@EXPORT       = qw();
@EXPORT_OK    = qw( $language $version $webuirevision $viewsize @menu $swroot $thisscript showhttpheaders showmenu showsection openpage closepage openbigbox closebigbox openbox closebox alertbox pageinfo writehash readhash getcgihash log age validip validmask validipormask validipandmask validport validportrange validmac validhostname basename connectedstate %tr );
%EXPORT_TAGS  = (
		standard   => [@EXPORT_OK],
		);


$|=1; # line buffering

# Work out some various details from the various system files.
# such as fixes number etc.

$version = '3.0-grizzly';

$webuirevision = 'ui-3.5';
$viewsize = 200;

# some system wide (yuck) global variables.  not pretty, but make things easier.

my @menu;
my $span = 0;

# some constant defaults.

$swroot = '/var/smoothwall';
$thisscript = basename($ENV{'SCRIPT_NAME'});

# customised settings (such as languages)

&readhash("${swroot}/main/settings", \%settings);
$language = $settings{'LANGUAGE'};

if ($language =~ /^(\w+)$/) {$language = $1;}
require "${swroot}/langs/base.pl";
require "${swroot}/langs/${language}.pl";
require "${swroot}/main/ui/alertboxes.en.pl";

# Display the page HTTP header

sub showhttpheaders
{
	print "Pragma: no-cache\n";
	print "Cache-control: no-cache\n";
	print "Connection: close\n";
	print "Content-type: text/html\n\n";
}

# Show the top section menu, this has the side effect of populating
# the @menu variable (which is ordered accordingly) with the pages
# or subsections for the section we are looking for.

sub showmenu
{
	$scriptname = $_[0];

	# load the list of sections from the relevant location.
        opendir(DIR, "/var/smoothwall/menu/");
        my @files = grep {!/\./} readdir(DIR);

	print <<END
<tr>
	<td class='mainmenu'>
<table style='float: right;'>
<tr>
END
	;
	my $first = "";

	foreach my $file ( sort @files ){
		if ( -d "/var/smoothwall/menu/$file" ){
			# this is a section ....
		        opendir(DIR2, "/var/smoothwall/menu/$file/");
		        my @pages = grep {/\.list/} readdir(DIR2);

			my $section = "no";
			my @tempmenu;

			foreach my $page ( sort @pages ){
				my $detail;
				open $detail, "</var/smoothwall/menu/$file/$page" or next;
				my ( $title, $link ) = split /:/, <$detail>;
				chomp $link;
				my ( $menu, $pos ) = ( $file =~ /(\d{2})(\d{2}).*/ );
				my $active;
				my ( $link2 ) = ( $link =~/([^\/]*)$/ );
				if ( $link2 eq $thisscript ){
					$section = "yes";
					$active = "true" 
				}
				push @tempmenu, { 'title' => $title, 'href' => $link, 'active' => $active };
			}

			if ( scalar @pages > 0 ){
				my ( $section_title ) = ( $file =~/\d{4}_(.*)/ );

				if ( $section eq "yes" ){
					@menu = @tempmenu;
					print "<td>$first<a class='activemenu' href='/cgi-bin/$menu[ 0 ]->{'href'}'>$section_title</a></td>";
				} else {
					print "<td>$first<a class='menu' href='/cgi-bin/$tempmenu[ 0 ]->{'href'}'>$section_title</a></td>";
				}
			}

			$first = " | ";
		}
	}

	print <<END
</tr></table></td>
</tr>
<tr>
	<td colspan='2' class='quicklink'>
		<!-- Quicklink Section -->
		<a href='/cgi-bin/shutdown.cgi'>$tr{'ssshutdown'}</a> | <a href="javascript:displayHelp('$thisscript');" title="This will popup a new window with the requested help file">help</a> <img src="/ui/img/help.gif" alt="">
	</td>
</tr>


<!-- Create the top menu -->

<tr>
	<td colspan='2'>
	<br/>
END
	;

	showsection( @menu );

	return;
}

sub showsection
{
	my @menu = @_;
	print <<END
<table class='mainmenu'>
<tr>
END
;
	my $remaining = 795;
	
	foreach my $item ( @menu ){
		my $width = 8 + (8 * length( $tr{ $item->{'title'} } ));
		if ( defined $item->{'active'} and $item->{'active'} eq "true" ){
			print "<td class='activetab' style='width: ".( $width + 16 )."px;'><a href='/cgi-bin/$item->{'href'}'>$tr{$item->{'title'}}</a> </td>";
		} else {
			print "<td  class='inactivetab' style='width: ${width}px;'><a href='/cgi-bin/$item->{'href'}'>$tr{$item->{'title'}}</a> </td>";
		}
		$span++;
		$remaining -= $width;
	}

	$span++;

	print <<END
	<td width='${remaining}px;' class='endtab'>&nbsp;</td>
	<td class='topend'></td>
</tr>
<tr>
	<td class='mainbody' colspan='$span'>
END
;

}

sub openpage
{
	$title = $_[0];
	$menu = $_[1];
	$extrahead = $_[2];
	$thissection = $_[3];

	if ($menu == 1) { $colspan = 2; } else { $colspan = 1; }

	print <<END
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
	$extrahead
	<title>$title - SmoothWall Express</title>
	<script language='javascript' SRC='/ui/js/script.js'></script>
	<link href='/ui/css/style.css' rel='stylesheet' type='text/css'>
</head>
END
	;

	if ( $thissection ne "help" ) {
		$currentconnection = &connectedstate();
		$cellwidth = $pagewidth / 2;
		print <<END
<body>
<table class='main'>
<tr>
	<td class='logo' rowspan='2'>
		<a href="/cgi-bin/credits.cgi"><img src="/ui/img/logo.gif" alt="SmoothWall Express $version" title="SmoothWall Express $version"></a>
	</td><td class='header'>
		<table>
		<tr>
			<td>
				<img src="/ui/img/netstatus.label.gif" alt="current connection status" title="current connection status">
			</td>
			<td>
				<a href="/cgi-bin/index.cgi"><img src="/ui/img/netstatus-wee.${currentconnection}.gif" alt="$currentconnection" title="$currentconnection">
			</td>
		</tr>
		</table>
	</td>
</tr>
END
		;
		&showmenu($thissection);
		print <<END
END
		;
	} else { 
		print <<END
<body onLoad="window.focus()">
END
		;
	}

}

sub closepage
{
	$thissection = $_[0];

	$sflogoimg = "/ui/assets/3.5/img/sflogo.png";

	if ( $thissection ne "blank" ) {
		print <<END
	</td>
	<td class='end'></td>
	</tr>
	<tr>
		<td colspan='$span' class='bottom'></td>
		<td class='bottomright'></td>
	</tr>
		<!-- End of the Main Body -->
</table>
	<br/>
	</td>
</tr>
<tr>
	<td class='footer' colspan='2'>
	<table class='blank'>
	<tr>
		<td>
		    	<strong>SmoothWall Express $version</strong><br/>
			SmoothWall&trade; is a trademark of <a href='http://www.smoothwall.net/'>SmoothWall Limited</a>.
		</td>
		<td style='text-align: right;'>
		    	&copy; 2000 - 2005 <a href='http://smoothwall.org/team/'>The SmoothWall Team</a><br/>
			<a href='/cgi-bin/credits.cgi'>$tr{'credits'}</a> - Portions &copy; <a href='http://smoothwall.org/sources.html'>original authors</a>
		</td>
	</tr>
	</table>
	</td>
</tr> 
</table>
END
		;
	}


	if ( $thissection ne "update" ) {
		print <<END
	</body>
	</html>
END
;
	}


}

sub openbigbox
{
}

sub closebigbox
{
}

sub openbox
{
	my ( $caption ) = @_;

	print <<END
<br/>
<table class='box'>
<tr>
	<td>
END
	;
	if ($caption) { 
		print "<span class='caption'>$caption</span><br/>\n"; 
	}
}

sub closebox
{
	print <<END
	</td>
</tr>
</table>
<br/>
END
	;
}

sub alertbox
{
	my $thiserror = $_[0];
	my $additional = $_[1];
	if ( $thiserror ne '' && $additional eq '' ) {
		&pageinfo( "error", $thiserror);
	} elsif ( $thiserror eq 'add' && $additional eq 'add' && $abouttext{$thisscript . "-additional"} ne '' ) {
		&pageinfo( $alertbox{"textadd"}, $abouttext{$thisscript . "-additional"});
	} elsif ( $thiserror eq 'add' && $additional eq 'add' && $abouttext{$thisscript . "-additional"} eq '' ) {
		# deliberately do nothing
	} else {
		&pageinfo( $alertbox{"textok"}, $abouttext{$thisscript});
	}
}

sub pageinfo 
{
	my $thisalerttype = $_[0];
	my $thisboxmessage = $_[1];

	print <<END
<br/>
END
;

	if ( $thisalerttype ne "error" ) {
		print "<table class='note'>";
		print "<tr>";
		print "<td class='note'>$thisboxmessage</td>";
	}  else { 
		print "<table class='warning'>";
		print "<tr>";
		print "<td class='warningimg'><img src='/ui/img/warning.jpg' alt='$tr{'error'}'></td><td class='warning'><strong>$tr{'error'}</strong>$thisboxmessage</td>";
	}


print <<END
	</tr>
</table>
END
;

}

sub writehash
{
	my $filename = $_[0];
	my $hash = $_[1];
	
	# write cgi vars to the file.
	open(FILE, ">${filename}") or die "Unable to write file $filename";
	flock FILE, 2;
	foreach $var (keys %$hash) 
	{
		$val = $hash->{$var};
		if ($val =~ / /) {
			$val = "\'$val\'"; }
		if (!($var =~ /^ACTION/)) {
			print FILE "${var}=${val}\n"; }
	}
	close FILE;
}

sub readhash
{
	my $filename = $_[0];
	my $hash = $_[1];
	my ($var, $val);

	open(FILE, $filename) or die "Unable to read file $filename";
	
	while (<FILE>)
	{
		chop;
		($var, $val) = split /=/, $_, 2;
		if ($var)
		{
			$val =~ s/^\'//g;
			$val =~ s/\'$//g;
			$hash->{$var} = $val;
		}
	}
	close FILE;
}

sub getcgihash
{
	my $hash = $_[0];
	my $buffer = '';
	my $length = $ENV{'CONTENT_LENGTH'};
	my ($name, $value); 
	my ($pair, @pairs, $read);
	my %hash;
	my $boundary;
	my %remotesettings;
	my %main;
	my %netsettings;
	my $redip = '0.0.0.0';
	my $referer;
	my $shorthostname;
	my @hostnameelements;
	
	if ($ENV{'REQUEST_METHOD'} ne 'POST') {
		return; }

	$ENV{'HTTP_REFERER'} =~ m/^(http|https)\:\/\/(.*?)[\:|\/]/;
	$referer = $2;

	&readhash("${swroot}/remote/settings", \%remotesettings);
	&readhash("${swroot}/main/settings", \%main);
	&readhash("${swroot}/ethernet/settings", \%netsettings);

	@hostnameelements = split(/\./, $main{'HOSTNAME'});
	$shorthostname = $hostnameelements[0];

	if (open(FILE, "${swroot}/red/local-ipaddress"))
	{
		$redip = <FILE>; chomp $redip;
		close(FILE);
	}

	if ($remotesettings{'ENABLE_SECURE_ADMIN'} eq 'on')
	{
		unless ($referer eq $main{'HOSTNAME'} ||
			$referer eq $shorthostname ||
			$referer eq $netsettings{'GREEN_ADDRESS'} ||
			$referer eq $redip)
		{
			&log("Referral $ENV{'HTTP_REFERER'} is not a SmoothWall page.");
			return;
		}
	}        
	
	$read = 0;
	$buffer = "";
	while($read < $length){
		$read = $read + (read(STDIN, $buf, 1024) or die "Could not read buffer:$read: $@");
		$buffer .= $buf;
	}
	unless($read == $length) {
		die "Could not read buffer: $!";
	}

	if($ENV{'CONTENT_TYPE'} =~ m/multipart\/form-data; boundary=(.*)/) {
		$boundary = $1;
		chomp $boundary;
		$boundary =~ s/\+/ /g;
		foreach (split(/$boundary/,$buffer)) {
			s!--$!!so;
			if(m/Content-Disposition: form-data; name="(.*?)"/is) {
				$name = $1;
			}
			if(m/Content-Disposition: form-data; name="$name".*?\015\012\015\012(.*)$/is) {
				$value = $1;
				$value =~ s!\015\012$!!so;
				$hash->{$name} = $value;
			}
			else { next; }
		}
	} else {
		@pairs = split(/&/, $buffer);

		foreach $pair (@pairs)
		{
			$pair =~ s/\+/ /g;
			($name, $value) = split(/=/, $pair);
			next unless $name; # fields MUST BE named!
			$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack('C', hex($1))/eg;
			$value =~s/[^\w\013\n!@#\$%\^\*()_\-\+=\{\}\[\]\\|;:\'\"<,>\.?\/`~\& ]//g;
			$hash->{$name} = $value;
    		}
    	}
	return %hash;
}

sub log
{
	system('/usr/bin/logger', '-t', 'smoothwall', $_[0]);
}

sub age
{
	my ($dev, $ino, $mode, $nlink, $uid, $gid, $rdev, $size,
	        $atime, $mtime, $ctime, $blksize, $blocks) = stat $_[0];
	my $now = time;

	my $totalsecs = $now - $mtime;
	my $days = int($totalsecs / 86400);
	my $totalhours = int($totalsecs / 3600);
	my $hours = $totalhours % 24;
	my $totalmins = int($totalsecs / 60);
	my $mins = $totalmins % 60;
	my $secs = $totalsecs % 60;

 	return "${days}d ${hours}h ${mins}m ${secs}s";
}

sub validip
{
	my $ip = $_[0];

	if (!($ip =~ /^(\d+)\.(\d+)\.(\d+)\.(\d+)$/)) {
		return 0; }
	else 
	{
		@octets = ($1, $2, $3, $4);
		foreach $_ (@octets)
		{
			if (/^0./) {
				return 0; }
			if ($_ < 0 || $_ > 255) {
				return 0; }
		}
		return 1;
	}
}

sub validmask
{
	my $mask = $_[0];

	# secord part an ip?
	if (&validip($mask)) {
		return 1; }
	# second part a number?
	if (/^0/) {
		return 0; }
	if (!($mask =~ /^\d+$/)) {
		return 0; }
	if ($mask >= 0 && $mask <= 32) {
		return 1; }
	return 0;
}

sub validipormask
{
	my $ipormask = $_[0];

	# see if it is a IP only.
	if (&validip($ipormask)) {
		return 1; }
	# split it into number and mask.
	if (!($ipormask =~ /^(.*?)\/(.*?)$/)) {
		return 0; }
	$ip = $1;
	$mask = $2;
	# first part not a ip?
	if (!(&validip($ip))) {
		return 0; }
	return &validmask($mask);
}

sub validipandmask
{
	my $ipandmask = $_[0];

	# split it into number and mask.
	if (!($ipandmask =~ /^(.*?)\/(.*?)$/)) {
		return 0; }
	$ip = $1;
	$mask = $2;
	# first part not a ip?
	if (!(&validip($ip))) {
		return 0; }
	return &validmask($mask);
}

sub validport
{
	$_ = $_[0];

	if (!/^\d+$/) {
		return 0; }
	if (/^0./) {
		return 0; }
	if ($_ >= 1 && $_ <= 65535) {
		return 1; }
	return 0;
}

sub validportrange
{
        my $ports = $_[0];
        my $left; my $right;    

        if (&validport($ports)) {
                return 1; }
        if ($ports =~ /:/)
        {
                $left = $`;
                $right = $';
                if (&validport($left) && &validport($right))
                {
                        if ($right > $left) {
                                return 1; }
                }
        }
        return 0;
}

sub validmac
{
	$_ = $_[0];

	if (/^[0-9a-fA-F]{2}[\:\-][0-9a-fA-F]{2}[\:\-][0-9a-fA-F]{2}[\:\-][0-9a-fA-F]{2}[\:\-][0-9a-fA-F]{2}[\:\-][0-9a-fA-F]{2}$/) {
		return 1; }
	return 0;
}

sub validhostname
{
        my $hostname = $_[0];
        my $part;

        if ($hostname eq '') {
                return 0; }
        if (length($hostname) > 255) {
                return 0; }
        @parts = split(/\./, $hostname);
        foreach $part (@parts)
        {
                if (length($part) > 64) {
                        return 0; }
                unless ($part =~ /^[a-zA-Z\d\-]+$/) {
                        return 0; }
                if ($part =~ /^\-/) {
                        return 0; }
                if ($part =~ /\-$/) {
                return 0; }
        }
        return 1;
}

sub basename {
	my ($filename) = @_;
	$filename =~ m!.*/(.*)!;
	if ($1) {
		return $1;
	} else {
		return $filename;
	}
}

sub connectedstate {
	my $locks = scalar(glob("/var/run/ppp-*.pid"));
	my $theconnstate;
	if ( -e "${swroot}/red/active" ) {
		$theconnstate = "connected";
	} elsif ($locks) {
		$theconnstate = "connecting";
	} else {
		$theconnstate = "idle";
	}
	return $theconnstate;
}


1;
