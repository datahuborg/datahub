from core.db.rlsmanager import RowLevelSecurityManager
from django.db.models import signals
from django.contrib.auth.models import User
from django.test import TestCase
import factory
from mock import patch


class RowLevelSecurityManagerTests(TestCase):

    @factory.django.mute_signals(signals.pre_save)
    def setUp(self):
        self.username = "test_username"
        self.repo_base = "test_username"
        self.repo = "test_repo"
        self.table = "test_table"
        self.user = User.objects.create_user(self.username)

        self.mock_connection = self.create_patch(
            'core.db.rlsmanager.core.db.connection.DataHubConnection')

        self.manager = RowLevelSecurityManager(self.username, self.repo_base)

    def create_patch(self, name):
        # helper method for creating patches
        patcher = patch(name)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    def test_create_security_policy(self):
        create_pol = self.mock_connection.return_value.create_security_policy
        self.manager.create_security_policy(policy="policy='True'",
                                            policy_type="select",
                                            grantee="test_grantee",
                                            repo=self.repo,
                                            table=self.repo)
        self.assertTrue(create_pol.called)

    def test_list_security_policies(self):
        list_policy = self.mock_connection.return_value.list_security_policies
        self.manager.list_security_policies(self.repo, self.table)
        self.assertTrue(list_policy.called)

    def test_find_security_policies(self):
        find_policies = self.mock_connection.return_value\
            .find_security_policies
        RowLevelSecurityManager.find_security_policies(
            repo_base=self.repo_base,
            repo=self.repo,
            table=self.table,
            policy="visible='True",
            policy_type="insert",
            grantee="test",
            grantor="test_grantor")
        self.assertTrue(find_policies.called)

    def test_find_security_policy_by_id(self):
        find_id = self.mock_connection.return_value.find_security_policy_by_id
        self.manager.find_security_policy_by_id(policy_id=1)
        self.assertTrue(find_id.called)

    def test_update_security_policy(self):
        update_pol = self.mock_connection.return_value.update_security_policy
        self.manager.update_security_policy(
            policy_id=1, new_policy="visible=False",
            new_policy_type="select", new_grantee="test_grantor")
        self.assertTrue(update_pol.called)

    def test_remove_security_policy(self):
        remove_pol = self.mock_connection.return_value.remove_security_policy
        self.manager.remove_security_policy(policy_id=1)
        self.assertTrue(remove_pol.called)
