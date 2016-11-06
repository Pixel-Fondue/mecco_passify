#python

import lx, modo

from add_items import *
from util import *
from symbol import *

passify_items = {
    QUICKFLOOR_MASKS:{
        NAME:"QuickFloor Masks",
        TYPE:"mask",
        REORDER:TOP
    },
    QUICKFLOOR_FG_MASK:{
        NAME:"Everything Else Mask",
        TYPE:"mask",
        PARENT:QUICKFLOOR_MASKS,
        REORDER:BOTTOM
    },
    QUICKFLOOR_FG_SHADER:{
        NAME:"Everything Else Shader",
        TYPE:"defaultShader",
        PARENT:QUICKFLOOR_FG_MASK,
        CHANNELS:{
            "quaEnable":0,
            "shdEnable":0,
            "lgtEnable":0,
            "fogEnable":0
        }
    },
    QUICKFLOOR_BG_MASK:{
        NAME:"Background Mask",
        TYPE:"mask",
        PARENT:QUICKFLOOR_MASKS,
        ITEMGRAPHS:[
            ('shadeLoc',QUICKFLOOR_BG_GRP)
            ],
        REORDER:TOP
    },
    QUICKFLOOR_BG_SHADER:{
        NAME:"Background Shader",
        TYPE:"defaultShader",
        PARENT:"quickFloor_bg_mask",
        CHANNELS:{
            "quaEnable":0,
            "shdEnable":0,
            "lgtEnable":0,
            "fogEnable":0
        }
    },
    QUICKFLOOR_BG_GRP:{
        NAME:"QuickFloor Group",
        TYPE:"group"
    },
    QUICKFLOOR_PGRP:{
        NAME:"QuickFloor Passes",
        TYPE:"group",
        GTYP:"render",
        ITEMGRAPHS:[
            ('itemGroups',QUICKFLOOR_FG_PASS),
            ('itemGroups',QUICKFLOOR_BG_PASS)
            ],
        GROUPCHANNELS:[
            (QUICKFLOOR_FG_SHADER,'visCam'),
            (QUICKFLOOR_BG_SHADER,'visCam')
        ]
    },
    QUICKFLOOR_FG_PASS:{
        NAME:"Everything Else",
        TYPE:"actionclip",
        CHANNELWRITE:[
            (QUICKFLOOR_BG_SHADER,'visCam',0),
            (QUICKFLOOR_FG_SHADER,'visCam',1)
        ]
    },
    QUICKFLOOR_BG_PASS:{
        NAME:"Background Pass",
        TYPE:"actionclip",
        CHANNELWRITE:[
            (QUICKFLOOR_BG_SHADER,'visCam',1),
            (QUICKFLOOR_FG_SHADER,'visCam',0)
        ]
    }
}

###

def build(hide_env_bg):
    add_items(passify_items)

    group = fetch_by_tag(QUICKFLOOR_PGRP)
    for i in modo.Scene().items('environment'):
        group.removeChannel('visCam',i)
        group.addChannel(i.channel('visCam'))
        i.channel('visCam').set(0, action=fetch_by_tag(QUICKFLOOR_FG_PASS).name)
        if hide_env_bg:
            i.channel('visCam').set(0, action=fetch_by_tag(QUICKFLOOR_BG_PASS).name)

def destroy():
    hitlist = list(fetch_tagged())
    # debug(", ".join([i.name for i in hitlist]))
    modo.Scene().removeItems(hitlist[0])
    if len(hitlist) > 1:
        destroy()

def add_selected():
    for i in get_selected_and_maskable():
        itemGraph = lx.object.ItemGraph(modo.Scene().GraphLookup('itemGroups'))
        itemGraph.AddLink(fetch_by_tag(QUICKFLOOR_BG_GRP),i)

def remove_selected():
    for i in get_selected_and_maskable():
        itemGraph = lx.object.ItemGraph(modo.Scene().GraphLookup('itemGroups'))
        itemGraph.DeleteLink(fetch_by_tag(QUICKFLOOR_BG_GRP),i)
