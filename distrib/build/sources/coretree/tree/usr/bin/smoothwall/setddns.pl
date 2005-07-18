#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

close(STDIN);
close(STDOUT);
close(STDERR);

require '/var/smoothwall/header.pl';

my %settings;
my %noipsettings;
my $filename = "${swroot}/ddns/config";
my $cachefile = "${swroot}/ddns/ipcache";
my $ipcache = 0;

open(FILE, "$filename") or die 'Unable to open config file.';
my @current = <FILE>;
close(FILE);
my $lines = $#current + 1;
unless($lines) { exit 0; }

open(IP, "${swroot}/red/local-ipaddress") or die 'Unable to open local-ipaddress file.';
my $ip = <IP>;
close(IP);
chomp $ip;

if ($ARGV[0] ne '-f')
{
	open(IPCACHE, "$cachefile");
	$ipcache = <IPCACHE>;
	close(IPCACHE);
	chomp $ipcache;
}

if ($ip ne $ipcache)
{
	my $id = 0;
	my $success = 0;
	my $line;

	foreach $line (@current)
	{
		$id++;
		chomp($line);
		my @temp = split(/\,/,$line);
		unless ($temp[7] eq "off")
		{
			$settings{'SERVICE'} = $temp[0];
			$settings{'HOSTNAME'} = $temp[1];
			$settings{'DOMAIN'} = $temp[2];
			$settings{'PROXY'} = $temp[3];
			$settings{'WILDCARDS'} = $temp[4];
			$settings{'LOGIN'} = $temp[5];
			$settings{'PASSWORD'} = $temp[6];
			$settings{'ENABLED'} = $temp[7];
			my @service = split(/\./, "$settings{'SERVICE'}");
			$settings{'SERVICE'} = "$service[0]";
			if ($settings{'SERVICE'} eq 'no-ip')
			{
				$noipsettings{'LOGIN'} = $settings{'LOGIN'};
				$noipsettings{'PASSWORD'} = $settings{'PASSWORD'};
				$noipsettings{'HOSTNAME'} = $settings{'HOSTNAME'};
				$noipsettings{'DOMAIN'} = $settings{'DOMAIN'};
				$noipsettings{'DAEMON'} = 'N';
				$noipsettings{'DEVICE'} = '';
				$noipsettings{'INTERVAL'} = '1';
				$noipsettings{'NAT'} = 'N';
				$noipsettings{'GROUP'} = ';';
				if ($settings{'PROXY'} eq 'on') { $noipsettings{'PROXY'} = 'Y'; }
				else { $noipsettings{'PROXY'} = 'N'; }

				&writehash("${swroot}/ddns/noipsettings", \%noipsettings);
				open(F, "${swroot}/ddns/noipsettings");
				my @unsorted = <F>;
				close(F);
				my @sorted = sort { $b cmp $a } @unsorted;
				open(F, ">${swroot}/ddns/noipsettings");
				flock F, 2;
				print F @sorted;
				close(F);

				my @ddnscommand = ('/usr/local/bin/noip','-c',"${swroot}/ddns/noipsettings",'-i',"$ip");

				my $result = system(@ddnscommand);

				if ( $result != 0) { &log("Dynamic DNS ip-update for $settings{'HOSTNAME'}.$settings{'DOMAIN'}: failure"); }
				else 
				{
					&log("Dynamic DNS ip-update for $settings{'HOSTNAME'}.$settings{'DOMAIN'}: success");
					$success++;
				}
			}
		   	elsif ($settings{'SERVICE'} eq 'dyndns-custom')
			{
				if ($settings{'WILDCARDS'} eq 'on') {$settings{'WILDCARDS'} = '-w';}
				else {$settings{'WILDCARDS'} = '';}
				my @ddnscommand = ('/usr/local/bin/addns.pl', "--username=$settings{'LOGIN'}", "--password=$settings{'PASSWORD'}", "--host=$settings{'HOSTNAME'}.$settings{'DOMAIN'}", "--system=custom", "--interface=eth1", "--method-iface", "--wildcard=$settings{'WILDCARDS'}");

				my $result = system(@ddnscommand);
				$result >>= 8;
				if ( $result == 1) { &log("Dynamic DNS addns for $settings{'HOSTNAME'}.$settings{'DOMAIN'}: Already set"); }
				elsif ( $result != 0) { &log("Dynamic DNS addns for $settings{'HOSTNAME'}.$settings{'DOMAIN'}: failure $result"); }
				else
				{
					&log("Dynamic DNS addns for $settings{'HOSTNAME'}.$settings{'DOMAIN'}: success");
					$success++;
				}
			}
			else
			{
				if ($settings{'WILDCARDS'} eq 'on') {$settings{'WILDCARDS'} = '-w';}
				else {$settings{'WILDCARDS'} = '';}
				my @ddnscommand = ('/usr/local/bin/ez-ipupdate', '-a', "$ip", '-S', "$settings{'SERVICE'}", '-u', "$settings{'LOGIN'}:$settings{'PASSWORD'}", '-h', "$settings{'HOSTNAME'}.$settings{'DOMAIN'}", "$settings{'WILDCARDS'}", '-q');

				my $result = system(@ddnscommand);
				if ( $result != 0) { &log("Dynamic DNS ip-update for $settings{'HOSTNAME'}.$settings{'DOMAIN'}: failure"); }
				else
				{
					&log("Dynamic DNS ip-update for $settings{'HOSTNAME'}.$settings{'DOMAIN'}: success");
					$success++;
				}
			}
		}
		else {
			$success++; }

	}

	if ($lines == $success)
	{
		open(IPCACHE, ">$cachefile");
		flock IPCACHE, 2;
		print IPCACHE $ip;
		close(IPCACHE);
	}
}

else { &log('Dyanmic DNS ip-update: your IP is already up-to-date'); }
