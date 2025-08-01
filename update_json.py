import json
from pathlib import Path

for file in ['tamga_kayitlari.json', 'test_tamga.json']:
    data = json.loads(Path(file).read_text(encoding='utf-8'))
    for tamga in data:
        for star_id, star in tamga['star_connections'].items():
            star['internet_config'] = {
                'website': f'https://{star_id.lower()}.example.com',
                'social_media': {'twitter': f'@{star_id}', 'instagram': f'@{star_id}'},
                'ecommerce': f'https://shop.{star_id.lower()}.example.com'
            }
    Path(file).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
