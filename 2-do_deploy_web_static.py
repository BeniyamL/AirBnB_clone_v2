#!/usr/bin/python3
""" module to deploy the archive to the server """

from fabric.api import run, put, env, sudo
import os.path


env.hosts = ["34.75.251.99", "35.237.151.121"]


def do_deploy(archive_path):
    """ function to deploy the archive to the remote server"""

    if os.path.exists(archive_path) is False:
        return False
    arch_name = archive_path.split("/")[-1]
    f_name = arch_name.split(".")[0]
    arch_path = "/tmp/{}".format(arch_name)
    f_path = "/data/web_static/releases/{}/".format(f_name)

    put(archive_path, arch_path)
    run("sudo mkdir -p {}".format(f_path))
    run("sudo tar -xzf {} -C {}".format(arch_path, f_path))
    run("sudo rm {}".format(arch_path))
    run("sudo mv -f {}web_static/* {}".format(f_path, f_path))
    run("sudo rm -rf {}web_static".format(f_path))
    run("sudo rm -rf /data/web_static/current")
    run("sudo ln -s {} /data/web_static/current".format(f_path))
    return True
