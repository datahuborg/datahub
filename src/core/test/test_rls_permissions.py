from core.db.rls_permissions import RLSPermissionsParser
from django.db.models import signals
from django.test import TestCase
import factory
from mock import patch


class RLS_Permissions(TestCase):

    """Tests all the query rewriter operations in query_rewriter.py."""

    @factory.django.mute_signals(signals.pre_save)
    def setUp(self):
        self.repo_base = "test_repobase"
        self.user = "test_user"
        self.rls_permissions_parser = RLSPermissionsParser(
            self.repo_base, self.user)

    def create_patch(self, name):
        # helper method for creating patches
        patcher = patch(name)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    def test_extract_permission_type(self):
        grant_permission = ("grant select access to kxzhang on test.customer "
                            "where customerid='1'")
        revoke_permission = ("revoke select access to kxzhang on test.customer"
                             " where customerid='1'")
        invalid_permission = ("give select access to kxzhang on test.customer "
                              "where customerid='1'")

        self.assertEqual(
            self.rls_permissions_parser.extract_permission_type(
                grant_permission), "grant")
        self.assertEqual(
            self.rls_permissions_parser.extract_permission_type(
                revoke_permission), "revoke")

        exception_raised = False
        try:
            self.rls_permissions_parser.extract_permission_type(
                invalid_permission)
        except Exception:
            exception_raised = True
        self.assertEqual(exception_raised, True)

    def test_extract_access_type(self):
        select_access = ("grant select access to kxzhang on test.customer "
                         "where customerid='1'")
        insert_access = ("grant insert access to kxzhang on test.customer "
                         "where customerid='1'")
        update_access = ("grant update access to kxzhang on test.customer "
                         "where customerid='1'")
        invalid_access = ("grant invalid access to kxzhang on test.customer "
                          "where customerid='1'")

        self.assertEqual(
            self.rls_permissions_parser.extract_access_type(select_access),
            "select")
        self.assertEqual(
            self.rls_permissions_parser.extract_access_type(insert_access),
            "insert")
        self.assertEqual(
            self.rls_permissions_parser.extract_access_type(update_access),
            "update")

        exception_raised = False
        try:
            self.rls_permissions_parser.extract_access_type(invalid_access)
        except Exception:
            exception_raised = True
        self.assertEqual(exception_raised, True)

    def test_extract_grantee(self):
        grant_permission = ("grant select access to kxzhang on test.customer "
                            "where customerid='1'")
        self.assertEqual(
            self.rls_permissions_parser.extract_grantee(grant_permission),
            "kxzhang")

    def test_extract_table_info(self):
        grant_permission = ("grant select access to kxzhang on test.customer "
                            "where customerid='1'")
        expected_table_info = ["test", "customer"]
        self.assertEqual(
            self.rls_permissions_parser.extract_table_info(grant_permission),
            expected_table_info)

    def test_extract_policy(self):
        grant_permission = ("grant select access to kxzhang on test.customer "
                            "where customerid='1'")
        expected_policy = "customerid='1'"
        self.assertEqual(
            self.rls_permissions_parser.extract_policy(grant_permission),
            expected_policy)

    def test_process_permissions_grant(self):
        grant_permission = ("grant select access to kxzhang on test.customer "
                            "where customerid='1'")

        mock_manager = self.create_patch(
            'core.db.rls_permissions.RowLevelSecurityManager')
        mock_manager = mock_manager.return_value.__enter__.return_value
        mock_create_policy = self.create_patch(
            'core.db.rls_permissions.RowLevelSecurityManager.'
            'create_security_policy')

        self.rls_permissions_parser.process_permissions(grant_permission)
        self.assertTrue(mock_create_policy.called)

    def test_process_permissions_revoke(self):
        mock_manager = self.create_patch(
            'core.db.rls_permissions.RowLevelSecurityManager')
        mock_manager = mock_manager.return_value.__enter__.return_value
        revoke_permission = ("revoke select access to kxzhang on test.customer"
                             " where customerid='1'")
        mock_find_policy = self.create_patch(
            'core.db.rls_permissions.RowLevelSecurityManager.'
            'find_security_policies')
        mock_find_policy.return_value = ["test_policy"]

        mock_remove_policy = self.create_patch(
            'core.db.rls_permissions.RowLevelSecurityManager.'
            'remove_security_policy')

        self.rls_permissions_parser.process_permissions(revoke_permission)
        self.assertTrue(mock_remove_policy.called)
