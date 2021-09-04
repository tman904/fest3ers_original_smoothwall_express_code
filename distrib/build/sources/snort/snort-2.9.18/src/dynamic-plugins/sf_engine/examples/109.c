/*
 * VRT RULES
 *
 * Copyright (C) 2014-2021 Cisco and/or its affiliates. All rights reserved.
 * Copyright (C) 2005-2013 Sourcefire, Inc.
 *
 * This file is autogenerated via rules2c, by Brian Caswell <bmc@sourcefire.com>
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "sf_snort_plugin_api.h"
#include "sf_snort_packet.h"
#include "detection_lib_meta.h"

/* declare detection functions */
int rule109eval(void *p);

/* declare rule data structures */
/* precompile the stuff that needs pre-compiled */
/* flow for sid 109 */
/* flow:established, from_server; */
static FlowFlags rule109flow1 =
{
    FLOW_ESTABLISHED|FLOW_TO_CLIENT
};

static RuleOption rule109option1 =
{
    OPTION_TYPE_FLOWFLAGS,
    { &rule109flow1 }
};

/* content for sid 109 */
// content:"NetBus";
static ContentInfo rule109content2 =
{
    (u_int8_t *)("NetBus"), /* pattern (now in snort content format) */
    0, /* depth */
    0, /* offset */
    CONTENT_BUF_NORMALIZED, /* flags */ // XXX - need to add CONTENT_FAST_PATTERN support
    NULL, /* holder for boyer/moore PTR */
    NULL, /* more holder info - byteform */
    0, /* byteform length */
    0, /* increment length*/
    0,                      /* holder for fp offset */
    0,                      /* holder for fp length */
    0,                      /* holder for fp only */
    NULL, // offset_refId
    NULL, // depth_refId
    NULL, // offset_location
    NULL  // depth_location
};

static RuleOption rule109option2 =
{
    OPTION_TYPE_CONTENT,
    { &rule109content2 }
};


/* references for sid 109 */
static RuleReference *rule109refs[] =
{
    NULL
};

RuleOption *rule109options[] =
{
    &rule109option1,
    &rule109option2,
    NULL
};

Rule rule109 = {

   /* rule header, akin to => tcp any any -> any any               */{
       IPPROTO_TCP, /* proto */
       "$HOME_NET", /* SRCIP     */
       "12345:12346", /* SRCPORT   */
       0, /* DIRECTION */
       "$EXTERNAL_NET", /* DSTIP     */
       "any", /* DSTPORT   */
   },
   /* metadata */
   {
       RULE_GID,  /* genid (HARDCODED!!!) */
       109, /* sigid */
       5, /* revision */

       "misc-activity", /* classification */
       0,  /* hardcoded priority XXX NOT PROVIDED BY GRAMMAR YET! */
       "BACKDOOR netbus active",     /* message */
       rule109refs, /* ptr to references */
       NULL /* Meta data */
   },
   rule109options, /* ptr to rule options */
    NULL,                               /* Use internal eval func */
    0,                                  /* Not initialized */
    0,                                  /* Rule option count, used internally */
    0,                                  /* Flag with no alert, used internally */
    NULL /* ptr to internal data... setup during rule registration */
};



/* detection functions */

int rule109eval(void *p) {
    /* cursors, formally known as doe_ptr */
    const u_int8_t *cursor_normal = 0;

    /* flow:established, from_server; */
    if (checkFlow(p, rule109options[0]->option_u.flowFlags)) {
        // content:"NetBus";
        if (contentMatch(p, rule109options[1]->option_u.content, &cursor_normal) > 0) {
            return RULE_MATCH;
        }
    }
    return RULE_NOMATCH;
}

