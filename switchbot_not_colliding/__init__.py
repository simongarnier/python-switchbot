from typing import List

from switchbot_not_colliding.client import SwitchBotClient
from switchbot_not_colliding.devices_not_colliding import Device
from switchbot_not_colliding.remotes import Remote

__version__ = "2.2.3"


class SwitchBot:
    def __init__(self, token: str, secret: str, nonce: str = ""):
        self.client = SwitchBotClient(token, secret, nonce)

    def devices(self) -> List[Device]:
        response = self.client.get("devices")
        return [
            Device.create(client=self.client, id=device["device_id"], **device)
            for device in response["body"]["device_list"]
        ]

    def device(self, id: str) -> Device:
        # Currently, SwitchBot API does not support to retrieve device_name,
        # enable_cloud_service and hub_device_id without getting all device list
        # Therefore, for backward compatibility reason,
        # we query all devices first, then return the matching device
        for device in self.devices():
            if device.id == id:
                return device
        raise ValueError(f"Unknown device {id}")

    def remotes(self) -> List[Remote]:
        response = self.client.get("devices")
        return [
            Remote.create(client=self.client, id=remote["device_id"], **remote)
            for remote in response["body"]["infrared_remote_list"]
        ]

    def remote(self, id: str) -> Remote:
        for remote in self.remotes():
            if remote.id == id:
                return remote
        raise ValueError(f"Unknown remote {id}")
