import os

from licensing.methods import Helpers, Key
from licensing.models import LicenseKey

LICENSE_FILE = "license.skm"

# Hardcoded credentials (safe for desktop apps)
RSA_PUBLIC_KEY = "<RSAKeyValue><Modulus>6U7Ej1UCblKepvfz1XeFqRIKVVeQBHh81n5uNeW5nPhrKwIuuw845Anj2y65w5f6sa2YKb55fcb7ZiBu4hUSJcId7W+zcMsd6DbQ541ObuZ7hlkeI2vSut7/yy1Vp31wf6RSVYR2N1Pq1hAT+xNeXZh/2T3o0eKRk6zbC3YZLPTC+Be3COP/LJXpEGWIeJvExxCdE8kNUkrD43uEXczG7xrqB6X6+XblFQSiVqjcnvA4eCrFlky39e2hIJbXJtV2QBUyorLRVwu3yJqDV0pcIPlcMCv1RcE5GHeost3KZvuIpJcVZRMnLnVXjNANODYr0x8zg79g7NsgI1ptEz3xWw==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"
AUTH_TOKEN = (
    "WyIxMDczNjU3MDEiLCJmOGJyL0VSa2lQTG1jbHR4UXpRdmpzOGg5L0pnTVFzakhRNXZ1RDg0Il0="
)
PRODUCT_ID = 29600


def save_license_to_file(license_obj: LicenseKey):
    """Save the validated license object to disk."""
    with open(LICENSE_FILE, "w") as f:
        f.write(license_obj.save_as_string())


def load_license_from_file(max_age_days=30) -> LicenseKey | None:
    """Load and validate the saved license file."""
    if not os.path.exists(LICENSE_FILE):
        return None

    try:
        with open(LICENSE_FILE, "r") as f:
            saved = f.read()
            license = LicenseKey.load_from_string(RSA_PUBLIC_KEY, saved, max_age_days)

            if license is None or not Helpers.IsOnRightMachine(license, v=2):
                print("❌ License file is invalid or for a different machine.")
                return None

            return license

    except Exception as e:
        print(f"[License Load Error] {e}")
        return None


def verify_license_key(license_key: str) -> tuple[bool, str]:
    """Check the key online, save if valid, return status and message."""
    result = Key.activate(
        token=AUTH_TOKEN,
        rsa_pub_key=RSA_PUBLIC_KEY,
        product_id=PRODUCT_ID,
        key=license_key,
        machine_code=Helpers.GetMachineCode(v=2),
    )

    if result[0] is None:
        return False, str(result[1])

    if not Helpers.IsOnRightMachine(result[0], v=2):
        return False, "This license is not valid for this machine."

    save_license_to_file(result[0])
    return True, "License verified and saved."


def license_exists_and_valid() -> bool:
    """Check if a valid license is saved locally."""
    return load_license_from_file() is not None
