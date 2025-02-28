#!/bin/bash
# Rename project from dataHarvest to data-harvester

echo "Renaming project references from dataHarvest to data-harvester..."

# Find all files except in .git directory
FILES=$(find . -type f \( -name "*.py" -o -name "*.md" -o -name "*.txt" -o -name "*.ini" -o -name "*.yaml" -o -name "*.sh" \) ! -path "./.git/*" ! -name "rename_project.sh")

for file in $FILES; do
    # Skip if file doesn't exist
    [ ! -f "$file" ] && continue

    # Create backup
    # cp "$file" "$file.bak"

    # Replace variations of dataHarvest
    # For package names (Python imports): dataHarvest -> data_harvester
    # For display names: dataHarvest -> data-harvester

    sed -i '' 's/dataHarvest/data-harvester/g' "$file"
    sed -i '' 's/DataHarvest/DataHarvester/g' "$file"

    echo "✓ Updated: $file"
done

echo ""
echo "Renaming complete!"
echo "Files updated: $(echo "$FILES" | wc -w)"
