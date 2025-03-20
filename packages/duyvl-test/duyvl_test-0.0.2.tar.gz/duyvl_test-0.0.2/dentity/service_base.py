"""
Base class and helper methods for the Service wrappers
"""

import base64
from abc import ABC
from typing import Dict

from betterproto import Message
from grpclib.client import Channel

import dentity
from dentity.proto.sdk.options.v1 import DentityOptions
from dentity.proto.services.account.v1 import AccountProfile
from dentity.proto.services.common.v1 import ResponseStatus
from dentity.dentity_util import dentity_config, create_channel


class ServiceBase(ABC):
    """
    Base class for service wrapper classes, provides the metadata functionality in a consistent manner.
    """

    def __init__(self, server_config: DentityOptions | Channel):
        if isinstance(server_config, Channel):
            # TODO - Cane we get the server_config from the channel?
            current_config = DentityOptions(
                server_endpoint=server_config._host,
                server_port=server_config._port,
                auth_token="",
                server_use_tls=server_config._scheme != "http",
            )
            self.service_options: DentityOptions = current_config or dentity_config()
            self._channel = server_config
        else:
            self.service_options: DentityOptions = server_config or dentity_config()
            self._channel: Channel = create_channel(self.service_options)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        """Close the underlying channel"""
        if hasattr(self, "_channel") and self._channel is not None:
            try:
                self._channel.close()
            except RuntimeError:
                # If the event loop is closed, NBD.
                pass

    def set_auth_token(self, auth_token: str | bytes | AccountProfile) -> None:
        if type(auth_token) is AccountProfile:
            auth_token = base64.urlsafe_b64encode(bytes(auth_token)).decode("utf8")
        if type(auth_token) is bytes:
            auth_token = base64.urlsafe_b64encode(auth_token).decode("utf-8")
        self.service_options.auth_token = auth_token

    def build_metadata(self, request: Message = None) -> Dict[str, str]:
        """
        Create call metadata by setting required authentication headers via `AccountProfile`
        :return: authentication headers with base-64 encoded Oberon
        """
        call_metadata = {
            "TrinsicSDKLanguage".lower(): "python",
            "TrinsicSDKVersion".lower(): dentity.__version__(),
        }
        auth_token = ""
        if request is not None:
            if self.service_options and self.service_options.auth_token:
                auth_token = self.service_options.auth_token

            call_metadata["authorization"] = f"Bearer {auth_token}"
        return call_metadata

    @property
    def channel(self):
        """Underlying channel"""
        return self._channel


class ResponseStatusException(Exception):
    """
    Exception raised when an action has a non-success response status.
    """

    def __init__(self, action: str, status: ResponseStatus):
        super().__init__(f"{action}, status={repr(status)}")
        self.status = status

    @staticmethod
    def assert_success(status: ResponseStatus, action: str) -> None:
        if status != ResponseStatus.SUCCESS:
            raise ResponseStatusException(action, status)
