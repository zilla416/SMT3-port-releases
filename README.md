# SMT3 Vita port: test builds

Test builds of the PS Vita port of Shin Megami Tensei III: Nocturne (USA). The latest build is on the [Releases](../../releases) page.

This repo holds the app (the VPK) and a small script, nothing from the game: no disc image, no saves, no movies. You make those yourself from your own disc, and they stay on your Vita in `ux0:data/smt3`.

## Setting up the game's data folder

The game runs from your own disc image of **Shin Megami Tensei III: Nocturne (USA)** (a plain `.iso`). Besides the image it reads one folder made from the same disc: `movies` (the game's movies, converted to a format the Vita can play). The script `tools/player_data.py` makes it.

You need, on a PC:
- Python 3.8 or newer (python.org);
- ffmpeg, a full build (it needs the libx264 and aac encoders). On Windows: `winget install Gyan.FFmpeg`. The script also finds ffmpeg on your PATH, or name it with `--ffmpeg <path>`.

Then, from this repo's folder:

```
python tools/player_data.py --iso "D:\Games\Shin Megami Tensei - Nocturne (USA).iso"
```

It writes a folder `smt3_vita_data` next to the image, with `movies` inside. Every movie is converted, so it takes a while.

On the Vita (with VitaShell over FTP or USB), `ux0:data/smt3` should then hold:

```
ux0:data/smt3/disc.iso      your disc image, renamed to disc.iso
ux0:data/smt3/movies/       from smt3_vita_data
```

The game makes its other folders (the memory card and so on) by itself the first time it runs.

## Installing and updating

1. Download the newest `smt3_*.vpk` from Releases.
2. Install it with VitaShell, also over a build you have. Your `ux0:data/smt3` folder (your disc image, saves and the rest) is not touched.
3. The game needs `libshacccg.suprx` extracted once on your Vita (the shader compiler vitaGL uses). If you play other vitaGL ports, you have it already. Guide: https://samilops2.gitbook.io/vita-troubleshooting-guide/shader-compiler/extract-libshacccg.suprx
   If the start screen says "The game cannot look inside ur0: on this Vita", turn on Settings > HENkaku Settings > Enable Unsafe Homebrew and start the game again.

## Saving

The game's memory card is a folder in `ux0:data/smt3/cards`. For testing, the port adds one extra: in the field, hold a finger on the front touch screen for about a second and a save point opens.

## Reporting a problem

- Say what happened and where in the game, and which build (the release name, for example `rp35`).
- Right after it happens, copy `ux0:data/smt3/log.txt` from the Vita and send it. The log is written while the game runs and is replaced at the next start.
- If the game hangs at start: put an empty file named `log.sync` in `ux0:data/smt3`, start it again and send `log.txt`.
