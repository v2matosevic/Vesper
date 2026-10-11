# Install Vesper on Windows

1. Open the latest GitHub release and download the installer for Vesper.
2. Run it and choose the install folder. Installation is per user and needs no administrator account.
3. Open the app from Start > Version2. Use Open or drag a local media file onto the window.

Vesper is independent. The default folder is `%LOCALAPPDATA%/Programs/Version2/Vesper`.
The optional Open with checkbox is off by default. No default-app/UserChoice settings are changed.
Choose your own defaults in Windows Settings > Apps > Default apps.
Vesper includes its complete decoder runtime. No extra codec-runtime download is needed.

## Portable use

Download that app's portable ZIP, extract it into a fresh folder and run its EXE. Keep every included file beside the executable. Do not run an EXE directly inside the ZIP. Source archives are for developers,
not an extra runtime requirement.

## Updates and removal

Keep your media in your own folders, separate from the installation. Install a newer release in the
same application folder after you close that application yourself. Do not replace files while it runs.
Uninstall through Windows Settings > Apps > Installed apps. App preferences/caches may remain in
`%LOCALAPPDATA%/Version2`; your original media is not modified by viewing/playback.

These builds are not code-signed. Verify the release's SHA256SUMS.txt against the downloaded file
with PowerShell `Get-FileHash -Algorithm SHA256 <file>`. Do not bypass security warnings if the
download's origin or checksum does not match. Format conditions are explained in FORMATS.md.
