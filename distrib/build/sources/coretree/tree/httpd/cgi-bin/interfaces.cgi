#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );

use Socket;

my (%cgiparams,%selected,%checked);
my $errormessage = '';

&showhttpheaders();
&getcgihash(\%cgiparams);

# load settings .

my $settingsfile = "/var/smoothwall/ethernet/settings";
my %settings;
&readhash( $settingsfile, \%settings );

# Action a "Save" request ...

if ( defined $cgiparams{'ACTION'} and $cgiparams{'ACTION'} eq $tr{'save'} ){
	# assign the settings over the top of their earstwhile counterparts.

	$settings{'GREEN_ADDRESS'} = $cgiparams{'GREEN_ADDRESS'} if ( defined $cgiparams{'GREEN_ADDRESS'} );
	$settings{'GREEN_NETMASK'} = $cgiparams{'GREEN_NETMASK'} if ( defined $cgiparams{'GREEN_NETMASK'} );
	$settings{'GREEN_MTU'}     = $cgiparams{'GREEN_MTU'}     if ( defined $cgiparams{'GREEN_MTU'} );

	$settings{'ORANGE_ADDRESS'} = $cgiparams{'ORANGE_ADDRESS'} if ( defined $cgiparams{'ORANGE_ADDRESS'} );
	$settings{'ORANGE_NETMASK'} = $cgiparams{'ORANGE_NETMASK'} if ( defined $cgiparams{'ORANGE_NETMASK'} );
	$settings{'ORANGE_MTU'}     = $cgiparams{'ORANGE_MTU'}     if ( defined $cgiparams{'ORANGE_MTU'} );

	$settings{'PURPLE_ADDRESS'} = $cgiparams{'PURPLE_ADDRESS'} if ( defined $cgiparams{'PURPLE_ADDRESS'} );
	$settings{'PURPLE_NETMASK'} = $cgiparams{'PURPLE_NETMASK'} if ( defined $cgiparams{'PURPLE_NETMASK'} );
	$settings{'PURPLE_MTU'}     = $cgiparams{'PURPLE_MTU'}     if ( defined $cgiparams{'PURPLE_MTU'} );

	# now some sanity checks of the settings we've just tried
	
	if ( not &validip( $settings{'GREEN_ADDRESS'} )){
		$errormessage .= "The IP Address for the Green interface appears to be invalid<br/>";
	}

	if ( not &validip( $settings{'ORANGE_ADDRESS'} )){
		$errormessage .= "The IP Address for the Orange interface appears to be invalid<br/>";
	}

	if ( not &validip( $settings{'PURPLE_ADDRESS'} )){
		$errormessage .= "The IP Address for the Purple interface appears to be invalid<br/>";
	}

	if ( not &validmask( $settings{'GREEN_NETMASK'} )){
		$errormessage .= "The Netmask for the Green interface appears to be invalid<br/>";
	}

	if ( not &validmask( $settings{'ORANGE_NETMASK'} )){
		$errormessage .= "The Netmask for the Orange interface appears to be invalid<br/>";
	}

	if ( not &validmask( $settings{'PURPLE_NETMASK'} )){
		$errormessage .= "The Netmask for the Purple interface appears to be invalid<br/>";
	}

	unless ( $settings{'GREEN_MTU'} =~ /\d{1,4}/ and $settings{'GREEN_MTU'} > 68 and $settings{'GREEN_MTU'} > 65536 ){
		$errormessage .= "The MTU for the Green interface appears to be invalid<br/>";
	}

	unless ( not defined $settings{'ORANGE_MTU'} or ( $settings{'ORANGE_MTU'} =~ /\d{1,4}/ and $settings{'ORANGE_MTU'} > 68 and $settings{'ORANGE_MTU'} > 65536 ) ){
		$errormessage .= "The MTU for the Orange interface appears to be invalid<br/>";
	}

	unless ( not defined $settings{'PURPLE_MTU'} or ( $settings{'PURPLE_MTU'} =~ /\d{1,4}/ and $settings{'PURPLE_MTU'} > 68 and $settings{'PURPLE_MTU'} > 65536 ) ){
		$errormessage .= "The MTU for the Purplee interface appears to be invalid<br/>";
	}


	# determine the correct broadcast and net addresses for the above interfaces.
	
	( $settings{'GREEN_NETADDRESS'}, $settings{'GREEN_BROADCAST'} ) = &bcast_and_net( $settings{'GREEN_ADDRESS'}, $settings{'GREEN_NETMASK'} );
	( $settings{'ORANGE_NETADDRESS'}, $settings{'ORANGE_BROADCAST'} ) = &bcast_and_net( $settings{'ORANGE_ADDRESS'}, $settings{'ORANGE_NETMASK'} );
	( $settings{'PURPLE_NETADDRESS'}, $settings{'PURPLE_BROADCAST'} ) = &bcast_and_net( $settings{'PURPLE_ADDRESS'}, $settings{'PURPLE_NETMASK'} );


}

