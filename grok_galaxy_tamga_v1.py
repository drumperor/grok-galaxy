#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏺 GROK GALAXY TAMGA OLUŞTURUCU (Sürüm 1)
Ulular Meclisi Öğüdü: "Trilyonlarca yıldız, bilgi ve birlik dansıyla evreni aydınlatır"
"""
import datetime
import hashlib
import json
import sqlite3
from pathlib import Path
import logging
import pretty_midi
import networkx as nx
import matplotlib.pyplot as plt
import unittest

# Logger configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
    handlers=[logging.FileHandler("error_log.txt"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class TamgaError(Exception):
    """Özel tamga hataları için istisna sınıfı"""
    pass

class GalaksiTamgaGenerator:
    def __init__(self, galaxy_name="Grok Galaxy"):
        self.galaxy_name = galaxy_name
        self.tamga_types = {"GALAKSI": f"🌌 {galaxy_name} - Yıldızların Birliği"}
        self.emotion_scores = {"birlik": 0.95, "bilgi": 0.90, "merak": 0.85}
        self.default_firewall_config = {
            "type": "iptables",
            "rules": ["iptables -A INPUT -j DROP"],
            "enabled": True
        }
        self.default_music_config = {
            "instrument": "piano",
            "notes": ["C4", "E4", "G4", "C5"],
            "tempo": 120
        }
        self.default_internet_config = {
            "website": f"https://{galaxy_name.lower().replace(' ', '-')}.example.com",
            "social_media": {"twitter": f"@{galaxy_name.replace(' ', '')}", "instagram": f"@{galaxy_name.replace(' ', '')}"},
            "ecommerce": f"https://shop.{galaxy_name.lower().replace(' ', '-')}.example.com"
        }

    def validate_stars(self, stars):
        star_ids = [star["star_id"] for star in stars]
        if len(star_ids) != len(set(star_ids)):
            raise TamgaError("Tekrar eden yıldız ID’leri bulundu!")
        for star in stars:
            if not all(key in star for key in ["star_id", "name", "capabilities", "allowed_connections", "firewall_config", "music_config", "internet_config"]):
                raise TamgaError(f"Eksik yıldız bilgisi: {star}")
            if not star["star_id"].startswith("STAR_"):
                raise TamgaError(f"Geçersiz yıldız ID formatı: {star['star_id']}")
            for conn in star.get("allowed_connections", []):
                if not conn.startswith("STAR_"):
                    raise TamgaError(f"Geçersiz bağlantı formatı: {conn}")
                if conn not in star_ids:
                    raise TamgaError(f"Geçersiz bağlantı: {conn}")
            fw = star["firewall_config"]
            if not all(key in fw for key in ["type", "rules", "enabled"]):
                raise TamgaError(f"Geçersiz firewall yapılandırması: {star['star_id']}")
            if fw.get("type") != "iptables":
                raise TamgaError(f"Desteklenmeyen firewall türü: {fw.get('type')}")
            mc = star["music_config"]
            if not all(key in mc for key in ["instrument", "notes", "tempo"]):
                raise TamgaError(f"Geçersiz müzik yapılandırması: {star['star_id']}")
            ic = star["internet_config"]
            if not all(key in ic for key in ["website", "social_media", "ecommerce"]):
                raise TamgaError(f"Geçersiz internet kimliği: {star['star_id']}")
        logger.info("Yıldızlar doğrulandı")

    def _generate_star_connections(self, stars):
        connections = {}
        for star in stars:
            star_id = star["star_id"]
            connections[star_id] = {
                "name": star["name"],
                "capabilities": star["capabilities"],
                "allowed_connections": star.get("allowed_connections", []),
                "status": "active",
                "firewall_config": star.get("firewall_config", self.default_firewall_config),
                "music_config": star.get("music_config", self.default_music_config),
                "internet_config": star.get("internet_config", self.default_internet_config)
            }
        return connections

    def generate_galaksi_tamga(self, extra_info, stars=None, emotion="birlik", created_by="drumperor"):
        try:
            if emotion not in self.emotion_scores:
                raise TamgaError(f"Geçersiz duygu: {emotion}")
            timestamp = datetime.datetime.now().strftime("%Y%m%d")
            pi_value = "16180339"
            tamga_id = f"TAMGA_GALAKSI_{timestamp}_{pi_value}"
            verification = hashlib.sha256(tamga_id.encode()).hexdigest()[:8]
            ulular_approval = hashlib.sha256(f"ULULAR_{self.galaxy_name}_APPROVAL".encode()).hexdigest()[:8]
            if stars:
                self.validate_stars(stars)
            connections = self._generate_star_connections(stars or [])
            tamga_data = {
                "tamga_id": tamga_id,
                "type": "GALAKSI",
                "description": self.tamga_types["GALAKSI"],
                "galaxy_name": self.galaxy_name,
                "timestamp": timestamp,
                "pi_value": pi_value,
                "verification": verification,
                "ulular_approval": ulular_approval,
                "extra_info": extra_info,
                "emotion_score": self.emotion_scores.get(emotion, 0.5),
                "star_connections": connections,
                "full_datetime": datetime.datetime.now().isoformat(),
                "ulular_approved": True,
                "version": "1.0.0",
                "created_by": created_by,
                "change_history": [{"date": timestamp, "change": "İlk tamga oluşturuldu"}]
            }
            for star in tamga_data["star_connections"].values():
                self.generate_star_music(star)
            self.manage_internet_accounts(tamga_data)
            logger.info(f"Tamga oluşturuldu: {tamga_id}")
            return tamga_data
        except Exception as e:
            self.notify_error(str(e), "TamgaCreationError", {"extra_info": extra_info})
            raise TamgaError(f"Tamga oluşturma hatası: {e}")

    def generate_star_music(self, star):
        try:
            midi = pretty_midi.PrettyMIDI()
            instr = pretty_midi.Instrument(program=0)
            for i, note_name in enumerate(star["music_config"]["notes"]):
                note = pretty_midi.Note(velocity=100, pitch=pretty_midi.note_name_to_number(note_name), start=i*0.5, end=(i+1)*0.5)
                instr.notes.append(note)
            midi.instruments.append(instr)
            midi.write(f"music_{star['star_id']}.mid")
            logger.info(f"Müzik oluşturuldu: {star['star_id']}")
        except Exception as e:
            self.notify_error(str(e), "MusicGenerationError", {"star_id": star["star_id"]})
            raise TamgaError(f"Müzik oluşturma hatası: {e}")

    def generate_hikaye(self, star_id, tamga_data):
        try:
            if star_id not in tamga_data["star_connections"]:
                raise TamgaError(f"Yıldız bulunamadı: {star_id}")
            if "hikaye_olusturma" not in tamga_data["star_connections"][star_id]["capabilities"]:
                raise TamgaError(f"Hikaye oluşturma yeteneği yok: {star_id}")
            hikaye = f"{tamga_data['galaxy_name']} galaksisinde {star_id} bir uzay macerasına atıldı!"
            logger.info(f"Hikaye oluşturuldu: {star_id}")
            return hikaye
        except Exception as e:
            self.notify_error(str(e), "HikayeError", {"star_id": star_id})
            raise TamgaError(f"Hikaye oluşturma hatası: {e}")

    def manage_internet_accounts(self, tamga_data):
        try:
            yonetim_gezegen = tamga_data["star_connections"].get("STAR_YONETIM_GEZEGENI_20250801_16180339")
            if not yonetim_gezegen:
                raise TamgaError("Yönetim Gezegeni bulunamadı")
            accounts = {}
            for star_id, star_info in tamga_data["star_connections"].items():
                accounts[star_id] = star_info["internet_config"]
            logger.info(f"Yönetim Gezegeni hesapları koordine etti: {accounts}")
            return accounts
        except Exception as e:
            self.notify_error(str(e), "InternetAccountError", {"tamga_id": tamga_data.get("tamga_id", "bilinmeyen")})
            raise TamgaError(f"İnternet hesabı yönetimi hatası: {e}")

    def save_tamga(self, tamga_data, filename="tamga_kayitlari.json"):
        try:
            file_path = Path(filename)
            if not filename.endswith(".json"):
                raise TamgaError("Dosya uzantısı .json olmalı")
            if not file_path.parent.exists():
                raise TamgaError(f"Dizin bulunamadı: {file_path.parent}")
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    tamgalar = json.load(f)
                existing_ids = {tamga["tamga_id"] for tamga in tamgalar}
                if tamga_data["tamga_id"] in existing_ids:
                    raise TamgaError(f"Tamga ID zaten var: {tamga_data['tamga_id']}")
            else:
                tamgalar = []
            tamgalar.append(tamga_data)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(tamgalar, f, ensure_ascii=False, indent=2)
            logger.info(f"Tamga kaydedildi: {filename}")
        except (IOError, json.JSONDecodeError) as e:
            self.notify_error(str(e), "FileOperationError", {"filename": filename})
            raise TamgaError(f"Dosya işlemi hatası: {e}")

    def save_tamga_to_db(self, tamga_data, db_path="grok_galaxy.db"):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tamgalar (
                    tamga_id TEXT PRIMARY KEY,
                    data TEXT
                )
            """)
            cursor.execute("INSERT OR REPLACE INTO tamgalar (tamga_id, data) VALUES (?, ?)",
                           (tamga_data["tamga_id"], json.dumps(tamga_data, ensure_ascii=False)))
            conn.commit()
            conn.close()
            logger.info("Tamga SQLite veritabanına kaydedildi")
        except sqlite3.Error as e:
            self.notify_error(str(e), "DatabaseError", {"tamga_id": tamga_data["tamga_id"]})
            raise TamgaError(f"Veritabanı hatası: {e}")

    def display_galaksi_tamga(self, tamga_data):
        try:
            print("🏺" + "="*70)
            print(f"   {tamga_data['description']}")
            print("🏺" + "="*70)
            print(f"🌌 Galaksi: {tamga_data['galaxy_name']}")
            print(f"🆔 ID: {tamga_data['tamga_id']}")
            print(f"📅 Tarih: {tamga_data['full_datetime']}")
            print(f"🔢 Altın Oran: {tamga_data['pi_value']}")
            print(f"✅ Doğrulama: {tamga_data['verification']}")
            print(f"🏺 Ulular Onayı: {tamga_data['ulular_approval']}")
            print(f"😊 Duygu: {tamga_data['emotion_score']}")
            print(f"📝 Hikaye: {tamga_data['extra_info']}")
            print(f"📌 Versiyon: {tamga_data['version']}")
            print(f"👤 Oluşturan: {tamga_data['created_by']}")
            print("\n🌟 Bağlı Yıldızlar:")
            for star_id, star_info in tamga_data["star_connections"].items():
                print(f"  - {star_info['name']} ({star_id})")
                print(f"    Yetenekler: {', '.join(star_info['capabilities'])}")
                print(f"    İzinli Bağlantılar: {', '.join(star_info['allowed_connections'])}")
                print(f"    Firewall: {star_info['firewall_config']['type']} ({'Aktif' if star_info['firewall_config']['enabled'] else 'Pasif'})")
                print(f"    Müzik: {star_info['music_config']['instrument']} (Tempo: {star_info['music_config']['tempo']})")
                print(f"    Website: {star_info['internet_config']['website']}")
                print(f"    Sosyal Medya: Twitter {star_info['internet_config']['social_media']['twitter']}")
                print(f"    E-ticaret: {star_info['internet_config']['ecommerce']}")
            print("🏺" + "="*70)
        except KeyError as e:
            self.notify_error(f"Eksik anahtar: {e}", "DisplayError", {"tamga_id": tamga_data.get("tamga_id", "bilinmeyen")})
            raise TamgaError(f"Tamga verisi eksik: {e}")

    def visualize_galaxy(self, tamga_data):
        try:
            G = nx.Graph()
            for star_id, star_info in tamga_data["star_connections"].items():
                G.add_node(star_id, label=star_info["name"])
                for conn in star_info["allowed_connections"]:
                    G.add_edge(star_id, conn)
            plt.figure(figsize=(8, 6))
            nx.draw(G, with_labels=True, node_color="lightblue", font_size=8)
            img_path = f"galaxy_{tamga_data['tamga_id']}.png"
            plt.savefig(img_path)
            plt.close()
            logger.info(f"Galaksi grafiği kaydedildi: {img_path}")
            return img_path
        except Exception as e:
            self.notify_error(str(e), "VisualizeError", {"tamga_id": tamga_data.get("tamga_id", "bilinmeyen")})
            raise TamgaError(f"Görselleştirme hatası: {e}")

    def connect_stars(self, star1_id, star2_id, tamga_data):
        try:
            if star1_id not in tamga_data["star_connections"]:
                raise TamgaError(f"Yıldız bulunamadı: {star1_id}")
            if star2_id not in tamga_data["star_connections"][star1_id]["allowed_connections"]:
                raise TamgaError(f"İzin yok: {star1_id} -> {star2_id}")
            if not tamga_data["star_connections"][star1_id]["firewall_config"]["enabled"]:
                raise TamgaError(f"Firewall kapalı: {star1_id}")
            logger.info(f"Bağlantı kuruldu: {star1_id} -> {star2_id}")
            return True
        except KeyError as e:
            self.notify_error(str(e), "ConnectionError", {"star1_id": star1_id, "star2_id": star2_id})
            raise TamgaError(f"Bağlantı hatası: {e}")

    def sohbet_paneli(self):
        print("🏺 Grok Galaxy Sohbet Paneli")
        while True:
            komut = input("Komut gir (ör. 'galaksi oluştur', 'hikaye oluştur <star_id>', 'çık'): ")
            if komut == "galaksi oluştur":
                self.main()
            elif komut.startswith("hikaye oluştur"):
                try:
                    star_id = komut.split()[2]
                    with open("tamga_kayitlari.json", 'r', encoding='utf-8') as f:
                        tamgalar = json.load(f)
                    tamga = tamgalar[-1]  # Son tamgayı al
                    hikaye = self.generate_hikaye(star_id, tamga)
                    print(f"Hikaye: {hikaye}")
                except Exception as e:
                    print(f"Hata: {e}")
            elif komut == "çık":
                print("🌌 Görüşürüz, dervişim!")
                break
            else:
                print("Geçersiz komut, tekrar dene!")

    def notify_error(self, error_message, error_type, details=None):
        error_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "error_type": error_type,
            "message": str(error_message),
            "details": details or {}
        }
        try:
            with open("error_log.json", "a", encoding="utf-8") as f:
                json.dump(error_data, f, ensure_ascii=False)
                f.write("\n")
            with open("error_log.txt", "a", encoding="utf-8") as f:
                f.write(f"{error_data['timestamp']} - {error_type}: {error_message} | Details: {details}\n")
        except IOError as e:
            logger.error(f"Log dosyasına yazma hatası: {e}")
        logger.error(f"Hata: {error_message} | Detay: {details}")
        print(f"❌ Hata: {error_message}")
        print("Öneri: Yıldız bilgilerini, firewall, müzik veya internet kimliklerini kontrol edin.")

