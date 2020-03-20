#! /usr/bin/env python3
#-----------------------------------------------------------------------
import dbus.service
import dbus

from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

#-----------------------------------------------------------------------
#for decorator parameter
DBUS_NAME = 'kr.gooroom.GHub'
DBUS_OBJ = '/kr/gooroom/GHub'
DBUS_IFACE = 'kr.gooroom.GHub'

#-----------------------------------------------------------------------
class GHub(dbus.service.Object):
    """
    |GHub.|
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
        GHub's main loop
        """

        #LOOPING ON
        self._loop.run()

    #@dbus.service.method(DBUS_IFACE, sender_keyword='sender', in_signature='s', out_signature='s')
    def exec_contrlr(self, args, sender=None):
        print('EXEC')
        DBUS_NAME = 'kr.gooroom.GController'
        DBUS_OBJ = '/kr/gooroom/GController'
        DBUS_IFACE = 'kr.gooroom.GController'
        
        system_bus = dbus.SystemBus()
        bus_object = system_bus.get_object(DBUS_NAME, DBUS_OBJ)
        bus_interface = dbus.Interface(bus_object, dbus_interface=DBUS_IFACE)
        r = bus_interface.ctrl_AppA(args)
        return r


    #@dbus.service.method(DBUS_IFACE, sender_keyword='sender', in_signature='s', out_signature='s')
    def get_log(self, args, sender=None):
        print('GET LOG')
        DBUS_NAME = 'kr.gooroom.myAppA'
        DBUS_OBJ = '/kr/gooroom/myAppA'
        DBUS_IFACE = 'kr.gooroom.myAppA'
        
        try:
            print('$0')
            system_bus = dbus.SystemBus()
            print('$1')
            ##수신하는 프로세스 없을 때 timeout 발생, py DBus에 timeout 정하는 
            bus_object = system_bus.get_object(DBUS_NAME, DBUS_OBJ)
            print('$2')
            bus_interface = dbus.Interface(bus_object, dbus_interface=DBUS_IFACE)
            print('$3')
            r = bus_interface.collect_log()
            print('$4')
            return r
        except DBusException as e:
            print(e)
        except:
            import traceback
            print(traceback.format_exc())


    @dbus.service.method(DBUS_IFACE, sender_keyword='sender', in_signature='s', out_signature='s')
    def input_task(self, args, sender=None):
        print('args=', args)
        if args == '1':
            return self.exec_contrlr('1')
        elif args == '2':
            return self.get_log('2')
        elif args == '3':
            return self.exec_contrlr('3')
        elif args == '4':
            return ""
        else:
            return "invalid command\n"

#-----------------------------------------------------------------------
if __name__ == '__main__':
    """
    main
    """

    me = None
    try:
        print("SUBIN")
        me = GHub()
        me.run()

    except:
        raise
