#!/usr/bin/env python3
"""
Wellspring Database Initialization Script
Creates and initializes the SQLite database with all required tables.
"""

import sqlite3
import os
from datetime import datetime
from pathlib import Path

# Database configuration
DB_PATH = Path(__file__).parent / "wellspring.db"
SCHEMA_VERSION = "1.0.0"

def create_database():
    """Create the Wellspring database with all required tables."""
    
    # Remove existing database if it exists
    if DB_PATH.exists():
        print(f"Removing existing database: {DB_PATH}")
        DB_PATH.unlink()
    
    # Create new database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Create database metadata table
    cursor.execute("""
        CREATE TABLE database_metadata (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Insert database metadata
    cursor.execute("""
        INSERT INTO database_metadata (key, value) VALUES 
        ('schema_version', ?),
        ('created_at', ?),
        ('book_title', 'The Wellspring Manual'),
        ('author', 'Brian V Jones'),
        ('total_pages', '300')
    """, (SCHEMA_VERSION, datetime.now().isoformat()))
    
    # Create research citations table
    cursor.execute("""
        CREATE TABLE research_citations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            citation_text TEXT NOT NULL,
            source_url TEXT,
            author TEXT,
            publication_date DATE,
            chapter_reference TEXT,
            page_number INTEGER,
            relevance_score REAL DEFAULT 0.0,
            verification_status TEXT DEFAULT 'pending',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create typography sessions table
    cursor.execute("""
        CREATE TABLE typography_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_name TEXT NOT NULL,
            input_file_path TEXT NOT NULL,
            output_file_path TEXT,
            em_dashes_found INTEGER DEFAULT 0,
            em_dashes_replaced INTEGER DEFAULT 0,
            replacement_patterns TEXT, -- JSON string of patterns
            processing_status TEXT DEFAULT 'pending',
            error_log TEXT,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            processing_time_seconds INTEGER
        )
    """)
    
    # Create workflow status table
    cursor.execute("""
        CREATE TABLE workflow_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workflow_name TEXT NOT NULL,
            workflow_type TEXT NOT NULL, -- 'em_dash', 'research', 'typography', 'full'
            status TEXT DEFAULT 'pending', -- 'pending', 'running', 'completed', 'failed'
            progress_percentage INTEGER DEFAULT 0,
            current_step TEXT,
            total_steps INTEGER,
            input_data TEXT, -- JSON string
            output_data TEXT, -- JSON string
            error_message TEXT,
            agent_assignments TEXT, -- JSON string of agent->task mappings
            started_by TEXT DEFAULT 'system',
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            estimated_completion TIMESTAMP
        )
    """)
    
    # Create agent logs table
    cursor.execute("""
        CREATE TABLE agent_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_name TEXT NOT NULL,
            agent_type TEXT NOT NULL,
            workflow_id INTEGER,
            action_type TEXT NOT NULL, -- 'start', 'progress', 'complete', 'error'
            message TEXT NOT NULL,
            data_payload TEXT, -- JSON string
            execution_time_ms INTEGER,
            memory_usage_mb INTEGER,
            logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (workflow_id) REFERENCES workflow_status(id)
        )
    """)
    
    # Create book metadata table
    cursor.execute("""
        CREATE TABLE book_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_name TEXT UNIQUE NOT NULL,
            property_value TEXT NOT NULL,
            property_type TEXT DEFAULT 'string', -- 'string', 'integer', 'boolean', 'json'
            section TEXT, -- 'general', 'typography', 'layout', 'content'
            is_editable BOOLEAN DEFAULT 1,
            description TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Insert book metadata
    book_metadata = [
        ('title', 'The Wellspring Manual', 'string', 'general', 1, 'Book title'),
        ('subtitle', 'Best practices for rapid delivery of behavioral health continuum infrastructure', 'string', 'general', 1, 'Book subtitle'),
        ('author', 'Brian V Jones', 'string', 'general', 1, 'Primary author'),
        ('organization', 'BHSME - Behavioral Health Subject Matter Experts', 'string', 'general', 1, 'Publishing organization'),
        ('contact_email', 'contact@bhsme.org', 'string', 'general', 1, 'Contact email'),
        ('publish_date', 'November 1, 2024', 'string', 'general', 1, 'Publication date'),
        ('total_pages', '300', 'integer', 'general', 1, 'Total number of pages'),
        ('current_phase', 'editing_and_formatting', 'string', 'general', 1, 'Current production phase'),
        ('margin_increase_points', '3', 'integer', 'typography', 1, 'Margin increase in points'),
        ('header_color_scheme', 'blue_gold', 'string', 'typography', 1, 'Header color scheme'),
        ('font_size_reduction_toc', '2', 'integer', 'typography', 1, 'Table of contents font size reduction'),
        ('blank_page_layout', '1', 'boolean', 'layout', 1, 'Use blank left pages before sections'),
        ('architectural_corners', '1', 'boolean', 'layout', 1, 'Include architectural corner designs'),
        ('infographics_enabled', '1', 'boolean', 'content', 1, 'Include infographics and visual aids'),
        ('checklist_format', '1', 'boolean', 'content', 1, 'Convert sections to checklists where appropriate')
    ]
    
    cursor.executemany("""
        INSERT INTO book_metadata (property_name, property_value, property_type, section, is_editable, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, book_metadata)
    
    # Create em dash patterns table
    cursor.execute("""
        CREATE TABLE em_dash_patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_text TEXT NOT NULL,
            context_before TEXT,
            context_after TEXT,
            replacement_text TEXT NOT NULL,
            replacement_type TEXT NOT NULL, -- 'comma', 'period', 'semicolon', 'colon', 'parentheses'
            confidence_score REAL DEFAULT 0.0,
            manual_review BOOLEAN DEFAULT 0,
            chapter_location TEXT,
            page_number INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            applied_at TIMESTAMP
        )
    """)
    
    # Create visual opportunities table
    cursor.execute("""
        CREATE TABLE visual_opportunities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_description TEXT NOT NULL,
            content_type TEXT NOT NULL, -- 'infographic', 'chart', 'checklist', 'diagram'
            data_content TEXT NOT NULL,
            suggested_format TEXT, -- 'bar_chart', 'pie_chart', 'flowchart', 'table', 'icon_list'
            priority_level TEXT DEFAULT 'medium', -- 'high', 'medium', 'low'
            chapter_reference TEXT,
            page_number INTEGER,
            implementation_status TEXT DEFAULT 'pending', -- 'pending', 'in_progress', 'completed'
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create indexes for performance
    cursor.execute("CREATE INDEX idx_citations_chapter ON research_citations(chapter_reference)")
    cursor.execute("CREATE INDEX idx_typography_status ON typography_sessions(processing_status)")
    cursor.execute("CREATE INDEX idx_workflow_status ON workflow_status(status, workflow_type)")
    cursor.execute("CREATE INDEX idx_agent_logs_workflow ON agent_logs(workflow_id, agent_name)")
    cursor.execute("CREATE INDEX idx_em_dash_chapter ON em_dash_patterns(chapter_location)")
    
    # Commit changes and close
    conn.commit()
    conn.close()
    
    print(f"✅ Database created successfully: {DB_PATH}")
    print(f"📊 Database size: {DB_PATH.stat().st_size} bytes")
    
    return True

def verify_database():
    """Verify database integrity and show table information."""
    
    if not DB_PATH.exists():
        print("❌ Database does not exist!")
        return False
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print(f"\n📋 Database Tables ({len(tables)} total):")
    
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"  • {table_name}: {count} records")
    
    # Show database metadata
    cursor.execute("SELECT key, value FROM database_metadata")
    metadata = cursor.fetchall()
    
    print(f"\n🔧 Database Metadata:")
    for key, value in metadata:
        print(f"  • {key}: {value}")
    
    conn.close()
    print(f"\n✅ Database verification completed successfully!")
    return True

if __name__ == "__main__":
    print("🚀 Initializing Wellspring Database...")
    
    # Create database directory if it doesn't exist
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # Create and initialize database
    if create_database():
        verify_database()
        print(f"\n🎉 Wellspring database is ready for use!")
    else:
        print(f"\n❌ Database initialization failed!")
        exit(1)