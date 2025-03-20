import os
import hashlib
from concurrent.futures import ThreadPoolExecutor
from typing import List, Union
import requests
from pathlib import Path
from fetchFQfromENA.get_fq_meta import fetch_tsv  # Metadata fetching function
import argparse
from typing import Tuple


def parse_args() -> Tuple[str, str, str, str]:
    parser = argparse.ArgumentParser(
    description='Download FASTQ files from ENA',
    add_help=True,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
    parser.add_argument('--accession', '-id', required=True,
                    help='Accession number (required)\nFormat example: PRJNA661210/SRP000123\nSupports ENA/NCBI standard accession formats')
    parser.add_argument('--type', '-t', choices=['ftp', 'aspera'], required=True,
                      help='Download protocol type\nftp: Standard FTP download\naspera: High-speed transfer protocol (requires private key)')
    parser.add_argument('--key', '-k',
                    help='Path to aspera private key\nRequired when using aspera protocol\nDefault location: ~/.aspera/connect/etc/asperaweb_id_dsa.openssh')
    parser.add_argument('--output', '-o',
                    help='Output directory\nDefault format: [accession].fastq.download\nAuto-create missing directories')
    args = parser.parse_args()

    if args.type == 'aspera' and not args.key:
        parser.error('--key is required when using aspera protocol')

    output_dir = args.output or f"{args.accession}.fastq.download"
    return args.accession, args.type, args.key, output_dir

def build_download_command(link: str, protocol: str, output_dir: str, key_path: str = None) -> str:
    if protocol == 'ftp':
        return f'wget -c {link} -P {output_dir}'
    elif protocol == 'aspera' and key_path:
        return f'ascp -P33001 -i {key_path} -QT -l100m -k1 -T {output_dir} {link}'
    

def process_metadata(accession: str, protocol: str) -> List[str]:
    meta_file = f'.{accession}.meta.txt'
    
    try:
        with open(meta_file, 'r') as f:
            header = f.readline().strip().split('\t')
            column_index = header.index('fastq_aspera' if protocol == 'aspera' else 'fastq_ftp')
            
            return [
    link.strip()
    for line in f
    if line.strip()
    for link in line.strip().split('\t')[column_index].split(';')
    if link.strip()
]
    except FileNotFoundError:
        print(f'Metadata file {meta_file} not found')
        return []


def main():
    accession, protocol, key_path, output_dir = parse_args()
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Fetch metadata file
    fetch_tsv(accession, output_path=f'.{accession}.meta.txt')
    
    # Process metadata
    download_links = process_metadata(accession, protocol)
    
    # Build download commands
    commands = [
        build_download_command(link, protocol, output_dir, key_path)
        for link in download_links
    ]
    
    # Execute download
    with ThreadPoolExecutor() as executor:
        executor.map(os.system, commands)

if __name__ == '__main__':
    main()