# -*- coding: utf-8 -*-
import os
import subprocess

from . import paths

_VERSION = None


def get_version():
    global _VERSION
    if _VERSION is None:
        _VERSION = _from_version_file() or _from_poetry() or _from_pi() or _from_git() or ''
    return _VERSION


def _from_version_file():
    project_root = paths.root_path()
    if project_root is None:
        return None
    version_file_path = os.path.join(project_root, 'VERSION')
    if os.path.exists(version_file_path):
        return open(version_file_path, 'r').read().strip()
    return None


def _from_poetry():
    try:
        version = subprocess.check_output(['poetry', 'version', '--short'], stderr=subprocess.DEVNULL)
        return version.decode().strip()
    except Exception:
        return None


def _from_pi():
    try:
        version = subprocess.check_output(['pi', 'version', '-s'], stderr=subprocess.DEVNULL)
        return version.decode().strip()
    except Exception:
        return None


def _from_git():
    try:
        u = subprocess.check_output(['git', 'describe', '--always'], stderr=subprocess.DEVNULL)
        d = subprocess.check_output(['git', 'rev-list', '--count', 'HEAD'], stderr=subprocess.DEVNULL)
        b = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], stderr=subprocess.DEVNULL)
        return f'{u.decode().strip()}-r{d.decode().strip()}-{b.decode().strip()}'
    except Exception:
        return None
