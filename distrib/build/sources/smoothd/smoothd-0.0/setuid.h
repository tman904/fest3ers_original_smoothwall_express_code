/* SmoothWall helper program - header file
 *
 * This program is distributed under the terms of the GNU General Public
 * Licence.  See the file COPYING for details.
 *
 * filename: setuid.h
 * Simple header file for all setuid progs. */

#ifndef __SETUID_H_
#define __SETUID_H_

#include <sys/types.h>
#include <vector>
#include <string>

#define STRING_SIZE 256
#define LETTERS "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
#define NUMBERS "0123456789"
#define NUMBERS_COLON "0123456789:"
#define LETTERS_NUMBERS LETTERS NUMBERS
#define LETTERS_NUMBERS_DOT LETTERS NUMBERS "."
#define IP_NUMBERS "./" NUMBERS
#define IP_NUMBERS_COLON ":" IP_NUMBERS
#define IP_NUMBERS_DASH "-" IP_NUMBERS

#define MAX_ARGS 100

#define MSG_RUNNING_COMMAND "Running command: "
#define MSG_ARG_START "["
#define MSG_ARG_END "] "
#define MSG_NEWLINE "\n"

int initsetuid(int closefd);
void cleanupsetuid(void);
void stripnl(char *s);
int simplesecuresysteml(char *arg, ...);
int simplesecuresystemv(char *argv[]);
int simplesecuresystemvenv(char *argv[], char * envp[]);
int simplesecuresystemvector(std::vector<std::string> &args);
int simplesecurepopenl(int writing, pid_t *ppid, char *arg, ...);
int simplesecurepopenv(int writing, pid_t *ppid, char *argv[]);
int simplesecurepeopenvector(int writing, pid_t *ppid, std::vector<std::string> &args);
int simplesecurepopenvenv(int writing, pid_t *ppid, char *argv[], char *envp[]);
int simplesecurepopenextl( int * pipefds, pid_t *ppid, char *arg, ...);
int simplesecurepopenextv( int * pipefds, pid_t *ppid, char *argv[]);
std::vector<std::string> simplesecurepopenvector(std::vector<std::string> &args,
                                                 std::vector<std::string> &input);
std::string calculatemd5(const char *filename);
std::string calculatemd5(std::string filename);
std::string message( std::string messageString );
std::string message( std::vector<std::string> parameters );

#endif
