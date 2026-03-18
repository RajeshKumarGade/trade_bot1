import os


def get_access_token():
    access_token = os.getenv("KITE_ACCESS_TOKEN", "").strip()
    if not access_token:
        # Fallback aliases to handle common env naming mistakes.
        access_token = os.getenv("ACCESS_TOKEN", "").strip()
    if not access_token:
        access_token = os.getenv("ZERODHA_ACCESS_TOKEN", "").strip()

    # Remove accidental wrapping quotes from Railway variable input.
    if (
        len(access_token) >= 2
        and access_token[0] == access_token[-1]
        and access_token[0] in ("'", '"')
    ):
        access_token = access_token[1:-1].strip()

    if not access_token:
        raise RuntimeError(
            "Access token missing. Set KITE_ACCESS_TOKEN in Railway service variables "
            "(or ACCESS_TOKEN / ZERODHA_ACCESS_TOKEN)."
        )
    print("Using access token from environment")
    return access_token
