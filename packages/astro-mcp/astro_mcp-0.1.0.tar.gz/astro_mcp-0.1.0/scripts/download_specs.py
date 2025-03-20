"""
Download the OpenAPI specs for the APIs.

This script downloads the latest Astro Platform API spec and saves it to the specs directory.
The spec will be included in the package when built and distributed.
"""

import os
import requests
from pathlib import Path

platform_api_spec = "https://api.astronomer.io/spec/platform/v1beta1"


def download_spec(url: str, output_file: str):
    """Download an OpenAPI spec from a URL and save it to a file.
    
    Args:
        url: The URL to download the spec from
        output_file: The file path to save the spec to
    """
    print(f"Downloading spec from {url}...")
    response = requests.get(url)
    response.raise_for_status()
    
    # Create the output directory if it doesn't exist
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w") as f:
        f.write(response.text)

    print(f"Downloaded {url} to {output_file}")


def main():
    """Download all specs."""
    # Use the script's directory as a reference to find the project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Define the output path
    output_file = project_root / "specs" / "platform_api_spec.yaml"
    
    # Download the spec
    download_spec(platform_api_spec, output_file)
    print("All specs downloaded successfully.")


if __name__ == "__main__":
    main()
