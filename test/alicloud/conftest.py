import os

import pytest

from cloudeasy.alicloud import *


@pytest.fixture(scope="session")
def alicloud_config() -> Config:
    return AliCloudConfig.from_ak_sk(
        ak=os.environ['AliCloud_AK'],
        sk=os.environ['AliCloud_SK']
    )


@pytest.fixture(scope="session")
def alicloud_account() -> str:
    return os.environ['AliCloud_Account']
