import pytest

from cloudeasy.alicloud import ResourceCenterManager
from ._shared import page_collector


@pytest.fixture(scope='class')
def resource_center(alicloud_config) -> ResourceCenterManager:
    return ResourceCenterManager(alicloud_config)


class TestAlicloudResourceManager:
    def test_get_service_status(self, resource_center):
        assert resource_center.service_status['ServiceStatus'] == "Enabled"

    @pytest.mark.skip(reason="This is only for resource directory accounts")
    def test_search_resource_cross_account(self, resource_center, cache, alicloud_account):
        pager = resource_center.search_resource_cross_account(alicloud_account)
        _ = page_collector(pager)
        cache.set('resource_cross', _[0])
        assert isinstance(_, list)

    @pytest.mark.skip(reason="This is only for resource directory accounts")
    def test_describe_resource_cross_account(self, resource_center, cache):
        resource = cache.get('resource_cross', None)
        detail = resource_center.describe_resource_cross_account(
            resource_id=resource['ResourceId'],
            account_id=resource['AccountId'],
            resource_region=resource['RegionId'],
            resource_type=resource['ResourceType']
        )
        assert detail

    def test_search_resource(self, resource_center, cache):
        pager = resource_center.search_resource_this_account(page_size=50)
        _ = page_collector(pager)
        cache.set('resource', _[0])
        assert isinstance(_, list)

    def test_describe_resource(self, resource_center, cache):
        resource = cache.get('resource', None)
        detail = resource_center.describe_resource_this_account(
            resource_id=resource['ResourceId'],
            resource_region=resource['RegionId'],
            resource_type=resource['ResourceType']
        )
        assert detail
