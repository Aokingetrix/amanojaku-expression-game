"""Check shipping images and audio on both supported operating systems."""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

from deepface_ver.core import assets
from deepface_ver.core.theme import load_theme


def test_shipping_theme_images_and_audio_decode():
    pygame.init()
    pygame.display.set_mode((1, 1))
    assets.clear_asset_caches()
    try:
        theme_path = Path(__file__).resolve().parents[1] / "data" / "theme.toml"
        theme = load_theme(theme_path)
        for path in set(theme.images.values()):
            image = assets.get_image(path)
            assert image.get_width() > 0 and image.get_height() > 0, path
        for path in theme.bgm.values():
            pygame.mixer.music.load(path)
            assert pygame.mixer.Sound(path).get_length() > 0, path
        for path in theme.se.values():
            assert pygame.mixer.Sound(path).get_length() > 0, path
        pygame.mixer.music.unload()
    finally:
        assets.clear_asset_caches()
        pygame.quit()
