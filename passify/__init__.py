#python

import modo, lx, lxu, traceback

DEBUG = True
BREAKPOINTS = True
TAG = "PSFY"

try:
    import compositing
except:
    traceback.print_exc()

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

def reorder(item,mode="top"):
    index = len(item.parent.children())-1 if mode == "top" else 0
    item.setParent(item.parent, index)

def debug(message):
    if BREAKPOINTS:
        modo.dialogs.alert("breakpoint",message)
    if DEBUG:
        lx.out("debug:" + message)

def deactivate_passes(pass_group):
    graph_kids = pass_group.itemGraph('itemGroups').forward()
    for p in [i for i in graph_kids if i.type == 'actionclip']:
        p.actionClip.SetActive(0)

def get_selected_and_maskable():
    """Returns a list of object(s) that can be masked."""

    items = modo.Scene().selected

    r = set()
    for item in items:
        if test_maskable(item):
            r.add(item)

    r = list(r)

    return r

def test_maskable(items):

    """Returns True if an item or items can be masked by shader tree masks.
    e.g. Mesh items return True, Camera items return False

    :param items: item(s) to test for maskability
    :type items: object or list of objects
    """

    if not isinstance(items,list):
        items = [items]

    hst_svc = lx.service.Host ()
    scn_svc = lx.service.Scene ()
    hst_svc.SpawnForTagsOnly ()

    r = list()
    for item in items:
        if item.isLocatorSuperType():
            item = item.internalItem

            type = scn_svc.ItemTypeName (item.Type ())

            factory = hst_svc.LookupServer (lx.symbol.u_PACKAGE, type, 1)

            for i in range (factory.TagCount ()):
                if (factory.TagByIndex (i)[0]== lx.symbol.sPKG_IS_MASK):
                    r.append(True)
                else:
                    r.append(False)
        else:
            r.append(False)

    if len(r) == 1:
        return r[0]
    return r

def add_items(items_dict):
    for i in fetch_tagged():
        if i.getTags()[TAG] in items_dict:
            items_dict[i.getTags()[TAG]]["item"] = i

    for k, v in {k:v for k, v in items_dict.iteritems() if "item" not in v}.iteritems():
        items_dict[k]["item"] = modo.Scene().addItem(v["type"])
        items_dict[k]["item"].name = v["name"]
        items_dict[k]["item"].setTag(TAG, k)

        if "reorder" in v:
            reorder(items_dict[k]["item"],v["reorder"])

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

    for k, v in {k:v for k, v in items_dict.iteritems() if "channelWrite" in v}.iteritems():
        for channel_tuple in v["channelWrite"]:
            fetch_by_tag(channel_tuple[0]).channel(channel_tuple[1]).set(channel_tuple[2], action=v["item"].name)

    return items_dict
