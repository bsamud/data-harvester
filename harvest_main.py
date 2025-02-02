#!/usr/bin/env python3
"""Main entry point for dataHarvest"""
import argparse
from common.logger import log
from common.app_config import get_config

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='dataHarvest Framework')
    parser.add_argument('-c', '--config', default='appconfig.ini')
    parser.add_argument('-p', '--process', help='Process ID')
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()

    config = get_config(args.config)
    log.info(f"dataHarvest started with config: {args.config}")

    if args.process:
        log.info(f"Running process: {args.process}")

if __name__ == '__main__':
    main()
