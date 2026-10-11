# Vesper formats and limits

Extensions, containers and codecs differ. This is representative coverage, not a promise for every file.

| Coverage | Formats | Conditions |
| --- | --- | --- |
| Vesper | MP4/MOV, MKV, AVI, WebM, TS/M2TS, MPEG, FLV, WMV, OGV, 3GP and representative H.264/HEVC/VP9/AV1 | Profile/hardware dependent; video display framebuffer capped at 4K; no HDR display guarantee |

Vesper accepts local files. URL protocols, external media references, UNC/device/mapped network and reparse paths are restricted. Subtitles have bounded size/cache. Browser search occurs only after your click; download there and load locally. No HDR display guarantee.
