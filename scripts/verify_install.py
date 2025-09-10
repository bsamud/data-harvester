#!/usr/bin/env python3
"""Verify data-harvester installation by checking all module imports."""

import sys

def check_import(module_name, description):
    """Try to import a module and report result."""
    try:
        __import__(module_name)
        print(f"  [OK] {description}")
        return True
    except ImportError as e:
        print(f"  [FAIL] {description}: {e}")
        return False

def main():
    print("Verifying data-harvester installation...\n")

    results = []

    # Core modules
    print("Core Modules:")
    results.append(check_import("ingest", "Ingest (web scraping)"))
    results.append(check_import("extract", "Extract (NLP/PDF)"))
    results.append(check_import("classify", "Classify (ML)"))
    results.append(check_import("scrub", "Scrub (text cleaning)"))
    results.append(check_import("enrich", "Enrich (data enrichment)"))
    results.append(check_import("convert", "Convert (format conversion)"))
    results.append(check_import("aggregate", "Aggregate (data loading)"))

    print("\nCommon Services:")
    results.append(check_import("common.logger", "Logger"))
    results.append(check_import("common.app_config", "AppConfig"))
    results.append(check_import("common.s3_utilities", "S3 Utilities"))
    results.append(check_import("common.parallel_processor", "Parallel Processor"))

    print("\nPlugin System:")
    results.append(check_import("plugins.core.plugin_base", "Plugin Base"))
    results.append(check_import("plugins.core.plugin_loader", "Plugin Loader"))

    print("\nDependencies:")
    results.append(check_import("scrapy", "Scrapy"))
    results.append(check_import("spacy", "spaCy"))
    results.append(check_import("sklearn", "scikit-learn"))
    results.append(check_import("pandas", "pandas"))
    results.append(check_import("boto3", "boto3 (AWS)"))
    results.append(check_import("PyPDF2", "PyPDF2"))

    # Summary
    passed = sum(results)
    total = len(results)
    print(f"\n{'='*40}")
    print(f"Results: {passed}/{total} checks passed")

    if passed == total:
        print("Installation verified successfully!")
        return 0
    else:
        print("Some checks failed. Review errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
