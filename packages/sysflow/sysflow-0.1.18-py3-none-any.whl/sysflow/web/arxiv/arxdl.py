#!/usr/bin/env python3
"""
arXiv Paper Downloader

A tool to download arXiv papers (both source files and PDF) using the arXiv ID or URL.
"""

import argparse
import os
import re
import sys
import tarfile
import urllib.request
from urllib.error import HTTPError, URLError


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Download arXiv papers (source and PDF)."
    )
    parser.add_argument(
        "arxiv_input", 
        help="arXiv ID (e.g., '2412.1891') or full URL (e.g., 'https://arxiv.org/abs/2412.1891')"
    )
    parser.add_argument(
        "-o", "--output-dir", 
        help="Output directory (default: the arXiv ID)",
        default=None
    )
    parser.add_argument(
        "--pdf-only", 
        action="store_true",
        help="Download only the PDF, not the source files"
    )
    parser.add_argument(
        "--source-only", 
        action="store_true",
        help="Download only the source files, not the PDF"
    )
    parser.add_argument(
        "-f", "--force", 
        action="store_true",
        help="Force download even if files already exist"
    )
    
    return parser.parse_args()


def extract_arxiv_id(input_str):
    """Extract arXiv ID from a string (could be ID or URL)."""
    # Match patterns like '2412.1891' or '2412.1891v1'
    id_pattern = r'(\d{4}\.\d{4,5})(v\d+)?'
    
    # Check if it's already just an ID
    if re.fullmatch(id_pattern, input_str):
        return input_str.split('v')[0]  # Remove version if present
    
    # Try to extract from URL
    url_match = re.search(rf'({id_pattern})', input_str)
    if url_match:
        return url_match.group(1).split('v')[0]  # Group 1 is the ID, remove version
    
    return None


def download_file(url, filename, description=None, force=False):
    """Download a file with progress reporting."""
    # Check if file already exists
    if os.path.exists(filename) and not force:
        print(f"{description or filename} already exists. Use --force to overwrite.")
        return True
    
    try:
        print(f"Downloading {description or filename}...")
        
        def progress_callback(blocks_transferred, block_size, total_size):
            if total_size > 0:
                percentage = min(100, blocks_transferred * block_size * 100 / total_size)
                print(f"\rProgress: {percentage:.1f}%", end="")
            else:
                print(f"\rDownloaded {blocks_transferred * block_size} bytes", end="")
        
        urllib.request.urlretrieve(url, filename, progress_callback)
        print("\nDownload complete!")
        return True
    except HTTPError as e:
        print(f"\nHTTP Error downloading {url}: {e.code} - {e.reason}")
        if os.path.exists(filename):
            os.remove(filename)
        return False
    except URLError as e:
        print(f"\nURL Error downloading {url}: {e.reason}")
        if os.path.exists(filename):
            os.remove(filename)
        return False
    except Exception as e:
        print(f"\nError downloading {url}: {e}")
        if os.path.exists(filename):
            os.remove(filename)
        return False


def download_and_extract_source(arxiv_id, output_dir, force=False):
    """Download and extract source files for an arXiv paper."""
    tarball = f"{output_dir}/{arxiv_id}.tar.gz"
    try:
        # Download source tarball
        url = f'https://arxiv.org/e-print/{arxiv_id}'
        if not download_file(url, tarball, "source files", force):
            return False
        
        # Extract files
        print(f"Extracting source files to {output_dir}...")
        try:
            with tarfile.open(tarball, "r:gz") as tar:
                # Check for any suspicious paths before extracting
                for member in tar.getmembers():
                    if os.path.isabs(member.name) or ".." in member.name:
                        print(f"Warning: Skipping potentially unsafe path in tarball: {member.name}")
                        continue
                    tar.extract(member, path=output_dir)
            print("Extraction complete!")
        except tarfile.ReadError:
            print("Error: The downloaded file is not a valid tar.gz archive.")
            return False
        
        # Clean up
        os.remove(tarball)
        return True
    except Exception as e:
        print(f"Error processing source files: {e}")
        if os.path.exists(tarball):
            os.remove(tarball)
        return False


def download_pdf(arxiv_id, output_dir, force=False):
    """Download PDF for an arXiv paper."""
    pdf_file = f"{output_dir}/{arxiv_id}.pdf"
    url = f'https://arxiv.org/pdf/{arxiv_id}.pdf'
    return download_file(url, pdf_file, "PDF", force)


def main():
    args = parse_args()
    
    # Extract arXiv ID if a URL was provided
    arxiv_id = extract_arxiv_id(args.arxiv_input)
    if not arxiv_id:
        print(f"Error: Could not extract a valid arXiv ID from '{args.arxiv_input}'")
        print("Please provide a valid arXiv ID (e.g., '2412.1891') or URL (e.g., 'https://arxiv.org/abs/2412.1891')")
        return 1
    
    # Determine output directory
    output_dir = args.output_dir or arxiv_id
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
    
    success = True
    
    # Download and extract source files
    if not args.pdf_only:
        success = download_and_extract_source(arxiv_id, output_dir, args.force) and success
    
    # Download PDF
    if not args.source_only:
        success = download_pdf(arxiv_id, output_dir, args.force) and success
    
    if success:
        print(f"Successfully downloaded arXiv paper {arxiv_id} to {output_dir}")
        return 0
    else:
        print(f"There were errors downloading arXiv paper {arxiv_id}")
        return 1


if __name__ == '__main__':
    sys.exit(main())