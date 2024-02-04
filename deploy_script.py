#!/usr/bin/python3
"""Fabric script to create and deploy an archive to web servers."""

from fabric.api import env, put, run, local
from datetime import datetime
from os.path import exists
from os import makedirs
import os

# Set the environment variables
env.hosts = ['WEB_01_IP_PLACEHOLDER', 'WEB_02_IP_PLACEHOLDER']
env.key_filename = '/root/.ssh/id_rsa'  # Replace with your private key path

def do_pack():
    """Create a compressed archive of the web_static folder."""
    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(timestamp)

        if not exists("versions"):
            makedirs("versions")

        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception as e:
        print(e)
        return None

def do_deploy(archive_path):
    """Distribute an archive to the web servers."""
    if not exists(archive_path):
        return False

    try:
        file_name = os.path.basename(archive_path)
        folder_name = file_name.split('.')[0]

        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/{}".format(file_name))

        # Create the release folder
        run("mkdir -p /data/web_static/releases/{}/".format(folder_name))

        # Uncompress the archive to the folder on the web server
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file_name, folder_name))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(file_name))

        # Move the contents to the proper location
        run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(folder_name, folder_name))

        # Delete the symbolic link /data/web_static/current
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(folder_name))

        return True
    except Exception as e:
        print(e)
        return False

def deploy():
    """Create and distribute an archive to the web servers."""
    archive_path = do_pack()
    if archive_path:
        return do_deploy(archive_path)
    return False
