# python

import lx, lxu.command, modo, passify


class commandClass(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('mode', lx.symbol.sTYPE_STRING)

    def basic_Execute(self, msg, flags):
        mode = self.dyna_String(0)

        if mode == passify.GROUP:
            the_group = lx.eval('group.current group:? type:pass')
            if the_group:
                modo.Scene().removeItems(the_group)

        if mode == passify.PASS:
            the_pass = lx.eval('layer.active layer:? type:pass')
            if the_pass:
                modo.Scene().removeItems(the_pass)

lx.bless(commandClass, passify.CMD_MANAGER_DELETE)
