#python

import lx, lxifc, lxu.command, modo, passify

CMD_NAME_FCL = "passify.listPasses"
CMD_NAME_ACTIVATE = "passify.activatePass"

NONE = "none"

def list_passes(group_tag):
        group = passify.fetch_by_tag(group_tag)

        if group == None:
            return []

        graph_kids = group.itemGraph('itemGroups').forward()
        passes = [i for i in graph_kids if i.type == lx.symbol.a_ACTIONCLIP]

        passes_list = []
        for p in passes:
            passes_list.append(CMD_NAME_ACTIVATE + " {%s} {%s}" % (group_tag, p.id))

        passes_list.append(CMD_NAME_ACTIVATE + " {%s} {%s}" % (group_tag, NONE))

        return passes_list


class passify_fcl(lxifc.UIValueHints):
    def __init__(self, items):
        self._items = items

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_FORM_COMMAND_LIST

    def uiv_FormCommandListCount(self):
        return len(self._items)

    def uiv_FormCommandListByIndex(self,index):
        return self._items[index]


class cmd_passify_fcl(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add('tag', lx.symbol.sTYPE_STRING)
        self.dyna_Add('query', lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_QUERY)

        self.not_svc = lx.service.NotifySys()
        self.notifier = None

    def cmd_NotifyAddClient (self, argument, object):
        if self.notifier is None:
            self.notifier = self.not_svc.Spawn ("passify.notifier", '')
            self.notifier.AddClient (object)

    def cmd_NotifyRemoveClient (self, object):
        if self.notifier is not None:
            self.notifier.RemoveClient (object)

    def arg_UIValueHints(self, index):
        if index == 1:
            return passify_fcl(list_passes(self.dyna_String(0)))
        return Passify_FCL_Notifiers()

    def cmd_Execute(self,flags):
        pass

    def cmd_Query(self,index,vaQuery):
        pass

lx.bless(cmd_passify_fcl, CMD_NAME_FCL)

class Passify_FCL_Notifiers(lxu.command.BasicHints):

    def __init__(self):
        self._notifiers = [('passify.notifier','')]


class cmd_passify_activate(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add('group_tag', lx.symbol.sTYPE_STRING)
        self.dyna_Add('pass_id', lx.symbol.sTYPE_STRING)

    def basic_ButtonName(self):
        group_tag = self.dyna_String(0) if self.dyna_IsSet(0) else None
        item_id = self.dyna_String(1) if self.dyna_IsSet(1) else None
        item_id = item_id if item_id != NONE else None

        if item_id == None:
            return "(none)"

        if item_id != None:
            try:
                return modo.Scene().item(item_id).name
            except:
                return "error: invalid pass id"

    def cmd_Execute(self,flags):
        group_tag = self.dyna_String(0) if self.dyna_IsSet(0) else None
        item_id = self.dyna_String(1) if self.dyna_IsSet(1) else None

        if item_id == NONE:
            graph_kids = passify.fetch_by_tag(group_tag).itemGraph('itemGroups').forward()
            passes = [i for i in graph_kids if i.type == lx.symbol.a_ACTIONCLIP]

            for p in passes:
                p.actionClip.SetActive(0)

        if item_id != NONE:
            try:
                modo.Scene().item(item_id).actionClip.SetActive(1)
            except NameError:
                return lx.symbol.e_FAILED

lx.bless(cmd_passify_activate, CMD_NAME_ACTIVATE)
