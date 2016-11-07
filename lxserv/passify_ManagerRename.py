# python

import lx, lxu.command, modo, passify


class commandClass(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('mode', lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_HIDDEN)
        self.dyna_Add('name', lx.symbol.sTYPE_STRING)

    def basic_Execute(self, msg, flags):
        mode = self.dyna_String(0)
        name = self.dyna_String(1)

        if mode == passify.GROUP:
            the_group = lx.eval('group.current group:? type:pass')
            if the_group:
                modo.Scene().item(the_group).name = name

        if mode == passify.PASS:
            the_pass = lx.eval('layer.active layer:? type:pass')
            if the_pass:
                modo.Scene().item(the_pass).name = name

lx.bless(commandClass, passify.CMD_MANAGER_RENAME)
