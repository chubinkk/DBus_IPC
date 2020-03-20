#! /usr/bin/env python3
#GController에 의해 실행/중지됨
#journald 최근 10개의 로그를 수집하는 명령을 처리할 수 있음
#-----------------------------------------------------------------------
import dbus.service
import dbus
import os
import sys
import subprocess

from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

#-----------------------------------------------------------------------
#for decorator parameter
DBUS_NAME = 'kr.gooroom.myAppA'
DBUS_OBJ = '/kr/gooroom/myAppA'
DBUS_IFACE = 'kr.gooroom.myAppA'

#-----------------------------------------------------------------------
class AppA(dbus.service.Object):
    """
    |AppA.|
    """

    def __init__(self):

        #DBUS
        DBusGMainLoop(set_as_default=True)
        self._loop = None
        self._loop = GLib.MainLoop()

        busname = dbus.service.BusName(DBUS_NAME, bus=dbus.SystemBus())
        dbus.service.Object.__init__(self, busname, DBUS_OBJ)

    def run(self):
        """
        AppA's main loop
        """

        #LOOPING ON
        self._loop.run()
    
    @dbus.service.method(DBUS_IFACE, sender_keyword='sender', in_signature='', out_signature='s')
    def collect_log(self, sender=None):
        return str(subprocess.check_output(['sudo', 'journalctl', '-n', '10']))

#-----------------------------------------------------------------------
if __name__ == '__main__':
    """
    main
    """

    me = None
    try:
        me = AppA()
        me.run()

    except:
        raise

