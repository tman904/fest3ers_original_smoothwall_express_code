#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );

my (%cgiparams,%selected,%checked);
my $config = "${swroot}/outbound/config";
my $settings = "${swroot}/outbound/settings";
my $ethSetFile = "${swroot}/ethernet/settings";

my $errormessage = '';

&showhttpheaders();

&getcgihash(\%cgiparams);

# Load inbound interfaces into %interfaces (excluding RED)
my %interfaces;
open(ETHSET, $ethSetFile) or die 'Unable to open ethernet settings.';
while(<ETHSET>) {
	if($_ =~ m/(\S+)_DEV=(\S+)/) {
		if(!($1 eq 'RED')) {
			$interfaces{$1} = $2;
		}
	}
}

# Load Configuration
my $configChanged = 0;
my @portRules = ();
if(open(FILE, $config)) {
	while(<FILE>) {
		chomp;
		push(@portRules, $_);
	}
} else {
	$configChanged++;
	# generate default config
}

# Load Settings
my $settingsChanged = 0;
my %interfaceRules;
if(open(FILE, $settings)) {
	while(<FILE>) {
		chomp;
		my @tempInterface = split(',', $_);
		@{ $interfaceRules{$tempInterface[0]} } = @tempInterface[1..$#tempInterface];
	}
} else {
	# generate default settings
	foreach $interface (keys %interfaces) {
		@{ $interfaceRules{$interface} } = ( 
			$interfaces{$interface},
			"off" );
	}
	$settingsChanged++;
}

# Save enables and disabled the outbound filtering service
if ($cgiparams{'ACTION'} eq $tr{'save'}) {
	foreach $interface (keys %interfaces) {
		if($cgiparams{"ENABLE$interface"} eq 'on') {
			@{ $interfaceRules{$interface} }[1] = 'on';
		} else {
			@{ $interfaceRules{$interface} }[1] = 'off';
		}
	}
	$settingsChanged++;
}

# Add a new allowed port
if ($cgiparams{'ACTION'} eq $tr{'add'}) {
	my $port;
	if(defined $cgiparams{'DEST_PORT'}) {
		$port = $cgiparams{'DEST_PORT'};
		if(!validportrange($port)) {
			$errormessage = $tr{'invalid port or range'};
		}
	}
	unless($errormessage) {
		if (defined $interfaces{$cgiparams{'INTERFACE'}}) {
			my $ruleEnable;
			if($cgiparams{'RULEENABLED'} eq 'on') {
				$ruleEnable = 'on';
			} else {
				$ruleEnable = 'off';
			}
			
			push(@portRules, "$cgiparams{'INTERFACE'},$cgiparams{'PROTOCOL'},$cgiparams{'DEST_PORT'},$ruleEnable");
			$configChanged++;
			&log($tr{'outbound rule added to '} . $cgiparams{'INTERFACE'});
		}
	}
}

$cgiparams{'INTERFACE'} = '';
$cgiparams{'PROTOCOL'} = '';
$cgiparams{'DEST_PORT'} = '';
$cgiparams{'RULEENABLED'} = '';

if ($cgiparams{'ACTION'} eq $tr{'remove'} || $cgiparams{'ACTION'} eq $tr{'edit'}) {
	my $id = 1;
	my $count = 0;
	foreach $line (@portRules) {
		if($cgiparams{$id} eq 'on') {
			$count++;
		}
		$id++;
	}
	
	if ($count == 0) {
		$errormessage = $tr{'nothing selected'};
	} elsif ($count > 1 && $cgiparams{'ACTION'} eq $tr{'edit'}) {
		$errormessage = $tr{'you can only select one item to edit'};
	}
	
	unless ($errormessage) {
		my $id = 1;
		my @newRules;
 		foreach $line (@portRules) {
			my @temp = split(',',$line);
			if($cgiparams{"$id"} eq 'on') {	
				if($cgiparams{'ACTION'} eq $tr{'edit'}) {
					$cgiparams{'INTERFACE'} = $temp[0];
					$cgiparams{'PROTOCOL'} = $temp[1];
					$cgiparams{'DEST_PORT'} = $temp[2];
					$cgiparams{'RULEENABLED'} = $temp[3];
				}
				&log($tr{'outbound rule removed from '} . $temp[0]);
			} else {
				push(@newRules, $line);
			}
			$id++;
		}
		@portRules = @newRules;

		$configChanged++;
	}
}

$selected{'INTERFACE'}{'ORANGE'} = '';
$selected{'INTERFACE'}{'PURPLE'} = '';
$selected{'INTERFACE'}{'GREEN'} = '';
$selected{'INTERFACE'}{$cgiparams{'INTERFACE'}} = 'SELECTED';

$selected{'PROTOCOL'}{'TCP'} = '';
$selected{'PROTOCOL'}{'UDP'} = '';
$selected{'PROTOCOL'}{$cgiparams{'PROTOCOL'}} = 'SELECTED';

$checked{'RULEENABLED'}{'off'} = '';
$checked{'RULEENABLED'}{'on'} = '';
$checked{'RULEENABLED'}{$cgiparams{'RULEENABLED'}} = 'CHECKED';

&openpage($tr{'outbound filtering'}, 1, '', 'networking');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage);

