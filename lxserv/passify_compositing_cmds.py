#Must be inside a folder called 'lxserv' somewhere in a MODO search path.

import lx
import lxu.command
import traceback
import passify

CMD_SETUP = 'passify.setupCompositing'
CMD_ADD_TO_LAYER = 'passify.addToCompLayer'
CMD_REMOVE_FROM_LAYER = 'passify.removeFromCompLayer'

class cmd_setup_class(lxu.command.BasicCommand):

    _first_run = True

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('hide_environments_fg', lx.symbol.sTYPE_BOOLEAN)
        self.dyna_Add('hide_environments_bg', lx.symbol.sTYPE_BOOLEAN)

    def arg_UIHints(self, index, hints):
        if index == 0:
            hints.Label("Hide Environments in Foreground")
        if index == 1:
            hints.Label("Hide Environments in Background")

    def cmd_DialogInit(self):
        if self._first_run:
            self.attr_SetInt(0, 1)
            self.attr_SetInt(1, 1)
            self.after_first_run()

    @classmethod
    def after_first_run(cls):
        cls._first_run = False

    def cmd_Flags (self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def CMD_EXE(self, msg, flags):
        hide_environments_fg = self.dyna_Bool(0) if self.dyna_IsSet(0) else True
        hide_environments_bg = self.dyna_Bool(1) if self.dyna_IsSet(1) else True

        passify.compositing.build(
            hide_environments_fg,
            hide_environments_bg
            )

    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())

    def basic_Enable(self,msg):
        return True

    def basic_ButtonName(self):
        return "Setup Compositing"

lx.bless(cmd_setup_class, CMD_SETUP)

class cmd_add_to_layer(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('layer_tag', lx.symbol.sTYPE_STRING)

    def cmd_Flags (self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def CMD_EXE(self, msg, flags):
        layer_tag = self.dyna_String(0)
        passify.compositing.add_selected(layer_tag)

    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())

    def basic_Enable(self,msg):
        return True

    def basic_ButtonName(self):
        if self.dyna_String(0) == 'bg_grp':
            return "Add to Background Group"
        if self.dyna_String(0) == 'fg_grp':
            return "Add to Foreground Group"

lx.bless(cmd_add_to_layer, CMD_ADD_TO_LAYER)

class cmd_remove_from_layer(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('layer_tag', lx.symbol.sTYPE_STRING)

    def cmd_Flags (self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def CMD_EXE(self, msg, flags):
        layer_tag = self.dyna_String(0)
        passify.compositing.remove_selected(layer_tag)

    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())

    def basic_Enable(self,msg):
        return True

    def basic_ButtonName(self):
        if self.dyna_String(0) == 'bg_grp':
            return "Remove from Background Group"
        if self.dyna_String(0) == 'fg_grp':
            return "Remove from Foreground Group"

lx.bless(cmd_remove_from_layer, CMD_REMOVE_FROM_LAYER)
