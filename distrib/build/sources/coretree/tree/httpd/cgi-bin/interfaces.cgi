#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use smoothtype qw( :standard );

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

use Data::Dumper;
print STDERR Dumper %settings;

	# assign the settings over the top of their earstwhile counterparts.

	$settings{'GREEN_ADDRESS'} = $cgiparams{'GREEN_ADDRESS'} if ( defined $cgiparams{'GREEN_ADDRESS'} );
	$settings{'GREEN_NETMASK'} = $cgiparams{'GREEN_NETMASK'} if ( defined $cgiparams{'GREEN_NETMASK'} );

	$settings{'ORANGE_ADDRESS'} = $cgiparams{'ORANGE_ADDRESS'} if ( defined $cgiparams{'ORANGE_ADDRESS'} );
	$settings{'ORANGE_NETMASK'} = $cgiparams{'ORANGE_NETMASK'} if ( defined $cgiparams{'ORANGE_NETMASK'} );

	$settings{'PURPLE_ADDRESS'} = $cgiparams{'PURPLE_ADDRESS'} if ( defined $cgiparams{'PURPLE_ADDRESS'} );
	$settings{'PURPLE_NETMASK'} = $cgiparams{'PURPLE_NETMASK'} if ( defined $cgiparams{'PURPLE_NETMASK'} );

	$settings{'RED_TYPE'} = $cgiparams{'RED_TYPE'} if ( defined $cgiparams{'RED_TYPE'} );
	$settings{'RED_DHCP_HOSTNAME'} = $cgiparams{'RED_DHCP_HOSTNAME'} if ( defined $cgiparams{'RED_DHCP_HOSTNAME'} );
	$settings{'RED_ADDRESS'} = $cgiparams{'RED_ADDRESS'} if ( defined $cgiparams{'RED_ADDRESS'} );
	$settings{'RED_NETMASK'} = $cgiparams{'RED_NETMASK'} if ( defined $cgiparams{'RED_NETMASK'} );

	$settings{'DEFAULT_GATEWAY'} = $cgiparams{'DEFAULT_GATEWAY'} if ( defined $cgiparams{'DEFAULT_GATEWAY'} );
	$settings{'DNS1'} = $cgiparams{'DNS1'} if ( defined $cgiparams{'DNS1'} );
	$settings{'DNS2'} = $cgiparams{'DNS2'} if ( defined $cgiparams{'DNS2'} );

	# now some sanity checks of the settings we've just tried
	
	if ( not &validip( $settings{'GREEN_ADDRESS'} )){
		$errormessage .= "The IP Address for the Green interface appears to be invalid<br/>";
	}

	if ( not &validmask( $settings{'GREEN_NETMASK'} )){
		$errormessage .= "The Netmask for the Green interface appears to be invalid<br/>";
	}

	( $settings{'GREEN_NETADDRESS'}, $settings{'GREEN_BROADCAST'} ) = &bcast_and_net( $settings{'GREEN_ADDRESS'}, $settings{'GREEN_NETMASK'} );


	if ( defined $settings{'ORANGE_ADDRESS'} and $settings{'ORANGE_ADDRESS'} ne "" ){
		if ( not &validip( $settings{'ORANGE_ADDRESS'} )){
			$errormessage .= "The IP Address for the Orange interface appears to be invalid<br/>";
		} elsif ( not &validmask( $settings{'ORANGE_NETMASK'} )){
			$errormessage .= "The Netmask for the Orange interface appears to be invalid<br/>";
		} else {
			( $settings{'ORANGE_NETADDRESS'}, $settings{'ORANGE_BROADCAST'} ) = &bcast_and_net( $settings{'ORANGE_ADDRESS'}, $settings{'ORANGE_NETMASK'} );
		}
	}


	if ( defined $settings{'PURPLE_ADDRESS'} and $settings{'PURPLE_ADDRESS'} ne "" ){
		if ( not &validip( $settings{'PURPLE_ADDRESS'} )){
			$errormessage .= "The IP Address for the Purple interface appears to be invalid<br/>";
		} elsif ( not &validmask( $settings{'PURPLE_NETMASK'} )){
			$errormessage .= "The Netmask for the Purple interface appears to be invalid<br/>";
		} else {
			( $settings{'PURPLE_NETADDRESS'}, $settings{'PURPLE_BROADCAST'} ) = &bcast_and_net( $settings{'PURPLE_ADDRESS'}, $settings{'PURPLE_NETMASK'} );
		}
	}


	if ( defined $settings{'RED_TYPE'} and $settings{'RED_TYPE'} ne "" ){
		if ( $settings{'RED_TYPE'} eq "STATIC" ){
			if ( not &validip( $settings{'RED_ADDRESS'} )){
				$errormessage .= "The IP Address for the Red interface appears to be invalid<br/>";
			} elsif ( not &validmask( $settings{'RED_NETMASK'} )){
				$errormessage .= "The Netmask for the Red interface appears to be invalid<br/>";
			} elsif ( $settings{'DEFAULT_GATEWAY'} ne "" and not &validmask( $settings{'DEFAULT_GATEWAY'} )){
				$errormessage .= "The Default Gateway appears to be invalid<br/>";
			} elsif ( $settings{'DNS1'} ne "" and not &validmask( $settings{'DNS1'} )){
				$errormessage .= "The Primary DNS appears to be invalid<br/>";
			} elsif ( $settings{'DNS2'} ne "" and not &validmask( $settings{'DNS2'} )){
				$errormessage .= "The Secondary DNS appears to be invalid<br/>";
			} else {
				if ( (not defined $settings{'DNS1'} or $settings{'DNS1'} eq "") and ( defined $settings{'DNS2'} and $settings{'DNS2'} ne "" ) ){
					$errormessage .= "The Primary DNS address should be set before specifying a Secondary DNS";
				} else {
					( $settings{'RED_NETADDRESS'}, $settings{'RED_BROADCAST'} ) = &bcast_and_net( $settings{'RED_ADDRESS'}, $settings{'RED_NETMASK'} );
				}
			}
		}
	}

	if ( $errormessage eq "" ){
		&writehash( $settingsfile, \%settings );
	}



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

