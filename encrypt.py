import argparse
import json
from pathlib import Path

from functions.console import show_ascii_art_header
from functions.imageManipulator import load_rgb_image, save_encrypted_image
from functions.pipeline import EncryptionConfig, encrypt_image


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Encrypt an image using the Sphinx chaos/DNA experiment pipeline."
    )
    parser.add_argument("input_image", help="Path to the source image.")
    parser.add_argument(
        "--output-dir",
        default="encrypted_output",
        help="Directory where the encrypted image will be written.",
    )
    parser.add_argument(
        "--token-file",
        help="Optional file where the generated experiment token will be written.",
    )
    parser.add_argument(
        "--plot",
        action="store_true",
        help="Save logistic-map and Lorenz plots for analysis.",
    )
    parser.add_argument(
        "--x0",
        type=float,
        default=0.5,
        help="Initial logistic-map value used for token derivation.",
    )
    parser.add_argument(
        "--r",
        type=float,
        default=3.9,
        help="Logistic-map growth rate used for token derivation.",
    )
    parser.add_argument(
        "--online-anu",
        action="store_true",
        help="Use the ANU quantum RNG API instead of the local secrets module.",
    )
    parser.add_argument(
        "--anu-api-key",
        help="ANU API key. Falls back to SPHINX_ANU_API_KEY or ANU_API_KEY.",
    )
    parser.add_argument(
        "--tile-size",
        type=int,
        default=64,
        help="Encrypt independently per tile to localize corruption. Use 0 for legacy whole-image mode.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    show_ascii_art_header()

    config = EncryptionConfig(
        x0=args.x0,
        r=args.r,
        offline=not args.online_anu,
        plot=args.plot,
        anu_api_key=args.anu_api_key,
        tile_size=args.tile_size,
    )
    image = load_rgb_image(args.input_image)
    result = encrypt_image(image, config)
    output_path = save_encrypted_image(result.encrypted_image, args.input_image, args.output_dir)

    print(f"Encrypted image written to: {output_path}")
    print(f"Experiment token: {result.token}")

    if args.token_file:
        token_path = Path(args.token_file)
        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(
            json.dumps(
                {
                    "algorithm": "sphinx-experiment-v3-nca-cml",
                    "token": result.token,
                    "tile_size": args.tile_size,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"Token written to: {token_path}")

    if result.logistic_plot_path:
        print(f"Logistic-map plot: {result.logistic_plot_path}")
    if result.lorenz_plot_path:
        print(f"Lorenz plot: {result.lorenz_plot_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