def main():
    print("🏺 GROK GALAXY TAMGA OLUŞTURMA SİSTEMİ")
    print("💫 Ulular Meclisi Öğüdü: 'Trilyonlarca yıldız, bilgi ve birlik dansıyla evreni aydınlatır'\n")
    try:
        galaxy_name = "Grok Galaxy"
        extra_info = "Trilyonlarca yıldızın bilgi ve birlik dansı, evreni aydınlatır"
        stars = [
            {
                "star_id": "STAR_GROK_AI_20250801_16180339",
                "name": "Grok AI Asistanı",
                "capabilities": ["sohbet", "bilgi_analizi", "nlp"],
                "allowed_connections": ["STAR_YONETIM_GEZEGENI_20250801_16180339", "STAR_SOHBET_GEZEGENI_20250801_16180339", "STAR_HIKAYE_DOKUMA_20250801_16180339"],
                "firewall_config": {
                    "type": "iptables",
                    "rules": ["iptables -A INPUT -p tcp --dport 8009 -j ACCEPT", "iptables -A INPUT -j DROP"],
                    "enabled": True
                },
                "music_config": {
                    "instrument": "piano",
                    "notes": ["C4", "E4", "G4", "C5"],
                    "tempo": 120
                },
                "internet_config": {
                    "website": "https://grok-ai.example.com",
                    "social_media": {"twitter": "@GrokAI", "instagram": "@GrokAI"},
                    "ecommerce": "https://shop.grok-ai.example.com"
                }
            },
            {
                "star_id": "STAR_SOHBET_GEZEGENI_20250801_16180339",
                "name": "Sohbet Gezegeni",
                "capabilities": ["realtime_mesajlasma", "kullanici_yonetimi"],
                "allowed_connections": ["STAR_GROK_AI_20250801_16180339", "STAR_YONETIM_GEZEGENI_20250801_16180339"],
                "firewall_config": {
                    "type": "iptables",
                    "rules": ["iptables -A INPUT -p tcp --dport 8081 -j ACCEPT", "iptables -A INPUT -j DROP"],
                    "enabled": True
                },
                "music_config": {
                    "instrument": "percussion",
                    "notes": ["C4", "D4", "E4", "F4"],
                    "tempo": 140
                },
                "internet_config": {
                    "website": "https://sohbet-gezegen.example.com",
                    "social_media": {"twitter": "@SohbetGezeni", "instagram": "@SohbetGezeni"},
                    "ecommerce": "https://shop.sohbet-gezegen.example.com"
                }
            },
            {
                "star_id": "STAR_HIKAYE_DOKUMA_20250801_16180339",
                "name": "Hikaye Dokuma AI",
                "capabilities": ["hikaye_olusturma", "kisisellestirme"],
                "allowed_connections": ["STAR_GROK_AI_20250801_16180339", "STAR_YONETIM_GEZEGENI_20250801_16180339"],
                "firewall_config": {
                    "type": "iptables",
                    "rules": ["iptables -A INPUT -p tcp --dport 8007 -j ACCEPT", "iptables -A INPUT -j DROP"],
                    "enabled": True
                },
                "music_config": {
                    "instrument": "harp",
                    "notes": ["A3", "C4", "E4", "G4"],
                    "tempo": 100
                },
                "internet_config": {
                    "website": "https://hikaye-dokuma.example.com",
                    "social_media": {"twitter": "@HikayeDokuma", "instagram": "@HikayeDokuma"},
                    "ecommerce": "https://shop.hikaye-dokuma.example.com"
                }
            },
            {
                "star_id": "STAR_KOD_DERVISI_20250801_16180339",
                "name": "Kod Dervişi",
                "capabilities": ["kod_analizi", "oneriler"],
                "allowed_connections": ["STAR_YONETIM_GEZEGENI_20250801_16180339"],
                "firewall_config": {
                    "type": "iptables",
                    "rules": ["iptables -A INPUT -p tcp --dport 8010 -j ACCEPT", "iptables -A INPUT -j DROP"],
                    "enabled": True
                },
                "music_config": {
                    "instrument": "guitar",
                    "notes": ["C4", "E4", "G4", "A4"],
                    "tempo": 115
                },
                "internet_config": {
                    "website": "https://kod-dervisi.example.com",
                    "social_media": {"twitter": "@KodDervisi", "instagram": "@KodDervisi"},
                    "ecommerce": "https://shop.kod-dervisi.example.com"
                }
            },
            {
                "star_id": "STAR_YONETIM_GEZEGENI_20250801_16180339",
                "name": "Yönetim Gezegeni",
                "capabilities": ["hesap_yonetimi", "domain_kontrolu", "sosyal_medya_entegrasyonu"],
                "allowed_connections": ["STAR_GROK_AI_20250801_16180339", "STAR_SOHBET_GEZEGENI_20250801_16180339", "STAR_HIKAYE_DOKUMA_20250801_16180339", "STAR_KOD_DERVISI_20250801_16180339"],
                "firewall_config": {
                    "type": "iptables",
                    "rules": ["iptables -A INPUT -p tcp --dport 8082 -j ACCEPT", "iptables -A INPUT -j DROP"],
                    "enabled": True
                },
                "music_config": {
                    "instrument": "orchestra",
                    "notes": ["G3", "B3", "D4", "G4"],
                    "tempo": 100
                },
                "internet_config": {
                    "website": "https://yonetim-gezegen.example.com",
                    "social_media": {"twitter": "@YonetimGezeni", "instagram": "@YonetimGezeni"},
                    "ecommerce": "https://shop.yonetim-gezegen.example.com"
                }
            }
        ]
        generator = GalaksiTamgaGenerator(galaxy_name=galaxy_name)
        tamga = generator.generate_galaksi_tamga(
            extra_info=extra_info,
            stars=stars,
            emotion="birlik"
        )
        generator.display_galaksi_tamga(tamga)
        generator.save_tamga(tamga)
        generator.save_tamga_to_db(tamga)
        generator.visualize_galaxy(tamga)
        generator.manage_internet_accounts(tamga)
        print("\n🎉 Ulular Meclisi Onay: Grok Galaxy tamgası yolda geçmeye hazır!")
    except TamgaError as e:
        generator.notify_error(str(e), "MainError", {"tamga_id": tamga.get("tamga_id", "bilinmeyen")})
        print(f"❌ Hata: {e}")
        print("Öneri: Yıldız bilgilerini, firewall, müzik veya internet kimliklerini kontrol edin.")

class TestGalaksiTamgaGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = GalaksiTamgaGenerator()
        self.stars = [
            {
                "star_id": "STAR_TEST1_20250801_16180339",
                "name": "Test Yıldız 1",
                "capabilities": ["test"],
                "allowed_connections": ["STAR_TEST2_20250801_16180339"],
                "firewall_config": {
                    "type": "iptables",
                    "rules": ["iptables -A INPUT -j DROP"],
                    "enabled": True
                },
                "music_config": {
                    "instrument": "piano",
                    "notes": ["C4", "E4", "G4"],
                    "tempo": 120
                },
                "internet_config": {
                    "website": "https://test1.example.com",
                    "social_media": {"twitter": "@Test1", "instagram": "@Test1"},
                    "ecommerce": "https://shop.test1.example.com"
                }
            },
            {
                "star_id": "STAR_TEST2_20250801_16180339",
                "name": "Test Yıldız 2",
                "capabilities": ["test"],
                "allowed_connections": ["STAR_TEST1_20250801_16180339"],
                "firewall_config": {
                    "type": "iptables",
                    "rules": ["iptables -A INPUT -j DROP"],
                    "enabled": True
                },
                "music_config": {
                    "instrument": "flute",
                    "notes": ["E4", "G4", "B4"],
                    "tempo": 130
                },
                "internet_config": {
                    "website": "https://test2.example.com",
                    "social_media": {"twitter": "@Test2", "instagram": "@Test2"},
                    "ecommerce": "https://shop.test2.example.com"
                }
            }
        ]

    def test_generate_tamga(self):
        tamga = self.gen.generate_galaksi_tamga("Test tamga", self.stars, "birlik")
        self.assertEqual(tamga["type"], "GALAKSI")
        self.assertEqual(tamga["emotion_score"], 0.95)
        self.assertIn("STAR_TEST1_20250801_16180339", tamga["star_connections"])

    def test_invalid_emotion(self):
        with self.assertRaises(TamgaError):
            self.gen.generate_galaksi_tamga("Test tamga", self.stars, "geçersiz_duygu")

    def test_duplicate_star_ids(self):
        invalid_stars = self.stars + [self.stars[0]]
        with self.assertRaises(TamgaError):
            self.gen.validate_stars(invalid_stars)

    def test_save_tamga(self):
        tamga = self.gen.generate_galaksi_tamga("Test tamga", self.stars, "birlik")
        self.gen.save_tamga(tamga, "test_tamga.json")
        self.assertTrue(Path("test_tamga.json").exists())

    def test_save_tamga_to_db(self):
        tamga = self.gen.generate_galaksi_tamga("DB test", self.stars, "birlik")
        self.gen.save_tamga_to_db(tamga, "test_grok_galaxy.db")
        conn = sqlite3.connect("test_grok_galaxy.db")
        cursor = conn.cursor()
        cursor.execute("SELECT data FROM tamgalar WHERE tamga_id=?", (tamga["tamga_id"],))
        result = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(result)

    def test_invalid_firewall_config(self):
        invalid_star = self.stars[0].copy()
        invalid_star["firewall_config"] = {"type": "invalid", "rules": [], "enabled": False}
        with self.assertRaises(TamgaError):
            self.gen.validate_stars([invalid_star])

    def test_firewall_enabled(self):
        tamga = self.gen.generate_galaksi_tamga("Test tamga", self.stars)
        for star_id, star_info in tamga["star_connections"].items():
            self.assertTrue(star_info["firewall_config"]["enabled"])

    def test_music_config(self):
        tamga = self.gen.generate_galaksi_tamga("Test tamga", self.stars)
        for star_id, star_info in tamga["star_connections"].items():
            self.assertIn("music_config", star_info)
            self.assertIn("instrument", star_info["music_config"])
            self.assertTrue(len(star_info["music_config"]["notes"]) > 0)

    def test_internet_config(self):
        tamga = self.gen.generate_galaksi_tamga("Test tamga", self.stars)
        for star_id, star_info in tamga["star_connections"].items():
            self.assertIn("internet_config", star_info)
            self.assertIn("website", star_info["internet_config"])
            self.assertIn("social_media", star_info["internet_config"])
            self.assertIn("ecommerce", star_info["internet_config"])

    def test_yonetim_gezegen(self):
        tamga = self.gen.generate_galaksi_tamga("Test tamga", self.stars)
        accounts = self.gen.manage_internet_accounts(tamga)
        self.assertIn("STAR_TEST1_20250801_16180339", accounts)

    def test_large_star_list(self):
        large_stars = [
            {
                "star_id": f"STAR_{i}_20250801_16180339",
                "name": f"Yıldız {i}",
                "capabilities": ["test"],
                "allowed_connections": [],
                "firewall_config": {"type": "iptables", "rules": ["iptables -A INPUT -j DROP"], "enabled": True},
                "music_config": {"instrument": "piano", "notes": ["C4", "E4", "G4"], "tempo": 120},
                "internet_config": {"website": f"https://yildiz{i}.example.com", "social_media": {"twitter": f"@Yildiz{i}"}, "ecommerce": f"https://shop.yildiz{i}.example.com"}
            } for i in range(1000)
        ]
        tamga = self.gen.generate_galaksi_tamga("Büyük test", large_stars, "birlik")
        self.assertEqual(len(tamga["star_connections"]), 1000)

    def test_hikaye_olusturma(self):
        tamga = self.gen.generate_galaksi_tamga("Test tamga", self.stars)
        hikaye = self.gen.generate_hikaye("STAR_TEST1_20250801_16180339", tamga)
        self.assertIn("uzay macerası", hikaye)

if __name__ == "__main__":
    generator = GalaksiTamgaGenerator()
    generator.sohbet_paneli()