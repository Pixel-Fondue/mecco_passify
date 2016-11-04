#python

import lx, modo, passify

passify_items = {
    "comping_masks":{
        "name":"Compositing Masks",
        "type":"mask",
        "move_to_top":True
    },
    "foreground_mask":{
        "name":"Foreground Mask",
        "type":"mask",
        "parent":"comping_masks",
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
        "parent":"comping_masks",
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
        "type":"actionclip",
        "channelWrite":[
            ('background_shader','visCam',0),
            ('foreground_shader','visCam',1)
        ]
    },
    "bg_pass":{
        "name":"Background Pass",
        "type":"actionclip",
        "channelWrite":[
            ('background_shader','visCam',1),
            ('foreground_shader','visCam',0)
        ]
    }
}

###

def build(hide_env_fg, hide_env_bg):
    passify.add_items(passify_items)

    group = passify.fetch_by_tag('comp_pGrp')
    for i in modo.Scene().items('environment'):
        group.removeChannel('visCam',i)
        if hide_env_fg:
            group.addChannel(i.channel('visCam'))
            i.channel('visCam').set(0, action=passify.fetch_by_tag("fg_pass").name)
        if hide_env_bg:
            group.addChannel(i.channel('visCam'))
            i.channel('visCam').set(0, action=passify.fetch_by_tag("bg_pass").name)


def add_selected(layer_tag):
    for i in passify.get_selected_and_maskable():
        itemGraph = lx.object.ItemGraph(modo.Scene().GraphLookup('itemGroups'))
        itemGraph.AddLink(passify.fetch_by_tag(layer_tag),i)

def remove_selected(layer_tag):
    for i in passify.get_selected_and_maskable():
        itemGraph = lx.object.ItemGraph(modo.Scene().GraphLookup('itemGroups'))
        itemGraph.DeleteLink(passify.fetch_by_tag(layer_tag),i)
