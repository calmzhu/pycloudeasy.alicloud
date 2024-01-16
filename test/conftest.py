import os
import sys
import time

import pytest

cwd = os.path.dirname(__file__)

sys.path.append(os.path.dirname(cwd))


@pytest.fixture(scope="function")
def pat():
    yield os.environ['GH_PAT']
    # avoid send too much request at a very short time while running pytest
    time.sleep(0.5)
