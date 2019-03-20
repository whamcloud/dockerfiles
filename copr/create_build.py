#!/usr/bin/env python2

import subprocess
import time
import os
import sys
import glob
import re
from copr.v3 import Client, CoprNoResultException

version_regex = r"(\d+\.\d+\.\d+)-(?:\d+\.(\d+)|(\d+))\..+"
valid_truthy_args = ["TRUE", "True", "true", "t", "T", "Y", "y", "YES", "Yes", "yes"]


def update_spec_with_new_release(spec_file):
    file = open(spec_file, "r")
    spec = file.read()
    file.close()

    release_matches = re.match(r".*# Release Start\nRelease:.*(\d)%{\?dist}\n# Release End.*", spec, re.DOTALL)
    cur_rel = [x for x in release_matches.groups() if x is not None].pop()
    print("Current release value: {}".format(cur_rel))
    new_rel = "{}.{}".format(int(time.time()), cur_rel)
    print("New release value: {}".format(new_rel))

    return re.sub(
        r".*# Release Start\nRelease:.*(\d)%{\?dist}\n# Release End.*",
        "# Release Start\nRelease:    {}{}\n# Release End".format(new_rel, "%{?dist}"),
        spec,
        re.DOTALL,
    )


def get_spec_file():
    try:
        return glob.glob("*.spec").pop()
    except Exception:
        raise Exception("Spec file could not be found!")


def write_new_spec(spec_file, new_data):
    file = open(spec_file, "w")
    file.write(new_data)
    file.close()


key = os.environ["KEY"]
iv = os.environ["IV"]

owner = os.environ["OWNER"]
project = os.environ["PROJECT"]
package = os.environ.get("PACKAGE")
spec = os.environ.get("SPEC")
srpm_path = os.environ.get("SRPM_PATH", "/tmp/*.src.rpm")
prod = os.environ.get("PROD", False)
local_only = os.environ.get("LOCAL_ONLY", False)

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


try:
    p = glob.glob(srpm_path).pop()
except:
    if prod not in valid_truthy_args:
        print("Development Mode: Updating release to include new epoch.")
        spec_file = get_spec_file()

        updated_spec = update_spec_with_new_release(spec_file)
        write_new_spec(spec_file, updated_spec)

    # Build the SRPM
    subprocess.call(
        [
            "make",
            "-f",
            "/build/.copr/Makefile",
            "srpm",
            "outdir={}".format(srpm_path.replace(os.path.basename(srpm_path), "")),
        ],
        cwd="/build",
    )

    p = glob.glob(srpm_path).pop()

if local_only in valid_truthy_args:
    print("Building the RPM from SRPM Locally.")
    subprocess.call(["rpmbuild", "--rebuild", p])
    rpm = glob.glob("/root/rpmbuild/RPMS/x86_64/*.rpm").pop()
    subprocess.call(["mv", rpm, "/build"])
    print("RPM location: /build/{}".format(os.path.basename(rpm)))
else:
    print("Uploading SRPM to Copr.")
    build = client.build_proxy.create_from_file(owner, project, p)

    while client.build_proxy.get(build.id).state in ["running", "pending", "starting", "importing"]:
        time.sleep(10)
        print("{} running. State: {}".format(build.id, client.build_proxy.get(build.id).state))

    final_state = client.build_proxy.get(build.id).state

    print("build {} {}".format(build.id, final_state))

    if final_state == "failed":
        sys.exit(1)
