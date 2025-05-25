#!/usr/bin/env python3
"""
Main Entry Point for Google ADK Em Dash Agent Framework
Provides CLI interface and orchestration for the em dash processing agents.
"""

import asyncio
import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

# Import agent framework components
from agents.em_dash_agents import (
    ORCHESTRATOR,
    analyze_file,
    process_file,
    create_and_execute_workflow,
    get_agent_status
)
from sessions.session_manager import SESSION_SERVICE
from config.agent_config import CONFIG

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EmDashCLI:
    """Command-line interface for the Google ADK Em Dash Agent Framework."""
    
    def __init__(self):
        """Initialize the CLI."""
        self.orchestrator = ORCHESTRATOR
        self.session_service = SESSION_SERVICE
        
    def create_parser(self) -> argparse.ArgumentParser:
        """Create the argument parser."""
        parser = argparse.ArgumentParser(
            description="Google ADK Em Dash Agent Framework",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Analyze a single file
  python main.py analyze sample.txt
  
  # Process a file with dry run
  python main.py process sample.txt output/ --dry-run
  
  # Execute complete workflow
  python main.py workflow "Chapter Processing" input/*.txt output/
  
  # Check system status
  python main.py status
  
  # List active sessions
  python main.py sessions list
            """
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Analyze command
        analyze_parser = subparsers.add_parser('analyze', help='Analyze files for em dash patterns')
        analyze_parser.add_argument('files', nargs='+', help='Files to analyze')
        analyze_parser.add_argument('--confidence', type=float, default=0.8, help='Confidence threshold')
        analyze_parser.add_argument('--context-length', type=int, default=50, help='Context length around em dashes')
        analyze_parser.add_argument('--output', help='Output file for analysis report')
        analyze_parser.add_argument('--session-id', help='Session ID for tracking')
        
        # Process command
        process_parser = subparsers.add_parser('process', help='Process files to replace em dashes')
        process_parser.add_argument('files', nargs='+', help='Files to process')
        process_parser.add_argument('output_dir', help='Output directory')
        process_parser.add_argument('--dry-run', action='store_true', help='Perform dry run only')
        process_parser.add_argument('--confidence', type=float, default=0.8, help='Confidence threshold')
        process_parser.add_argument('--backup', action='store_true', default=True, help='Create backups')
        process_parser.add_argument('--session-id', help='Session ID for tracking')
        
        # Workflow command
        workflow_parser = subparsers.add_parser('workflow', help='Execute complete em dash workflow')
        workflow_parser.add_argument('name', help='Workflow name')
        workflow_parser.add_argument('files', nargs='+', help='Input files')
        workflow_parser.add_argument('output_dir', help='Output directory')
        workflow_parser.add_argument('--config', help='Configuration file (JSON)')
        workflow_parser.add_argument('--dry-run-first', action='store_true', default=True, help='Perform dry run first')
        workflow_parser.add_argument('--parallel', action='store_true', help='Enable parallel processing')
        
        # Status command
        status_parser = subparsers.add_parser('status', help='Show system status')
        status_parser.add_argument('--detailed', action='store_true', help='Show detailed status')
        
        # Sessions command
        sessions_parser = subparsers.add_parser('sessions', help='Manage sessions')
        sessions_subparsers = sessions_parser.add_subparsers(dest='sessions_action')
        
        sessions_subparsers.add_parser('list', help='List active sessions')
        sessions_subparsers.add_parser('stats', help='Show session statistics')
        sessions_subparsers.add_parser('cleanup', help='Clean up expired sessions')
        
        session_get_parser = sessions_subparsers.add_parser('get', help='Get session details')
        session_get_parser.add_argument('session_id', help='Session ID')
        
        session_pause_parser = sessions_subparsers.add_parser('pause', help='Pause session')
        session_pause_parser.add_argument('session_id', help='Session ID')
        
        session_resume_parser = sessions_subparsers.add_parser('resume', help='Resume session')
        session_resume_parser.add_argument('session_id', help='Session ID')
        
        # Config command
        config_parser = subparsers.add_parser('config', help='Show configuration')
        config_parser.add_argument('--agents', action='store_true', help='Show agent configurations')
        config_parser.add_argument('--tools', action='store_true', help='Show tool configurations')
        
        return parser
    
    async def run_analyze(self, args) -> int:
        """Run analysis command."""
        try:
            print(f"🔍 Analyzing {len(args.files)} file(s) for em dash patterns...")
            
            configuration = {
                'confidence_threshold': args.confidence,
                'context_length': args.context_length
            }
            
            results = []
            for file_path in args.files:
                print(f"  • Analyzing: {file_path}")
                
                result = await analyze_file(
                    file_path,
                    session_id=args.session_id,
                    configuration=configuration
                )
                
                results.append({
                    'file': file_path,
                    'result': result
                })
                
                # Print summary
                if 'em_dash_analysis' in result:
                    analysis = result['em_dash_analysis']
                    print(f"    ✓ Found {analysis.get('total_em_dashes', 0)} em dash patterns")
                    print(f"    ✓ Average confidence: {analysis.get('average_confidence', 0):.2f}")
            
            # Save results if output specified
            if args.output:
                output_path = Path(args.output)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_path, 'w') as f:
                    json.dump(results, f, indent=2, default=str)
                
                print(f"📄 Analysis results saved to: {output_path}")
            
            print(f"✅ Analysis completed successfully!")
            return 0
            
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            logger.error(f"Analysis error: {e}")
            return 1
    
    async def run_process(self, args) -> int:
        """Run processing command."""
        try:
            print(f"🔧 Processing {len(args.files)} file(s) for em dash replacement...")
            
            configuration = {
                'confidence_threshold': args.confidence,
                'backup_enabled': args.backup,
                'dry_run': args.dry_run
            }
            
            results = []
            for file_path in args.files:
                print(f"  • Processing: {file_path} {'(DRY RUN)' if args.dry_run else ''}")
                
                result = await process_file(
                    file_path,
                    args.output_dir,
                    dry_run=args.dry_run,
                    session_id=args.session_id,
                    configuration=configuration
                )
                
                results.append({
                    'file': file_path,
                    'result': result
                })
                
                # Print summary
                if 'em_dash_processing' in result:
                    processing = result['em_dash_processing']
                    print(f"    ✓ Replaced {processing.get('replacements_made', 0)}/{processing.get('total_em_dashes', 0)} em dashes")
                    if processing.get('backup_file'):
                        print(f"    ✓ Backup created: {processing['backup_file']}")
            
            print(f"✅ Processing completed successfully!")
            return 0
            
        except Exception as e:
            print(f"❌ Processing failed: {e}")
            logger.error(f"Processing error: {e}")
            return 1
    
    async def run_workflow(self, args) -> int:
        """Run workflow command."""
        try:
            print(f"🚀 Executing workflow: {args.name}")
            print(f"  • Input files: {len(args.files)}")
            print(f"  • Output directory: {args.output_dir}")
            
            # Load configuration if provided
            configuration = {}
            if args.config:
                with open(args.config, 'r') as f:
                    configuration = json.load(f)
            
            # Add CLI options to configuration
            configuration.update({
                'dry_run_first': args.dry_run_first,
                'parallel_processing': args.parallel
            })
            
            result = await create_and_execute_workflow(
                args.name,
                args.files,
                args.output_dir,
                configuration=configuration
            )
            
            # Print workflow summary
            if 'workflow_coordination' in result:
                workflow = result['workflow_coordination']
                print(f"  ✓ Workflow ID: {workflow.get('workflow_id')}")
                print(f"  ✓ Status: {workflow.get('status')}")
                print(f"  ✓ Progress: {workflow.get('progress_percentage', 0):.1f}%")
            
            print(f"✅ Workflow completed successfully!")
            return 0
            
        except Exception as e:
            print(f"❌ Workflow failed: {e}")
            logger.error(f"Workflow error: {e}")
            return 1
    
    def run_status(self, args) -> int:
        """Run status command."""
        try:
            print("📊 Google ADK Em Dash Agent Framework Status")
            print("=" * 60)
            
            status = get_agent_status()
            
            # System information
            print(f"\n🖥️  System Information:")
            config = status['configuration']
            print(f"  • Database connected: {config['database_connected']}")
            print(f"  • Default model: {config['default_model']}")
            print(f"  • Workspace: {config['workspace_path']}")
            print(f"  • Active sessions: {status['active_sessions']}")
            
            # Agent status
            print(f"\n🤖 Agent Status:")
            for name, info in status['agents'].items():
                print(f"  • {name}:")
                print(f"    - Status: {info['status']}")
                print(f"    - Model: {info['model']}")
                print(f"    - Capabilities: {', '.join(info['capabilities'])}")
            
            # Detailed information if requested
            if args.detailed:
                print(f"\n📈 Session Statistics:")
                session_stats = self.session_service.get_session_statistics()
                print(f"  • Active sessions: {session_stats['active_sessions']}")
                print(f"  • By agent: {session_stats['by_agent']}")
                print(f"  • By type: {session_stats['by_type']}")
                print(f"  • By status: {session_stats['by_status']}")
            
            return 0
            
        except Exception as e:
            print(f"❌ Status check failed: {e}")
            logger.error(f"Status error: {e}")
            return 1
    
    def run_sessions(self, args) -> int:
        """Run sessions command."""
        try:
            if args.sessions_action == 'list':
                sessions = self.session_service.list_sessions()
                print(f"📋 Active Sessions ({len(sessions)}):")
                
                if not sessions:
                    print("  No active sessions")
                else:
                    for session in sessions:
                        print(f"  • {session.session_id}")
                        print(f"    - Agent: {session.agent_name}")
                        print(f"    - Type: {session.session_type}")
                        print(f"    - Status: {session.status}")
                        print(f"    - Created: {session.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            
            elif args.sessions_action == 'stats':
                stats = self.session_service.get_session_statistics()
                print(f"📊 Session Statistics:")
                print(f"  • Active sessions: {stats['active_sessions']}")
                print(f"  • By agent: {stats['by_agent']}")
                print(f"  • By type: {stats['by_type']}")
                print(f"  • By status: {stats['by_status']}")
                
                if stats['oldest_session']:
                    print(f"  • Oldest session: {stats['oldest_session']['session_id']} ({stats['oldest_session']['created_at']})")
                if stats['newest_session']:
                    print(f"  • Newest session: {stats['newest_session']['session_id']} ({stats['newest_session']['created_at']})")
            
            elif args.sessions_action == 'cleanup':
                cleaned = self.session_service.cleanup_expired_sessions()
                print(f"🧹 Cleaned up {cleaned} expired sessions")
            
            elif args.sessions_action == 'get':
                session = self.session_service.get_session(args.session_id)
                if session:
                    print(f"📄 Session Details: {args.session_id}")
                    print(f"  • Agent: {session.agent_name}")
                    print(f"  • Type: {session.session_type}")
                    print(f"  • Status: {session.status}")
                    print(f"  • Created: {session.created_at}")
                    print(f"  • Last Activity: {session.last_activity}")
                    print(f"  • Input Data: {json.dumps(session.input_data, indent=2)}")
                    print(f"  • Progress: {json.dumps(session.progress_data, indent=2)}")
                else:
                    print(f"❌ Session not found: {args.session_id}")
                    return 1
            
            elif args.sessions_action == 'pause':
                if self.session_service.pause_session(args.session_id):
                    print(f"⏸️  Paused session: {args.session_id}")
                else:
                    print(f"❌ Failed to pause session: {args.session_id}")
                    return 1
            
            elif args.sessions_action == 'resume':
                if self.session_service.resume_session(args.session_id):
                    print(f"▶️  Resumed session: {args.session_id}")
                else:
                    print(f"❌ Failed to resume session: {args.session_id}")
                    return 1
            
            return 0
            
        except Exception as e:
            print(f"❌ Sessions command failed: {e}")
            logger.error(f"Sessions error: {e}")
            return 1
    
    def run_config(self, args) -> int:
        """Run config command."""
        try:
            print("⚙️  Google ADK Em Dash Agent Configuration")
            print("=" * 60)
            
            if args.agents:
                print(f"\n🤖 Agent Configurations:")
                for agent_name in ['em_dash_analyzer', 'em_dash_processor', 'em_dash_coordinator']:
                    config = CONFIG.get_agent_config(agent_name)
                    print(f"  • {agent_name}:")
                    print(f"    - Model: {config.model}")
                    print(f"    - Temperature: {config.temperature}")
                    print(f"    - Max Tokens: {config.max_tokens}")
                    print(f"    - Tools: {len(config.tools)}")
            
            if args.tools:
                print(f"\n🔧 Tool Configurations:")
                tool_configs = CONFIG.get_tool_configurations()
                for category, config in tool_configs.items():
                    print(f"  • {category}:")
                    for key, value in config.items():
                        print(f"    - {key}: {value}")
            
            if not args.agents and not args.tools:
                print(f"\n📋 General Configuration:")
                print(f"  • Database Path: {CONFIG.db_path}")
                print(f"  • Workspace Path: {CONFIG.workspace_path}")
                print(f"  • Default Model: {CONFIG.default_model}")
                print(f"  • Alternative Model: {CONFIG.alternative_model}")
            
            return 0
            
        except Exception as e:
            print(f"❌ Config command failed: {e}")
            logger.error(f"Config error: {e}")
            return 1
    
    async def run(self, args: List[str] = None) -> int:
        """Run the CLI with given arguments."""
        parser = self.create_parser()
        parsed_args = parser.parse_args(args)
        
        if not parsed_args.command:
            parser.print_help()
            return 1
        
        try:
            if parsed_args.command == 'analyze':
                return await self.run_analyze(parsed_args)
            elif parsed_args.command == 'process':
                return await self.run_process(parsed_args)
            elif parsed_args.command == 'workflow':
                return await self.run_workflow(parsed_args)
            elif parsed_args.command == 'status':
                return self.run_status(parsed_args)
            elif parsed_args.command == 'sessions':
                return self.run_sessions(parsed_args)
            elif parsed_args.command == 'config':
                return self.run_config(parsed_args)
            else:
                print(f"❌ Unknown command: {parsed_args.command}")
                return 1
                
        except KeyboardInterrupt:
            print(f"\n⚠️  Operation cancelled by user")
            return 130
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            logger.error(f"Unexpected error: {e}")
            return 1

async def main():
    """Main entry point."""
    print("🤖 Google ADK Em Dash Agent Framework")
    print("=" * 60)
    
    cli = EmDashCLI()
    exit_code = await cli.run()
    sys.exit(exit_code)

if __name__ == "__main__":
    asyncio.run(main())