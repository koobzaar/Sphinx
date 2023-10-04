import argparse
import json
from pathlib import Path

from functions.console import show_ascii_art_header
from functions.imageManipulator import load_rgb_image, save_decrypted_image
from functions.pipeline import EncryptionConfig, decrypt_image


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Decrypt an image produced by the Sphinx chaos/DNA experiment pipeline."
    )
    parser.add_argument("input_image", help="Path to the encrypted image.")
    token_group = parser.add_mutually_exclusive_group(required=True)
    token_group.add_argument("--token", help="Experiment token printed by encrypt.py.")
    token_group.add_argument("--token-file", help="Path to a file containing the experiment token.")
    parser.add_argument(
        "--output-dir",
        default="decrypted_output",
        help="Directory where the decrypted image will be written.",
    )
    parser.add_argument(
        "--tile-size",
        type=int,
        default=None,
        help="Tile size used during encryption. Overrides any value stored in --token-file.",
    )
    return parser


def _read_token_and_tile_size(args: argparse.Namespace) -> tuple[str, int | None]:
    if args.token:
        return args.token.strip(), None
    token_path = Path(args.token_file)
    raw_content = token_path.read_text(encoding="utf-8").strip()
    try:
        payload = json.loads(raw_content)
    except json.JSONDecodeError:
        return raw_content, None
    return payload["token"].strip(), payload.get("tile_size")


def main() -> int:
    args = build_parser().parse_args()
    show_ascii_art_header()

    token, stored_tile_size = _read_token_and_tile_size(args)
    image = load_rgb_image(args.input_image)
    tile_size = args.tile_size if args.tile_size is not None else (stored_tile_size if stored_tile_size is not None else 64)
    result = decrypt_image(image, token, EncryptionConfig(tile_size=tile_size))
    output_path = save_decrypted_image(result.decrypted_image, args.input_image, args.output_dir)

    print(f"Decrypted image written to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
