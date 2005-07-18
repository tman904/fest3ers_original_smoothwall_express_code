#!/usr/bin/perl

require "/var/smoothwall/header.pl";

my (%eth,%isdn,%pppsettings);

&readhash("${swroot}/ethernet/settings", \%eth);
&readhash("${swroot}/isdn/settings", \%isdn);
&readhash("${swroot}/ppp/settings", \%pppsettings);
&readhash("${swroot}/adsl/settings", \%adslsettings);

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

my $extra = "ADSL_DEVICE=$adslsettings{'DEVICE'},ADSL_ECITYPE=$adslsettings{'ECITYPE'},ISDN_TYPE=$isdnsettings{'TYPE'}";
my $info = "cpu_vid=$vid&cpu_model=$model&cpu_mhz=$mhz&mem=$mem&hdd=$disk&inst_type=$eth{'CONFIG_TYPE'}&isdn=$pppsettings{'COMPORT'}&version=$version-$revision&extra=$extra";
$info =~ s/\s//g;
my $length = length($info);
my $xhost = "www.smoothwall.org";

use IO::Socket;
$sock = new IO::Socket::INET ( PeerAddr => $xhost, PeerPort => 80, Proto => 'tcp', Timeout => 5 ) or die "Could not connect to host\n\n";
print $sock "GET http://www.smoothwall.org/cgi-bin/machine_reg.cgi?$info HTTP/1.1\n";
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
