#!/usr/bin/env python3
# Copied from the SMT3-port repo (private), commit e857c3d, tools/player_data.py.
"""The Vita build's movie folder from a player's own Nocturne disc image, in one command (2026-11-17, for the releases repo's README).

NEW: written here, after the DDS port's tools/player_data.py (G:/Ports/DDS-port/tools/player_data.py, read only), which also makes the music. Nocturne has no
ATRAC3 music (kb/game/sound-and-assets.md:3), so the only folder made ahead of time is:
  movies/  the movies: the /MOVIE* files of the disc (plain ISO 9660 files) as H.264 + AAC .mp4 (movie_convert.py, next to this file; kb/adr/0004)
Besides it the Vita build reads the disc image itself (ux0:data/smt3/disc.iso). Needs Python 3.8 or newer and ffmpeg with the libx264 and aac encoders (the
usual full builds have them).

  player_data.py --iso <your disc image> [--out <folder>] [--ffmpeg <ffmpeg executable>] [--movies TITLE1M,MENU] [--jobs 2]

The executable at the disc's root names the game (SLUS_209.11, CLAUDE.md). The output folder is refused inside this repo (no game data in git).
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import movie_convert as mc  # noqa: E402

GAMES = {"SLUS_209.11": "smt3"}   # Shin Megami Tensei III: Nocturne (USA), CLAUDE.md
TITLE = "Shin Megami Tensei III: Nocturne (USA)"


class DataError(Exception):
	pass


def which_game(iso: mc.Iso) -> str:
	paths = {e.path.upper() for e in iso.walk()}
	for exe, game in GAMES.items():
		if "/" + exe.upper() in paths:   # the full path: only the root's file matches
			return game
	raise DataError(f"{iso.path}: {' nor '.join(GAMES)} is not at the disc's root: not a {TITLE} disc image")


def main(argv=None) -> int:
	ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
	ap.add_argument("--iso", type=Path, required=True, help=f"your {TITLE} disc image (a plain .iso)")
	ap.add_argument("--out", type=Path, help="the output folder (default: smt3_vita_data next to the image)")
	ap.add_argument("--ffmpeg", help="the ffmpeg executable (default: the one on the PATH)")
	ap.add_argument("--movies", help="comma separated movie names to make (default: all)")
	ap.add_argument("--jobs", type=int, default=2, help="movies made side by side (default 2)")
	a = ap.parse_args(argv)
	ffmpeg = mc.find_ffmpeg(a.ffmpeg)
	if not ffmpeg:
		print("player_data: ffmpeg not found: install it (with libx264), or name it with --ffmpeg", file=sys.stderr)
		return 2
	try:
		with mc.Iso(a.iso) as iso:
			game = which_game(iso)
		out = (a.out or a.iso.resolve().parent / f"{game}_vita_data").resolve()
		if mc.inside_repo(out):
			raise DataError(f"refused: {out} is inside this repo (game data stays out of git)")
	except (DataError, mc.MovieError) as ex:
		print(f"player_data: {ex}", file=sys.stderr)
		return 2
	args = ["--game", game, "--iso", str(a.iso), "--out", str(out / "movies"), "--ffmpeg", ffmpeg, "--jobs", str(a.jobs)]
	if a.movies:
		args += ["--only", a.movies]
	rc = mc.main(args)
	if rc:
		return rc
	shutil.rmtree(out / "movies" / ".work", ignore_errors=True)
	print(f"player_data: done. Copy the folder movies from {out} into ux0:data/{game}/ on the Vita, next to disc.iso.")
	return 0


if __name__ == "__main__":
	sys.exit(main())
