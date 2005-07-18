#include "configvar.hpp"
#include <vector>
#include <iostream>
#include <fstream>


// read in var=val


int configvar::readvar( const char * filename, const char * delimiter )
{
    std::ifstream input ( filename );
    char buffer[ 2048 ];

    params.clear();
	
    if ( !input ) return 1;

    while ( input ){
        if ( !input.getline( buffer, sizeof( buffer )) ) {
            break;
        }
        
        char * command = buffer;
        if ( !( *command ) ) continue;
        
        char * parameter = strstr( buffer, delimiter );
        if ( !parameter ) continue;
        
        if ( (parameter + strlen( delimiter )) > buffer + strlen( buffer ))
            continue;
        
        *parameter = '\0';
        parameter += strlen( delimiter );
	
        
        while ( *parameter == '"' || *parameter == '\'' || *parameter == ' ') parameter++;
        int offset = strlen( parameter ) - 1;
        
        while ( parameter[ offset ] == '"' || parameter[ offset ] == '\'' ) parameter[ offset-- ] = '\0';
        
        offset = strlen( command ) - 1;
        while ( command[ offset ] == ' ' ) command[ offset-- ] = '\0';
	
        params[ command ] = parameter;
    }

    input.close();

    return 0;
}



#define NUMBERS "0123456789"
#define NUMBERS_COLON "0123456789:"
#define LETTERS_NUMBERS LETTERS NUMBERS
#define IP_NUMBERS "./" NUMBERS
#define IP_NUMBERS_COLON ":" IP_NUMBERS
#define IP_NUMBERS_DASH "-" IP_NUMB

int safeatoi( const char * a )
{
    if (strspn(a, NUMBERS) != strlen(a)){
        return 0;
    }
    
    return atoi( a );
}

int safeatoi( std::string a )
{
    return( safeatoi( a.c_str() ) );
}

