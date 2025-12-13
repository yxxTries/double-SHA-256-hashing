"""
Bitcoin-style mining simulator.
Only performs double SHA-256 hashing and nonce search.
"""

from __future__ import annotations
import hashlib
import struct
import time


def double_sha256(data: bytes) -> bytes:
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def mine_block(
    message: bytes,
    difficulty: int,
    max_nonce: int = 0xFFFFFFFF,
) -> dict | None:
    """
    Mine by finding a nonce such that:
    double_sha256(message || nonce_le) starts with `difficulty`
    leading zero hex digits.
    """
    if difficulty < 0:
        raise ValueError("difficulty must be >= 0")

    target_prefix = "0" * difficulty
    start_time = time.perf_counter()

    for nonce in range(max_nonce + 1):
        payload = message + struct.pack("<I", nonce)
        hash_hex = double_sha256(payload).hex()

        if hash_hex.startswith(target_prefix):
            elapsed = time.perf_counter() - start_time
            return {
                "message": message,
                "difficulty": difficulty,
                "nonce": nonce,
                "hash": hash_hex,
                "elapsed_seconds": elapsed,
                "hashrate_hps": (nonce + 1) / elapsed if elapsed > 0 else float("inf"),
            }

    return None


def main() -> None:
    # ---- PARAMETERS (edit these) ----
    MESSAGE = b"hello world"
    DIFFICULTY = 4
    MAX_NONCE = 10_000_000
    # ---------------------------------

    result = mine_block(
        message=MESSAGE,
        difficulty=DIFFICULTY,
        max_nonce=MAX_NONCE,
    )

    if result is None:
        print("No valid nonce found.")
        return

    print("BLOCK MINED")
    print(f"Message:    {result['message'].decode()}")
    print(f"Difficulty: {result['difficulty']}")
    print(f"Nonce:      {result['nonce']}")
    print(f"Hash:       {result['hash']}")
    print(f"Time (s):   {result['elapsed_seconds']:.6f}")
    print(f"Hashrate:   {result['hashrate_hps']:.0f} H/s")


if __name__ == "__main__":
    main()
