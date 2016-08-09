#! /usr/bin/gawk

BEGIN {
  certLines = "";
  last1st = "";
  last2nd = "";
}

/BEGIN CERT/ {
  if (last2nd != "") {
    printf("%s\n",last2nd);
    print certLines > last2nd ".pem";
    last1st= "";
    last2nd = "";
  }
  certLines = "";
}

{
  certLines = certLines "\n" $0;
  gsub(/[ /]/,"_",$0);
  gsub(/[()]/,"=",$0);
  last2nd = last1st;
  last1st = $0;
}
