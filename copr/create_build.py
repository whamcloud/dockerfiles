#!/usr/bin/env python2

import subprocess
import time
import os
import sys
import glob
import re
from copr.v3 import Client, CoprNoResultException
from packaging import version

version_regex = r"(\d+\.\d+\.\d)+-(?:\d+\.(\d+)|(\d+))\..+"


def get_version_from_spec(spec_file):
    file = open(spec_file, "r")
    spec = file.read()
    file.close()

    return re.match(r".*Version:.*(\d+\.\d+\.\d+).*", spec, re.DOTALL).group(1)


def update_spec_with_new_release(spec_file, release_num):
    file = open(spec_file, "r")
    spec = file.read()
    file.close()

    return re.sub(
        r".*# Release Start\nRelease:.*(\d)%{\?dist}\n# Release End.*",
        "# Release Start\nRelease:    {}{}\n# Release End".format(release_num, "%{?dist}"),
        spec,
        re.DOTALL,
    )


def get_release_num(builds, version_regex, spec_file):
    release_num = 1

    try:
        build = sorted(builds, key=lambda x: x.ended_on, reverse=True)[0]
        v = build.source_package.get("version")
        matches = re.match(version_regex, v)
        ver, rel = [x for x in matches.groups() if x is not None]

        spec_ver = get_version_from_spec(spec_file)

        if version.parse(ver) == version.parse(spec_ver):
            release_num = rel + 1
    except Exception:
        print("Initial build.")

    return release_num


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
    if not prod in ["TRUE", "True", "true", "t", "T", "Y", "y", "YES", "Yes", "yes"]:
        spec_file = get_spec_file()
        epoch = int(time.time())
        builds = client.build_proxy.get_list(*args, status="succeeded")
        release_num = get_release_num(builds, version_regex, spec_file)

        updated_spec = update_spec_with_new_release(spec_file, "{}.{}".format(epoch, release_num))
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

build = client.build_proxy.create_from_file(owner, project, p)


while client.build_proxy.get(build.id).state in ["running", "pending", "starting", "importing"]:
    time.sleep(10)
    print("{} running. State: {}".format(build.id, client.build_proxy.get(build.id).state))

final_state = client.build_proxy.get(build.id).state

print("build {} {}".format(build.id, final_state))


if final_state == "failed":
    sys.exit(1)
