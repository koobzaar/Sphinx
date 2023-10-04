# Sphinx

Sphinx is an old image-encryption experiment built around chaotic maps and DNA-style image transforms. It is now framed as an educational prototype and code-rehabilitation exercise, not as production cryptography.

## What This Is

- A small research-inspired experiment for exploring image transforms built from SHA-256-derived one-time tokens, an NCA-CML-inspired keystream generator, and DNA-style symbol operations.
- A portfolio cleanup of an earlier prototype, with a focus on reproducibility, clearer interfaces, and more honest claims.
- A place to study how design choices affect diffusion, locality, and failure modes in custom image ciphers.

## What This Is Not

- Not a secure cryptography library.
- Not a replacement for standard authenticated encryption such as AES-GCM or ChaCha20-Poly1305.
- Not a formally analyzed or security-proven scheme.

If you need real confidentiality or integrity, use standard modern cryptography. This repository is for experimentation and learning.

## Current Pipeline

1. Load an input image as RGB.
2. Derive a 256-bit experiment token from the image summary vector plus either:
   - local randomness from Python's `secrets` module, or
   - optional randomness from the ANU quantum RNG API.
3. Split the image into tiles.
4. For each tile:
   - derive a tile-specific token from the global token,
   - generate NCA-CML-inspired rule selectors, row-operation selectors, column permutations, and pixel keystreams,
   - encode RGB bytes with one of the 8 valid DNA rules for each channel,
   - interleave the DNA rows into a combined matrix and shuffle its columns,
   - apply row-wise DNA addition, subtraction, or XOR according to the dynamic selector stream,
   - decode with complementary DNA rules,
   - apply the paper-shaped pixel diffusion stage.
5. Save the encrypted image and print the token.

Decryption reverses the same tile-local pipeline.

## Why The Tile-Based Change Matters

The old image-wide permutation had a bad failure mode: if a local part of the encrypted image was lost or overwritten, the inverse permutation spread that damage across the whole decrypted image as noise.

The current implementation encrypts tiles independently by default. That means:

- localized ciphertext damage tends to stay localized after decryption,
- damaged regions are easier to inspect,
- the system is more resilient to partial data loss,
- the diffusion/locality tradeoff is now explicit through `--tile-size`.

Use smaller tiles for better damage containment. Use `--tile-size 0` to run a single whole-image block.

## Installation

```bash
python -m pip install -r requirements.txt
```

## Usage

Encrypt an image with the default tile-local mode:

```bash
python encrypt.py images/m6kuvrsdpy551.png --token-file output/token.json
```

Choose a smaller tile size to contain corruption more aggressively:

```bash
python encrypt.py images/m6kuvrsdpy551.png --tile-size 32 --token-file output/token.json
```

Enable analysis plots:

```bash
python encrypt.py images/m6kuvrsdpy551.png --plot --token-file output/token.json
```

Decrypt with the saved metadata file:

```bash
python decrypt.py encrypted_output/<encrypted-file>.png --token-file output/token.json
```

You can also pass the token directly:

```bash
python decrypt.py encrypted_output/<encrypted-file>.png --token <64-hex-token> --tile-size 64
```

## Files

- `encrypt.py`: CLI entrypoint for encryption.
- `decrypt.py`: CLI entrypoint for decryption.
- `functions/pipeline.py`: deterministic orchestration for encrypt/decrypt.
- `functions/generateSecureKey.py`: token derivation and optional analysis helpers.
- `functions/ncaCml.py`: NCA-CML-inspired parameter updates, rule selection, permutations, and keystream generation.
- `functions/matrixDNAManipulator.py`: the 8 DNA rules plus DNA addition, subtraction, XOR, and inverse operations.
- `functions/pipeline.py`: tile-local paper-shaped encryption/decryption orchestration.

## Testing

```bash
python -m unittest discover -s tests
```

The test suite covers:

- encrypt/decrypt round-trip,
- DNA encode/decode round-trip,
- RGB channel ordering,
- deterministic NCA-CML key-material generation,
- CLI smoke tests,
- localized damage staying inside the affected tile.

## Limitations

- The algorithm is custom and should not be treated as secure cryptography.
- Tile-local processing improves resilience to partial data loss, but it also reduces global diffusion compared with a whole-image permutation.
- The current implementation is inspired by the 2018 paper, but it is still a pragmatic reconstruction rather than a claim of exact scientific reproduction.
- The ANU API path is optional and requires an API key via `SPHINX_ANU_API_KEY` or `ANU_API_KEY`.

## Reference

This repository was inspired by chaos-based image-encryption literature, including:

- https://www.sciencedirect.com/science/article/abs/pii/S0165168418300859

## Author

Bruno Bezerra Trigueiro  
[bruno.trigueiro@proton.me](mailto:bruno.trigueiro@proton.me)  
[LinkedIn](https://www.linkedin.com/in/brunotrigueiro/)
 
