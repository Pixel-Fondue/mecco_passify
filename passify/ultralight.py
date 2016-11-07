#python

import lx, modo

from add_items import *
from util import *
from var import *

def build(include_environments, include_lumigons, headroom):
    group = fetch_by_tag(ULTRALIGHT_PGRP)

    if not group:
        add_items({
            ULTRALIGHT_PGRP:{
                TAGS:[ULTRALIGHT, ULTRALIGHT_PGRP],
                NAME:message(ULTRALIGHT_PGRP),
                TYPE:"group",
                GTYP:"render"
            }
        })

    group = fetch_by_tag(ULTRALIGHT_PGRP)

    for pass_ in [p for p in group.itemGraph('itemGroups').forward() if p.type == 'actionclip']:
        modo.Scene().removeItems(pass_)

    items = set()
    for i in modo.Scene().iterItems():
        if 'radiance' not in i.channelNames:
            continue
        if not include_environments and i.type == 'environment':
            continue
        if not include_lumigons and not i.isLocatorSuperType():
            continue
        if i.channel('radiance').get() > 0:
            items.add(i)

    for item in items:
        # debug(item.name,True)
        channel = item.channel('radiance')
        if channel not in group.groupChannels:
            group.addChannel(channel)

        actionclip = modo.Scene().addItem('actionclip')
        actionclip.name = " ".join((item.name, message("Pass")))
        actionclip.setTag(TAG, buildTag((ULTRALIGHT_PASS,item.id)))

        itemGraph = lx.object.ItemGraph(modo.Scene().GraphLookup('itemGroups'))
        itemGraph.AddLink(group,actionclip)

    for item in [i._item for i in group.groupChannels]:
        for pass_ in [p for p in group.itemGraph('itemGroups').forward() if p.type == 'actionclip']:
            item.channel('radiance').set(0.0, action=pass_.name)

        value = item.channel('radiance').get()
        value =  value + (value * headroom)
        item.channel('radiance').set(value, action=fetch_by_tag(item.id).name)

    return group

def destroy():
    hitlist = fetch_by_tag(ULTRALIGHT, True)

    if not hitlist:
        return

    modo.Scene().removeItems(hitlist[0])
    if len(hitlist) > 1:
        destroy()
