#!/usr/bin/env python3

import subprocess
import time
import os
import sys
from copr.v3 import Client, CoprNoResultException

key = os.environ["KEY"]
iv = os.environ["IV"]

owner = os.environ["OWNER"]
project = os.environ["PROJECT"]
package = os.environ["PACKAGE"]
clone_url = os.environ["CLONE_URL"]
ish = os.environ.get("COMMITISH", "master")
spec = os.environ["SPEC"]

res = subprocess.run(
    ["openssl", "aes-256-cbc", "-K", key, "-iv", iv, "-in", "/tmp/copr-mfl.enc", "-out", "/root/.config/copr", "-d"]
)

if res.stderr:
    print("stdout: {}, stderr: {}".format(res.stdout, res.stderr))

client = Client.create_from_config_file()

args = (owner, project, package)

try:
    client.package_proxy.get(*args)
except CoprNoResultException:
    client.package_proxy.add(
        *args, source_type="scm", source={"clone_url": clone_url, "source_build_method": "make_srpm", "spec": spec}
    )

build = client.package_proxy.build(*args)

while client.build_proxy.get(build.id).state in ["running", "pending", "starting", "importing"]:
    time.sleep(10)
    print("{} running. State: {}".format(build.id), client.build_proxy.get(build.id).state)

final_state = client.build_proxy.get(build.id).state

print("build {} finshed. State: {}".format(build.id, final_state))


if final_state == "failed":
    sys.exit(1)
