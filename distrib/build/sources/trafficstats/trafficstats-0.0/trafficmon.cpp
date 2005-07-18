// This collects live stats and displays them as a realtime graph using curses
// Martin Houston, Smoothwall Ltd.
#include <curses.h>
#include <signal.h>
#include <cstdlib>
#include <cstring>
#include <string>
#include <iostream>
#include <time.h>
#include "traffic_config.hpp"
#include "trafstats_core.hpp"


// these are needed to keep the iptables libs happy
const char *program_name = "trafficmon";
const char *program_version = "2";

// here is our config class
traffic_config traf_config;
// signal hander so we cleanly finish using curses
static void finish(int sig);

// signal hander so we can cope with X term resize events
static void resize(int sig);

// package all the repeatable stuff from when we start curses both
// originally and after a resize event
static void start_curses();

// these are globals so render_line can pick them up
// displayable rows
int screen_max_rows = 0;
// displayable cols
int screen_max_cols = 0;
int do_resize = 0;
// where we start - 0 to begin with, gets updated as scroll
int start_row = 0;
// total amount of data there is to show
int max_rows = 0;

void render_line(int linenum,const char *direction, 
                 const char *legend, const char *dev,
                 double barpercent, const char *shownrate,
                 int bgcolor = COLOR_BLACK) {
    
    int startpos, graphcols, graphlimit;
    int barcolour;
    int barchar;
    int i;
    // are we below what is visible or above?
    
    // first return if not this many lines on the screen
    if(linenum < start_row || linenum > (start_row+(screen_max_rows-1)))
        return;
    linenum -= start_row; // displaying this section on screen

    startpos = 0;
    graphcols = screen_max_cols - startpos;
    graphlimit = int(graphcols * barpercent);
    if(barpercent < 0.30) {
        barcolour = COLOR_GREEN;
        barchar = ACS_HLINE; // for mono terminals
    }
    else if(barpercent < 0.75) {
        barcolour = COLOR_YELLOW;
        barchar = ACS_BOARD; // chequered block > 30%
    }
    else {
        barcolour = COLOR_RED;
        barchar = ACS_BLOCK; // solid block > 75%
    }
    // be more pretty if can use background colour to show the graph,
    // else use _

    mvprintw(linenum,0,"%s %s", direction,dev); 
    clrtoeol();
    // partial overwrite of the legend possible
    mvprintw(linenum,12," %s",legend); 
    
    if(!has_colors()) {
        // need the line of whatever character is appropriate
        for(i = 0; i < graphlimit;i++)
            addch(barchar);
    }
    // now the rate - put on top of the bar in the case of the no color version
    mvprintw(linenum, 40 + ((screen_max_cols-startpos)/2-strlen(shownrate)),shownrate);
    if(has_colors()) {
        // whole line background
        mvchgat(linenum,0,screen_max_cols,A_NORMAL,bgcolor,NULL);
        // show the graph part as a colour if possible
        mvchgat(linenum,startpos,graphlimit, A_NORMAL,barcolour, NULL );
    }
}

int handle_input() {
    int c = getch();

    switch(c) {
    case KEY_UP:
 
        if(start_row > 0)
            start_row--; // back down towards 0
        break;
        
    case KEY_PPAGE:
        if(start_row > screen_max_rows+1) // are we > than size of a page
            start_row -= (screen_max_rows+1); // if so can go back
        else
            start_row = 0; // else all the way back to the beginning
        break;

    case KEY_DOWN:
        if(start_row < (max_rows - screen_max_rows))
            start_row++; // can show more
        break;

    case KEY_NPAGE:
        if(start_row < (max_rows - (screen_max_rows*2)))
            start_row += screen_max_rows;
        else
            start_row = (max_rows - screen_max_rows); // last visible page
        break;
    }
    return c;
}
        
// exit curses in an orderley fashon.

static void finish(int sig)
{
    endwin();

    // any non-curses wrapup here

    exit(0);
}

// Can't call curses funcs reliably during signal handling so
// just set a global flag.

static void resize(int sig)
{    
    (void) signal(SIGWINCH, SIG_IGN); 
    do_resize = 1; // set the flag
   
}

