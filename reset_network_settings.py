import sys

import tools

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if '-y' in sys.argv[1] or 'y' in sys.argv[1]:
            tools.reset_network_settings(ask_usr=False)
            exit(0)
    tools.reset_network_settings()
