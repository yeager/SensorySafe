"""Startpunkt för SensorySafe-applikationen."""

import sys
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw

from . import __app_id__
from .window import SensorySafeWindow


class SensorySafeApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id=__app_id__)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = SensorySafeWindow(application=self)
        win.present()


def main():
    app = SensorySafeApp()
    return app.run(sys.argv)


if __name__ == "__main__":
    main()
