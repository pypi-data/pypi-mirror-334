"""
Utility functions for the Dentity services SDK
"""

import asyncio
import dataclasses
import platform
from datetime import datetime
from distutils.util import strtobool
from os import getenv
from typing import Tuple

from grpclib.client import Channel

from dentity.proto.sdk.options.v1 import DentityOptions


def dentity_config(auth_token: str = None) -> DentityOptions:
    """
    Test Server configuration - if environment variables aren't set, default to production
    Args:
        auth_token: Existing auth token to use (instead of `clone_options_with_auth_token(trinsic_config(), auth_token)`)
    Returns:
        [DentityOptions](/reference/proto/#DentityOptions)
    """
    endpoint = getenv("TEST_SERVER_ENDPOINT", "prod.dentity.cloud")
    port = int(getenv("TEST_SERVER_PORT", 443))
    use_tls = bool(strtobool(getenv("TEST_SERVER_USE_TLS", "true")))
    return DentityOptions(
        server_endpoint=endpoint,
        server_port=port,
        server_use_tls=use_tls,
        auth_token=auth_token,
    )


def clone_options_with_auth_token(
    options: DentityOptions, auth_token: str
) -> DentityOptions:
    """
    Clone the service options and replace the authentication token.
    Args:
        options:
        auth_token:

    Returns:
        [DentityOptions](/reference/proto/#DentityOptions)
    """
    cloned = dataclasses.replace(options)
    cloned.auth_token = auth_token
    return cloned


def create_channel(config: DentityOptions) -> Channel:
    """
    Create the channel from the provided URL
    Args:
        config: Server configuration
    Returns:
        connected `Channel`
    """
    return Channel(
        host=config.server_endpoint, port=config.server_port, ssl=config.server_use_tls
    )


def convert_to_epoch_seconds(
    valid_from: datetime, valid_until: datetime
) -> Tuple[float, float]:
    """
    Convert provided datetime objects to seconds since the UNIX epoch - this works around windows strptime() limitations.
    Args:
        valid_from: start time, or 1970-01-01
        valid_until: end time, or 9999-12-31
    Returns:
        valid_from, valid_until as floating point seconds.
    """
    valid_from = valid_from or datetime(1, 1, 1)
    valid_until = valid_until or datetime(9999, 12, 31)
    epoch = datetime(1970, 1, 1)
    valid_from_epoch = (valid_from - epoch).total_seconds()
    valid_until_epoch = (valid_until - epoch).total_seconds()
    return valid_from_epoch, valid_until_epoch


def set_eventloop_policy() -> None:
    """Set the event loop policy on windows to eliminate the `RuntimeError: Event loop is closed`"""
    # https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
