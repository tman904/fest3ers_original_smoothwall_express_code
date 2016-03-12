#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use smoothd qw( message );
use strict;
use warnings;

my %uploadsettings;
$uploadsettings{'ACTION'} = '';

&showhttpheaders();

&getcgihash(\%uploadsettings);

my $errormessage = '';
my $extramessage = '';

if ($uploadsettings{'ACTION'} eq $tr{'upload'}) {
	if (length($uploadsettings{'FH'}) > 1) {
		open(FILE, ">${swroot}/adsl/mgmt.o") or $errormessage = $tr{'could not create file'};
		flock FILE, 2;
		print FILE $uploadsettings{'FH'};
		close (FILE);
		$extramessage = $tr{'upload successful'};
	}
	undef $uploadsettings{'FH'};

	my $success = message('alcateladslfw');
		
	$errormessage = $tr{'smoothd failure'} unless ($success);	
}

&openpage($tr{'usb adsl setup'}, 1, '', 'maintenance');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage);

&openbox($tr{'mgmt upload'});
print <<END
$tr{'usb adsl help'}
<P>
<form method='post' ENCTYPE='multipart/form-data' action='?'>
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>

	<td class='base' style='text-align:right;'>$tr{'upload filec'}</td>
	<td><input type="file" name="FH"> <input type='submit' name='ACTION' value='$tr{'upload'}'></td>
</tr>
</table>
</form>
END
;

print "<div class='base' style='text-align:center; font-size: 200%;'>$extramessage</div>\n";

&closebox();

&alertbox('add','add');

&closebigbox();

&closepage();

