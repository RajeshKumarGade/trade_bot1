import os


def get_access_token():
    access_token = os.getenv("KITE_ACCESS_TOKEN", "").strip()
    if not access_token:
        raise RuntimeError(
            "KITE_ACCESS_TOKEN is required. Set it in Railway service variables."
        )
    print("Using KITE_ACCESS_TOKEN from environment")
    return access_token
