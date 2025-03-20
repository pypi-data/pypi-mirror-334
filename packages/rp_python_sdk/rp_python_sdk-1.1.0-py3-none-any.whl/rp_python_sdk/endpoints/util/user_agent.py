from rp_python_sdk.endpoints.util.system_info import get_system_info
from rp_python_sdk.endpoints.util.version_info import get_version_info
from rp_python_sdk.sdk_config import SdkConfig


def build_user_agent(config: SdkConfig) -> str:
    version = get_version_info()
    platform = get_system_info()
    return f"cid-rp-python-sdk/{version} ({platform}) +{config.client_id}"
