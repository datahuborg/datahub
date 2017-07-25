#!/usr/bin/env python
"""
Build and modify pdb password database
"""
import os
import re
import sys
import time
import gnupg
import yaml
import shutil
import getpass
import argparse
import logging

class PDB(object):
    """
    All password db management routines
    """
    def __init__(self, pdbfile="pdb.gpg", keyserver="pool.sks-keyservers.net", passphrase=""):
        self.pdbfile = os.path.abspath(pdbfile)
        self._pdbfilebak = "{0}.bak".format(pdbfile)
        self.gpg = gnupg.GPG()
        self.keyserver = keyserver
        self.passphrase = passphrase
        self.logger = logging.getLogger(__name__)

    def init(self):
        """
        Initialize a new password db store
        """
        self.y = {"version": int(time.time())}
        recipient_email = raw_input("Enter Email ID: ")
        self.import_key(emailid=recipient_email)
        self.encrypt(emailid_list=[recipient_email])

    def list_users(self):
        """
        Get user list from the encrypted pdb file
        """
        crypt = self._decrypt_file()

        self.logger.info(crypt.stderr)
        raw_userlist = crypt.stderr.split('\n')
        userlist = list()
        for index, line in enumerate(raw_userlist):
            if 'gpg: encrypted' in line:
                m = re.search('ID (\w+)', line)
                keyid = m.group(1).strip()
                userline = raw_userlist[index+1].strip()
                userlist.append((keyid, userline))
        return userlist

    def list_user_emails(self):
        userlist = self.list_users()
        keys, emails = zip(*userlist)
        r = re.compile(r'(\b[\w.]+@+[\w.]+.+[\w.]\b)')
        emailid_list = list()
        for email in emails:
            try:
                emailid_list.append(r.search(email).group(1))
            except AttributeError:
                pass

        return list(emailid_list)

    def list_user_keyids(self):
        userlist = self.list_users()
        key_list, emailid_list = zip(*userlist)
        return list(key_list)

    def add_user(self, recipient_email):
        """
        Add user to encryption
        """
        self.import_key(emailid=recipient_email)
        emailid_list = self.list_user_emails()
        self.y = self.decrypt()
        emailid_list.append(recipient_email)
        self.encrypt(emailid_list=emailid_list)

    def delete_user(self, recipient_email):
        """
        Remove user from encryption
        """
        emailid_list = self.list_user_emails()
        if recipient_email not in emailid_list:
            raise Exception("User {0} not present!".format(recipient_email))
        else:
            emailid_list.remove(recipient_email)
            self.y = self.decrypt()
            self.encrypt(emailid_list=emailid_list)

    def _decrypt_file(self):
        try:
            with open(self.pdbfile, 'rb') as f:
                crypt = self.gpg.decrypt_file(f)
                if crypt.status == 'need passphrase':
                    if not self.passphrase:
                        self.passphrase = getpass.getpass('Passphrase needed: ')
                    with open(self.pdbfile, 'rb') as f:
                        crypt = self.gpg.decrypt_file(f, passphrase=self.passphrase)
        except IOError as e:
                raise e

        return crypt

    def decrypt(self):
        crypt = self._decrypt_file()
        y = yaml.load(crypt.data)
        return y

    def list_keys(self):
        y = self.decrypt()
        print y.keys()

    def show_key(self, key, y=None):
        if not y:
            y = self.decrypt()
        try:
            print y[key]
        except (KeyError, TypeError):
            exit("Key not found")

    def _delete_key(self, key):
        self.y = self.decrypt()
        try:
            payload = self.y[key]
        except KeyError:
            print "Key not found"
            exit(1)

        print "{0} : {1}".format(key, payload)
        if not raw_input("Remove the above entry? (y/n) ") == "y":
            exit(1)

        del(self.y[key])

    def delete_key(self, key):
        self._delete_key(key)
        emailid_list = self.list_user_emails()
        self.encrypt(emailid_list=emailid_list)

    def _add_key(self, key, payload):
        try:
            self.y = self.decrypt()
            self.y[key] = yaml.load(payload)
        except (KeyError, TypeError):
            exit("ERROR: Adding Key failed!")

    def add_key(self, key):
        payload = raw_input("Enter YAML payload: \n")
        try:
            yaml.load(payload)
        except ValueError:
            exit("YAML validation failed!")

        print "Adding the following key and payload: "
        print "{0} : {1}".format(key, payload)
        if not raw_input("Proceed? (y/n) ") == "y":
            exit(1)

        self._add_key(key, payload)
        emailid_list = self.list_user_emails()
        self.encrypt(emailid_list=emailid_list)

    def import_key(self, keyid=None, emailid=None):
        if keyid:
            local_key_list = " ".join([key['subkeys'][0][0] for key in self.gpg.list_keys()])
            search_criteria = keyid
        elif emailid:
            local_key_list = "".join([key['uids'][0] for key in self.gpg.list_keys()])
            search_criteria = emailid
        else:
            raise ValueError("keyid or emailid not set")

        self.logger.debug(local_key_list)
        if search_criteria in local_key_list:
            self.logger.info("Key already present for {0}, skipping...".format(
                search_criteria))
            return

        self.logger.info("Searching keys on keyserver %s" % self.keyserver)
        results = self.gpg.search_keys(search_criteria,
                                       keyserver=self.keyserver)
        try:
            keyid = results[0]['keyid']
            user = results[0]['uids']
            if self.gpg.recv_keys(self.keyserver, keyid):
                self.logger.info("Added {0} - {1}".format(user, keyid))
                return (keyid, user)
        except IndexError:
            raise Exception("Key not found! Invalid User or Keyid")

    def import_user_keys(self):
        users = self.list_users()
        for user in users:
            self.import_key(keyid=user[0])

    def encrypt(self, emailid_list=None, keyid_list=None):
        data = yaml.dump(self.y, default_flow_style=False, explicit_start=True)
        if emailid_list:
            local_emailid_list = "".join([gpgkey['uids'][0] for gpgkey in self.gpg.list_keys()])
            for email in emailid_list:
                if not email in local_emailid_list:
                    raise ValueError("Key not found for user {0)!".format(email))

        elif keyid_list:
            raise NotImplemented

        self.logger.info("Encrypting with: ")
        for email in emailid_list:
            self.logger.info("{0}".format(emailid_list))
        try:
            shutil.copy(self.pdbfile, self._pdbfilebak)
        except IOError:
            pass
        c = self.gpg.encrypt(data, emailid_list, output=self.pdbfile,
                             armor=False, always_trust=True)

        if not os.path.exists(self.pdbfile):
            print self.pdbfile
            shutil.copy(self._pdbfilebak, self.pdbfile)
            os.remove(self._pdbfilebak)

        if c.status:
            print "Encryption complete"
        else:
            print "Error: Encryption Failed"
            print c.stderr
            exit(1)

