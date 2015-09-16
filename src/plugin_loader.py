import os
import sys
import traceback
from common import common

if __name__ == '__main__':
    common.ToolsUtil.git_path = os.path.abspath('..')

    if len(sys.argv) < 2:
        print 'usage:python %s plugin_name [args]' % (sys.argv[0])
        exit(1)
    else:
        plugin_name = sys.argv[1]
        for arg in sys.argv:
            common.ToolsUtil.command_args.append(arg)

        sys.argv = sys.argv[1:]
        module_name = 'plugins.' + plugin_name + '.' + plugin_name
        common.ToolsUtil.plugin_path = os.getcwd()
        common.ToolsUtil.plugin_path = os.path.join(common.ToolsUtil.plugin_path, 'plugins')
        common.ToolsUtil.plugin_path = os.path.join(common.ToolsUtil.plugin_path, plugin_name)

        try:
            module_ins = __import__(module_name)
        except ImportError:
            print '\"%s\" plugin not exist' % (plugin_name)
            exit(1)
        except Exception, e:
            traceback.print_exc()
            exit(1)