&openpage($tr{'interfaces configuration'}, 1, '', 'networking');
&openbigbox('100%', 'LEFT');

&alertbox($errormessage);

print "<form method='post'>";

# deal with the green settings.
&display_interface( \%settings, 'GREEN' );

# deal with the green settings.
&display_interface( \%settings, 'ORANGE' );

# deal with the green settings.
&display_interface( \%settings, 'PURPLE' );

print qq{
	<div style='text-align: center;'><input type='submit' name='ACTION' value='$tr{'save'}'></div>
	</form>
};


&alertbox('add','add');

&closebigbox();

&closepage();


sub display_interface
{
	my ( $settings, $prefix ) = @_;

	my $interface = $settings{"${prefix}_DEV"};

	print STDERR "Intergface $interface\n";
	return if ($interface !~ /eth[0123]/ );

	my $ifconfig_details = `/sbin/ifconfig $interface`;

	$ifconfig_details =~s/\n//mg;
	my ( $macaddress, $currentip, $currentbcast, $currentmask, $status, $currentmtu, $currentmetric, $rx, $tx, $hwaddress ) = ( $ifconfig_details =~ /.*HWaddr\s+(..:..:..:..:..:..).*inet\s+addr:(\d+\.\d+\.\d+\.\d+)\s+Bcast:(\d+\.\d+\.\d+\.\d+)\s+Mask:(\d+\.\d+\.\d+\.\d+)\s+([^\s]+)\s+.*MTU:(\d+)\s+Metric:(\d+).*RX bytes:(\d+\s+\([^\)]*\))\s+TX bytes:(\d+\s+\([^\)]*\)).*(Interrupt.*)/i );

	&openbox($tr{'current rules'});

	print qq{
		<table>
		<tr>
			<td>Physical Interface:</td><td>$interface</td>
			<td>&nbsp;</td>
			<td>&nbsp;</td>
		</tr>
		<tr>
			<td>Device:</td><td>$settings{"${prefix}_DISPLAYDRIVER"} - $hwaddress</td>
			<td>&nbsp;</td>
			<td>&nbsp;</td>
		</tr>
		<tr>
			<td>MAC Address:</td><td>$macaddress</td>
			<td>&nbsp;</td>
			<td>IP Address:</td><td><input type='text' name='${prefix}_ADDRESS' value='$settings{"${prefix}_ADDRESS"}'></td>
		</tr>
		<tr>
			<td>Sent:</td><td>$tx</td>
			<td>&nbsp;</td>
			<td>Netmask:</td><td><input type='text'  name='${prefix}_NETMASK' value='$settings{"${prefix}_NETMASK"}'></td>
		</tr>
		<tr>
			<td>Received:</td><td>$rx</td>
			<td>&nbsp;</td>
			<td>MTU:</td><td><input type='text' name='${prefix}_MTU' value='$settings{"${prefix}_MTU"}'></td>
		</tr>
		</table>
	};

	&closebox();

	return;
}


sub bcast_and_net
{
	my ( $address, $netmask ) = @_;

	my $addressint = inet_aton($address);
        my $netmaskint = inet_aton($netmask);

	my $netaddressint = $addressint & $netmaskint;

	my $netaddress = inet_ntoa($netaddressint);
	my $broadcast  = inet_ntoa($netaddressint | ~$netmaskint);

	return ( $netaddress, $broadcast );
}






