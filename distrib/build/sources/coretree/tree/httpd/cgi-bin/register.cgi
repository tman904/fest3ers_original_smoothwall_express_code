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

my @temp = split('\&',$ENV{'QUERY_STRING'});

foreach my $pair ( @temp ){
	my ( $var, $val ) = split /=/, $pair;
	$settings{ $var } = $val;
}

use Data::Dumper;
print STDERR Dumper %settings;

my ( $reg, $regval );
if ( open ( $reg, "</var/smoothwall/registered" )){
	$regval = <$reg>;
}

if ( $regval ne "" ){
	&openbox();
	print $regval;
	&closebox();
	close $reg;
} elsif ($settings{'ACTION'} eq "Register" ){
	register( \%settings );
} else {
	register_page();
}

&alertbox($errormessage);

&closebigbox();
&closepage();

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
		print $reg "$tr{'reg thankyou'} <strong>$settings->{'id'}</strong>\n";
		close $reg;
	}

	&closebox();
}


sub register_page
{
print "<form method='post' action='http://www.smoothwall.org/cgi-bin/express_register.cgi'>\n";

&openbox( $tr{'reg about you'} );

print <<END
<table class='centered'>
	<tr>
		<td style='width: 25%;'>$tr{'reg title'}</td>
		<td><input type='text' name='title' title='$tr{'reg title title'}'></td>
	</tr>
	<tr>
		<td>$tr{'reg name'}</td>
		<td><input type='text' name='name'></td>
	</tr>
	<tr>
		<td>$tr{'reg surname'}</td>
		<td><input type='text' name='surname' title='$tr{'reg surname title'}'></td>
	</tr>
	<tr>
		<td>$tr{'reg email address'}</td>
		<td><input type='text' name='email'></td>
	</tr>
	<tr>
		<td style='vertical-align: top;'>$tr{'reg postal address'}</td>
		<td><textarea name='address' style='width: 300px; height: 70px;'></textarea></td>
	</tr>
	<tr>
		<td>$tr{'reg country'}</td>
		<td>
			<select name='country'>
				<option value="AF">Afghanistan
				<option value="AL">Albania
				<option value="DZ">Algeria
				<option value="AS">American Samoa
				<option value="AD">Andorra
				<option value="AO">Angola
				<option value="AI">Anguilla
				<option value="AQ">Antarctica
				<option value="AG">Antigua And Barbuda
				<option value="AR">Argentina
				<option value="AM">Armenia
				<option value="AW">Aruba
				<option value="AU">Australia
				<option value="AT">Austria
				<option value="AZ">Azerbaijan
				<option value="BS">Bahamas, The
				<option value="BH">Bahrain
				<option value="BD">Bangladesh
				<option value="BB">Barbados
				<option value="BY">Belarus
				<option value="BE">Belgium
				<option value="BZ">Belize
				<option value="BJ">Benin
				<option value="BM">Bermuda
				<option value="BT">Bhutan
				<option value="BO">Bolivia
				<option value="BA">Bosnia and Herzegovina
				<option value="BW">Botswana
				<option value="BV">Bouvet Island
				<option value="BR">Brazil
				<option value="IO">British Indian Ocean Territory
				<option value="BN">Brunei
				<option value="BG">Bulgaria
				<option value="BF">Burkina Faso
				<option value="BI">Burundi
				<option value="KH">Cambodia
				<option value="CM">Cameroon
				<option value="CA">Canada
				<option value="CV">Cape Verde
				<option value="KY">Cayman Islands
				<option value="CF">Central African Republic
				<option value="TD">Chad
				<option value="CL">Chile
				<option value="CN">China
				<option value="CX">Christmas Island
				<option value="CC">Cocos (Keeling) Islands
				<option value="CO">Colombia
				<option value="KM">Comoros
				<option value="CG">Congo
				<option value="CD">Congo, Democractic Republic of the
				<option value="CK">Cook Islands
				<option value="CR">Costa Rica
				<option value="CI">Cote D'Ivoire (Ivory Coast)
				<option value="HR">Croatia (Hrvatska)
				<option value="CU">Cuba
				<option value="CY">Cyprus
				<option value="CZ">Czech Republic
				<option value="DK">Denmark
				<option value="DJ">Djibouti
				<option value="DM">Dominica
				<option value="DO">Dominican Republic
				<option value="TP">East Timor
				<option value="EC">Ecuador
				<option value="EG">Egypt
				<option value="SV">El Salvador
				<option value="GQ">Equatorial Guinea
				<option value="ER">Eritrea
				<option value="EE">Estonia
				<option value="ET">Ethiopia
				<option value="FK">Falkland Islands (Islas Malvinas)
				<option value="FO">Faroe Islands
				<option value="FJ">Fiji Islands
				<option value="FI">Finland
				<option value="FR">France
				<option value="GF">French Guiana
				<option value="PF">French Polynesia
				<option value="TF">French Southern Territories
				<option value="GA">Gabon
				<option value="GM">Gambia, The
				<option value="GE">Georgia
				<option value="DE">Germany
				<option value="GH">Ghana
				<option value="GI">Gibraltar
				<option value="GR">Greece
				<option value="GL">Greenland
				<option value="GD">Grenada
				<option value="GP">Guadeloupe
				<option value="GU">Guam
				<option value="GT">Guatemala
				<option value="GN">Guinea
				<option value="GW">Guinea-Bissau
				<option value="GY">Guyana
				<option value="HT">Haiti
				<option value="HM">Heard and McDonald Islands
				<option value="HN">Honduras
				<option value="HK">Hong Kong S.A.R.
				<option value="HU">Hungary
				<option value="IS">Iceland
				<option value="IN">India
				<option value="ID">Indonesia
				<option value="IR">Iran
				<option value="IQ">Iraq
				<option value="IE">Ireland
				<option value="IL">Israel
				<option value="IT">Italy
				<option value="JM">Jamaica
				<option value="JP">Japan
				<option value="JO">Jordan
				<option value="KZ">Kazakhstan
				<option value="KE">Kenya
				<option value="KI">Kiribati
				<option value="KR">Korea
				<option value="KP">Korea, North
				<option value="KW">Kuwait
				<option value="KG">Kyrgyzstan
				<option value="LA">Laos
				<option value="LV">Latvia
				<option value="LB">Lebanon
				<option value="LS">Lesotho
				<option value="LR">Liberia
				<option value="LY">Libya
				<option value="LI">Liechtenstein
				<option value="LT">Lithuania
				<option value="LU">Luxembourg
				<option value="MO">Macau S.A.R.
				<option value="MK">Macedonia, Former Yugoslav Republic of
				<option value="MG">Madagascar
				<option value="MW">Malawi
				<option value="MY">Malaysia
				<option value="MV">Maldives
				<option value="ML">Mali
				<option value="MT">Malta
				<option value="MH">Marshall Islands
				<option value="MQ">Martinique
				<option value="MR">Mauritania
				<option value="MU">Mauritius
				<option value="YT">Mayotte
				<option value="MX">Mexico
				<option value="FM">Micronesia
				<option value="MD">Moldova
				<option value="MC">Monaco
				<option value="MN">Mongolia
				<option value="MS">Montserrat
				<option value="MA">Morocco
				<option value="MZ">Mozambique
				<option value="MM">Myanmar
				<option value="NA">Namibia
				<option value="NR">Nauru
				<option value="NP">Nepal
				<option value="AN">Netherlands Antilles
				<option value="NL">Netherlands, The
				<option value="NC">New Caledonia
				<option value="NZ">New Zealand
				<option value="NI">Nicaragua
				<option value="NE">Niger
				<option value="NG">Nigeria
				<option value="NU">Niue
				<option value="NF">Norfolk Island
				<option value="MP">Northern Mariana Islands
				<option value="NO">Norway
				<option value="OM">Oman
				<option value="PK">Pakistan
				<option value="PW">Palau
				<option value="PA">Panama
				<option value="PG">Papua new Guinea
				<option value="PY">Paraguay
				<option value="PE">Peru
				<option value="PH">Philippines
				<option value="PN">Pitcairn Island
				<option value="PL">Poland
				<option value="PT">Portugal
				<option value="PR">Puerto Rico
				<option value="QA">Qatar
				<option value="RE">Reunion
				<option value="RO">Romania
				<option value="RU">Russia
				<option value="RW">Rwanda
				<option value="SH">Saint Helena
				<option value="KN">Saint Kitts And Nevis
				<option value="LC">Saint Lucia
				<option value="PM">Saint Pierre and Miquelon
				<option value="VC">Saint Vincent And The Grenadines
				<option value="WS">Samoa
				<option value="SM">San Marino
				<option value="ST">Sao Tome and Principe
				<option value="SA">Saudi Arabia
				<option value="SN">Senegal
				<option value="SC">Seychelles
				<option value="SL">Sierra Leone
				<option value="SG">Singapore
				<option value="SK">Slovakia
				<option value="SI">Slovenia
				<option value="SB">Solomon Islands
				<option value="SO">Somalia
				<option value="ZA">South Africa
				<option value="GS">South Georgia / South Sandwich Islands
				<option value="ES">Spain
				<option value="LK">Sri Lanka
				<option value="SD">Sudan
				<option value="SR">Suriname
				<option value="SJ">Svalbard And Jan Mayen Islands
				<option value="SZ">Swaziland
				<option value="SE">Sweden
				<option value="CH">Switzerland
				<option value="SY">Syria
				<option value="TW">Taiwan
				<option value="TJ">Tajikistan
				<option value="TZ">Tanzania
				<option value="TH">Thailand
				<option value="TG">Togo
				<option value="TK">Tokelau
				<option value="TO">Tonga
				<option value="TT">Trinidad And Tobago
				<option value="TN">Tunisia
				<option value="TR">Turkey
				<option value="TM">Turkmenistan
				<option value="TC">Turks And Caicos Islands
				<option value="TV">Tuvalu
				<option value="UG">Uganda
				<option value="UA">Ukraine
				<option value="AE">United Arab Emirates
				<option value="UK" SELECTED>United Kingdom
				<option value="US">United States
				<option value="UM">United States Minor Outlying Islands
				<option value="UY">Uruguay
				<option value="UZ">Uzbekistan
				<option value="VU">Vanuatu
				<option value="VA">Vatican City State (Holy See)
				<option value="VE">Venezuela
				<option value="VN">Vietnam
				<option value="VG">Virgin Islands (British)
				<option value="VI">Virgin Islands (US)
				<option value="WF">Wallis And Futuna Islands
				<option value="YE">Yemen
				<option value="YU">Yugoslavia
				<option value="ZM">Zambia
				<option value="ZW">Zimbabwe
				<option value="other">Other;
			</select>
		</td>
	</tr>

</table>
END
;
&closebox();

&openbox( $tr{'reg about network'} );
print <<END
<table class='centered'>
	<tr>
		<td style='width: 25%;'>$tr{'reg usage'}</td>
		<td><select name='status'>
			<option value='individual'>$tr{'reg individual'}
			<option value='consultant'>$tr{'reg consultant'}
			<option value='reseller'  >$tr{'reg reseller'  }
			<option value='company'   >$tr{'reg company'   }
			<option value='non-profit'>$tr{'reg non-profit'}
			<option value='other'     >$tr{'reg other'     }
		</select></td>
	</tr>
	<tr>
		<td>$tr{'reg size'}</td>
		<td><select name='size'>
			<option value="1">$tr{'reg single'}
			<option value="2-5">2 - 5
			<option value='6-10'>6 - 10
			<option value="11-20">11 - 20
			<option value="21-50">21 - 50
			<option value="51-99">51 - 99
			<option value="100-200">100 - 200
			<option value="200+">200+
			<option value="other">$tr{'reg other'}
		</select></td>
	</tr>
	<tr>
		<td>$tr{'reg type'}</td>
		<td><select name='type'>
			<option value='domestic'>$tr{'reg domestic'}
			<option value='domesticbusiness'>$tr{'reg domesticbusiness'}
			<option value='business'>$tr{'reg business'}
			<option value='other'>$tr{'reg other'}
		</select></td>
	</tr>
	<tr>
		<td style='vertical-align: top;'>$tr{'reg composition'}</td>
		<td>
		<table>
			<tr>
				<td><input type='checkbox' name='windows2003'> Windows 2003</td>
				<td><input type='checkbox' name='windows2000'> Windows 2000</td>
				<td><input type='checkbox' name='windowsxp'> Windows XP</td>
			</tr>
			<tr>
				<td><input type='checkbox' name='windows9x'> Windows 9x</td>
				<td><input type='checkbox' name='windows3'> Windows 3.1</td>
				<td><input type='checkbox' name='linux'> Linux &trade;</td>
			</tr>
			<tr>
				<td><input type='checkbox' name='bsd'> FreeBSD</td>
				<td><input type='checkbox' name='solaris'> Solaris</td>
				<td><input type='checkbox' name='unix'> Other Unix</td>
			</tr>
			<tr>
				<td><input type='checkbox' name='mac'> Apple &reg;</td>
				<td><input type='checkbox' name='risc'> RISC OS &copy;</td>
				<td><input type='checkbox' name='beos'> BeOS</td>
			</tr>
			<tr>
				<td><input type='checkbox' name='amiga'> Amiga</td>
				<td><input type='checkbox' name='wireless'> Wireless</td>
				<td>$tr{'reg other'} <input type='text' name='osother'></td>
			</tr>
		</table>
		</td>
	</tr>
</table>
END
;
&closebox();

&openbox( 'Comments' );

print <<END
<table class='centered'>
	<tr>
		<td><textarea name='comments' style='width: 700px; height: 150px;'>$tr{'reg enter comments'}</textarea></td>
	</tr>
</table>
END
;

&closebox();

&openbox( $tr{'reg info'} );

print <<END
<table class='centered'>
	<tr>
		<td><input type='checkbox' name='gplcontact'></td>
		<td>
			$tr{'reg gpl optin'}
		</td>
	</tr>
	<tr>
		<td><input type='checkbox' name='ltdcontact'></td>
		<td>
			$tr{'reg ltd optin'}
		</td>
	</tr>
	<tr>
		<td colspan='2' style='color: #505050;'>
			<br/>
			$tr{'reg privacy'}
		</td>
	</tr>
</table>
END
;

&closebox();

print <<END
<table class='centered'>
	<tr>
		<td style='text-align: center;'><input name="ACTION" type='submit' value='$tr{'register'}'></td>
	</tr>
</table>
END
;

print "</form>\n";
}


