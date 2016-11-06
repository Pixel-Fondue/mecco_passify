#python

import lx, modo

from add_items import *
from util import *
from symbol import *

def build():
    passify_items = {
        TOGGLER_PGRP:{
            TAGS:[TOGGLER, TOGGLER_PGRP],
            NAME:message(TOGGLER_PGRP),
            TYPE:"group",
            GTYP:"render"
        }
    }

    return add_items(passify_items)

def destroy():
    hitlist = fetch_by_tag(TOGGLER, True)
    # debug(", ".join([i.name for i in hitlist]))
    modo.Scene().removeItems(hitlist[0])
    if len(hitlist) > 1:
        destroy()

def add_selected():
    for item in get_selected_and_maskable():

        channel = item.channel('render')
        if channel not in group.groupChannels:
            group.addChannel(channel)

        actionclip = modo.Scene().addItem('actionclip')
        actionclip.name = " ".join((item.name, message("Pass")))
        actionclip.setTag(TAG, buildTag((TOGGLER_PASS,item.id)))

        itemGraph = lx.object.ItemGraph(modo.Scene().GraphLookup('shadeLoc'))
        itemGraph.AddLink(group,actionclip)

        for pass_ in [p for p in group.itemGraph('shadeLoc').forward() if p.type == 'actionclip']:
            item.channel('render').set(0, action=pass_.name)

        item.channel('render').set(1, action=actionclip.name)

def remove_selected():
    for item in get_selected_and_maskable():
        channel = item.channel('render')
        if channel not in group.groupChannels:
            group.removeChannel(channel)

        actionclip = fetch_by_tag(item.id)
        if actionclip != None:
            modo.Scene().removeItems(actionclip)
