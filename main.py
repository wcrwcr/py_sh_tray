from lib import sys_tray


def main():
    app = sys_tray.shTrayApp(False)
    app.MainLoop()


if __name__ == '__main__':
    main()