# if red is on an etherNet, if so we can show some configuration options for it.
&display_red_interface( \%settings );



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

	return if ($interface !~ /eth[0123]/ );

	my $ifconfig_details = `/sbin/ifconfig $interface`;

	$ifconfig_details =~s/\n//mg;
	my ( $macaddress, $currentip, $currentbcast, $currentmask, $status, $currentmtu, $currentmetric, $rx, $tx, $hwaddress ) = ( $ifconfig_details =~ /.*HWaddr\s+(..:..:..:..:..:..).*inet\s+addr:(\d+\.\d+\.\d+\.\d+)\s+Bcast:(\d+\.\d+\.\d+\.\d+)\s+Mask:(\d+\.\d+\.\d+\.\d+)\s+([^\s]+)\s+.*MTU:(\d+)\s+Metric:(\d+).*RX bytes:(\d+\s+\([^\)]*\))\s+TX bytes:(\d+\s+\([^\)]*\)).*(Interrupt.*)/i );

	&openbox(${prefix});

	print qq{
		<table style='width: 100%;'>
		<tr>
			<td style='wdith: 25%;'>Physical Interface:</td>
			<td>$interface</td>
			<td>IP Address:</td>
			<td><input type='text' name='${prefix}_ADDRESS' value='$settings{"${prefix}_ADDRESS"}'></td>
		</tr>
		<tr>
			<td>Device:</td>
			<td>$settings{"${prefix}_DISPLAYDRIVER"}</td>
			<td>Netmask:</td>
			<td><input type='text'  name='${prefix}_NETMASK' value='$settings{"${prefix}_NETMASK"}'></td>
		</tr>
		<tr>
			<td>MAC Address:</td><td>$macaddress</td>
			<td>&nbsp;</td>
			<td>&nbsp;</td>
		</tr>
		</table>
	};

	&closebox();

	return;
}

