#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );

my %cgiparams;
my $death = 0;
my $rebirth = 0;

&showhttpheaders();

$cgiparams{'ACTION'} = '';
&getcgihash(\%cgiparams);

my %uisettings;
my %checked;
$checked{'on'} = " checked";

&readhash("${swroot}/main/ui/settings", \%uisettings);

if ($cgiparams{'ACTION'} eq $tr{'save'})
{
	$uisettings{'MENU'} = $cgiparams{'MENU'};
	&writehash("${swroot}/main/ui/settings", \%uisettings);
}

use Data::Dumper;
print STDERR Dumper %uisettings;
	
&openpage( $tr{'preferences'}, 1, '', 'maintenance');

&openbigbox('100%', 'LEFT');

print "<form method='post'>\n";

&openbox($tr{'user interface'});

print <<END
<table style='width: 100%;'>
<tr>
	<td style='width: 25%;'>$tr{'ui menus'}</td>
	<td style='width: 25%;'><input type='checkbox' name='MENU' $checked{$uisettings{'MENU'}}></td>
	<td style='width: 25%;'>&nbsp;</td>
	<td style='width: 25%;'>&nbsp;</td>
</tr>
<tr>
	<td colspan='4' style='text-align: center;'>
		<input type='submit' name='ACTION' value='$tr{'save'}'>
	</td>
</tr>
</table>
END
;

&closebox();

print "</form>\n";

&closebigbox();

&closepage();
