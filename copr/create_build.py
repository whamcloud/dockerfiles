#!/usr/bin/env python2

import subprocess
import time
import os
import sys
import glob
from copr.v3 import Client, CoprNoResultException

key = os.environ["KEY"]
iv = os.environ["IV"]

owner = os.environ["OWNER"]
project = os.environ["PROJECT"]
package = os.environ.get("PACKAGE")
clone_url = os.environ.get("CLONE_URL")
spec = os.environ.get("SPEC")
ish = os.environ.get("COMMITISH", "master")
srpm_path = os.environ.get("SRPM_PATH")
project_dirname = os.environ.get("PROJECT_DIRNAME")

subprocess.call(
    ["openssl", "aes-256-cbc", "-K", key, "-iv", iv, "-in", "/tmp/copr-mfl.enc", "-out", "/root/.config/copr", "-d"]
)

client = Client.create_from_config_file()

args = (owner, project, package)

if srpm_path:
    try:
        p = glob.glob(srpm_path).pop()
    except:
        subprocess.call(
            [
                "make",
                "-f",
                "/build/.copr/Makefile",
                "srpm",
                "outdir={}".format(srpm_path.replace(os.path.basename(srpm_path), "")),
            ]
        )
        p = glob.glob(srpm_path).pop()

    build = client.build_proxy.create_from_file(owner, project, p)
else:
    try:
        client.package_proxy.get(*args)
    except CoprNoResultException:
        client.package_proxy.add(
            *args,
            source_type="scm",
            source_dict={"clone_url": clone_url, "source_build_method": "make_srpm", "spec": spec, "committish": ish}
        )

    build = client.package_proxy.build(*args, buildopts=None, project_dirname=project_dirname)

while client.build_proxy.get(build.id).state in ["running", "pending", "starting", "importing"]:
    time.sleep(10)
    print("{} running. State: {}".format(build.id, client.build_proxy.get(build.id).state))

final_state = client.build_proxy.get(build.id).state

print("build {} {}".format(build.id, final_state))


if final_state == "failed":
    sys.exit(1)
