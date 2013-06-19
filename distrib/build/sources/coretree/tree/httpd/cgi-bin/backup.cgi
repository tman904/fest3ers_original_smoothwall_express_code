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
use smoothtype qw(:standard);

my (%cgiparams,%selected,%checked);
my $filename = "${swroot}/backup/config";
my $flagfile = "${swroot}/backup/flag";
my $maxwidth = 20;

&showhttpheaders();

$cgiparams{'ENABLED'} = 'off';

$cgiparams{'COLUMN'} = 1;
$cgiparams{'ORDER'} = $tr{'log ascending'};
$cgiparams{'STATE'} = 'idle';

&getcgihash(\%cgiparams);

if ($ENV{'QUERY_STRING'} && 
    ( not defined $cgiparams{'ACTION'} or $cgiparams{'ACTION'} eq "" ))
{
  my @temp = split(',',$ENV{'QUERY_STRING'});
  $cgiparams{'ORDER'}  = $temp[1] if ( defined $temp[ 1 ] and $temp[ 1 ] ne "" );
  $cgiparams{'COLUMN'} = $temp[0] if ( defined $temp[ 0 ] and $temp[ 0 ] ne "" );
}

my $errormessage = '';
my @service = ();

# There is no action for 'Add Drive'; it is handled in javascript

if ($cgiparams{'ACTION'} eq $tr{'remove'})
{
        open(FILE, "$filename") or die 'Unable to open config file.';
        my @current = <FILE>;
        close(FILE);

        my $count = 0;
        my $id = 0;
        my $line;
        foreach $line (@current)
        {
                $id++;
                if ($cgiparams{$id} eq "on") {
                        $count++; }
        }
        if ($count == 0) {
                $errormessage .= $tr{'nothing selected'}; }
        unless ($errormessage)
        {
                open(FILE, ">$filename") or die 'Unable to open config file.';
                flock FILE, 2;
                my $id = 0;
                foreach $line (@current)
                {
                        $id++;
                        unless ($cgiparams{$id} eq "on") {
                                print FILE "$line"; }
                }
                close(FILE);
                # Write settings file
                system('/usr/bin/smoothwall/backup_sys -S');

        }
}




&openpage($tr{'bu pnp backup'}, 1, '', 'services');

&openbigbox('100%', 'LEFT');

# Include the simple_monitor function
print <<END;
<script type='text/javascript'
        language='JavaScript'
        src='/ui/js/monitor.js'>
</script>
<script type='text/javascript'
        language='JavaScript'
        src='/ui/js/backup_monitor.js'>
</script>
<script type='text/javascript'
        language='JavaScript'
        src='/ui/js/backup_add_drive.js'>
</script>
<script type='text/javascript'
        language='JavaScript'>
  // Schedule the first one
  var backupState = 'start';  // Initial state
  var lastFileno = 0;         // Detect when progress bar should change
  var whichBar = 0;           // Which progress bar
  var maxwidth = '${maxwidth}';
  var removePrompt = '$tr{'bu remove drive'}';
  var backupMonitorObj = new Object();
  var addDriveMonitorObj = new Object();
  var addDriveOneShotObj = new Object();

  simpleMonitor(backupMonitorObj, '/cgi-bin/txt-bu-flag.cgi', handleFlag);
</script>
END

&alertbox($errormessage);

print "<form method='post'>\n";

&openbox($tr{'bu backup statusc'});

# Read .../backup/flag into $flag
open FLAG, $flagfile;
read FLAG, $flag, 500;
close FLAG;

print <<END
<table width='100%' cellpadding='0' cellspacing='0'>
<tr>
	<td colspan='3'><p class='close' id='buStatus' style='height:2.5em; margin-left:4em'></p></td>
