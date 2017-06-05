# python

import lx, lxu.command, modo, passify

class commandClass(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def basic_Execute(self, msg, flags):
        try:
            lx.eval('%s %s' (passify.CMD_MANAGER_APPLY_DISCARD, passify.APPLY))
        except:
            pass

        the_pass = lx.eval('layer.active layer:? type:pass')
        if the_pass:
            modo.Scene().duplicateItem(modo.Item(the_pass))

        notifier = passify.Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)

    def arg_UIValueHints(self, index):
        return Notifiers()

    def basic_Enable(self,msg):
        try:
            lx.eval('layer.active layer:? type:pass')
            return True
        except:
            return False

class Notifiers(lxu.command.BasicHints):

    def __init__(self):
        self._notifiers = [('notifier.layerAutoAdd',''),('notifier.editAction','')]

lx.bless(commandClass, passify.CMD_MANAGER_PASS_DUP)
