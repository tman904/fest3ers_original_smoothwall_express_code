#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );

# What do we need help with?
my $needhelpwith = $ENV{'QUERY_STRING'};

unless ($needhelpwith =~ /^[A-Za-z0-9\.]+$/) {
	$needhelpwith = 'index.cgi';
}

# Prepare to display
&showhttpheaders();

&openpage($tr{'help'}, 1, '', 'help');

&openbigbox();

&openbox('');

# Tricky part. We want only the language glossaries; each language could have
#   completely different glossaries, unlike UI strings. In help's case, we don't
#   overwrite English. If there's no $language glossary, there are no
#   pop-up tool tips.
# Look for the help file. If found, then read the glossaries. No sense in wasting
#   CPU cycles reading glossaries if no help file is available.
# The first help file found satisfies the request. Thus it's possible for mods to
#   completely override stock help.

if ($uisettings{'ALWAYS_ENGLISH'} ne 'off')
{
  # Read the help file, if any
  # Mods (checked first) can replace the stock help (checked last)
  while (</var/smoothwall/mods/*/httpd/html/help/$needhelpwith.html.en /httpd/html/help/$needhelpwith.html.en>)
  {
    if (-f $_)
    {
      open (FILE, $_);
      # include all English glossaries
      # mods can override/supplement stock glossaries
      while (</usr/lib/smoothwall/langs/glossary.en.pl /var/smoothwall/mods/*/usr/lib/smoothwall/langs/glossary.en.pl>)
      {
        if (-f $_)
        {
            require $_;
        }
      }
      last;
    }
  }
} else {
  # Read the help file, if any
  # Mods (checked first) can replace the stock help (checked last)
  while (</var/smoothwall/mods/*/httpd/html/help/$needhelpwith.html.$language /httpd/html/help/$needhelpwith.html.$language >)
  {
    if (-f $_)
    {
      open (FILE, $_);
      # include all $language glossaries
      # mods can override/supplement stock glossaries
      while (</usr/lib/smoothwall/langs/glossary.${language}.pl /var/smoothwall/mods/*/usr/lib/smoothwall/langs/glossary.${language}.pl>)
      {
        if (-f $_)
        {
            require $_;
        }
      }
      last;
    }
  }
}
require "/usr/lib/smoothwall/langs/glossary.base.pl";

# Read the help file.
my $line;
while ( <FILE> ){
	$line =~s/\n/ /g;
	$line .= $_;
}
close (FILE);

print <<END
<table>
<tr>
	<td class='helpheader'>
		<a href="javascript:window.close();"><img src="/ui/img/help.footer.png" alt="Smoothwall Express Online Help - click to close window"></a>
	</td>
</tr>
<tr>
	<td style='text-align: justify; font-size: 11px;'>
END
;

foreach my $term ( keys %glossary ){
	$line =~s/([\W])($term)([^\w:])/$1\01$2\02$term\03$3/ig;
	$glossary{$term} =~ s/(['\\"])/\\\1/g;
}

$line =~ s/\01([^\02]*)\02([^\03]*)\03/<span style='color: #008b00;' onMouseOver="return Tip('$glossary{$2}');" onmouseout="UnTip();">$1<\/span>/ig;
print $line;

print <<END
	</td>
</tr>
<tr>
	<td class='helpfooter'>
		<a href="javascript:window.close();"><img alt="Close this window" src="/ui/img/help.footer.png" border="0"></a>
	</td>
</tr>
</table>
END
;

&closebox();

&closebigbox();

&closepage('blank');

