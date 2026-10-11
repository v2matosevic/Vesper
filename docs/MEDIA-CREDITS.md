# Media credits and what the pictures show

Vesper's own code and artwork are MIT licensed, and the complete Windows distribution is GPL-3.0-or-later
(see [LICENSING.md](LICENSING.md)). The film in the README pictures is a third-party work with its own
terms, listed here with where it came from. Nothing from the film is committed to this repository
except the pictures themselves. Everything below was checked on 2026-10-11.

## What each picture is

| Picture | Kind | What it shows |
| --- | --- | --- |
| `docs/media/hero.jpg` | Mockup | Two captures placed in a drawn Windows-style window frame over a blurred film frame, beside Vesper's icon and name. It is not a screenshot. |
| `docs/screenshots/player.png`, `compact-window.png`, `subtitle-tracks.png`, `playback-info.png`, `start-screen-light.png` | Actual captures of the installed app | Made with the installed Vesper 0.2.1 (`vesper.exe`, SHA-256 `c5f6a93212c7b9c4cdf91bb06405c250e45e9cdb991943ef1e0345550929930d`) and its own self-ending capture mode, `vesper --native-smoke <file> --out <folder>`. The mode opens the file in a hidden native OpenGL window, lets libmpv decode and draw it, draws Vesper's interface on top and reads the pixels back. Nothing is edited. The clock reads 0:00 because the interface state is fixed when the capture starts, and the picture is a frame from the first seconds of the excerpt. The subtitle menu in `subtitle-tracks.png` and the information panel in `playback-info.png` are opened by the capture mode; their contents (the file's real tracks, its real codec facts) are real. The "Subtitle delay +0.2 s" notice in `playback-info.png` is text the capture mode stages, not a delay that was set. |
| `docs/screenshots/vesper.png` | Earlier screenshot | The first public screenshot, made with generated colour-bar media. Kept for the record, no longer shown in the README. |

## The film

- *Tears of Steel*, produced by the Blender Foundation (Mango open movie project), 2012. The film's
  closing credits list its cast and crew. The pictures here show two of its scenes.
- License: Creative Commons Attribution 3.0. The project's sharing page says everything it publishes,
  including the film, subtitles and sound mixes, is CC BY 3.0 with the attribution
  "(CC) Blender Foundation | mango.blender.org".
  [mango.blender.org/sharing](https://mango.blender.org/sharing/),
  [license text](https://creativecommons.org/licenses/by/3.0/).
- Official downloads used: from [download.blender.org/demo/movies/ToS](https://download.blender.org/demo/movies/ToS/):
  `ToS-4k-1920.mov.zip` (the 4K-rendered version, 1920 pixels wide, H.264 + AAC, 12 min 14 s), the
  `TOS_MUSIC+FX_NO_DIALOGUE.aif` music-and-effects mix, and the subtitles `TOS-en/Croatian/es/de/fr-orig/it/nl/ru.srt`
  from the `subtitles` folder.
- Changes: two 40 second excerpts were cut (from 25.2 s and 239.0 s), re-encoded with ffmpeg
  (H.264 CRF 17, AAC 192 kbit/s) and given eight subtitle tracks (the official SRT files shifted to the
  excerpt's timeline and tagged with their languages) and a second audio track, the official music and
  effects mix, delayed by 30 ms, which is the offset measured between it and the film's AAC track.
  The excerpts are not published here. The film itself is not redistributed.

| Local original (not committed) | SHA-256 |
| --- | --- |
| `ToS-4k-1920.mov.zip` | `58f2dd086aeefe110b10a6d9d7529faa68cf6ec3035eb2410036b1e7896f426a` |
| `ToS-4k-1920.mov` (inside the zip) | `bd2b5bc6c16d4085034f47ef7e4b3938afe86b4eec4ac3cf2685367d3b0b23b0` |
| `TOS_MUSIC+FX_NO_DIALOGUE.aif` | `ba05dc3ae9f869170819ef9f74401e6c01ccc4afa9e8c926a076bea7b29741e0` |
| `TOS-en.srt` | `ce9578f6fe098a5821045a38884b229160f9e7ba27890448a92f5be330c6e6fe` |
| `TOS-Croatian.srt` | `743a93583ba89f65fb803e9707bf6a92bdf26b4bb8271efb6ad4930b47a3cd4c` |
| `TOS-es.srt` | `b1936989cf42eda28988ec9120a80b7303562ea6429e49441160ba688da39a5c` |
| `TOS-de.srt` | `666685daa9064a5a59144e47bddd2d570bbdda199df6e4e39f3273e479ab1f4b` |
| `TOS-fr-orig.srt` | `94cc887d34c83ee909dfe141edaccc2afc1ae8c23c7929b60e2f73905968c708` |
| `TOS-it.srt` | `6b8f6023b88b16acadea52d1664aa92ef132d7481e3e1957f1f334260477c870` |
| `TOS-nl.srt` | `1146fe8a924306d680d9b7c82cf652e56e9f1ed28c81142fa477daee04b45b58` |
| `TOS-ru.srt` | `3fcb17b4671bcc6f3b92c823eeeab134234e739cd8878ed5a4c1ab56b320829c` |
| Excerpt 1, `Tears of Steel - excerpt.mkv` | `ad4e7f045908856adbd6e7afb8122d76737b6becab46f132febf1b591bbf81a2` |
| Excerpt 2, `Tears of Steel - excerpt 2.mkv` | `a36efe782be8b7646242dd33230a902648d01e01833ec5914fe2624fde0f136b` |

The film's separate original soundtrack by Joram Letwory is licensed under CC BY-ND 3.0 and is not used.

## Reproducing the pictures

The media stays in the ignored folder `demo-media/` (`originals`, `clips`, `captures`, `work`).

1. Download the files above into `demo-media/originals` and unzip the film.
2. Cut an excerpt: `ffmpeg -ss 25.2 -t 40 -i ToS-4k-1920.mov ... -c:v libx264 -crf 17 -c:a aac`, add the
   music-and-effects mix (delayed 30 ms) and the shifted subtitles as further streams, and save it as
   `demo-media/clips/Tears of Steel - excerpt.mkv`. The second excerpt starts at 239.0 s.
3. Capture: `vesper.exe --native-smoke "demo-media/clips/Tears of Steel - excerpt.mkv" --out demo-media/captures/bridge`
   (and the second excerpt into `captures/lab`).
4. Take one frame at 27 s as `demo-media/work/backdrop.png`, then compose the hero:
   `python scripts/showcase/compose-hero.py` (needs Pillow and numpy).
