import socket

import anvil.server
import servicemanager
import win32event
import win32service
import win32serviceutil

from abc import ABCMeta, abstractmethod


class AnvilWindowsService(
    win32serviceutil.ServiceFramework, metaclass=ABCMeta
):
    _svc_name_ = "AnvilWindowsService"
    _svc_display_name_ = "Anvil Windows Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def run(
        self, anvil_key,
        pre_connect=None,
        pre_connect_args=None,
        post_connect=None,
        post_connect_args=None
    ):
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        rc = None
        if pre_connect:
            pre_connect(*pre_connect_args)
        anvil.server.connect(anvil_key)
        if post_connect:
            post_connect(*post_connect_args)
        while rc != win32event.WAIT_OBJECT_0:
            rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)

    @abstractmethod
    def SvcDoRun(self):
        pass


def manage_service(service, args):
    if len(args) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(service)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(service)
