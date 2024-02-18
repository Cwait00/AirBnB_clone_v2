#!/usr/bin/python3
"""
Fabric script for deploying web_static content to web servers.
"""

from fabric.api import env, put, run
from os.path import exists

# Define the hosts and SSH key
env.hosts = ['172.17.0.3', 'WEB_01_IP_PLACEHOLDER', 'WEB_02_IP_PLACEHOLDER']
env.key_filename = '/root/.ssh/id_rsa'  # Use the full path to your private key


def do_deploy(archive_path):
    """
    Deploy the web_static content to the web servers.

    Args:
        archive_path (str): Path to the archive file to deploy.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    # Check if the archive file exists
    if not exists(archive_path):
        print("Error: Archive file does not exist.")
        return False

    # Extract file name and folder name from the archive path
    file_name = archive_path.split('/')[-1]
    folder_name = file_name.split('.')[0]

    try:
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

        print("New version deployed!")
        return True
    except Exception as e:
        print("Error:", str(e))
        return False


def check_status():
    """
    Check if hbnb_static/0-index.html is available on both web servers.
    """
    for host in env.hosts:
        status_code = run("curl -s -o /dev/null -w '%{http_code}' http://{}/hbnb_static/0-index.html".format(host))
        if status_code == '200':
            print("hbnb_static/0-index.html is available on", host)
        else:
            print("hbnb_static/0-index.html is not available on", host)


# Example usage:
# do_deploy('path/to/your/archive.tgz')
# check_status()
