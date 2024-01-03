import os
import uuid

import pytest

from cloudeasy.alicloud import DnsManager
from ._shared import page_collector


@pytest.fixture(scope='class')
def dns_manager(alicloud_config) -> DnsManager:
    return DnsManager(alicloud_config)


@pytest.fixture(scope='class')
def domain(alicloud_config) -> str:
    return os.environ['AliCloud_TEST_DOMAIN']


class TestDnsManager:
    def test_list_domains(self, dns_manager):
        domains = page_collector(dns_manager.list_domains(page_size=5))
        assert isinstance(domains, list)

    def test_list_resource_records(self, dns_manager, domain):
        records = page_collector(dns_manager.list_dns_resource_records(page_size=20, domain=domain))
        assert isinstance(records, list)

    def test_add_resource_record(self, dns_manager, domain, cache):
        random_name = uuid.uuid4().hex
        record = dns_manager.add_resource_record(
            domain=domain,
            hostname=random_name,
            resource_type="A",
            resource_data="127.0.0.1"
        )
        cache.set("test_record", record['RecordId'])
        cache.set("test_record_hostname", random_name)
        assert record['RecordId'] is not None

    def test_query_resource_record(self, dns_manager, domain, cache):
        hostname = cache.get('test_record_hostname', None)
        record_id = cache.get("test_record", None)
        assert hostname is not None
        assert record_id is not None
        records = page_collector(dns_manager.query_resource_record(domain=domain, hostname=hostname))
        assert record_id in [x['RecordId'] for x in records]

    def test_update_resource_record(self, dns_manager, domain, cache):
        record_id = cache.get("test_record", None)
        response = dns_manager.update_resource_record(aliyun_record_id=record_id, hostname="localhost", resource_type="A", resource_data="127.0.0.2")
        assert response['RecordId'] == record_id

    def test_get_resource_record(self, dns_manager, domain, cache):
        record_id = cache.get("test_record", None)
        response = dns_manager.get_resource_record(aliyun_resource_id=record_id)
        assert response['Type'] == 'A' and \
               response['RR'] == 'localhost' and \
               response['Value'] == '127.0.0.2' and \
               response['RecordId'] == record_id

    @pytest.mark.run('last')
    def test_delete_resource_record(self, dns_manager, cache):
        record_id = cache.get("test_record", None)
        assert record_id is not None
        response = dns_manager.delete_resource_record(aliyun_record_id=record_id)
        assert response['RecordId'] == record_id
