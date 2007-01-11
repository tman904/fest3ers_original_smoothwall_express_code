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

my (%cgiparams,%selected,%checked);
my $config = "${swroot}/outbound/config";
my $settings = "${swroot}/outbound/settings";
my $machinesettings = "${swroot}/outbound/machines";
my $ethSetFile = "${swroot}/ethernet/settings";

my $errormessage = '';

&showhttpheaders();

$cgiparams{'COLUMN'} = 1;
$cgiparams{'ORDER'} = $tr{'log ascending'};

&getcgihash(\%cgiparams);

$cgiparams{'RULEENABLED'} = 'on'     if ( not defined $cgiparams{'ACTION'} );
$cgiparams{'MACHINEENABLED'} = 'on'  if ( not defined $cgiparams{'MACHINEACTION'} );

use Data::Dumper;
print STDERR Dumper %cgiparams;

if ($ENV{'QUERY_STRING'} && ( not defined $cgiparams{'ACTION'} or $cgiparams{'ACTION'} eq "" ))
{
        my @temp = split(',',$ENV{'QUERY_STRING'});
        $cgiparams{'ORDER'}  = $temp[1] if ( defined $temp[ 1 ] and $temp[ 1 ] ne "" );
        $cgiparams{'COLUMN'} = $temp[0] if ( defined $temp[ 0 ] and $temp[ 0 ] ne "" );
}

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

my %settings;

&readhash("$config", \%settings);

my %selected;
$selected{"GREEN$settings{'GREEN'}"} = " selected ";
$selected{"ORANGE$settings{'ORANGE'}"} = " selected ";
$selected{"PURPLE$settings{'PURPLE'}"} = " selected ";

my %checked;
$checked{'on'} = " checked ";

# Save the settings as is required.

if ( defined $cgiparams{'ACTION'} and $cgiparams{'ACTION'} eq $tr{'save'} ){
	$settings{'GREEN'} = $cgiparams{'ENABLEGREEN'};
	$settings{'ORANGE'} = $cgiparams{'ENABLEORANGE'};
	$settings{'PURPLE'} = $cgiparams{'ENABLEPURPLE'};

	&writehash("$config", \%settings);
}

my $errormessage = "";

if ( defined $cgiparams{'ACTION'} and $cgiparams{'ACTION'} eq $tr{'add'} ){
	my $interface = $cgiparams{'INTERFACE'};
	my $enabled   = $cgiparams{'RULEENABLED'};
	my $service   = $cgiparams{'SERVICE'};
	my $port      = $cgiparams{'PORT'};

	if ( $service eq "user" ){
		if ( not &validportrange( $port ) ){
			$errormessage = $tr{'invalid port or range'};
		} else {
			$service = $port;
		}
	}

	if ( $errormessage eq "" ){	
		open(FILE,">>$settings") or die 'Unable to open config file.';
		flock FILE, 2;
		print FILE "$interface,$enabled,$service\n";
		close(FILE);
	}
}

my $service = 'user';

if ( defined $cgiparams{'ACTION'} and $cgiparams{'ACTION'} eq $tr{'edit'} or $cgiparams{'ACTION'} eq $tr{'remove'}){
	open(FILE, "$settings") or die 'Unable to open config file.';
	my @current = <FILE>;
	close(FILE);

	foreach $line (@current)
	{
		$id++;
		if ($cgiparams{$id} eq "on") {
			$count++; 
		}
	}

	if ($count == 0) {
		$errormessage = $tr{'nothing selected'}; 
	}
	if ($count > 1 && $cgiparams{'ACTION'} eq $tr{'edit'}) {
		$errormessage = $tr{'you can only select one item to edit'}; 
	}
	
	unless ($errormessage)
	{
		open(FILE, ">$settings") or die 'Unable to open config file.';
		flock FILE, 2;
		$id = 0;
		foreach $line (@current)
		{
			$id++;
			unless ($cgiparams{$id} eq "on") {
				print FILE "$line"; 
			} elsif ($cgiparams{'ACTION'} eq $tr{'edit'}) {
				chomp($line);
				my @temp = split(/\,/,$line);
				$cgiparams{'INTERFACE'} = $temp[0];
				$cgiparams{'RULEENABLED'} = $temp[1];
				$service = $temp[2];
			}
		}
		close(FILE);
	}
}

