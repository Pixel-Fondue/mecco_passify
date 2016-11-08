import lx, modo, lxu.command, traceback, passify

class myGreatCommand(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('state', lx.symbol.sTYPE_BOOLEAN)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_QUERY)

    def cmd_Flags (self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def CMD_EXE(self, msg, flags):
        if lx.eval('layer.autoAdd state:?') == 'on':

            lx.eval('layer.autoAdd state:off')
            preset = lx.eval('scheme.loadPreset ?')
            lx.eval('scheme.loadPreset %s' % preset)

        elif lx.eval('layer.autoAdd state:?') == 'off':

            active_group = lx.eval('group.current group:? type:pass')

            if not active_group:
                modo.dialogs.alert(passify.message('error','no_active_pass'))
                return lx.symbol.e_FAILED

            color = lx.eval('user.value mecco_passify_autoAddColor ?')
            lx.eval('layer.autoAdd state:on')
            lx.eval('pref.value color.backdrop {%s}' % color)
            lx.eval('pref.value color.deformers {%s}' % color)

    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())

    def cmd_Query(self,index,vaQuery):
        va = lx.object.ValueArray()
        va.set(vaQuery)
        if index == 0:
            if lx.eval('layer.autoAdd state:?') == 'on':
                va.AddInt(1)
            else:
                va.AddInt(0)
        return lx.result.OK

    def arg_UIValueHints(self, index):
        return Cropper_Channel_Notifiers()

    def basic_Enable(self,msg):
        return True


class Cropper_Channel_Notifiers(lxu.command.BasicHints):

    def __init__(self):
        self._notifiers = [('notifier.layerAutoAdd','')]

lx.bless(myGreatCommand, passify.CMD_MANAGER_AUTOADD)
