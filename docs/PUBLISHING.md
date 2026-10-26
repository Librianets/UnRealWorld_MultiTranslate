Package 0.25 for game 3.89.1: GUI/updater 0.25; bootstrap/DLL/catalogues 0.24.
Build the hook bootstrap first, then the GUI. Include URWUpdater.ps1.
Run utilities/package_release.cmd: both ZIPs must include their edition-specific update_manifest.json.
Publish both ZIPs plus SHA256SUMS.txt together in the latest stable release.
The updater requires the exact Hook_VERSION.zip / Hook_VERSION_lite.zip asset names and hook-VERSION tag.
Never replace published assets or move existing tags. Old releases remain available.
