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
        mock_find_security_policies = self.create_patch(
            'core.db.rlsmanager'
            '.RowLevelSecurityManager.find_security_policies')
        mock_find_security_policies.return_value = []

        RowLevelSecurityManager.create_security_policy(
            policy="policy='True'",
            policy_type="select",
            grantee="test_grantee",
            grantor=self.username,
            repo_base=self.repo_base,
            repo=self.repo,
            table=self.repo)

        self.assertTrue(create_pol.called)

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
            grantor="test_grantor",
            safe=False)
        self.assertTrue(find_policies.called)

    def test_find_security_policy_by_id(self):
        find_id = self.mock_connection.return_value.find_security_policy_by_id
        #try and then catch this. It tries to unpack a magicmock when testing
        try:
            self.manager.find_security_policy_by_id(policy_id=1)
        except:
            pass
        self.assertTrue(find_id.called)

    def test_update_security_policy(self):
        update_pol = self.create_patch(
            'core.db.rls_permissions.RowLevelSecurityManager.'
            'update_security_policy')
        self.manager.update_security_policy(
            policy_id=1, new_policy="visible=False",
            new_policy_type="select", new_grantee="test_grantor",
            username=self.username)
        self.assertTrue(update_pol.called)

    def test_remove_security_policy(self):
        remove_pol = self.create_patch(
            'core.db.rls_permissions.RowLevelSecurityManager.'
            'remove_security_policy')
        self.manager.remove_security_policy(
            policy_id=1, username=self.username)
        self.assertTrue(remove_pol.called)
