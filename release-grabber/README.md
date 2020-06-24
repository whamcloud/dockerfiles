# Release Grabber

This image provides a method to generate a local repo with IML. Images have been tagged for IML 6.0 and 6.1.

## Examples

To generate a repo with the base packages needed for IML 6.1 (Not including Lustre / ZFS)

```sh
docker run -v $(pwd):/build imlteam/release-grabber:6.1
```

To generate a repo with the base packages needed for IML 6.1 (Including patchless Lustre / ZFS)

```sh
docker run -v $(pwd):/build -e WITH_LUSTRE_PATCHLESS imlteam/release-grabber:6.1
```

To generate a repo with only the manager packages needed for IML 6.1

```sh
docker run -v $(pwd):/build -e MANAGER_ONLY imlteam/release-grabber:6.1
```

To generate a repo for IML 6.0 (Not including Lustre / ZFS):

```sh
docker run -v $(pwd):/build imlteam/release-grabber:6.0
```
