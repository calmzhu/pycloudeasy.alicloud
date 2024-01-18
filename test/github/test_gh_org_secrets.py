import os

import pytest

from cloudeasy.github.manager import OrgSecretManager


@pytest.fixture(scope="function")
def org_secret(pat):
    return OrgSecretManager(pat)


@pytest.fixture(scope="session")
def gh_org():
    return os.environ['GH_TEST_ORG']


class TestGithubOrgSecrets:
    def test_list_org_secrets(self, org_secret, gh_org):
        x = org_secret.list_organization_secrets(gh_org)
        assert 'secrets' in x
