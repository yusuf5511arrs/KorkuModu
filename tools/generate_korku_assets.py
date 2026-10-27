import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RP = os.path.join(ROOT, 'KorkuModu_RP')
TEXTURE_DIR = os.path.join(RP, 'textures', 'entity')
SOUND_DIR = os.path.join(RP, 'sounds', 'ambient')

os.makedirs(TEXTURE_DIR, exist_ok=True)
os.makedirs(SOUND_DIR, exist_ok=True)


def make_texture(path, emissive=False):
    width, height = 1024, 1024
    img = Image.new('RGBA', (width, height), (12, 14, 18, 255))
    draw = ImageDraw.Draw(img)

    for i in range(0, 1400, 9):
        alpha = max(0, 90 - i // 20)
        x0 = i % width
        y0 = (i * 7) % height
        r = 8 + (i % 30)
        draw.ellipse((x0 - r, y0 - r, x0 + r, y0 + r), fill=(35, 42, 52, alpha))

    draw.ellipse((320, 150, 700, 900), fill=(170, 180, 198, 220))
    draw.ellipse((360, 250, 660, 560), fill=(215, 222, 232, 255))
    draw.ellipse((420, 390, 500, 460), fill=(18, 22, 30, 255))
    draw.ellipse((520, 390, 600, 460), fill=(18, 22, 30, 255))
    draw.arc((430, 430, 590, 510), start=200, end=340, fill=(30, 30, 35, 255), width=12)

    arm = (180, 190, 205, 255)
    draw.rounded_rectangle((240, 420, 320, 860), radius=32, fill=arm)
    draw.rounded_rectangle((700, 420, 780, 860), radius=32, fill=arm)
    draw.rounded_rectangle((380, 860, 470, 1010), radius=24, fill=arm)
    draw.rounded_rectangle((550, 860, 640, 1010), radius=24, fill=arm)

    if emissive:
        glow = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        g = ImageDraw.Draw(glow)
        g.ellipse((420, 385, 500, 455), fill=(90, 120, 180, 170))
        g.ellipse((520, 385, 600, 455), fill=(90, 120, 180, 170))
        img = Image.alpha_composite(img, glow)

    img = img.filter(ImageFilter.GaussianBlur(radius=1.2))
    img.save(path)


def write_ogg(signal, sr, path):
    try:
        import soundfile as sf
        sf.write(path, signal.astype(np.float32), sr)
        return
    except Exception:
        import wave
        out_wav = path.replace('.ogg', '.wav')
        pcm = np.int16(signal * 32767)
        with wave.open(out_wav, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sr)
            wf.writeframes(pcm.tobytes())
        print(f'Created fallback WAV: {out_wav}')


def make_heartbeat(path):
    sr = 22050
    t = np.linspace(0, 3.8, int(3.8 * sr), endpoint=False)
    signal = (np.sin(2 * np.pi * 1.6 * t) * 0.45 + ((np.sin(2 * np.pi * 2.6 * t) + 1) / 2.0) * 0.35 + np.random.normal(0, 0.05, len(t))) * 0.7
    write_ogg(np.clip(signal, -1.0, 1.0), sr, path)


def make_whisper(path):
    sr = 22050
    t = np.linspace(0, 5.2, int(5.2 * sr), endpoint=False)
    signal = (
        np.sin(2 * np.pi * 160 * t) * 0.22 +
        0.6 * np.sin(2 * np.pi * 80 * t + 0.7) * 0.28 +
        0.25 * np.sin(2 * np.pi * 5 * t) +
        np.random.normal(0, 0.045, len(t))
    ) * 0.7
    write_ogg(np.clip(signal, -1.0, 1.0), sr, path)


def make_approach(path):
    sr = 22050
    t = np.linspace(0, 4.0, int(4.0 * sr), endpoint=False)
    signal = (
        np.sin(2 * np.pi * 45 * t) * 0.4 +
        0.5 * np.sin(2 * np.pi * (30 + 18 * (t / (4.0))) * t) +
        np.random.normal(0, 0.06, len(t))
    ) * 0.8
    write_ogg(np.clip(signal, -1.0, 1.0), sr, path)


def make_jump(path):
    sr = 22050
    t = np.linspace(0, 1.2, int(1.2 * sr), endpoint=False)
    signal = (
        np.exp(-10 * t) * np.sin(2 * np.pi * 240 * t) * 0.7 +
        np.exp(-150 * (t - 0.18) ** 2) * 0.9
    ) * 0.8
    write_ogg(np.clip(signal, -1.0, 1.0), sr, path)


def main():
    make_texture(os.path.join(TEXTURE_DIR, 'korku_canavar.png'))
    make_texture(os.path.join(TEXTURE_DIR, 'korku_canavar_emissive.png'), emissive=True)
    make_heartbeat(os.path.join(SOUND_DIR, 'korku_heartbeat.ogg'))
    make_whisper(os.path.join(SOUND_DIR, 'korku_whisper.ogg'))
    make_approach(os.path.join(SOUND_DIR, 'korku_approach.ogg'))
    make_jump(os.path.join(SOUND_DIR, 'korku_jump.ogg'))
    print('Asset generation complete')


if __name__ == '__main__':
    main()
