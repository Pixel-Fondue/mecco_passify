#python

import lx, modo
from var import *

def message(key_string):
    """Retreive from passify message table."""
    return lx.eval('query messageservice msgfind ? @passify@%s@' % key_string)

def buildTag(parts_list):
    """Concatenate tags comprised of multiple parts."""
    return TAG_SEP.join(parts_list)

def fetch_tagged():
    """Returns a list of modo items with PSFY tags."""
    tagged = set()
    for i in modo.Scene().iterItems():
        if i.hasTag(TAG):
            tagged.add(i)
    return tagged

def fetch_by_tag(tags, list_=False):
    """Looks for an item in the current scene containing any of the supplied PSFY tags.
    Returns the first item encountered by default, or a list if list param is True.
    (Note: PSFY tags are hyphen-separated lists.)

    :param tag: PSFY tag to find
    :type tag: str or list

    :param list_: return a list instead of first encounter
    :type list_: bool"""

    tags = [tags] if isinstance(tags, str) else tags
    found = set()

    for i in fetch_tagged():
        if [t for t in tags if t in i.getTags()[TAG].split(TAG_SEP)]:
            found.add(i)

    if found:
        if list_:
            return list(found)
        if not list_:
            return list(found)[0]

    if not found:
        return None

def reorder(item,mode=TOP):
    """Reorders a modo item to the top or bottom of its parent hierarchy.

    :param item: message to display
    :type item: modo item

    :param mode: where to place within parent
    :type mode: "top" or "bottom" """

    index = len(item.parent.children())-1 if mode == TOP else 0
    item.setParent(item.parent, index)

def debug(message_string, do_break=False):
    """Prints a debug message in the Event Log if DEBUG is True.
    Throws a dialog with the same message if BREAKPOINTS and do_break are True.

    :param message: message to display
    :type message: str

    :param do_break: throw dialog
    :type do_break: bool"""

    if BREAKPOINTS and do_break:
        modo.dialogs.alert("breakpoint", message_string)
    if DEBUG:
        lx.out("debug: " + message_string)

def deactivate_passes(pass_group):
    """Deactivates all passes in supplied pass group.

    :param pass_group: item(s) to test for maskability
    :type pass_group: modo item object or list of objects
    """
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

    if not isinstance(items,(list, tuple)):
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
