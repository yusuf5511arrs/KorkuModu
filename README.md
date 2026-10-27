KorkuModu - simple horror add-on
=================================

Bu proje, Bedrock 1.26.x için kolay ve çalışır bir psikolojik korku mobu hazırlar.

Kullanım:
1. pip install -r requirements.txt
2. python tools/generate_korku_assets.py
3. KorkuModu klasörünü zip yap
4. Minecraft Bedrock'te yükle
5. Komut: /summon korku:canavar

Ana klasör yapısı:
- KorkuModu_BP/
- KorkuModu_RP/
- tools/

İstenen assetler otomatik oluşturulur:
- KorkuModu_RP/textures/entity/korku_canavar.png
- KorkuModu_RP/textures/entity/korku_canavar_emissive.png
- KorkuModu_RP/sounds/ambient/korku_heartbeat.ogg
- KorkuModu_RP/sounds/ambient/korku_whisper.ogg
- KorkuModu_RP/sounds/ambient/korku_approach.ogg
- KorkuModu_RP/sounds/ambient/korku_jump.ogg

Bu proje, "korku:canavar" adında bir canavar üretir. Özgürce rahat davranabilir, sağ-sol dolaşabilir, karanlıkta daha fazla hissedilir ve korkutucu bir atmosfer yaratır.
