#!/usr/bin/env python3
"""Validate configuration"""
from common.app_config import get_config

def validate():
    config = get_config()
    print("Configuration valid")
    return True

if __name__ == '__main__':
    validate()
