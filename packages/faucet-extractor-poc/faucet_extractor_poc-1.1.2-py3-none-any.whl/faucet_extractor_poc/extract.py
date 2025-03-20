import argparse
import os
import sys
import time
from typing import List, Tuple

from dotenv import load_dotenv

from .discord.webhook import send_workflow_run_alert
from .utils.validation import is_valid_address

from .faucets.bera import BeraFaucet
from .faucets.monad import MonadFaucet

VALID_FAUCET_TYPES = {"BERA", "LUMIA", "MON", "IP"}


def process_address(address: str, faucet_type: str) -> bool:
    """Process a single ERC20 address for a specific faucet"""
    try:
        if faucet_type == "BERA":
            bera_faucet = BeraFaucet()
            return bera_faucet.claim(address)
        if faucet_type == "LUMIA":
            print("Not implemented")
            return False
        if faucet_type == "MON":
            monad_faucet = MonadFaucet()
            return monad_faucet.claim(address)
        if faucet_type == "IP":
            print("Not implemented")
            return False
    except (ValueError, TypeError, RuntimeError) as e:
        print(f"Error processing address {address} on faucet {faucet_type}: {str(e)}")
    return False


def process_addresses_with_retries(
    addresses: List[str], faucet_type: str, max_retries: int = 10
) -> Tuple[dict, int]:
    """
    Process addresses with retries for failed attempts.
    Returns the address status and the number of attempts made.
    """
    # Track addresses and their failure counts
    address_status = {addr: {"failed": 0, "success": False} for addr in addresses}

    attempt = 1
    while True:
        failed_addresses = []
        print(f"\nAttempt {attempt} of {max_retries}")

        # Process only addresses that haven't succeeded yet
        for address in addresses:
            if address_status[address]["success"]:
                continue

            if address_status[address]["failed"] >= max_retries:
                print(
                    f"Address {address} reached max retries ({max_retries}), skipping"
                )
                continue

            success = process_address(address, faucet_type)
            if success:
                address_status[address]["success"] = True
            else:
                address_status[address]["failed"] += 1
                failed_addresses.append(address)

            time.sleep(5)

        # Check if all addresses succeeded or reached max retries
        all_done = all(
            status["success"] or status["failed"] >= max_retries
            for status in address_status.values()
        )

        if all_done or attempt >= max_retries:
            break

        if failed_addresses:
            print(f"Retrying failed addresses: {failed_addresses}")
            time.sleep(30)  # Wait 45 seconds before retrying

        attempt += 1

    successful_count = sum(1 for status in address_status.values() if status["success"])

    # Print final status
    print("\nFinal Status:")
    for address, status in address_status.items():
        if status["success"]:
            print(f"Address {address}: Succeeded")
        else:
            print(f"Address {address}: Failed after {status['failed']} attempts")

    alert_message = "Workflow run successful for all addresses."
    if successful_count != len(addresses):
        alert_message = f"Workflow run unsuccessful for {len(addresses) - successful_count} addresses."

    send_workflow_run_alert(
        faucet_type, alert_message, len(addresses), successful_count, attempt
    )

    return address_status, attempt


def main():
    parser = argparse.ArgumentParser(
        description="Process ERC20 token addresses with specific faucet type"
    )
    parser.add_argument(
        "-f",
        "--faucet",
        required=True,
        type=lambda s: s.upper(),
        choices=VALID_FAUCET_TYPES,
        help=f'Faucet type to use ({", ".join(VALID_FAUCET_TYPES)})',
    )
    parser.add_argument(
        "addresses",
        nargs="*",
        help="ERC20 token addresses (space-separated) or use ERC20_ADDRESSES env var",
    )

    args = parser.parse_args()

    # Get faucet type
    faucet_type = args.faucet

    # Initialize addresses list
    addresses = []

    # First check if addresses were provided via CLI
    if args.addresses:
        addresses = args.addresses
    else:
        # If no CLI args, fall back to environment variable
        addresses_str = os.environ.get("ERC20_ADDRESSES", "")
        if addresses_str:
            addresses = [addr.strip() for addr in addresses_str.split(",")]

    # If still no addresses, exit with error
    if not addresses:
        print(
            "Error: No addresses provided."
            "Either provide addresses as arguments or set ERC20_ADDRESSES env variable"
        )
        sys.exit(1)

    # Validate addresses
    valid_addresses = []
    for address in addresses:
        if not address:
            continue
        if not is_valid_address(address):
            print(f"Invalid address format: {address}, skipping")
            continue
        valid_addresses.append(address)

    if not valid_addresses:
        print("No valid addresses to process")
        sys.exit(1)

    # Process addresses with retries
    process_addresses_with_retries(
        valid_addresses, faucet_type, max_retries=max(1, len(valid_addresses) // 2)
    )


if __name__ == "__main__":
    load_dotenv()

    try:
        main()
    except (ValueError, TypeError, RuntimeError, KeyboardInterrupt) as e:
        print(str(e))
        sys.exit(1)