// encapsulate this into a func so can reinit after window change too.
// dont care about any previous window contents
static void start_curses() {
   
    (void) signal(SIGWINCH, resize);      

    (void) initscr();      // initialize the curses library
    keypad(stdscr, TRUE);  // enable keyboard mapping 
    (void) nonl();         // tell curses not to do NL->CR/NL on output 
    (void) nodelay(stdscr,true);       // take input chars one at a time, no wait for \n 
    (void) noecho();       // don't echo input 
    curs_set(0);           // make cursor invisible - no visible user input

    if (has_colors())
    {
        start_color();       
        // fg first then bg
        // white text on black
        init_pair(COLOR_BLACK, COLOR_WHITE,COLOR_BLACK);
        // white text on dark blue
        init_pair(COLOR_BLUE, COLOR_WHITE, COLOR_BLUE);
        init_pair(COLOR_MAGENTA, COLOR_BLACK, COLOR_MAGENTA);
        init_pair(COLOR_CYAN, COLOR_BLACK, COLOR_CYAN);

        // graph bar colours
        init_pair(COLOR_GREEN, COLOR_BLACK, COLOR_GREEN);       
        init_pair(COLOR_YELLOW, COLOR_BLACK, COLOR_YELLOW);
        init_pair(COLOR_RED, COLOR_BLACK, COLOR_RED);


        // now try to redefine BLUE MAGENTA AND CYAN
        // to be nicer choices - bluey greyscales
        // scale byte vals up to 1:999 values
        init_color(COLOR_BLUE, 200, 200, 300);
        init_color(COLOR_MAGENTA, 700, 700, 800);
        init_color(COLOR_CYAN, 900, 900, 999);

        // and realy bright bars
        init_color(COLOR_RED, 999, 0, 0);
        init_color(COLOR_GREEN, 0, 999, 0);
        init_color(COLOR_YELLOW, 999, 999, 0);
        
    }
}


