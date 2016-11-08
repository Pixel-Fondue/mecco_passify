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
            lx.eval('edit.apply')
            lx.eval('passify.ManagerAutoAdd 0')

        if mode == passify.DISCARD:
            lx.eval('edit.discard')
            lx.eval('passify.ManagerAutoAdd 0')

    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())

    def basic_Enable(self,msg):
        try:
            cmd_svc = lx.service.Command()
            cmd = cmd_svc.Spawn(lx.symbol.iCTAG_NULL, 'edit.apply')
            try:
                cmd.Enable(msg)
                return True
            except:
                return False
        except Exception:
            lx.out(traceback.format_exc())

    def arg_UIValueHints(self, index):
        return Channel_Notifiers()

lx.bless(commandClass, passify.CMD_MANAGER_APPLY_DISCARD)


class Channel_Notifiers(lxu.command.BasicHints):

    def __init__(self):
        self._notifiers = [('notifier.editAction','')]
