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

my (%remotesettings, %checked);
my $errormessage='';
my $infomessage='';

&showhttpheaders();

$remotesettings{'ENABLE_SSH'} = 'off';
$remotesettings{'ENABLE_SSH_GREEN'} = 'off';
$remotesettings{'ENABLE_SSH_PURPLE'} = 'off';
$remotesettings{'ENABLE_SECURE_ADMIN'} = 'off';
$remotesettings{'ACTION'} = '';

my $refresh = '';
my $success = '';

&getcgihash(\%remotesettings);

if ($remotesettings{'ACTION'} eq $tr{'save'}) {
	$remotesettings{'ENABLE_SSH'} = 'on';
	&writehash("${swroot}/remote/settings", \%remotesettings);

	if ($remotesettings{'ENABLE_SSH_GREEN'} eq 'on'
	 || $remotesettings{'ENABLE_SSH_PURPLE'} eq 'on') {
		&log($tr{'ssh is enabled'});
	}
	else {
		&log($tr{'ssh is disabled'});
	}
	$success = message('sshdrestart');
	$infomessage .= $success ."<br />\n" if ($success);
	$errormessage .= "Remote Access restart failed." unless ($success);
}

$remotesettings{'ENABLE_SECURE_ADMIN'} = 'off';
&readhash("${swroot}/remote/settings", \%remotesettings);

$checked{'ENABLE_SSH_GREEN'}{'off'} = '';
$checked{'ENABLE_SSH_GREEN'}{'on'} = '';
$checked{'ENABLE_SSH_GREEN'}{$remotesettings{'ENABLE_SSH_GREEN'}} = 'CHECKED';
$checked{'ENABLE_SSH_PURPLE'}{'off'} = '';
$checked{'ENABLE_SSH_PURPLE'}{'on'} = '';
$checked{'ENABLE_SSH_PURPLE'}{$remotesettings{'ENABLE_SSH_PURPLE'}} = 'CHECKED';

$checked{'ENABLE_SECURE_ADMIN'}{'off'} = '';
$checked{'ENABLE_SECURE_ADMIN'}{'on'} = '';
$checked{'ENABLE_SECURE_ADMIN'}{$remotesettings{'ENABLE_SECURE_ADMIN'}} = 'CHECKED';

&openpage($tr{'remote access'}, 1, $refresh, 'services');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage, "", $infomessage);

print "<form method='POST' action='?'><div>\n";

&openbox($tr{'remote access2'});
print <<END
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='width:25%;' class='base'>$tr{'ssh enable green'}:</td>
	<td style='width:25%;'>
          <input type='checkbox' name='ENABLE_SSH_GREEN' $checked{'ENABLE_SSH_GREEN'}{'on'}>
        </td>
	<td style='width:25%;' class='base'><img src='/ui/img/blob.gif' alt='*' style='vertical-align: text-top;'>&nbsp;$tr{'secure admin'}</td>
	<td style='width:25%;'><input type='checkbox' name='ENABLE_SECURE_ADMIN' $checked{'ENABLE_SECURE_ADMIN'}{'on'}></td>
</tr>
<tr>
	<td style='width:25%;' class='base'>$tr{'ssh enable purple'}:</td>
	<td style='width:25%;'>
          <input type='checkbox' name='ENABLE_SSH_PURPLE' $checked{'ENABLE_SSH_PURPLE'}{'on'}>
        </td>
	<td>&nbsp;<td><td>&nbsp;</td>
</tr>
</table>
<br />
<img src='/ui/img/blob.gif' alt='*' style='vertical-align: text-top;'>&nbsp;
<span class='base'>$tr{'secure admin long'}</span>
END
;
&closebox();

print <<END
<table style='width: 60%; border: none; margin-left:auto; margin-right:auto'>
<tr>
        <td style='text-align: center;'><input type='submit' name='ACTION' value='$tr{'save'}'></td>
</tr>
</table>
END
;

print "</div></form>\n";

&alertbox('add', 'add');
&closebigbox();
&closepage();
