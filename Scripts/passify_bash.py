#python

import modo

import modo

DEBUG = True
BREAKPOINTS = True
TAG = "PSFY"

passify_items = {
    "passify_mask":{
        "name":"Passify Masks",
        "type":"mask",
        "move_to_top":True
    },
    "foreground_mask":{
        "name":"Foreground Mask",
        "type":"mask",
        "parent":"passify_mask",
        "itemGraphs":[
            ('shadeLoc',"fg_grp")
            ]
    },
    "foreground_shader":{
        "name":"Foreground Shader",
        "type":"defaultShader",
        "parent":"foreground_mask",
        "channels":{
            "quaEnable":0,
            "shdEnable":0,
            "lgtEnable":0,
            "fogEnable":0
        }
    },
    "background_mask":{
        "name":"Background Mask",
        "type":"mask",
        "parent":"passify_mask",
        "itemGraphs":[
            ('shadeLoc',"bg_grp")
            ]
    },
    "background_shader":{
        "name":"Background Shader",
        "type":"defaultShader",
        "parent":"background_mask",
        "channels":{
            "quaEnable":0,
            "shdEnable":0,
            "lgtEnable":0,
            "fogEnable":0
        }
    },
    "top_grp":{
        "name":"Passify Groups",
        "type":"group"
    },
    "fg_grp":{
        "name":"Foreground Group",
        "type":"group",
        "parent":"top_grp",
    },
    "bg_grp":{
        "name":"Background Group",
        "type":"group",
        "parent":"top_grp",
    },
    "comp_pGrp":{
        "name":"Passify Compositing",
        "type":"group",
        "GTYP":"render",
        "itemGraphs":[
            ('itemGroups','fg_pass'),
            ('itemGroups','bg_pass')
            ],
        "groupChannels":[
            ('foreground_shader','visCam'),
            ('background_shader','visCam')
        ]
    },
    "fg_pass":{
        "name":"Foreground Pass",
        "type":"actionclip"
    },
    "bg_pass":{
        "name":"Background Pass",
        "type":"actionclip"
    }
}

###

def fetch_tagged():
    tagged = set()
    for i in modo.Scene().iterItems():
        if i.hasTag(TAG):
            tagged.add(i)
    return tagged

def fetch_by_tag(tag):
    for i in fetch_tagged():
        if i.getTags()[TAG] == tag:
            return i
    return None

def move_to_top(item):
    item.setParent(item.parent, len(item.parent.children()))

def debug(message):
    if BREAKPOINTS:
        modo.dialogs.alert("breakpoint",message)
    if DEBUG:
        lx.out("debug:" + message)

def add_items(items_dict):
    for i in fetch_tagged():
        if i.getTags()[TAG] in items_dict:
            items_dict[i.getTags()[TAG]]["item"] = i

    for k, v in {k:v for k, v in items_dict.iteritems() if "item" not in v}.iteritems():
        items_dict[k]["item"] = modo.Scene().addItem(v["type"])
        items_dict[k]["item"].name = v["name"]
        items_dict[k]["item"].setTag(TAG, k)

        if "move_to_top" in v and v["move_to_top"]:
            move_to_top(items_dict[k]["item"])

        if "GTYP" in v:
            items_dict[k]["item"].setTag('GTYP',v["GTYP"])

        if "channels" in v:
            for channel, value in v["channels"].iteritems():
                items_dict[k]["item"].channel(channel).set(value)

    for k, v in {k:v for k, v in items_dict.iteritems() if "parent" in v}.iteritems():
        items_dict[k]["item"].setParent(fetch_by_tag(v["parent"]))

    for k, v in {k:v for k, v in items_dict.iteritems() if "itemGraphs" in v}.iteritems():
        links = v["itemGraphs"] if hasattr(v["itemGraphs"], '__iter__') else [v["itemGraphs"]]

        for i in links:
            itemGraph = lx.object.ItemGraph(modo.Scene().GraphLookup(i[0]))
            itemGraph.AddLink(items_dict[k]["item"],fetch_by_tag(i[1]))

    for k, v in {k:v for k, v in items_dict.iteritems() if "groupChannels" in v}.iteritems():
        for channel_tuple in v["groupChannels"]:
            channel = fetch_by_tag(channel_tuple[0]).channel(channel_tuple[1])
            if channel not in items_dict[k]["item"].groupChannels:
                items_dict[k]["item"].addChannel(channel)

    return items_dict

def deactivate_passes(pass_group):
    graph_kids = pass_group.itemGraph('itemGroups').forward()
    for p in [i for i in graph_kids if i.type == 'actionclip']:
        p.actionClip.SetActive(0)

###


add_items(passify_items)
