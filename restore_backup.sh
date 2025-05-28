#!/bin/bash

# Quick Backup Restoration for Safe Experimentation
echo "🔄 Wellspring Backup Restoration"
echo "Available backups:"
ls -la chapter_formatting_backups/backup_*/

# Use latest backup by default
LATEST_BACKUP=$(ls -t chapter_formatting_backups/backup_*/ | head -1)
echo ""
echo "📁 Latest backup: $LATEST_BACKUP"
echo "🔄 Restoring output folder from backup..."

# Restore the output folder
rm -rf output/*
cp chapter_formatting_backups/backup_20250526_184648/* output/

echo "✅ Output folder restored!"
echo "📂 Files restored:"
ls -la output/

echo ""
echo "🎯 Ready for next experiment!"