int  main(int argc, char *argv[]) {

    int delay = 250000;
    // nonsense to scale graphs against internal speed so do it agains download speed of fastest external interface.
    double fastest_download_speed = 0;
    double bitrate = 0;
    double nowrate = 0;
    if(argc > 1)
        delay = atoi(argv[1]);
    if(traffic_iptables_missing()) {
        
        fprintf(stderr,"tables not in place yet, cannot run\n");
        exit(0);
    }

    Vtraf_stat_samples s;
    Vtraf_stat_samples_iterator si;
    StrSet_iterator devidx,ruleidx;
    Vstring_iterator classidx;
    Vtraf_iterator ia,ib;

    // now init curses
    (void) signal(SIGINT, finish); 
    
    start_curses();       
       
    max_rows = 0;
    getmaxyx(stdscr,screen_max_rows,screen_max_cols);  // get the number of rows and columns 
    
    if(!collect_a_sample(s)) {
        move(0,0);
        clrtobot();
        printw("Cannot get first sample");
        refresh();
        sleep(1);
        move(0,0);
        clrtobot();
    }
    usleep(delay);
    for (;;) {
        timestamp now, last_sec,avg_time,expiry;
        gettimeofday(&now.t, NULL);
        last_sec = avg_time = expiry = now;
        // take off 1/2 a sec
        if(last_sec.t.tv_usec >= 500000) {
            // just trim microsecs
            last_sec.t.tv_usec -= 500000;
        }
        else {
            // in 1st half of sec so go back 1 and forward a half
            last_sec.t.tv_sec -= 1;
            last_sec.t.tv_usec += 500000;
        }
        avg_time.t.tv_sec -= 20; // 20 sec average, so doesnt jump madly
        expiry.t.tv_sec -= (21); // Any data 21 sec old is not needed anymore
        truncate_sample_set(s, expiry);

        // winge if reached 100 samples
        if(s.size() > 100) {
            
            move(0,0);
            clrtobot();
            printw("sample set %d",s.size());
            refresh();
            sleep(1);
        }

        int linenum = 0;
        if(do_resize) {
            endwin();
            start_curses();
            refresh();           
            do_resize = 0;
            getmaxyx(stdscr,screen_max_rows,screen_max_cols); 
        }
        (void) handle_input();
        move(0,0);
       
        if(!collect_a_sample(s)) {
            clrtobot();
            printw("Cannot get next sample");
            refresh();
            sleep(1);
            move(0,0);
            clrtobot();
        }
        else {
            usleep(delay);
        }
        
        
        // now render the samples
        // first another chance to respond to keypress
        (void) handle_input();
        
        traf_stat_collection_item & last =  s.back(); // take a ref to make following code less nasty
         
        
        // externals with a BLUE background 
        StrSet &ext_devs = last.ext_devs;
        StrSet &int_devs = last.int_devs;
        
        bool do_ext_devs = ext_devs.size() > 0;
        bool do_int_devs = int_devs.size() > 0;
        // get all DOWN out of the way first devs/classes/rules then UP
        if(do_ext_devs) 
            for (devidx = ext_devs.begin(); devidx != ext_devs.end(); devidx++) {
                std::string label = *devidx + "_ext_in";
                // take a ref to this particular item
                if(last.stats.count(label) > 0) {
                    
                    if(traf_config.interface_speed(*devidx, "download") > fastest_download_speed)
                        fastest_download_speed = traf_config.interface_speed(*devidx, "download"); 
                    nowrate = average_bit_rate(s,label,last_sec, now);
                    bitrate = average_bit_rate(s,label,avg_time, now);
                    if(bitrate >= 0) {
                        render_line(linenum++,
                                    "DOWN",
                                    "ext in", 
                                    (*devidx).c_str(), 
                                    nowrate/traf_config.interface_speed(*devidx, "download"), 
                                    format_rate(bitrate, nowrate).c_str(), 
                                    COLOR_BLUE);
                    }
                }
                // else this label not there so no stats
            }
            
        
        if(do_int_devs) 
            for (devidx = int_devs.begin(); devidx != int_devs.end(); devidx++) { 
                std::string label = *devidx + "_int_out";
                if(last.stats.count(label) > 0) {
                    
                    nowrate = average_bit_rate(s,label,last_sec, now);
                    bitrate = average_bit_rate(s,label,avg_time, now);
                    if(bitrate >= 0) {
                        render_line(linenum++,
                                    "DOWN",
                                    "int out", 
                                    (*devidx).c_str(), 
                                    nowrate/fastest_download_speed, 
                                    format_rate(bitrate, nowrate).c_str(), 
                                    COLOR_BLUE);
                    }
                }
            }
        
        
        
        // Now breakdown of flow through classes, on a CYAN background
        // externals first, then internals as interface speed has to be
        // treated differentley
        Vstring classes = last.class_indexes_in_order();
        StrSet &rules = last.rules;
        
        if(do_int_devs && classes.size() > 0) {
            for (devidx = last.int_devs.begin(); devidx != last.int_devs.end(); devidx++) {
                
                for (classidx = classes.begin(); classidx != classes.end(); classidx++) { 
                    
                    std::string label = *devidx + "_class_" + *classidx;
                    if(last.stats.count(label) > 0) {
                        
                        nowrate = average_bit_rate(s,label,last_sec, now); 
                        bitrate = average_bit_rate(s,label,avg_time, now);
                        if(bitrate >= 0) {
                            render_line(linenum++,
                                        "DOWN",
                                        (*classidx).c_str(), 
                                        (*devidx).c_str(), 
                                        nowrate/fastest_download_speed, 
                                        format_rate(bitrate, nowrate).c_str(), 
                                        COLOR_CYAN);
                        }
                    }
                }
            }
        }
        
        // lastly rules on a MAGENTA background
        
        if(do_int_devs && rules.size() > 0) {
            for (devidx = int_devs.begin(); devidx != int_devs.end(); devidx++) {
                
                for (ruleidx = rules.begin(); ruleidx != rules.end(); ruleidx++) {
                    
                    std::string label = *devidx + "_rule_" + *ruleidx;
                    if(last.stats.count(label) > 0) {
                        
                        nowrate = average_bit_rate(s,label,last_sec, now);
                        bitrate = average_bit_rate(s,label,avg_time, now);
                        if(bitrate >= 0) {
                            render_line(linenum++,
                                        "DOWN",
                                        (*ruleidx).c_str(), 
                                        (*devidx).c_str(), 
                                        nowrate/fastest_download_speed, 
                                        format_rate(bitrate, nowrate).c_str(), 
                                        COLOR_MAGENTA);
                        }
                    }
                }
            }
        }
        if(do_ext_devs)
            for (devidx = ext_devs.begin(); devidx != ext_devs.end(); devidx++) {
                
                std::string label = *devidx + "_ext_out";
                // take a ref to this particular item
                if(last.stats.count(label) > 0) {
                    
                    nowrate = average_bit_rate(s,label,last_sec, now);
                    bitrate = average_bit_rate(s,label,avg_time, now);
                    if(bitrate >= 0) {
                        render_line(linenum++,
                                    "UP  ",
                                    "ext out", 
                                    (*devidx).c_str(), 
                                    nowrate/traf_config.interface_speed(*devidx, "upload"), 
                                    format_rate(bitrate, nowrate).c_str(), 
                                    COLOR_BLUE);
                    }
                }
            }
        if(do_int_devs)
            for (devidx = int_devs.begin(); devidx != int_devs.end(); devidx++) {
                std::string label = *devidx + "_int_in";
                if(last.stats.count(label) > 0) {
                    
                    nowrate = average_bit_rate(s,label,last_sec, now);
                    bitrate = average_bit_rate(s,label,avg_time, now);
                    if(bitrate >= 0) {
                        render_line(linenum++,
                                    "UP  ",
                                    "int in", 
                                    (*devidx).c_str(), 
                                    nowrate/fastest_download_speed, 
                                    format_rate(bitrate, nowrate).c_str(), 
                                    COLOR_BLUE);
                    }
                }
            }
        if(do_ext_devs && classes.size() > 0) {
            for (devidx = last.ext_devs.begin(); devidx != last.ext_devs.end(); devidx++) {
                
                for (classidx = classes.begin(); classidx != classes.end(); classidx++) {
                    
                    
                    std::string label = *devidx + "_class_" + *classidx;
                    if(last.stats.count(label) > 0) {
                        
                        nowrate = average_bit_rate(s,label,last_sec, now);
                        bitrate = average_bit_rate(s,label,avg_time, now);
                        if(bitrate >= 0) {
                            render_line(linenum++,
                                        "UP  ",
                                        (*classidx).c_str(), 
                                        (*devidx).c_str(), 
                                        nowrate/traf_config.interface_speed(*devidx, "upload"), 
                                        format_rate(bitrate, nowrate).c_str(), 
                                        COLOR_CYAN);
                        }
                    }
                }
            }   
        }
        if(do_ext_devs && rules.size() > 0) {
            for (devidx = ext_devs.begin(); devidx != ext_devs.end(); devidx++) {
                
                for (ruleidx = rules.begin(); ruleidx != rules.end(); ruleidx++) {
                    std::string label = *devidx + "_rule_" + *ruleidx;
                    if(last.stats.count(label) > 0) {
                        
                        nowrate = average_bit_rate(s,label,last_sec, now);
                        bitrate = average_bit_rate(s,label,avg_time, now);
                        if(bitrate >= 0) {
                            render_line(linenum++,
                                        "UP  ",
                                        (*ruleidx).c_str(), 
                                        (*devidx).c_str(), 
                                        nowrate/traf_config.interface_speed(*devidx,"upload"), 
                                        format_rate(bitrate, nowrate).c_str(), 
                                        COLOR_MAGENTA);
                        }
                    }
                }
            }
        }
        max_rows = linenum; 
        move(max_rows,0);
        clrtobot(); // rest of the screen
        refresh();  
        // now loose any unchanged stats
        last.compress();

    
        if(max_rows == 0) {
            time_t now;
            time(&now);
            printw("%s", ctime(&now));
            mvprintw(screen_max_rows/2, (screen_max_cols-strlen("NO TRAFFIC AT PRESENT"))/2,"NO TRAFFIC AT PRESENT");
            refresh();
            sleep(1); // ease load        
        }
    }

}
             

