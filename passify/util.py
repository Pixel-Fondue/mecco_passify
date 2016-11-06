#python

import lx, modo
from symbol import *

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

def reorder(item,mode=TOP):
    index = len(item.parent.children())-1 if mode == TOP else 0
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