if ( defined $cgiparams{'MACHINEACTION'} and $cgiparams{'MACHINEACTION'} eq $tr{'add'} ){
	my $machine = $cgiparams{'MACHINE'};
	my $enabled = $cgiparams{'MACHINEENABLED'};

	unless ( &validip( $machine ) ){
		$errormessage = "invalid ip";
	}

	if ( $errormessage eq "" ){	
		open(FILE,">>$machinesettings") or die 'Unable to open config file.';
		flock FILE, 2;
		print FILE "$machine,$enabled\n";
		close(FILE);
		$cgiparams{'MACHINE'} = "";
		$cgiparams{'MACHINEENABLED'} = "on";

	}
}

if ( defined $cgiparams{'MACHINEACTION'} and $cgiparams{'MACHINEACTION'} eq $tr{'edit'} or $cgiparams{'MACHINEACTION'} eq $tr{'remove'}){
	open(FILE, "$machinesettings") or die 'Unable to open config file.';
	my @current = <FILE>;
	close(FILE);

	foreach $line (@current)
	{
		$id++;
		if ($cgiparams{$id} eq "on") {
			$count++; 
		}
	}

	if ($count == 0) {
		$errormessage = $tr{'nothing selected'}; 
	}
	if ($count > 1 && $cgiparams{'ACTION'} eq $tr{'edit'}) {
		$errormessage = $tr{'you can only select one item to edit'}; 
	}
	
	unless ($errormessage)
	{
		open(FILE, ">$machinesettings") or die 'Unable to open config file.';
		flock FILE, 2;
		$id = 0;
		foreach $line (@current)
		{
			$id++;
			unless ($cgiparams{$id} eq "on") {
				print FILE "$line"; 
			} elsif ($cgiparams{'MACHINEACTION'} eq $tr{'edit'}) {
				chomp($line);
				my @temp = split(/\,/,$line);
				$cgiparams{'MACHINE'} = $temp[0];
				$cgiparams{'MACHINEENABLED'} = $temp[1];
				$service = $temp[2];
			}
		}
		close(FILE);
	}
}

&openpage($tr{'outbound filtering'}, 1, '', 'networking');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage);

&openbox($tr{'filtered interfaces'} . ':');
print "<form method='post'>\n";
print '<table style=\'width: 100%;\'>' . "\n";
print '<tr>' . "\n";

my $unused = 6;
my $width = 90 / $unused;
foreach $interface (keys(%interfaces)) {
	print qq{
	<tr>
	<td style='width: 35%;'>$tr{'traffic is 1'}$interface$tr{'traffic is 2'}</td>
	<td style='width: 25%;'>
		<select name=\"ENABLE$interface\"'>
			<option $selected{'GREENoff'} value='off'>$tr{'unfiltered'}</option>
			<option $selected{'GREENallow'} value='allow'>$tr{'allowed'}</option>
			<option $selected{'GREENblock'} value='block'>$tr{'blocked'}</option>
		</select>
	</td>
	<td style='width: 40%;'></td>
	</tr>
	};
}

print qq{
	<tr>
	<td colspan='3' style='text-align: center;'>
		<input type="submit" name="ACTION" value="$tr{'save'}">
	</td></tr>
	</table>
	</form>
};
&closebox();

&openbox($tr{'add a new exception'});

print qq{
<form method='post'>
<table style='width: 100%;'>
<tr>
	<td>$tr{'interface'}</td>
	<td><select name='INTERFACE'>
};

foreach my $colour (sort keys %interfaces) {
	print "<option value='$colour'>$colour</option>\n";
}

print qq{
		</select>
	</td>
	<td>$tr{'enabled'}</td>
	<td><input type='checkbox' name='RULEENABLED' $checked{$cgiparams{'RULEENABLED'}}></td>
</tr>
<tr>
	@{[&portlist('SERVICE', $tr{'application servicec'}, 'PORT', $tr{'portc'}, $service)]}
</tr>
<tr>
	<td colspan='4' style='text-align: center;'>
		<input type="submit" name="ACTION" value="$tr{'add'}">
	</td>
</tr>
</table>
</form>
};