</tr>
<tr>
        <td class='base' style='width:20%; margin:1px'>
          $tr{'bu var backupc'}
        </td>
        <td style='margin:1px'>
          <div style='width:${maxwidth}em; height:100%; border:lightgrey 1px solid;'>
            <div class='progressbar'
                 id='buProgressVar'
                 style='width:0; height:100%; background-color:#000090'>&nbsp;</div>
          </div>
        </td style='margin:1px'>
        <td style='margin:1px' class='progressend'>&nbsp;</td>
</tr>
<tr>
        <td class='base' style='width:20%'>
          $tr{'bu total backupc'}
        </td>
        <td style='margin:1px'>
          <div style='width:${maxwidth}em; height:100%; border:lightgrey 1px solid;'>
            <div class='progressbar'
                 id='buProgressTotal'
                 style='width:0; height:100%; background-color:#000090'>&nbsp;</div>
          </div>
        </td>
        <td class='progressend' style='margin:1px'>&nbsp;</td>
</tr>
</table>
END
;
&closebox();

&openbox();

&openbox($tr{'bu known mediac'});

my %render_settings =
(
	'url'     => "/cgi-bin/backup.cgi?[%COL%],[%ORD%]",
	'columns' => 
	[
		{ 
			column => '1',
			title  => "$tr{'bu name'}",
			size   => 20,
			valign => 'top',
			maxrowspan => 2,
			sort   => 'cmp',
		},
		{
			column => '2',
			title  => "$tr{'bu id'}",
			size   => 70,
			sort   => 'cmp'
		},
		{
			title  => "$tr{'mark'}", 
			size   => 10,
			mark   => ' ',
		},

	]
);

&displaytable($filename, \%render_settings, $cgiparams{'ORDER'}, $cgiparams{'COLUMN'} );

print <<END
<table class='blank'>
<tr>
<td style='width: 50%; text-align:center;'><input type='submit' name='ACTION' value="$tr{'remove'}"></td>
<td style='width: 50%; text-align:center;'><input type='submit' name='ACTION' value='$tr{'edit'}'></td>
</tr>
</table>
END
;
&closebox();

&openbox();

print<<END;
<table class='blank'>
<tr>
  <td align='center' style='width: 20%;text-align:center'>
    <input id='buAddDrive' type='submit' name='ACTION' value='$tr{"bu add drive"}'
           onclick='simpleMonitor(addDriveMonitorObj, "/cgi-bin/txt-bu-startAdd.cgi", handleAddFlag); return false;'
           style='margin:.2em; text-align:center'><br />
    <input id='buOK' type='submit' disabled='disabled' name='ACTION' value='$tr{"bu ok"}'
           onclick='simpleMonitor(addDriveOneShotObj, "/cgi-bin/txt-bu-setRsp.cgi?rsp="+buNameEntry.value, no_op);
                    return false;'
           style='margin:.2em; text-align:center'><br />
    <input id='buCancel' type='submit' disabled='disabled' name='ACTION' value='$tr{"bu cancel"}'
           onclick='simpleMonitor(addDriveOneShotObj, "/cgi-bin/txt-bu-cancelAdd.cgi", no_op); return false;'
           style='margin:.2em; text-align:center'>
  </td>
  <td style='width:75%'>
    <p id='buPrompt'>$tr{'bu default prompt'}</p>
    <div id='buInput' style='display:none'>
      <p style='display:inline-block; text-align:right; margin-right:.5em'>
        $tr{'bu name'}:
      </p>
      <input id='buNameEntry' type='text' name='driveName' style='width:50%'
             onkeyup='if (buNameEntry.value.match(/^[a-zA-Z0-9_-]+\$/) == null)
                         buNameEntry.style.backgroundColor="#ffdddd";
                       else
                         buNameEntry.style.backgroundColor="";
                       ;'>
      <p style='display:inline-block; margin-right:.5em'>
        <i>allowed: (A-Z, a-z, 0-9, _, -)</i>
      </p>
    </div>
  </td>
</tr>
</table>
<div id='debug' style='border:green 2pt solid; display:none'></div>
END
  

&closebox();

&closebox();

&alertbox('add','add');

&closebigbox();

&closepage();
