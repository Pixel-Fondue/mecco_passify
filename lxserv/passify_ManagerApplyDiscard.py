# python

import lx, lxu.command, modo, passify, traceback


class commandClass(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('mode', lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_QUERY)

    def CMD_EXE(self, msg, flags):
        mode = self.dyna_String(0)

        if mode == passify.APPLY:
            try:
                lx.eval('!edit.apply')
            except:
                pass
            try:
                lx.eval('!passify.ManagerAutoAdd 0')
            except:
                pass

        if mode == passify.DISCARD:
            if test_edit_apply():
                lx.eval('!edit.apply')
            try:
                lx.eval('!passify.ManagerAutoAdd 0')
            except:
                pass

    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())

    def basic_Enable(self,msg):
        try:
            return test_edit_apply()
        except Exception:
            lx.out(traceback.format_exc())

    def arg_UIValueHints(self, index):
        return Channel_Notifiers()

lx.bless(commandClass, passify.CMD_MANAGER_APPLY_DISCARD)


class Channel_Notifiers(lxu.command.BasicHints):

    def __init__(self):
        self._notifiers = [('notifier.editAction','')]
