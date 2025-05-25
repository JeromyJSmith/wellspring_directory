#!/bin/bash

# Wellspring Book Production Setup Script
# This script initializes the complete environment for AI-assisted book production

set -e # Exit on any error

echo "🌊 Wellspring Book Production Setup"
echo "===================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project configuration
WORKSPACE_DIR="/Users/ojeromyo/Desktop/wellspring_directory"
DB_PATH="shared_utils/data/wellspring.db"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
echo ""
print_status "Checking prerequisites..."

# Check if we're in the right directory
if [[ ! -f "README.md" ]] || [[ ! -d ".cursor" ]]; then
    print_error "Please run this script from the wellspring_directory root"
    exit 1
fi

# Check Node.js
if ! command -v node &>/dev/null; then
    print_error "Node.js is required but not installed"
    exit 1
fi

# Check Python
if ! command -v python3 &>/dev/null; then
    print_error "Python 3 is required but not installed"
    exit 1
fi

print_success "Prerequisites check passed"

# Create directory structure
echo ""
print_status "Creating directory structure..."

mkdir -p em_dash_replacement/{input,output,logs,scripts,changelog,infographic_placeholders}
mkdir -p deep_research_agent/{citations,extracted_statements,reports,logs,scripts,visual_opportunities}
mkdir -p shared_utils/{data,notebooks}
mkdir -p docs
mkdir -p icons

print_success "Directory structure created"

# Install MCP dependencies
echo ""
print_status "Installing MCP server dependencies..."

# Core MCP servers
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-brave-search
npm install -g @modelcontextprotocol/server-fetch
npm install -g @modelcontextprotocol/server-puppeteer
npm install -g @modelcontextprotocol/server-time
npm install -g @modelcontextprotocol/server-sequential-thinking
npm install -g @modelcontextprotocol/server-sqlite

# Additional MCP servers
npm install -g mcp-server-firecrawl
npm install -g mcp-notion
npm install -g mcp-browser-tools
npm install -g mcp-wcgw
npm install -g mcp-21st-devmagic
npm install -g mcp-exa

print_success "MCP servers installed"

# Initialize SQLite database
echo ""
print_status "Initializing SQLite database..."

mkdir -p "$(dirname "$DB_PATH")"

sqlite3 "$DB_PATH" <<'EOF'
-- Research citations table
CREATE TABLE IF NOT EXISTS research_citations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_url TEXT NOT NULL,
    title TEXT,
    content TEXT,
    author TEXT,
    publish_date TEXT,
    extraction_method TEXT,
    confidence_score REAL,
    tags TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Typography processing sessions
CREATE TABLE IF NOT EXISTS typography_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_file TEXT NOT NULL,
    output_file TEXT NOT NULL,
    changes_made INTEGER DEFAULT 0,
    em_dashes_replaced INTEGER DEFAULT 0,
    processing_time_ms INTEGER,
    status TEXT DEFAULT 'completed',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Workflow status tracking
CREATE TABLE IF NOT EXISTS workflow_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    workflow_type TEXT NOT NULL,
    status TEXT NOT NULL,
    agent TEXT,
    task_description TEXT,
    progress_percentage INTEGER DEFAULT 0,
    details TEXT,
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    error_message TEXT
);

-- Agent coordination logs
CREATE TABLE IF NOT EXISTS agent_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_name TEXT NOT NULL,
    action TEXT NOT NULL,
    input_data TEXT,
    output_data TEXT,
    execution_time_ms INTEGER,
    status TEXT DEFAULT 'success',
    error_details TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Book production metadata
CREATE TABLE IF NOT EXISTS book_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_title TEXT,
    author TEXT,
    version TEXT,
    total_pages INTEGER,
    word_count INTEGER,
    last_processed DATETIME,
    status TEXT DEFAULT 'in_progress'
);

-- Insert initial data
INSERT OR IGNORE INTO book_metadata (book_title, author, version, status) 
VALUES ('The Wellspring Manual', 'AI-Assisted Production', '1.0.0', 'in_progress');

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_research_citations_url ON research_citations(source_url);
CREATE INDEX IF NOT EXISTS idx_workflow_status_type ON workflow_status(workflow_type);
CREATE INDEX IF NOT EXISTS idx_agent_logs_agent ON agent_logs(agent_name);
CREATE INDEX IF NOT EXISTS idx_typography_sessions_file ON typography_sessions(input_file);
EOF

print_success "Database initialized with schema"

# Create environment template
echo ""
print_status "Creating environment configuration template..."

cat >env_template.txt <<'EOF'
# Wellspring Book Production Environment Configuration
# Copy these variables to your .env file and fill in actual values

# WEB SEARCH & RESEARCH TOOLS
BRAVE_API_KEY=your_brave_search_api_key_here
FIRECRAWL_API_KEY=your_firecrawl_api_key_here
EXA_API_KEY=your_exa_search_api_key_here

# EXTERNAL INTEGRATIONS
NOTION_TOKEN=your_notion_integration_token_here

# PROJECT PATHS
WELLSPRING_WORKSPACE=/Users/ojeromyo/Desktop/wellspring_directory
FILESYSTEM_ALLOWED_PATHS=/Users/ojeromyo/Desktop/wellspring_directory

# COMPONENT SETTINGS
EM_DASH_REPLACEMENT_ENABLED=true
DEEP_RESEARCH_AGENT_ENABLED=true
MAX_RESEARCH_SOURCES=50
EOF

print_success "Environment template created (see env_template.txt)"

# Test database connectivity
echo ""
print_status "Testing database connectivity..."

if sqlite3 "$DB_PATH" "SELECT 'Database OK' as status;"; then
    print_success "Database connectivity test passed"
else
    print_error "Database connectivity test failed"
    exit 1
fi

# Create initial test files
echo ""
print_status "Creating test files..."

# Create a sample input file for em dash testing
cat >em_dash_replacement/input/sample_test.txt <<'EOF'
This is a sample text file for testing the em dash replacement functionality. 

The text contains various types of dashes -- like this -- that should be converted to proper em dashes.

Here are some examples:
- Regular text with -- double hyphens -- that need fixing
- Text with spaced -- dashes -- throughout
- Mixed content with--attached--dashes

This file will be used to test the typography correction workflow.
EOF

print_success "Sample test file created"

# Activate virtual environment and install Python dependencies
echo ""
print_status "Setting up Python environment..."

if [[ -d ".venv" ]]; then
    source .venv/bin/activate
    pip install --upgrade pip
    pip install sqlite3 pathlib datetime
    print_success "Python environment activated and updated"
else
    print_warning "Virtual environment not found at .venv/"
fi

# Display setup summary
echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
print_success "Wellspring book production system is ready!"
echo ""
echo "Next steps:"
echo "1. Create a .env file with your API keys (see env_template.txt)"
echo "2. Restart Cursor to load the new MCP configuration"
echo "3. Test the system with: 'Test em dash replacement workflow'"
echo "4. Refer to .cursor/rules/setup_guide.mdc for detailed instructions"
echo ""
echo "Available workflows:"
echo "- Em dash replacement: Process files in em_dash_replacement/input/"
echo "- Deep research: AI-powered research with citation management"
echo "- Integrated book production: End-to-end content processing"
echo ""
echo "Agent system:"
echo "- PlanningArchitect: Coordinates all workflows"
echo "- DataLayerAgent (Roo): Manages all data operations"
echo "- DeepResearchAgent: Handles web research and citations"
echo "- TypographyAgent: Processes text for typography corrections"
echo "- And more specialized agents for specific tasks"
echo ""
print_status "Check .cursor/rules/ for complete documentation"
