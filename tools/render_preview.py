"""Render real UI screens without a camera or personal player data.

Run from the repository root: python -m tools.render_preview
"""

from __future__ import annotations

import os
import random
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

from deepface_ver.core import assets, settings, utils
from deepface_ver.core.game_manager import GameManager
from deepface_ver.core.theme import load_theme
from deepface_ver.ui import drawing
from deepface_ver.ui.ui_elements import FloatingImage

OUTPUT = Path(__file__).resolve().parents[1] / "docs" / "images"


def main() -> None:
    pygame.init()
    pygame.display.set_mode((1, 1))
    assets.clear_asset_caches()
    try:
        theme = load_theme(settings.DATA_DIR / "theme.toml")
        settings.apply_theme(theme)
        OUTPUT.mkdir(parents=True, exist_ok=True)
        surface = pygame.Surface((1280, 480))
        background = utils.create_background_surface(1280, 480)
        random.seed(2026)
        sprites = [FloatingImage(path, 1280, 480) for path in settings.EMOTION_IMAGE_PATHS.values()]
        drawing.draw_title_screen(surface, background, sprites)
        pygame.image.save(surface, str(OUTPUT / "title.png"))
        game = GameManager(1280, 480, {})
        drawing.draw_emotion_map_screen(surface, background, game, 1280, 480)
        pygame.image.save(surface, str(OUTPUT / "emotion-map.png"))
        print(f"UI previews saved under {OUTPUT}")
    finally:
        assets.clear_asset_caches()
        pygame.quit()


if __name__ == "__main__":
    main()
