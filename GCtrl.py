#! /usr/bin/env python3
#Ctrl.py
#AppA를 실행/정지시키는 모듈
#-----------------------------------------------------------------------
import dbus.service
import dbus
import os

from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

#-----------------------------------------------------------------------
#for decorator parameter
DBUS_NAME = 'kr.gooroom.GController'
DBUS_OBJ = '/kr/gooroom/GController'
DBUS_IFACE = 'kr.gooroom.GController'

#-----------------------------------------------------------------------
class GCtrl(dbus.service.Object):
    """
    |GCtrl.|
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
        GCtrl's main loop
        """

        #LOOPING ON 
        self._loop.run()

    @dbus.service.method(DBUS_IFACE, sender_keyword='sender', in_signature='s', out_signature='s')
    def ctrl_AppA(self, args, sender=None):
        if args == '1':
            os.system('systemctl start myAppA.service')
            return "AppA started\n"
        elif args == '3':
            os.system('systemctl stop myAppA.service')
            return "AppA stopped\n"
        return "Invalid cmd"

#-----------------------------------------------------------------------
if __name__ == '__main__':
    """
    main
    """

    me = None
    try:
        me = GCtrl()
        me.run()

    except:
        raise
