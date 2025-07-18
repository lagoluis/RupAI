import argparse
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from hedra_avatar.core.assets import create_asset, upload_asset
from hedra_avatar.core.generation import start_generation
from hedra_avatar.core.poll import wait_and_download
from hedra_avatar.core.utils import get_credit_balance

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Hedra Avatar Pipeline")
    parser.add_argument("--wav", required=True, type=Path, help="Path to the audio file.")
    parser.add_argument("--img", required=True, type=Path, help="Path to the image file.")
    parser.add_argument("--prompt", help="Prompt for the generation.")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.getenv("HEDRA_API_KEY")
    if not api_key:
        print("Error: HEDRA_API_KEY not found in .env file.", file=sys.stderr)
        sys.exit(1)

    try:
        print("Checking credit balance...")
        balance = get_credit_balance(api_key)
        if balance < 1: # Assuming 1 credit is needed for a generation
            print(f"Error: Insufficient credits. Current balance: {balance}", file=sys.stderr)
            sys.exit(1)
        print(f"Current credit balance: {balance}")

        print("Creating audio asset...")
        audio_asset_id = create_asset(args.wav.name, "audio", api_key)
        upload_asset(audio_asset_id, args.wav, api_key)

        print("Creating image asset...")
        image_asset_id = create_asset(args.img.name, "image", api_key)
        upload_asset(image_asset_id, args.img, api_key)

        print("Starting generation...")
        prompt = args.prompt or f"A video of a person speaking."
        generation_id = start_generation(image_asset_id, audio_asset_id, prompt, api_key)

        print(f"Waiting for generation {generation_id} to complete...")
        output_path = wait_and_download(generation_id, Path("output"), api_key)

        print(f"\n✅ Video downloaded to: {output_path}")

    except Exception as e:
        print(f"\n❌ An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
