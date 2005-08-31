#!/usr/bin/perl

use lib "/usr/lib/smoothwall";
use header qw( :standard );

my (%eth,%isdn,%pppsettings);

# detail connection details, this is how the smoothie connects to the
# outside world.  We have no interest in passwords or anything of that
# ilk of course, but knowing modem types and drivers is always good
# for support purposes.

# determine the Ethernet Settings

&readhash("${swroot}/ethernet/settings", \%eth);

# And the ISDN Settings (if enabled)

&readhash("${swroot}/isdn/settings", \%isdn);

# PPP Settings

&readhash("${swroot}/ppp/settings", \%pppsettings);

# ADSL Settings

&readhash("${swroot}/adsl/settings", \%adslsettings);

# Retrieve details about the CPU, again this is for general purpose
# information about what to support (can we finally drop i386 support
# and turn on some optimisations ? )

open(CPU, "/proc/cpuinfo") or die "Could not open /proc/cpuinfo";
my ($junk,$mhz,$model,$vid);
while(<CPU>)
{
	if($_ =~ m/^cpu MH/) { ($junk,$mhz) = split(/\:/,$_,-1); }
	if($_ =~ m/^vendor_id/) { ($junk,$vid) = split(/\:/,$_,-1); }
	if($_ =~ m/^model\sna/) { ($junk,$model) = split(/\:/,$_,-1); }
}
close(CPU);

$mhz =~ s/^\s+//;
$mhz =~ s/\s+$//;
$vid =~ s/^\s+//;
$vid =~ s/\s+$//;
$model =~ s/^\s+//;
$model =~ s/\s+$//;

# Detail memory use and amounts on the machine.

open(MEM, "/proc/meminfo") or die "Could not open /proc/meminfo";
my ($lp);
while(<MEM>)
{
	if($_ =~ m/^MemTotal/) { ($junk,$lp) = split(/\:/,$_,-1); }
}
close(MEM);
$lp =~ s/^\s+//;
$lp =~ s/\s+$//;
my $mem;
($mem,$junk) = split(/\s/,$lp);

# Partitioning information, should we start worrying about logging
# and come up with new methods of storing it etc..

open(DISK, "/proc/partitions") or die "Could not open /proc/partitions";
my (@this,$disk);
while(<DISK>)
{
	my @test = split(/\s/,$_,-1);
	undef @this;
	my $item;	
	foreach $item (@test)
	{
		unless($item eq "") { push(@this,$item); }
		if($this[3] eq "hda") { $disk = $this[2]; }
	}
}
close(DISK);

# discover some LSPCI information, this will give us an indication of the sort
# of hardware we're coming up against and the sort of drivers we need to 
# support.
my $lspci;

open(PIPE, '-|') || exec( '/usr/sbin/lspci' );
while ( my $line = <PIPE>) { 
	chomp $line;
	my ( $busid, $type, $name ) = ( $line =~ /([^\s]+)\s+([^:]+):\s+(.*)/ );
	$lspci .= "$busid|$type|$name||";
}
close(PIPE);

# discover various bits of information about the modules which are loaded
# this will give some hint as to how well the driver discovery code is working
# amongst other things.

my $lsmod;

open(PIPE, '-|') || exec( '/bin/lsmod' );
while ( my $line = <PIPE>) { 
	chomp $line;
	my ( $driver, $size, $usedby ) = ( $line =~ /([^\s]+)\s+([^\s]+)\s+(.*)/ );
	$lsmod .= "$driver|$size|$usedby||";
}
close(PIPE);

# discover various interesting things about the USB Bus, this is in a 
# perpetual state of flux and a widish range of details can only serve
# to make sense of some of it.

my $usbbus;

if (open(USB, "/proc/bus/usb/devices"))
{
	while( my $line = <USB>)
	{
		chomp $line;
		$line =~s/#//g;
		$usbbus .= "$line|";
	}
	close(USB);
}

# construct the additional information.

my $extra;

$extra .= "ADSL_DEVICE=$adslsettings{'DEVICE'}&";
$extra .= "ADSL_ECITYPE=$adslsettings{'ECITYPE'}&";
$extra .= "ISDN_TYPE=$isdnsettings{'TYPE'}&";
$extra .= "LSMOD=$lsmod&";
$extra .= "LSPCI=$lspci&";
$extra .= "USBBUS=$usbbus";

my $info = "cpu_vid=$vid&cpu_model=$model&cpu_mhz=$mhz&mem=$mem&hdd=$disk&inst_type=$eth{'CONFIG_TYPE'}&isdn=$pppsettings{'COMPORT'}&version=$version-$revision$extra";
$info =~ s/\s/%20/g;

my $length = length($info);
my $xhost = "www.smoothwall.org";

use IO::Socket;
$sock = new IO::Socket::INET ( PeerAddr => $xhost, PeerPort => 80, Proto => 'tcp', Timeout => 5 ) or die "Could not connect to host\n\n";
print $sock "GET http://www.smoothwall.org/cgi-bin/express3.cgi?$info HTTP/1.1\n";
print $sock "Host: www.smoothwall.org\n\n";
undef $/;
$retsrt = <$sock>;
close $sock;

@page = split(/\n/,$retsrt,-1);
$found = 0;
foreach(@page)
{
	if($_ =~ m/^status/)
	{
		@temp = split(/\=/,$_,2);
		$found = 1;
	}
}

if ($found == 1)
{
	if ($temp[1] =~ /^success/) {
		exit 0; }
	else {
		exit 1; }
}
else {
	exit 2; }
