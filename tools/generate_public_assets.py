"""Rebuild original geometric icons and short synthesized BGM for the game.

No samples or existing recordings are used. Run from the repository root:
    python tools/generate_public_assets.py
"""

from __future__ import annotations

import math
import os
import struct
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "deepface_ver" / "data" / "public"
SAMPLE_RATE = 24000

# MIDI pitches written for this project, in eighth notes; zero denotes a rest.
MELODIES = {
    "title": (
        72,
        0,
        76,
        79,
        74,
        0,
        77,
        81,
        76,
        79,
        84,
        0,
        79,
        76,
        74,
        0,
        69,
        72,
        76,
        0,
        74,
        77,
        81,
        0,
        71,
        74,
        79,
        77,
        76,
        74,
        72,
        0,
    ),
    "play": (
        72,
        79,
        76,
        79,
        74,
        81,
        77,
        81,
        76,
        84,
        79,
        84,
        74,
        81,
        77,
        79,
        69,
        76,
        72,
        76,
        71,
        77,
        74,
        77,
        67,
        74,
        71,
        74,
        72,
        79,
        76,
        0,
    ),
    "finish": (
        76,
        0,
        79,
        0,
        84,
        0,
        83,
        81,
        79,
        0,
        76,
        0,
        74,
        0,
        72,
        0,
        69,
        0,
        72,
        76,
        77,
        0,
        74,
        0,
        71,
        74,
        79,
        0,
        72,
        0,
        0,
        0,
    ),
}
CHORDS = ((48, 52, 55), (50, 53, 57), (52, 55, 59), (55, 59, 62))


def add_note(samples: list[float], pitch: int, start: float, duration: float, gain: float):
    if not pitch:
        return
    frequency = 440 * 2 ** ((pitch - 69) / 12)
    offset = round(start * SAMPLE_RATE)
    count = round(duration * SAMPLE_RATE)
    for index in range(min(count, len(samples) - offset)):
        time = index / SAMPLE_RATE
        # Smooth attack/release, with a quiet second harmonic for a soft bell tone.
        envelope = min(1, time / 0.012, (duration - time) / 0.045)
        phase = math.tau * frequency * time
        tone = math.sin(phase) + 0.18 * math.sin(phase * 2)
        samples[offset + index] += gain * envelope * math.exp(-2 * time) * tone


def music() -> None:
    directory = ROOT / "sounds"
    directory.mkdir(parents=True, exist_ok=True)
    for name, notes in MELODIES.items():
        beat = 60 / {"title": 100, "play": 120, "finish": 90}[name]
        duration = len(notes) * beat / 2
        samples = [0.0] * round(duration * SAMPLE_RATE)
        for index, pitch in enumerate(notes):
            add_note(samples, pitch, index * beat / 2, beat * 0.43, 0.20)
            if index % 4 == 0:
                chord = CHORDS[(index // 8) % len(CHORDS)]
                for chord_pitch in chord:
                    add_note(samples, chord_pitch, index * beat / 2, beat * 1.8, 0.065)
        # Keep transitions and looping free of discontinuities at the boundary.
        peak = max(1.0, max(abs(value) for value in samples) / 0.8)
        audio = bytearray()
        for index, value in enumerate(samples):
            fade = min(1.0, index / 480, (len(samples) - 1 - index) / 1200)
            audio.extend(struct.pack("<h", round(value * fade / peak * 32767)))
        with wave.open(str(directory / f"bgm_{name}.wav"), "wb") as output:
            output.setnchannels(1)
            output.setsampwidth(2)
            output.setframerate(SAMPLE_RATE)
            output.writeframes(audio)


def icons() -> None:
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
    import pygame

    directory = ROOT / "icons"
    directory.mkdir(parents=True, exist_ok=True)
    ink = (32, 47, 69)
    for name in ("clock", "heart", "question"):
        surface = pygame.Surface((256, 256), pygame.SRCALPHA)
        if name == "clock":
            pygame.draw.circle(surface, ink, (128, 136), 94)
            pygame.draw.circle(surface, (240, 250, 255), (128, 136), 82)
            pygame.draw.rect(surface, ink, (108, 18, 40, 18), border_radius=6)
            pygame.draw.line(surface, ink, (128, 136), (128, 80), 12)
            pygame.draw.line(surface, ink, (128, 136), (170, 153), 12)
            pygame.draw.circle(surface, ink, (128, 136), 9)
        elif name == "heart":
            for color, radius, bottom in ((ink, 53, 229), ((244, 99, 125), 44, 215)):
                pygame.draw.circle(surface, color, (80, 88), radius)
                pygame.draw.circle(surface, color, (176, 88), radius)
                pygame.draw.polygon(
                    surface, color, [(80 - radius, 100), (176 + radius, 100), (128, bottom)]
                )
        else:
            pygame.draw.circle(surface, ink, (128, 125), 101)
            pygame.draw.circle(surface, (239, 235, 255), (128, 125), 90)
            pygame.draw.arc(surface, ink, (84, 62, 88, 80), -math.pi / 2, math.pi, 14)
            pygame.draw.line(surface, ink, (128, 136), (128, 160), 14)
            pygame.draw.circle(surface, ink, (128, 186), 9)
        pygame.image.save(surface, str(directory / f"{name}.png"))


if __name__ == "__main__":
    music()
    icons()
    print(f"Generated original BGM and icons under {ROOT}")
