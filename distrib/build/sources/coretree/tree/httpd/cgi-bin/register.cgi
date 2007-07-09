#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use IO::Socket;

&showhttpheaders();

&openpage($tr{'register'}, 1, "", 'register');
&openbigbox();

my (%settings,$errormessage);
&getcgihash(\%settings);

my @temp = split('\&',$ENV{'QUERY_STRING'});

foreach my $pair ( @temp ){
	my ( $var, $val ) = split /=/, $pair;
	$settings{ $var } = $val;
}

my ( $reg, $regval );
if ( open ( $reg, "</var/smoothwall/registered" )){
	$regval = <$reg>;
}

my $sysid = &getsystemid();

if ( $regval ne "" ){
	&openbox();
	print $regval;
	&closebox();
	close $reg;
} elsif ($settings{'ACTION'} eq $tr{'register'} ){
	register( \%settings );
} elsif ($settings{'ACTION'} eq $tr{'no thanks'} ){
	&dont_register();
} else {
	register_page();
}

&alertbox($errormessage);

&closebigbox();
&closepage();

sub dont_register
{
	my ( $settings ) = @_;
	
	&openbox();
	
	print <<END
	$tr{'reg nevermind'}
END
;

	my $reg;
	if( open ( $reg, ">/var/smoothwall/registered" )){
		print $reg "";
		close $reg;
	}

	&closebox();
}

sub register
{
	my ( $settings ) = @_;
	
	&openbox();
	
	print <<END
	
	$tr{'reg thankyou'}; <strong>$settings->{'id'}</strong>
END
;

	my $reg;
	if( open ( $reg, ">/var/smoothwall/registered" )){
		print $reg "$tr{'reg thankyou'}; <strong>$settings->{'id'}</strong>\n";
		close $reg;
	}

	&closebox();
}


sub register_page
{

&openbox('');

print <<END
<div align="center"><h2>SmoothWall Express $version</h2>
<p>Express $version $webuirevision
</div>
END
;

&closebox();

# START x3 add bit
#print "<form method='post'>\n";
print <<END
<form method='post' action='https://my.smoothwall.org/cgi-bin/signin.cgi'>
<input type="hidden" name=id value=$sysid>
END
;

&openbox( $tr{'x3_reg'} );

print <<END
<table class='centered'>
	<tr>
		<td colspan='2'>
			<br/>
			$tr{'x3_reg_info'}
			<br/>
			<br/>
		</td>
	</tr>
</table>
END
;

print <<END
<table class='centered'>
	<tr>
		<td style='text-align: center;'><input name="ACTION" type='submit' value='$tr{'register'}'></td>
</form>
<form method='post'>
		<td style='text-align: center;'><input name="ACTION" type='submit' value='$tr{'no thanks'}'></td>
	</tr>
</table>
END
;

print "</form>\n";

&closebox();
# END x3 add bit

&openbox( $tr{'credits_and_legal'} );

print <<END
<div align="center">
<table border="0" cellpadding="3" cellspacing="0" width="90%">

<tr><td width="50%" align="left" valign="top">
<center>
SmoothWall Express $version<br>
Copyright &copy; 2000 - 2007 the <a href="http://smoothwall.org/team/" target="_breakoutWindow">SmoothWall Team</a>
</center>
<p>
A full team listing can be found <a href="http://smoothwall.org/team/"
 target="_breakoutWindow">on our website</a>.
Portions of this software are copyright &copy; the original
authors, the source code of such portions are 
<a href="http://smoothwall.org/sources.html"
 target="_breakoutWindow">available under the terms of the appropriate 
licenses</a>.
</p>
</td>
<td width="50%" align="left" valign="top">
<p>
For more information about SmoothWall Express, 
please visit our website at
<a href="http://smoothwall.org/"
 target="_breakoutWindow">http://smoothwall.org/</a>
</p>
<p>
For more information about SmoothWall products, please visit 
our website at <a href="http://www.smoothwall.net/"
 target="_breakoutWindow">http://www.smoothwall.net/</a>
</p>
</td>
</table>

<p>
SmoothWall&trade; is a trademark of SmoothWall Limited.
Linux&reg; is a registered trademark of Linus Torvalds.
All other trademarks and copyrights are property of their
respective owners.
Stock photography used courtesy of
<a href="http://istockphoto.com/">iStockphoto.com</a>.
</p>
</div>
END
;

&closebox();
}
