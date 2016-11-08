import lx, lxu.command, passify

class commandClass(lxu.command.BasicCommand):
    def basic_Execute(self, msg, flags):
        lx.eval('select.drop channel')
        try:
            lx.eval('group.scan mode:sel type:chan grpType:pass')
            lx.eval('tool.set channel.haul on')
        except:
            pass

lx.bless(commandClass, passify.CMD_MANAGER_HAUL_GROUP_CHANNELS)
