#!/usr/bin/env python2

import subprocess
import time
import os
import sys
import glob
import re
from copr.v3 import Client, CoprNoResultException

valid_truthy_args = ["TRUE", "True", "true", "t", "T", "Y", "y", "YES", "Yes", "yes"]


def update_spec_with_new_release(spec_file):
    file = open(spec_file, "r")
    spec = file.read()
    file.close()

    release_regex1 = r".*# Release Start\nRelease:\s*(\d+)([^\d]*)\n# Release End.*"
    matches1 = re.findall(release_regex1, spec)

    release_regex2 = r".*# Release Start\nRelease:\s*(\d+\.\d+)(.*)\n# Release End.*"
    matches2 = re.findall(release_regex2, spec)

    if matches1:
        [(val, rest)] = matches1

        return re.sub(
            release_regex1,
            "# Release Start\nRelease:    {}.{}{}\n# Release End".format(val, int(time.time()), rest),
            spec,
            re.DOTALL,
        )
    if matches2:
        [(val, rest)] = matches2

        return re.sub(
            release_regex2,
            "# Release Start\nRelease:    {}.{}{}\n# Release End".format(
                val[0 : val.index(".")], int(time.time()), rest
            ),
            spec,
            re.DOTALL,
        )


def write_new_spec(spec_file, new_data):
    file = open(spec_file, "w")
    file.write(new_data)
    file.close()


key = os.environ.get("KEY", "")
iv = os.environ.get("IV", "")

owner = os.environ.get("OWNER", "")
project = os.environ.get("PROJECT", "")
package = os.environ.get("PACKAGE", "")
spec = os.environ.get("SPEC")
srpm_path = os.environ.get("SRPM_PATH", "/tmp/*.src.rpm")
srpm_task = os.environ.get("SRPM_TASK", "srpm")
prod = os.environ.get("PROD", False)
local_only = os.environ.get("LOCAL_ONLY", False)

try:
    p = glob.glob(srpm_path).pop()
except Exception:
    if prod not in valid_truthy_args:
        print("Development Mode: Updating release to include new epoch.")

        updated_spec = update_spec_with_new_release(spec)
        write_new_spec(spec, updated_spec)

    # Build the SRPM
    subprocess.call(
        [
            "make",
            "-f",
            "/build/.copr/Makefile",
            srpm_task,
            "outdir={}".format(srpm_path.replace(os.path.basename(srpm_path), "")),
        ],
        cwd="/build",
    )

    p = glob.glob(srpm_path).pop()

if local_only in valid_truthy_args:
    print("Building the RPM's from SRPM Locally.")
    subprocess.call(["rpmbuild", "--rebuild", p, "-D", "%_topdir /build/_topdir"], cwd="/build")
    print("RPM's located under: /build/_topdir/RPMS")
else:
    subprocess.call(
        ["openssl", "aes-256-cbc", "-K", key, "-iv", iv, "-in", "/tmp/copr-mfl.enc", "-out", "/root/.config/copr", "-d"]
    )

    client = Client.create_from_config_file()

    args = (owner, project, package)

    try:
        client.project_proxy.get(owner, project)
    except CoprNoResultException:
        print("project {}/{} not found. Creating it.".format(owner, project))
        client.project_proxy.add(owner, project, ["epel-7-x86_64"])

    print("Uploading SRPM to Copr.")
    build = client.build_proxy.create_from_file(owner, project, p)

    while client.build_proxy.get(build.id).state in ["running", "pending", "starting", "importing"]:
        time.sleep(10)
        print("{} running. State: {}".format(build.id, client.build_proxy.get(build.id).state))

    final_state = client.build_proxy.get(build.id).state

    print("build {} {}".format(build.id, final_state))

    if final_state == "failed":
        sys.exit(1)
