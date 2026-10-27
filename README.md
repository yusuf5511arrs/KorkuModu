KorkuModu
=========

Bedrock 1.26.x psikolojik korku mob add-on projesi.

Bu repo, add-on yapısını içerir. Görsel ve ses dosyaları burada üretilemez; ama otomatik üretici hazırdır.

Hızlı kullanım:
1. pip install -r requirements.txt
2. python tools/generate_korku_assets.py
3. Ardından KorkuModu klasörünü zipleyip Minecraft Bedrock’a yükle.

Oluşacak dosyalar:
- KorkuModu_RP/textures/entity/korku_canavari.png
- KorkuModu_RP/textures/entity/korku_canavari_emissive.png
- KorkuModu_RP/sounds/ambient/korku_heartbeat.ogg
- KorkuModu_RP/sounds/ambient/korku_whisper.ogg
- KorkuModu_RP/sounds/ambient/korku_approach.ogg
- KorkuModu_RP/sounds/ambient/korku_jump.ogg

Sonra komut:
/summon korku:canavar

Not: Bu ortam doğrudan binary indirme işlemi yapamadığı için, görsel ve ses dosyaları otomatik üretilen yerel script ile oluşturuluyor.
