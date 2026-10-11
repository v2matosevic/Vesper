# Vesper 0.2.1 verification

Verified on Windows 11 x64. Scoped evidence is not a guarantee for every file, GPU or Windows configuration.

| App | Installed release checks |
| --- | --- |
| Vesper | 33 media fixtures including five 4K profiles and three expected rejections; playback/track/subtitle controller checks; native OpenGL video/subtitle readback and complete five-second paused-idle check |

All installed payload files match their manifests. Start-menu and uninstall records report 0.2.1. Portable archives passed CRC and every manifest hash. Strict release lint/build checks passed locally.

Desktop tests (93 library, two binary, eight real-player regressions) and headless tests (79 library, eight real-player regressions) passed with mpv 0.41.0 / FFmpeg 9.0.2. A native dependency reload abort was reproduced and fixed by retaining the chosen DLL for the process lifetime. All 131 pinned DLL hashes match. Five 4K profiles produced changing D3D11VA-copy pictures on this PC; brief samples are not a feature-film endurance check.

Not verified: owner-operated drag/drop, physical media keys/clipboard/fullscreen/mixed-DPI, long listening/A-V sync, perceptual quality, HDR display output, every rare profile or another GPU. The native computer-control helper was unavailable. Screenshots are captures of the installed app made with its own capture mode on an openly licensed film excerpt; see MEDIA-CREDITS.md.
