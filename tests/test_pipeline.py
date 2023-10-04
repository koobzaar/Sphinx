import subprocess
import tempfile
import unittest
from pathlib import Path

import numpy as np

from functions.imageManipulator import load_rgb_image, merge_rgb_channels, split_rgb_channels
from functions.matrixDNAManipulator import DnaDecoder, DnaEncoder, DnaRules
from functions.ncaCml import derive_key_material
from functions.pipeline import EncryptionConfig, decrypt_image, encrypt_image


REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURE_PATH = REPO_ROOT / "tests" / "fixtures" / "sample.ppm"


class PipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.image = load_rgb_image(FIXTURE_PATH)
        self.random_bytes = bytes(range(32))

    def test_encrypt_then_decrypt_round_trip(self) -> None:
        config = EncryptionConfig(tile_size=2)
        encrypted = encrypt_image(self.image, config, random_bytes=self.random_bytes)
        decrypted = decrypt_image(encrypted.encrypted_image, encrypted.token, config)
        np.testing.assert_array_equal(decrypted.decrypted_image, self.image)

    def test_localized_damage_stays_within_tile(self) -> None:
        config = EncryptionConfig(tile_size=2)
        encrypted = encrypt_image(self.image, config, random_bytes=self.random_bytes)
        damaged = encrypted.encrypted_image.copy()
        damaged[0:2, 0:2] = 255

        decrypted = decrypt_image(damaged, encrypted.token, config).decrypted_image
        unchanged_mask = np.ones(self.image.shape[:2], dtype=bool)
        unchanged_mask[0:2, 0:2] = False

        np.testing.assert_array_equal(decrypted[unchanged_mask], self.image[unchanged_mask])
        self.assertFalse(np.array_equal(decrypted[0:2, 0:2], self.image[0:2, 0:2]))

    def test_channel_helpers_preserve_rgb_order(self) -> None:
        red, green, blue = split_rgb_channels(self.image)
        rebuilt = merge_rgb_channels(red, green, blue)
        np.testing.assert_array_equal(rebuilt, self.image)


class DnaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.image = load_rgb_image(FIXTURE_PATH)

    def test_dna_round_trip(self) -> None:
        red, green, blue = split_rgb_channels(self.image)
        encoder = DnaEncoder()
        decoder = DnaDecoder()
        for red_rule in range(8):
            rules = DnaRules(red_rule, (red_rule + 1) % 8, (red_rule + 2) % 8)
            encoded = encoder.encode(red, green, blue, rules)
            decoded = decoder.decode(*encoded, rules)
            for source, recovered in zip((red, green, blue), decoded):
                np.testing.assert_array_equal(source, recovered)

    def test_key_material_is_deterministic(self) -> None:
        first = derive_key_material(4, 4, "ab" * 32, EncryptionConfig().nca_cml)
        second = derive_key_material(4, 4, "ab" * 32, EncryptionConfig().nca_cml)
        self.assertEqual(first.rules, second.rules)
        np.testing.assert_array_equal(first.row_operations, second.row_operations)
        np.testing.assert_array_equal(first.ks1, second.ks1)
        np.testing.assert_array_equal(first.ks2, second.ks2)
        np.testing.assert_array_equal(first.ks3, second.ks3)


class CliSmokeTests(unittest.TestCase):
    def test_encrypt_and_decrypt_scripts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            encrypted_dir = temp_path / "encrypted"
            decrypted_dir = temp_path / "decrypted"
            token_file = temp_path / "token.json"

            encrypt_process = subprocess.run(
                [
                    "python",
                    "encrypt.py",
                    str(FIXTURE_PATH),
                    "--output-dir",
                    str(encrypted_dir),
                    "--token-file",
                    str(token_file),
                    "--tile-size",
                    "2",
                ],
                cwd=REPO_ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(encrypt_process.returncode, 0)

            encrypted_files = list(encrypted_dir.glob("*.png"))
            self.assertEqual(len(encrypted_files), 1)

            decrypt_process = subprocess.run(
                [
                    "python",
                    "decrypt.py",
                    str(encrypted_files[0]),
                    "--token-file",
                    str(token_file),
                    "--output-dir",
                    str(decrypted_dir),
                ],
                cwd=REPO_ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(decrypt_process.returncode, 0)

            decrypted_files = list(decrypted_dir.glob("*.png"))
            self.assertEqual(len(decrypted_files), 1)
            decrypted_image = load_rgb_image(decrypted_files[0])
            expected_image = load_rgb_image(FIXTURE_PATH)
            np.testing.assert_array_equal(decrypted_image, expected_image)


if __name__ == "__main__":
    unittest.main()
