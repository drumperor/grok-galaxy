# Grok Galaxy API Kullanım Kılavuzu

Bu dosya, Grok Galaxy projesinin REST API, WebSocket ve görselleştirme özelliklerinin nasıl kullanılacağını ve örnek istekleri içermektedir.

## API Endpointleri

### 1. Tamga Oluşturma
- **POST /api/tamga**
- Gönderilecek JSON örneği:
```
{
  "extra_info": "Yıldızlar arası bilgi paylaşımı",
  "stars": [
    {
      "star_id": "STAR_1",
      "name": "Yıldız 1",
      "capabilities": ["sohbet"],
      "allowed_connections": ["STAR_2"]
    },
    {
      "star_id": "STAR_2",
      "name": "Yıldız 2",
      "capabilities": ["analiz"],
      "allowed_connections": ["STAR_1"]
    }
  ],
  "emotion": "birlik"
}
```
- Dönen yanıt: Tamga JSON objesi

### 2. Yıldızlar Arası Bağlantı
- **POST /api/connect**
- Gönderilecek JSON örneği:
```
{
  "tamga_id": "TAMGA_GALAKSI_20250801_16180339",
  "star1": "STAR_1",
  "star2": "STAR_2"
}
```
- Dönen yanıt: {"success": true}
- WebSocket ile bağlantı bilgisi yayınlanır (event: 'star_connection')

### 3. Görselleştirme
- **GET /api/visualize/<tamga_id>**
- Dönen yanıt: {"image_path": "galaxy_<tamga_id>.png"}

## WebSocket
- Bağlantı: ws://localhost:5000/
- Event: 'star_connection' (yeni bağlantı kurulduğunda yayınlanır)

## Swagger/OpenAPI
- Otomatik dokümantasyon için: http://localhost:5000/

## Gereksinimler
- Flask
- Flask-RESTX
- Flask-SocketIO
- NetworkX
- Matplotlib

## Sunucu Başlatma
```bash
pip install flask flask-restx flask-socketio networkx matplotlib
python3 grok_galaxy_tamga.py
```

## Notlar
- Görselleştirme PNG dosyası olarak kaydedilir.
- WebSocket ile gerçek zamanlı yıldız bağlantılarını izleyebilirsiniz.
- API endpointleri Swagger arayüzü ile test edilebilir.
