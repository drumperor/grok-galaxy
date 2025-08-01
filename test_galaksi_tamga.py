import unittest

from grok_galaxy_tamga import GalaksiTamgaGenerator, TamgaError

class TestGalaksiTamgaGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = GalaksiTamgaGenerator()

    def test_validate_empty(self):
        # validate_stars should accept empty list without error
        try:
            self.gen.validate_stars([])
        except Exception as e:
            self.fail(f"validate_stars raised an exception on empty list: {e}")

    def test_validate_invalid_star_id(self):
        # Invalid star_id should raise TamgaError
        invalid_star = {
            "star_id": "BAD_ID",
            "name": "test",
            "capabilities": [],
            "allowed_connections": [],
            "firewall_config": {"type": "iptables", "rules": [], "enabled": True},
            "music_config": {"instrument": "piano", "notes": [], "tempo": 120},
            "internet_config": {}
        }
        with self.assertRaises(TamgaError):
            self.gen.validate_stars([invalid_star])

if __name__ == '__main__':
    unittest.main()
