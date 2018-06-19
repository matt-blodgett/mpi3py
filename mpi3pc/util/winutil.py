import wmi
import queue
import threading
import pythoncom


QDiskEvents = queue.Queue()
QProccessEvents = queue.Queue()


EVENT_OP = 'operation'
EVENT_CR = 'creation'
EVENT_DEL = 'deletion'
EVENT_MOD = 'modification'


DRIVE_TYPES = {
  0: 'Unknown',
  1: 'No Root Directory',
  2: 'Removable Disk',
  3: 'Local Disk',
  4: 'Network Drive',
  5: 'Compact Disc',
  6: 'RAM Disk'
}


# def running_processes():
#     w = wmi.WMI()
#
#     kwargs = {'Name': 'notepad.exe'}
#
#     for process in w.Win32_Process(**kwargs):
#         print(process.ProcessId)
#
#     # for process in w.Win32_Process():
#     #     print(process.ProcessId, process.Name, '-', process.ParentProcessId)
#
# def sound_devices():
#     w = wmi.WMI()
#     for wmi_object in w.Win32_SoundDevice():
#         print(wmi_object.Caption)


def removable_drives():
    w = wmi.WMI()
    for disk in w.Win32_LogicalDisk(DriveType=2):
        yield disk.DeviceID


def disk_space(disk_id):
    w = wmi.WMI()
    disk = w.Win32_LogicalDisk(DeviceID=disk_id)[0]
    size, free = int(disk.Size), int(disk.FreeSpace)
    allocated = int(size-free)
    return size, free, allocated


class MonitorQueue(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

    def run(self):
        while True:
            process = QProccessEvents.get()
            print(process.event_type, '-', process.Name, '-', process.timestamp, '-', process.CreationClassName)

            # disk = QDiskEvents.get()
            # print(disk.event_type, '-', disk.Name, '-', disk.VolumeName, '-', disk.DriveType, '-', DRIVE_TYPES[disk.DriveType], '-', disk.CreationClassName)


class WmiMonitor(threading.Thread):

    def __init__(self, event, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = True

        kwargs['notification_type'] = event
        self._watch_kwargs = kwargs
        self._Win32_Class = None
        self._monitor = True
        self._queue = None

    def release(self):
        self._monitor = False

    def run(self):
        pythoncom.CoInitialize()

        wmi_connect = wmi.WMI()
        wmi_instance = getattr(wmi_connect, self._Win32_Class)
        wmi_listener = wmi_instance.watch_for(**self._watch_kwargs)

        while self._monitor:
            wmi_object = wmi_listener()
            self._queue.put(wmi_object)

        pythoncom.CoUninitialize()


class ProcessMonitor(WmiMonitor):

    def __init__(self, event, **kwargs):
        WmiMonitor.__init__(self, event, **kwargs)
        self._queue = QProccessEvents
        self._Win32_Class = 'Win32_Process'


class DiskMonitor(WmiMonitor):

    def __init__(self, event, **kwargs):
        WmiMonitor.__init__(self, event, **kwargs)
        self._queue = QDiskEvents
        self._Win32_Class = 'Win32_LogicalDisk'

#
#
# PROCESS
# print(process.Name)
# print(process.ExecutablePath)
# print(process.ProcessId)
# print(process.ThreadCount)
# print(process.ParentProcessId)


# DISK
# print(disk.Caption)
# print(disk.DeviceID)
# print(disk.DriveType)
# print(disk.FreeSpace)
# print(disk.Size)
# print(disk.VolumeName)
# print(disk.Availability)
# print(disk.SystemName)
# print(process.CreationClassName)
#


# def notepad_test():
#     w = wmi.WMI()
#
#     filename = r'C:\\Users\\mablodgett\\Desktop\\test.txt'
#     process = w.Win32_Process
#     process_id, result = process.Create(CommandLine='notepad.exe ' + filename)
#     watcher = w.watch_for(
#       notification_type='deletion',
#       wmi_class='Win32_Process',
#       delay_secs=1,
#       ProcessId=process_id
#     )
#
#     watcher()
#     print('This is what you wrote:')
#     print(open(filename).read())
#
#
# def notepad_test_2():
#     w = wmi.WMI()
#
#     process_id, return_value = w.Win32_Process.Create(CommandLine='notepad.exe')
#     for process in w.Win32_Process(ProcessId=process_id):
#         print(process.ProcessId, process.Name)
#
#     result = process.Terminate()

# w = wmi.WMI()
# for wmi_object in w.Win32_Processor():
#     print(wmi_object.Name)
