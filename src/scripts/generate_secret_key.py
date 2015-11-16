#!/usr/bin/env python

# Generates a new SECRET_KEY at src/config/secret_key.py.

from django.utils.crypto import get_random_string
import os.path


def generate_key(path):
    # Same generator used by Django's startproject command.
    # https://github.com/django/django/blob/stable/1.8.x/django/core/management/commands/startproject.py
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    key = get_random_string(50, chars)

    with open(key_path, 'w') as file:
        file.write("SECRET_KEY = '{0}'\n".format(key))

if __name__ == '__main__':
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.dirname(scripts_dir)
    key_path = os.path.join(src_dir, 'config', 'secret_key.py')

    generate_key(key_path)
