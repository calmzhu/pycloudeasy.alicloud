import os

import pytest

from cloudeasy.alicloud import SecurityGroupManager, SecurityGroupRuleSchema


@pytest.fixture(scope='class')
def security_group_manager(alicloud_config) -> SecurityGroupManager:
    return SecurityGroupManager(alicloud_config)


@pytest.fixture(scope='class')
def sg_id():
    return os.environ['AliCloud_ECS_SG']


class TestSecurityGroupManager:
    @pytest.mark.run(order=0)
    def test_create_rule(self, security_group_manager, sg_id, cache):
        rules: list[SecurityGroupRuleSchema] = [
            {"Policy": "accept", "Description": "pycloudeasy-test", "SourceCidrIp": "127.2.0.1", "PortRange": "443/443", "IpProtocol": "TCP"},
            {"Policy": "accept", "Description": "pycloudeasy-test", "SourceCidrIp": "172.0.0.1", "PortRange": "443/443", "IpProtocol": "TCP"}
        ]
        yes = security_group_manager.create_rules(sg_id, rules)
        assert isinstance(yes, dict)

    @pytest.mark.run(order=1)
    def test_list_rules(self, security_group_manager, sg_id, cache):
        rules = security_group_manager.get_sg_rules(sg_id)
        assert isinstance(rules, list)
        cache.set("rules", rules)

    @pytest.mark.run(order=2)
    def test_delete_rules(self, security_group_manager, sg_id, cache):
        rules = cache.get("rules", [])
        rule_ids = [x['SecurityGroupRuleId'] for x in rules if x['Description'] == 'pycloudeasy-test']
        assert len(rule_ids) > 0
        yes = security_group_manager.delete_rules(sg_id, rule_ids)
        assert isinstance(yes, dict)