&closebox();

&openbox($tr{'always allow'});

print qq{
	<form method='post'>
	<table style='width: 100%;'>
	<tr>
		<td style='width: 25%;'>$tr{'ip addressc'}</td>
		<td style='width: 25%;'><input type='text' name='MACHINE' id='address' @{[jsvalidip('address')]} value='$cgiparams{'MACHINE'}'/></td>
		<td style='width: 25%;'>$tr{'enabled'}</td>
		<td style='width: 25%;'><input type='checkbox' name='MACHINEENABLED' $checked{$cgiparams{'MACHINEENABLED'}}></td>
	</tr>
	<tr>
		<td colspan='4' style='text-align: center;'><input type='submit' name='MACHINEACTION' value='$tr{'add'}'></td>
	</tr>
	</table>
	</form>
};

&closebox();

&openbox($tr{'current exceptions'});
print "<form method='post'>\n";

my %render_settings = (
                        'url'     => "/cgi-bin/outbound.cgi?[%COL%],[%ORD%]",
                        'columns' => [ 
                                { 
                                        column => '1',
                                        title  => "$tr{'interface'}",
                                        size   => 30,
					sort   => 'cmp',
                                },
                                {
                                        column => '3',
                                        title  => "$tr{'application service'}",
                                        size   => 50,
                                        sort   => \&ipcompare,
                                },
                                {
                                        column => '2',
                                        title  => "$tr{'enabledtitle'}",
                                        size   => 10,
                                        tr     => 'onoff',
                                        align  => 'center',
                                },
                                {
                                        title  => "$tr{'mark'}", 
                                        size   => 10,
                                        mark   => ' ',
                                },
				{
					column => '1',
					colour => 'colour',
					tr     => { 'GREEN' => 'green', 'ORANGE' => 'orange', 'PURPLE' => 'purple' },
				},
                                { 
                                        column => '4',
                                        title => "$tr{'comment'}",
                                        break => 'line',
                                }
                        ]
                );

&displaytable( $settings, \%render_settings, $cgiparams{'ORDER'}, $cgiparams{'COLUMN'} );

print <<END
<table class='blank'>
<tr>
	<td style='width: 50%; text-align: center;'><input type='submit' name='ACTION' value='$tr{'remove'}'></td>
	<td style='width: 50%; text-align: center;'><input type='submit' name='ACTION' value='$tr{'edit'}'></td>
</tr>
</table>
</form>
END
;
&closebox();

&openbox($tr{'allowed machines'});
print "<form method='post'>\n";

my %render_settings = (
                        'url'     => "/cgi-bin/outbound.cgi?$cgiparams{'COLUMN'},$cgiparams{'ORDER'},[%COL%],[%ORD%]",
                        'columns' => [ 
                                { 
                                        column => '1',
                                        title  => "$tr{'ip address'}",
                                        size   => 30,
					sort   => 'cmp',
                                },
                                {
                                        column => '2',
                                        title  => "$tr{'enabledtitle'}",
                                        size   => 10,
                                        tr     => 'onoff',
                                        align  => 'center',
                                },
                                {
                                        title  => "$tr{'mark'}", 
                                        size   => 10,
                                        mark   => ' ',
                                },
                                { 
                                        column => '3',
                                        title => "$tr{'comment'}",
                                        break => 'line',
                                }
                        ]
                );

&displaytable( $machinesettings, \%render_settings, $cgiparams{'MACHINEORDER'}, $cgiparams{'MACHINECOLUMN'} );

print <<END
<table class='blank'>
<tr>
	<td style='width: 50%; text-align: center;'><input type='submit' name='MACHINEACTION' value='$tr{'remove'}'></td>
	<td style='width: 50%; text-align: center;'><input type='submit' name='MACHINEACTION' value='$tr{'edit'}'></td>
</tr>
</table>
</form>
END
;

&closebox();
&alertbox('add','add');
&closebigbox();
&closepage();

