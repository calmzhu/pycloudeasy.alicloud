import os

import pytest

from cloudeasy.github import GithubClient


@pytest.fixture(scope="session")
def gh_client():
    x = GithubClient()
    x.login_via_pat(os.environ['GH_PAT'])
    return x


@pytest.fixture(scope="session")
def gh_org():
    return os.environ['GH_TEST_ORG']


@pytest.fixture(scope="session")
def gh_repo():
    return os.environ['GH_TEST_REPO'].split("/")


@pytest.fixture(scope="session")
def secret_meta():
    return "TEST_SECRET_NAME", "TEST_SECRET_VALUE"


class TestGithubRepoSecrets:

    @pytest.mark.run(order=1)
    def test_get_repo_public_key(self, gh_client, gh_repo, cache):
        key = gh_client.get_repo_public_key(*gh_repo)
        cache.set('PUBLIC_KEY', key)
        assert 'key' in key and 'key_id' in key

    @pytest.mark.run(order=2)
    def test_set_repo_secrets(self, gh_client, gh_repo, cache, secret_meta):
        key = cache.get("PUBLIC_KEY", None)
        _NAME, _DATA = secret_meta
        gh_repo_owner, gh_repo_name = gh_repo
        secret = gh_client.put_repo_secrets(
            gh_repo_owner, gh_repo_name, _NAME,
            data=_DATA,
            encrypted_key_id=key['key_id'],
            public_key=key['key'])
        assert secret is True

    @pytest.mark.run(order=2)
    def test_set_repo_secrets(self, gh_client, gh_repo, cache):
        gh_repo_owner, gh_repo_name = gh_repo
        x = gh_client.set_repo_secret(gh_repo_owner, gh_repo_name, "TEST_SECRET_NAME", "TEST_SECRET_VALUE")
        assert x is True

    @pytest.mark.run(order=3)
    def test_get_repo_secrets(self, gh_client, gh_repo, cache, secret_meta):
        secret_name, secret_value = secret_meta
        gh_repo_owner, gh_repo_name = gh_repo
        secret = gh_client.get_repo_secret(gh_repo_owner, gh_repo_name, secret_name)
        assert secret['name'] == secret_name

    @pytest.mark.run(order=3)
    def test_list_repo_secrets(self, gh_client, gh_repo, cache):
        x = gh_client.list_repo_secrets(*gh_repo)
        cache.set("SECRET_NAME", x["secrets"][0]['name'])
        assert bool(cache.get("SECRET_NAME", None)) is True


class TestGithubOrgSecrets:
    def test_list_org_secrets(self, gh_client, gh_org):
        x = gh_client.list_organization_secrets(gh_org)
        print(x)
