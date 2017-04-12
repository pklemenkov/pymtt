import grp
import hashlib
import pwd
import subprocess
import sys
import os
import os.path

import json


DIR = os.path.dirname(os.path.abspath(__file__))
PLIST_CMD = os.path.join(DIR, "plist")
PLIST_BSD_LOCAL = os.path.join(DIR, "BSD.local.dist")


def makeplist(root, prefix='/usr/local', user=None, group=None):
    return gen_manifest(root, prefix, user, group)


def _makeplist(root):
    cmd = "ruby {plist_cmd} -d -m {plist_bsd_local} {root}".format(plist_cmd=PLIST_CMD, plist_bsd_local=PLIST_BSD_LOCAL, root=root)
    return subprocess.check_output([cmd], shell=True).split('\n')


def parse_plist(plist):
    dirs = []
    files = []
    for entry in plist:
        if not entry:
            continue
        data = entry.split('@dirrm ')
        if len(data) == 2:
            dirs.append(data[-1])
        else:
            files.append(data[-1])
    return dirs, files


def get_stat(path, user, group):
    meta = {}
    stat = os.stat(path)
    meta['uname'] = user if user is not None else pwd.getpwuid(stat.st_uid).pw_name
    meta['gname'] = group if group is not None else grp.getgrgid(stat.st_gid).gr_name
    meta['perm'] = oct(stat.st_mode & 0777)

    return meta


def gen_manifest(root, prefix, user, group):
    data = {
        'dirs': [],
        'files': {}
    }
    plist = _makeplist(os.path.join(root, prefix[1:]))
    dirs, files = parse_plist(plist)
    for dir in dirs:
        path = os.path.join(root, prefix[1:], dir)
        data['dirs'].append({os.path.join(prefix, dir): get_stat(path, user, group)})
    for _file in files:
        path = os.path.join(root, prefix[1:], _file)
        with open(path) as f:
            h = hashlib.sha256()
            h.update(f.read())
        meta = get_stat(path, user, group)
        meta['sum'] = h.hexdigest() if not os.path.islink(path) else "-"
        data['files'][os.path.join(prefix, _file)] = meta
    return yaml.safe_dump(data, default_style='"', default_flow_style=True)[1:-1]
