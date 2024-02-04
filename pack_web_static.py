#!/usr/bin/python3
"""
Script to generate a .tgz archive from the contents of the web_static folder
"""

import os
from datetime import datetime
import tarfile

def do_pack():
    """
    Create a tar gzipped archive of the directory web_static.
    """
    # Create the folder if it doesn't exist
    if not os.path.exists("versions"):
        os.makedirs("versions")

    # Generate the archive path
    now = datetime.utcnow()
    archive_path = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        now.year, now.month, now.day, now.hour, now.minute, now.second)

    try:
        with tarfile.open(archive_path, "w:gz") as archive:
            archive.add("web_static", arcname=os.path.basename("web_static"))

        return archive_path
    except Exception as e:
        print(f"Error creating archive: {e}")
        return None

if __name__ == "__main__":
    result = do_pack()
    if result:
        print(f"web_static packed: {result}")
    else:
        print("Packaging failed.")