sub display_red_interface
{
	my ( $settings ) = @_;

	my $interface = $settings{"RED_DEV"};

	return if ($interface !~ /eth[0123]/ );

	my $ifconfig_details = `/sbin/ifconfig $interface`;

	$ifconfig_details =~s/\n//mg;
	my ( $macaddress, $currentip, $currentbcast, $currentmask, $status, $currentmtu, $currentmetric, $rx, $tx, $hwaddress ) = ( $ifconfig_details =~ /.*HWaddr\s+(..:..:..:..:..:..).*inet\s+addr:(\d+\.\d+\.\d+\.\d+)\s+Bcast:(\d+\.\d+\.\d+\.\d+)\s+Mask:(\d+\.\d+\.\d+\.\d+)\s+([^\s]+)\s+.*MTU:(\d+)\s+Metric:(\d+).*RX bytes:(\d+\s+\([^\)]*\))\s+TX bytes:(\d+\s+\([^\)]*\)).*(Interrupt.*)/i );

	&openbox("RED");

	my %selected;
	$selected{$settings{'RED_TYPE'}} = " selected";


	print qq{
		<table style='width: 100%;'>
		<tr>
			<td style='width: 25%;'>Physical Interface:</td>
			<td style='width: 25%;'>$interface</td>
			<td style='width: 25%;'>Connection Method:</td>
			<td style='width: 25%;'>
			<script>
function optify( field )
{
	var inputval = document.getElementById(field).value;
	if ( inputval == 'DHCP' ){
		_enable('hostname');
		_disable('ipaddress');
		_disable('netmask');
		_disable('gateway');
		_disable('primary');
		_disable('secondary');
	} else if ( inputval == 'STATIC' ){
		_disable('hostname');
		_enable('ipaddress');
		_enable('netmask');
		_enable('gateway');
		_enable('primary');
		_enable('secondary');
	} else if ( inputval == 'PPPOE' ){
		_disable('hostname');
		_disable('ipaddress');
		_disable('netmask');
		_disable('gateway');
		_disable('primary');
		_disable('secondary');
	}
}
			</script>
			<select name='RED_TYPE' id='type' onChange="optify('type');">
				<option value='STATIC' $selected{'STATIC'}>Static</option>
				<option value='DHCP'   $selected{'DHCP'}>DHCP</option>
				<option value='PPPOE'  $selected{'PPPOE'}>PPPOE</option>
			</select>
			</td>

		</tr>
		<tr>
			<td>Device:</td>
			<td>$settings{"RED_DISPLAYDRIVER"}</td>
			<td>DHCP Hostname</td>
			<td><input type='text' id='hostname' name='RED_DHCP_HOSTNAME' value='$settings{'RED_DHCP_HOSTNAME'}'></td>
		</tr>
		<tr>
			<td>MAC Address:</td>
			<td>$macaddress</td>
			<td>IP Address:</td>
			<td><input id='ipaddress'  @{[jsvalidip('ipaddress')]}  type='text' name='RED_ADDRESS' value='$settings{"RED_ADDRESS"}'></td>
		</tr>
		<tr>
			<td></td>
			<td></td>
			<td>Netmask:</td><td><input id='netmask' type='text'  @{[jsvalidip('netmask')]}  name='RED_NETMASK' value='$settings{"RED_NETMASK"}'></td>
		</tr>
		</table>
	};

	&closebox();

	&openbox("DNS and Gateway settings:");

	print qq{
		<table style='width: 100%;'>
		<tr>
			<td style='width: 25%;'>Default Gateway:</td>
			<td style='width: 25%;'><input id='gateway'  @{[jsvalidip('gateway','true')]}  type='text' name='DEFAULT_GATEWAY' value='$settings{"DEFAULT_GATEWAY"}'></td>
			<td style='width: 25%;'>Primary DNS:</td>
			<td style='width: 25%;'><input id='primary'  @{[jsvalidip('primary','true')]}  type='text' name='DNS1' value='$settings{"DNS1"}'></td>
		</tr>
		<tr>
			<td></td>
			<td></td>
			<td>Secondary DNS:</td>
			<td style='width: 25%;'><input id='secondary'  @{[jsvalidip('secondary','true')]}  type='text' name='DNS2' value='$settings{"DNS2"}'></td>
		</tr>
		</table>
	};

	&closebox();

	push @_validation_items, "optify('type')" ;

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






