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

if ($cgiparams{'ACTION'} eq $tr{'bu add medium'})
{
  if ($cgiparams{'STATE'} eq "PluggedIn") {
    # validate name: only [A-Za-z -_]
    unless($cgiparams{'NAME'} =~ /^[A-Za-z0-9 -_]+$/) {
      $errormessage .= $tr{'bu invalid name'};
    }
    # is it in use?
    if(system("grep '".$cgiparams{'NAME'}."' ${swroot}/backup/config >/dev/null 2>&1")) {
      $errormessage .= $tr{'bu name used'};
    }
    unless ($errormessage)
    {
      open(FILE,">>$filename") or die 'Unable to open config file.';
      flock FILE, 2;
      print FILE "$cgiparams{'NAME'},$cgiparams{'ID'}\n";
      close(FILE);
      undef %cgiparams;
      $cgiparams{'COLUMN'} = 1;
      $cgiparams{'ORDER'} = $tr{'log ascending'};

      #system('/usr/bin/smoothwall/writepnpbackup.pl');
    }
  }
}

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
        if ($count > 1 && $cgiparams{'ACTION'} eq $tr{'edit'}) {
                $errormessage = $tr{'you can only select one item to edit'}; }
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
                        elsif ($cgiparams{'ACTION'} eq $tr{'edit'})
                        {
                                chomp($line);
                                my @temp = split(/\,/,$line);
                                $cgiparams{'IP'} = $temp[0];
                                $cgiparams{'HOSTNAME'} = $temp[1];
                                $cgiparams{'ENABLED'} = $temp[2];
                                $cgiparams{'COMMENT'} = $temp[3];
                        }
                }
                close(FILE);

                #system('/usr/bin/smoothwall/writepnpackup.pl');

        }
}




&openpage($tr{'bu pnp backup'}, 1, '', 'services');

&openbigbox('100%', 'LEFT');

# Include the simple_monitor function
print "
<script type='text/javascript'
        language='JavaScript'
        src='/ui/js/monitor.js'>
</script>
<script type='text/javascript'
        language='JavaScript'
        src='/ui/js/backup_monitor.js'>
</script>
<script type='text/javascript'
        language='JavaScript'>
  // Schedule the first one
  var backupState = 'start';  // Initial state
  var lastFileno = 0;         // Detect when progress bar should change
  var whichBar = 0;           // Which progress bar
  var maxwidth = ${maxwidth};
  var removePrompt = '$tr{'bu remove drive'}';

  simpleMonitor('/cgi-bin/txt-bu-flag.cgi', handleFlag);
</script>\n";

&alertbox($errormessage);

print "<FORM METHOD='POST'>\n";

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

&openbox($tr{'bu known mediac'});

my %render_settings =
(
	'url'     => "/cgi-bin/hosts.cgi?[%COL%],[%ORD%]",
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
<td style='width: 50%; text-align:center;'><input type='submit' name='ACTION' value='$tr{'remove'}'></td>
<td style='width: 50%; text-align:center;'><input type='submit' name='ACTION' value='$tr{'edit'}'></td>
</tr>
</table>
END
;
&closebox();

&alertbox('add','add');

&closebigbox();

&closepage();