def main():
    cli = argparse.ArgumentParser(description="Utility to work with the pdb password store")

    group = cli.add_mutually_exclusive_group()
    group.add_argument("-lk", "--list-keys", help="List all top-level keys", action="store_true")
    group.add_argument("-sk", "--show-key", help="show key payload")
    group.add_argument("-ak", "--add-key", help="Add new key")
    group.add_argument("-dk", "--delete-key", help="Remove Key")

    group = cli.add_mutually_exclusive_group()
    group.add_argument("-lu", "--list-users", help="List all users", action="store_true")
    group.add_argument("-au", "--add-user", help="Add user to pdb")
    group.add_argument("-du", "--delete-user", help="Remove user from pdb")

    cli.add_argument("-p", "--passphrase", help="GPG passpharse", default="")
    cli.add_argument("-f", "--file", help="Path to pdb file", default="pdb.gpg")
    cli.add_argument("-ks", "--keyserver", help="Keyserver to use", default="pool.sks-keyservers.net")
    cli.add_argument("-i", "--init", help="initilize a new pdb database", action="store_true")
    cli.add_argument("-imp", "--import-all", help="Import public keys for all users", action="store_true")
    cli.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    cli.add_argument('-d', '--debug', action='store_true', help='Debug output')

    args = cli.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    elif args.debug:
        logging.basicConfig(level=logging.DEBUG)

    pdb = PDB(pdbfile=args.file, keyserver=args.keyserver, passphrase=args.passphrase)

    if args.init:
        pdb.init()
    elif args.list_keys:
        pdb.list_keys()
    elif args.show_key:
        pdb.show_key(args.show_key)
    elif args.add_key:
        y = pdb.add_key(args.add_key)
    elif args.delete_key:
        y = pdb.delete_key(args.delete_key)
    elif args.import_all:
        pdb.import_user_keys()
    elif args.list_users:
        user_list = pdb.list_users()
        for keyid, user in user_list:
            print "KeyID: {0} - User: {1}".format(keyid.encode('utf-8'), user.encode('utf-8'))
    elif args.add_user:
        pdb.add_user(args.add_user)
    elif args.delete_user:
        pdb.delete_user(args.delete_user)
    else:
        cli.print_help()

if __name__ == '__main__':
    main()

# vim: autoindent tabstop=4 expandtab smarttab shiftwidth=4 softtabstop=4 tw=0
