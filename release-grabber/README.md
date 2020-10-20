# Release Grabber

This image provides a method to generate a local repo with IML. Images have been tagged for IML 6.2.

## Examples

To generate a repo with the base packages needed for IML 6.2 (Not including Lustre / ZFS)

```sh
docker run -v $(pwd):/build imlteam/release-grabber:6.2
```

To generate a repo with the base packages needed for IML 6.2 (Including patchless Lustre / ZFS)

```sh
docker run -v $(pwd):/build -e WITH_LUSTRE_PATCHLESS=true imlteam/release-grabber:6.2
```

To generate a repo with only the manager packages needed for IML 6.2

```sh
docker run -v $(pwd):/build -e MANAGER_ONLY=true imlteam/release-grabber:6.2
```
