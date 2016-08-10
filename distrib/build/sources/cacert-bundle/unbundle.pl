#! /usr/bin/perl -w

my $certLines = "";
my $last1st = "";
my $last2nd = "";

# Read the bundled certs and unpack
open BUNDLE, "<ca-certificates.crt";
while (<BUNDLE>) {
  if ($_ =~ /BEGIN CERT/) {
    # If a cert was just finished, emit it and reset
    if ($last2nd ne "") {
      printf("%s\n", $last2nd);
      if (open (outFILE, ">$last2nd.pem")) {
        print outFILE $certLines;
        close (outFILE);
      }
    }
    $last1st= "";
    $last2nd = "";
    $certLines = "";
  }

  # Assemble the cert, change chars as needed, keep the previous two lines
  $certLines .= $_;
  chomp;
  s/[ \/]/_/g;
  s/[()]/=/g;
  $last2nd = $last1st;
  $last1st = $_;
}
close(BUNDLE);
