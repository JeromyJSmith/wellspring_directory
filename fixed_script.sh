#!/bin/bash

echo "\U0001F527 Creating full directory structure..."

mkdir -p em_dash_replacement/input
mkdir -p em_dash_replacement/output
mkdir -p em_dash_replacement/scripts
mkdir -p em_dash_replacement/logs
mkdir -p em_dash_replacement/infographic_placeholders
mkdir -p em_dash_replacement/changelog

mkdir -p deep_research_agent/extracted_statements
mkdir -p deep_research_agent/citations
mkdir -p deep_research_agent/visual_opportunities
mkdir -p deep_research_agent/scripts
mkdir -p deep_research_agent/logs
mkdir -p deep_research_agent/reports

mkdir -p shared_utils/uv_env
mkdir -p shared_utils/notebooks
mkdir -p shared_utils/data

echo "✅ Directory structure created."

echo "\U0001F680 Initializing UV Python environment..."

cd shared_utils/uv_env || exit 1

# Initialize UV project + create virtual env
uv init . && \
uv venv .venv --python python3.13 --seed && \
source .venv/bin/activate && \
uv pip install pandas jupyter rich openpyxl numpy matplotlib

echo "✅ UV environment set up and activated with pandas and jupyter installed."

echo "\U0001F4C2 You can now open Cursor IDE and start implementing your scripts in:"
echo "  - em_dash_replacement/scripts/"
echo "  - deep_research_agent/scripts/"
