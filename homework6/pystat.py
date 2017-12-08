#!/bin/python

import commands
import json
import os
import re


def get_versions(name, rexp):
    l = os.listdir("/home/" + name + "/.pyenv/versions")
    r = re.compile(rexp)
    versions = filter(r.match, l)
    return versions


def pack_parser (s):
    tmp_dict = {}
    for x in s.split('\n'):
        tmp_dict.update({x.split('==')[0]: x.split('==')[1]})
    return tmp_dict


if __name__ == "__main__":
    info = []
    output_file_name = "./python-info"

    if os.path.exists('/usr/bin/python'):
        d = {}
        version = re.findall('[\d.]+', commands.getoutput("/usr/bin/python --version"))[0]
        d.update({"version": version, "python exec": "/usr/bin/python", "name": "Python system " + version})
    if os.path.exists('/usr/bin/pip'):
        packs = commands.getoutput("/usr/bin/pip freeze")
        if packs:
            d.update({"installed packages": pack_parser(packs)})
    else:
        d.update({"pip exec": None, "installed packages": "Please install pip to discover packages"})

    info.append(d)

    users = os.listdir("/home/")

    for user in users:
        if os.path.exists("/home/" + user + "/.pyenv"):
            versions = get_versions(user, "\d+\.\d+\.\d+")
            if versions:
                for version in versions:
                    d = {}
                    d = {"version": version, "name": "Python pyenv " + version}
                    if os.path.exists("/home/" + user + "/.pyenv/versions/" + version + "/bin/python"):
                        d.update({"python exec": "/home/" + user + "/.pyenv/versions/" + version + "/bin/python"})
                    if os.path.exists("/home/" + user + "/.pyenv/versions/" + version + "/bin/pip"):
                        d.update({"pip exec": "/home/" + user + "/.pyenv/versions/" + version + "/bin/pip"})
                    d.update({"installed packages": None})
                    if d['pip exec']:
                        packs = commands.getoutput(d['pip exec'] + " freeze")
                        if packs:
                            d.update({"installed packages": pack_parser(packs)})
                    d.update({"virtualenvs": []})
                    venvs = os.listdir("/home/" + user + "/.pyenv/versions/" + version + "/envs/")
                    for venv in venvs:
                        d1 = {"name" : venv}
                        if os.path.exists("/home/" + user + "/.pyenv/versions/" + version + "/envs/" + venv + "/bin/pip"):
                            venv_packs = commands.getoutput("/home/" + user + "/.pyenv/versions/" + version + "/envs/" + venv + "/bin/pip freeze")
                            if venv_packs:
                                d1.update({"installed packages": pack_parser(venv_packs)})
                        d["virtualenvs"].append(d1)
                    info.append(d)

    f = open(output_file_name + ".json", 'w')
    f.write(json.dumps(info)+"\n")
    f.close()

    try:
        import yaml
        f = open(output_file_name + ".yaml", 'w')
        stream = yaml.dump(info, default_flow_style=False)
        f.write(stream.replace('\n- ', '\n\n- '))
        f.close()
    except Exception:
        print "Can't save to yaml file, please install module"