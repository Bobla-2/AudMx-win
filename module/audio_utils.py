from pycaw.api.mmdeviceapi import IMMDeviceEnumerator
from pycaw.constants import CLSID_MMDeviceEnumerator
from pycaw.pycaw import IAudioEndpointVolume
from pycaw.api.audiopolicy import (
    IAudioSessionControl2,
    IAudioSessionManager2,
)
from pycaw.constants import (
    DEVICE_STATE,
    EDataFlow,
)
from pycaw.utils import AudioSession, AudioUtilities
import comtypes
from comtypes import CLSCTX_ALL
from module.ENUM.enums import dictVolumeDBtoProsent


def set_master_volume(vol: float):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    volume.SetMasterVolumeLevel(dictVolumeDBtoProsent[int(vol * 100)], None)

def set_all_master_volume(vol: float):
    devices = GetAllDevicesActive()
    for dev in devices:
        interface = dev._dev.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        volume.SetMasterVolumeLevelScalar(vol, None)

def GetAllDevicesActive():
    devices = []
    deviceEnumerator = comtypes.CoCreateInstance(
        CLSID_MMDeviceEnumerator, IMMDeviceEnumerator, comtypes.CLSCTX_INPROC_SERVER
    )
    if deviceEnumerator is None:
        return devices

    collection = deviceEnumerator.EnumAudioEndpoints(
        EDataFlow.eRender.value, DEVICE_STATE.ACTIVE.value
    )
    if collection is None:
        return devices

    count = collection.GetCount()
    for i in range(count):
        dev = collection.Item(i)
        if dev is not None:
            devices.append(AudioUtilities.CreateDevice(dev))
    return devices


def get_all_sessions_all_devices():
    all_sessions = []

    devices = GetAllDevicesActive()

    for device in devices:
        try:
            iface = device._dev.Activate(IAudioSessionManager2._iid_, CLSCTX_ALL, None)
            session_manager = iface.QueryInterface(IAudioSessionManager2)
            enumerator = session_manager.GetSessionEnumerator()

            for i in range(enumerator.GetCount()):
                session = enumerator.GetSession(i)
                ctl2 = session.QueryInterface(IAudioSessionControl2)
                audio_session = AudioSession(ctl2)
                all_sessions.append(audio_session)

        except Exception as e:
            print(f"Ошибка при обработке устройства: {e}")

    return all_sessions