print "<FORM METHOD='POST'>\n";

&openbox($tr{'filtered interfaces'} . ':');
print '<table style=\'width: 100%;\'>' . "\n";
print '<tr>' . "\n";

my $unused = 6;
my $width = 90 / $unused;
foreach $interface (keys(%interfaces)) {
	print "<td style='width: $width%;'>" . $interface . ':</td>';
	print "<td style='width: $width%;'><input type=\"checkbox\" name=\"ENABLE" . $interface . '"';
	if(@{ $interfaceRules{$interface} }[1] eq 'on') { print " CHECKED"; }
	print '></td>' . "\n";
	$unused -= 2;
}
print "<td style='width: $width%;'>&nbsp;</td>\n"x$unused;

print '<td><input type="submit" name="ACTION" value="' . "$tr{'save'}" . '"></td></tr>' . "\n";
print '</table>' . "\n";

&closebox();

&openbox($tr{'add a new rule'});
print <<END
<table style='width: 100%;'>
<tr>
	<td style='width: 15%;'>
		$tr{'interface'}:
	</td>
	<td style='width: 15%;'>
		<select name='INTERFACE'>
END
;
foreach my $colour (sort keys %interfaces) {
	print "<option value='$colour'>$colour</option>\n";
}

print <<END
		</select>
	</td>

	<td style='width: 15%;'>
		$tr{'protocol'}:
	</td>
	<td style='width: 15%;'>
		<select name='PROTOCOL'>
			<option value='TCP'>TCP</option>
			<option value='UDP'>UDP</option>
		</select>
	</td>


	<td style='width: 15%;'>
		$tr{'destination portc'}
	</td>

	<td style='width: 20%;'>
		<input type='text' name='DEST_PORT' value='$cgiparams{'DEST_PORT'}' size='6'>
	</td>
	</tr>
</table>

<table style='width: 100%;'>
	<tr>
	<td class='base' width='50%' align='center'>$tr{'enabled'}<input type='CHECKBOX' name='RULEENABLED' $checked{'RULEENABLED'}{'on'}></td>
	<td width='50%' align='center'><input type='submit' name='ACTION' value='$tr{'add'}'></td>
	</tr>
</table>
END
;
&closebox();

&openbox($tr{'current rules'});
print <<END
<table class='centered'>
<tr>
	<th style='width: 25%;'>$tr{'interface'}</th>
	<th style='width: 25%;'>$tr{'protocol'}</th>
	<th style='width: 25%;'>$tr{'destination port'}</th>
	<th style='width: 15%;'>$tr{'enabledtitle'}</th>
	<th style='width: 10%;'>$tr{'mark'}</th>
</tr>
END
;

my $id = 0;
foreach $line (@portRules) {
	$id++;
	my @temp = split(',', $line);
	
	$interface = $temp[0];
	$protocol = $temp[1];
	$destport = $temp[2];

	if ($id % 2) {
		print "<tr class='dark'>\n";
	} else {
              	print "<tr class='light'>\n";
	}
	
	if ($temp[3] eq 'on') {
		$gif = 'on.gif';
	} else {
		$gif = 'off.gif';
	}
	print <<END
	<td align='center'>$interface</td>
	<td align='center'>$protocol</td>
	<td align='center'>$destport</td>
	<td align='center'><img src='/ui/img/$gif'></td>
	<td align='center'><input type='checkbox' name='$id'></td>
	</tr>
END
;
}

print <<END
</table>
<table class='blank'>
<tr>
	<td style='width: 50%; text-align: center;'><input type='submit' name='ACTION' value='$tr{'remove'}'></td>
	<td style='width: 50%; text-align: center;'><input type='submit' name='ACTION' value='$tr{'edit'}'></td>
</tr>
</table>
END
;

# Write out configuration
if($configChanged > 0) {
	if(open(FILE, ">$config")) {
		foreach $line (@portRules) {
			print FILE "$line\n";
		}
		close(FILE);
	} else {
		die 'Unable to write out config.';
	}
}

# Write out settings
if($settingsChanged > 0) {
	if(open(FILE, ">$settings")) {
		foreach $interface (keys %interfaces) {
			print FILE "$interface,";
			print FILE join(',',@{ $interfaceRules{$interface} });
			print FILE "\n";
		}
	} else {
		die 'Unable to write out settings.';
	}
}	

if(($configChanged > 0) || ($settingsChanged > 0)) {
	system('/usr/bin/setuids/setoutbound');
}

&closebox();
&alertbox('add','add');
&closebigbox();
&closepage();

