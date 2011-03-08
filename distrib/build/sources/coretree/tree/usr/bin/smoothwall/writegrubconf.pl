#!/usr/bin/perl
#
# Copyright 2005-2010 SmoothWall Ltd

use lib "/usr/lib/smoothwall";
use header qw( :standard );

my %hwprofilesettings;
my %kernelsettings;

&readhash("${swroot}/main/hwprofile", \%hwprofilesettings);
&readhash("${swroot}/main/kernel", \%kernelsettings);

my $append; my $serial;

$append = $hwprofilesettings{'EXTRA_KERNEL_CMDLINE'};

my $file;

open ( $file, "/usr/lib/smoothwall/menu.lst.in" );
my @grub = <$file>;
close ($file);

if ( scalar @ARGV ){
	@specialgrub = <STDIN>;
}

open ( $file, ">/boot/grub/menu.lst" ) or die "Unable to write menu.lst $!";

print $file $serial;

foreach my $line ( @grub ){
	print $file "$line";
}

print $file "default 0\n";

foreach my $line ( @specialgrub ){
	print $file "$line";
}

my $rootdev = $hwprofilesettings{'ROOT_DEV'};

my $kernelpath = '';
if ( not defined $hwprofilesettings{'BOOT_DEV'} ){
	$kernelpath = '/boot';
}

foreach my $kerneltype ('runtime')
{
	print $file "title SmoothWall-$kerneltype\n";

	print $file "kernel ${kernelpath}/vmlinuz-$kernelsettings{'CURRENT'}-${kerneltype} root=$rootdev $append\n";
	print $file "initrd ${kernelpath}/initrd-$kernelsettings{'CURRENT'}-${kerneltype}.gz\n";

	if ($kernelsettings{'OLD'})
	{
		print $file "title SmoothWall-${kerneltype}-OLD\n";
		if ( defined $grubroot and $grubroot ne '' ){
			print $file "root ($grubroot)\n";
		}
		print $file "kernel ${kernelpath}/vmlinuz-$kernelsettings{'OLD'}-${kerneltype} root=$rootdev $append\n";
		print $file "initrd ${kernelpath}/initrd-$kernelsettings{'OLD'}-${kerneltype}.gz\n";
	}
}

close($file);
