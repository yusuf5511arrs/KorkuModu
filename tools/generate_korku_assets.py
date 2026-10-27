import os
import math
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RP = os.path.join(ROOT, 'KorkuModu_RP')
TEXTURE_DIR = os.path.join(RP, 'textures', 'entity')
SOUND_DIR = os.path.join(RP, 'sounds', 'ambient')

os.makedirs(TEXTURE_DIR, exist_ok=True)
os.makedirs(SOUND_DIR, exist_ok=True)


def make_horror_texture(path: str, emissive=False):
    width, height = 1024, 1024
    img = Image.new('RGBA', (width, height), (10, 12, 18, 255))
    draw = ImageDraw.Draw(img)

    # Foggy background
    for i in range(0, 1200, 8):
        alpha = max(0, 80 - i // 18)
        x0 = i % width
        y0 = (i * 7) % height
        r = 10 + (i % 30)
        draw.ellipse((x0 - r, y0 - r, x0 + r, y0 + r), fill=(40, 50, 62, alpha))

    # Body silhouette
    body = (
        320, 130, 700, 900
    )
    draw.ellipse((body[0], body[1], body[2], body[3]), fill=(170, 180, 195, 220))

    # Face
    face = (360, 240, 660, 560)
    draw.ellipse((face[0], face[1], face[2], face[3]), fill=(210, 220, 230, 255))

    # Hollow eye sockets
    eye_y = 390
    draw.ellipse((420, eye_y, 500, eye_y + 70), fill=(18, 22, 28, 255))
    draw.ellipse((520, eye_y, 600, eye_y + 70), fill=(18, 22, 28, 255))

    # Mouth shadow
    draw.arc((430, 430, 590, 510), start=200, end=340, fill=(30, 30, 35, 255), width=12)

    # Long arms
    arm_color = (182, 193, 205, 255)
    draw.rounded_rectangle((240, 420, 320, 860), radius=30, fill=arm_color)
    draw.rounded_rectangle((700, 420, 780, 860), radius=30, fill=arm_color)

    # Long legs
    draw.rounded_rectangle((380, 860, 470, 1010), radius=24, fill=arm_color)
    draw.rounded_rectangle((550, 860, 640, 1010), radius=24, fill=arm_color)

    # Distortive pale face / gaunt shape
    draw.line((300, 340, 270, 500), fill=(130, 138, 150, 255), width=18)
    draw.line((760, 340, 790, 500), fill=(130, 138, 150, 255), width=18)

    # Emissive glow if needed
    if emissive:
        glow = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow)
        glow_draw.ellipse((420, 385, 500, 455), fill=(100, 140, 220, 160))
        glow_draw.ellipse((520, 385, 600, 455), fill=(100, 140, 220, 160))
        img = Image.alpha_composite(img, glow)

    # Add slight blurred edges for atmospheric horror feel
    img = img.filter(ImageFilter.GaussianBlur(radius=1.2))
    img.save(path)


def generate_heartbeat(path: str):
    sample_rate = 22050
    duration = 3.8
    t = np.linspace(0, duration, int(duration * sample_rate), endpoint=False)
    base = np.sin(2 * np.pi * 1.6 * t)
    pulse = ((np.sin(2 * np.pi * 2.6 * t) + 1) / 2.0) * 0.35
    noise = np.random.normal(0, 0.05, len(t))
    signal = (base * 0.45 + pulse + noise) * 0.7
    signal = np.clip(signal, -1.0, 1.0)
    write_ogg_from_array(signal, sample_rate, path)


def generate_whisper(path: str):
    sample_rate = 22050
    duration = 5.2
    t = np.linspace(0, duration, int(duration * sample_rate), endpoint=False)
    a = np.sin(2 * np.pi * 160 * t)
    b = 0.6 * np.sin(2 * np.pi * 80 * t + 0.7)
    c = 0.25 * np.sin(2 * np.pi * 5 * t)
    noise = np.random.normal(0, 0.045, len(t))
    signal = (a * 0.22 + b * 0.28 + c + noise) * 0.7
    signal = np.clip(signal, -1.0, 1.0)
    write_ogg_from_array(signal, sample_rate, path)


def generate_approach(path: str):
    sample_rate = 22050
    duration = 4.0
    t = np.linspace(0, duration, int(duration * sample_rate), endpoint=False)
    low = np.sin(2 * np.pi * 45 * t)
    sweep = np.sin(2 * np.pi * (30 + 18 * (t / duration)) * t)
    noise = np.random.normal(0, 0.06, len(t))
    signal = (low * 0.4 + 0.5 * sweep + noise) * 0.8
    signal = np.clip(signal, -1.0, 1.0)
    write_ogg_from_array(signal, sample_rate, path)


def generate_jump(path: str):
    sample_rate = 22050
    duration = 1.2
    t = np.linspace(0, duration, int(duration * sample_rate), endpoint=False)
    rise = np.exp(-10 * t) * np.sin(2 * np.pi * 240 * t)
    click = np.exp(-150 * (t - 0.18) ** 2) * 0.9
    signal = (rise * 0.7 + click) * 0.8
    signal = np.clip(signal, -1.0, 1.0)
    write_ogg_from_array(signal, sample_rate, path)


def write_ogg_from_array(signal: np.ndarray, sample_rate: int, path: str):
    try:
        import soundfile as sf
        sf.write(path, signal.astype(np.float32), sample_rate)
        return
    except Exception:
        pass

    # fallback: write a .wav file if soundfile not available, and inform user
    import wave
    out_wav = path.replace('.ogg', '.wav')
    pcm = np.int16(signal * 32767)
    with wave.open(out_wav, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(pcm.tobytes())

    print(f"Created WAV fallback at {out_wav}. Install soundfile+ffmpeg to produce OGG automatically.")


def main():
    make_horror_texture(os.path.join(TEXTURE_DIR, 'korku_canavari.png'))
    make_horror_texture(os.path.join(TEXTURE_DIR, 'korku_canavari_emissive.png'), emissive=True)
    generate_heartbeat(os.path.join(SOUND_DIR, 'korku_heartbeat.ogg'))
    generate_whisper(os.path.join(SOUND_DIR, 'korku_whisper.ogg'))
    generate_approach(os.path.join(SOUND_DIR, 'korku_approach.ogg'))
    generate_jump(os.path.join(SOUND_DIR, 'korku_jump.ogg'))
    print('Asset generation complete.')
    print(f'Textures -> {TEXTURE_DIR}')
    print(f'Sounds -> {SOUND_DIR}')


if __name__ == '__main__':
    main()
