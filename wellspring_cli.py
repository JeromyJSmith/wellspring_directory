#!/usr/bin/env python3
"""
Wellspring Book Production CLI
Main command-line interface for the Wellspring AI-assisted book production system.
"""

import asyncio
import argparse
import sys
import json
from pathlib import Path
from datetime import datetime
import logging

# Add project modules to path
sys.path.append(str(Path(__file__).parent))

from shared_utils.agent_coordinator import AgentCoordinator
from shared_utils.data.init_database import create_database, verify_database
from em_dash_replacement.scripts.em_dash_analyzer import EmDashAnalyzer
from em_dash_replacement.scripts.em_dash_processor import EmDashProcessor, ProcessingSession
from deep_research_agent.scripts.deep_research_agent import DeepResearchAgent

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WellspringCLI:
    """Main CLI interface for Wellspring book production system."""
    
    def __init__(self):
        """Initialize the CLI."""
        self.project_root = Path(__file__).parent
        self.db_path = self.project_root / "shared_utils" / "data" / "wellspring.db"
        self.coordinator = None
        
    def setup_system(self):
        """Initialize the complete system."""
        print("🚀 Initializing Wellspring Book Production System...")
        print("=" * 60)
        
        # Create database if it doesn't exist
        if not self.db_path.exists():
            print("📊 Creating database...")
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            create_database()
            print("✅ Database created successfully!")
        else:
            print("📊 Verifying existing database...")
            verify_database()
            print("✅ Database verified!")
        
        # Initialize agent coordinator
        print("🤖 Initializing agent coordinator...")
        self.coordinator = AgentCoordinator(str(self.db_path))
        print("✅ Agent coordinator ready!")
        
        # Create required directories
        directories = [
            "em_dash_replacement/input",
            "em_dash_replacement/output", 
            "em_dash_replacement/logs",
            "deep_research_agent/reports",
            "deep_research_agent/citations",
            "deep_research_agent/logs",
            "shared_utils/data"
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
        
        print("📁 Directory structure verified!")
        print("\n🎉 System initialization completed successfully!")
        
        return True
    
    def analyze_em_dashes(self, input_file: str, chapter_name: str = None):
        """Analyze em dashes in a file."""
        print(f"🔍 Analyzing em dashes in: {input_file}")
        
        input_path = Path(input_file)
        if not input_path.exists():
            print(f"❌ Input file not found: {input_file}")
            return False
        
        # Initialize analyzer
        analyzer = EmDashAnalyzer(str(self.db_path))
        
        # Analyze file
        matches = analyzer.analyze_file(input_path)
        
        if matches:
            # Generate report
            report = analyzer.generate_analysis_report(matches)
            
            # Display results
            print(f"\n📊 Analysis Results:")
            print(f"  • Total em dashes found: {report['total_matches']}")
            print(f"  • Average confidence: {report['average_confidence']}")
            print(f"  • High confidence replacements: {report['high_confidence_replacements']}")
            print(f"  • Manual review needed: {report['manual_review_needed']}")
            
            print(f"\n📋 Replacement Types:")
            for rep_type, count in report['replacement_types'].items():
                print(f"  • {rep_type}: {count}")
            
            print(f"\n💡 Recommendation: {report['processing_recommendation']}")
            
            # Save to database
            chapter_location = chapter_name or input_path.stem
            analyzer.save_analysis_to_db(matches, chapter_location)
            print(f"\n✅ Analysis saved to database")
            
            return True
        else:
            print("ℹ️  No em dashes found in the file")
            return False
    
    def process_em_dashes(self, input_file: str, output_file: str = None, dry_run: bool = True, confidence_threshold: float = 0.8):
        """Process em dash replacements."""
        print(f"🔧 Processing em dashes: {input_file}")
        print(f"   Dry run: {dry_run}")
        print(f"   Confidence threshold: {confidence_threshold}")
        
        input_path = Path(input_file)
        if not input_path.exists():
            print(f"❌ Input file not found: {input_file}")
            return False
        
        # Determine output file
        if output_file is None:
            output_dir = self.project_root / "em_dash_replacement" / "output"
            output_path = output_dir / f"{input_path.stem}_processed.txt"
        else:
            output_path = Path(output_file)
        
        # Initialize processor
        processor = EmDashProcessor(str(self.db_path))
        
        # Create processing session
        session = ProcessingSession(
            session_name=f"processing_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            input_file=input_path,
            output_file=output_path,
            dry_run=dry_run,
            confidence_threshold=confidence_threshold
        )
        
        # Process file
        result = processor.process_file(session)
        
        if result['success']:
            print("\n✅ Processing completed successfully!")
            
            # Display processed content preview if dry run
            if dry_run and result.get('processed_content'):
                print("\n📄 Processed Content Preview:")
                print("-" * 50)
                preview = result['processed_content'][:500]
                print(preview + "..." if len(result['processed_content']) > 500 else preview)
                print("-" * 50)
            
            # Display report
            report = processor.generate_processing_report(result['stats'])
            print(f"\n{report}")
            
            if not dry_run:
                print(f"\n📁 Output saved to: {output_path}")
            
            return True
        else:
            print(f"\n❌ Processing failed: {result['error']}")
            return False
    
    def run_deep_research(self, input_file: str, chapter_name: str = None):
        """Run deep research analysis."""
        print(f"🔍 Running deep research analysis: {input_file}")
        
        input_path = Path(input_file)
        if not input_path.exists():
            print(f"❌ Input file not found: {input_file}")
            return False
        
        # Read file content
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return False
        
        # Initialize research agent
        agent = DeepResearchAgent(str(self.db_path))
        
        chapter_location = chapter_name or input_path.stem
        
        # Perform research analysis
        print("🔍 Extracting quotes...")
        quotes = agent.extract_quotes(content, chapter_location)
        
        print("📚 Researching citations...")
        citations = []
        for quote in quotes:
            citation = agent.research_quote_authenticity(quote)
            citation.relevance_score = agent.verify_quote_relevance(quote, content)
            citations.append(citation)
        
        print("✅ Fact-checking claims...")
        fact_checks = agent.fact_check_claims(content)
        
        print("🎨 Identifying visual opportunities...")
        visual_ops = agent.identify_visual_opportunities(content, chapter_location)
        
        # Generate and display report
        report = agent.generate_research_report(quotes, citations, fact_checks, visual_ops)
        print(f"\n{report}")
        
        # Save results to database
        agent.save_research_results(quotes, citations, fact_checks, visual_ops)
        print(f"\n✅ Research results saved to database")
        
        # Save detailed report
        report_dir = self.project_root / "deep_research_agent" / "reports"
        report_file = report_dir / f"{chapter_location}_research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
            f.write("\n\n" + "="*60 + "\n")
            f.write("DETAILED FINDINGS\n")
            f.write("="*60 + "\n\n")
            
            f.write("QUOTES FOUND:\n")
            for i, quote in enumerate(quotes, 1):
                f.write(f"{i}. \"{quote.text}\" - {quote.author}\n")
                f.write(f"   Context: {quote.context[:100]}...\n")
                f.write(f"   Relevance: {agent.verify_quote_relevance(quote, content):.2f}\n\n")
            
            f.write("\nVISUAL OPPORTUNITIES:\n")
            for i, vo in enumerate(visual_ops, 1):
                f.write(f"{i}. {vo.content_type} - {vo.suggested_format} ({vo.priority_level} priority)\n")
                f.write(f"   Location: {vo.location}\n")
                f.write(f"   Content: {vo.data_content[:100]}...\n\n")
        
        print(f"📄 Detailed report saved to: {report_file}")
        
        return True
    
    async def run_full_workflow(self, workflow_type: str, input_data: dict):
        """Run a complete workflow using the agent coordinator."""
        if not self.coordinator:
            print("❌ System not initialized. Run 'setup' command first.")
            return False
        
        print(f"🚀 Starting {workflow_type} workflow...")
        
        try:
            # Create workflow
            workflow_id = self.coordinator.create_workflow(workflow_type, input_data)
            print(f"📋 Created workflow: {workflow_id}")
            
            # Execute workflow
            print("⚡ Executing workflow...")
            result = await self.coordinator.execute_workflow(workflow_id)
            
            print(f"\n✅ Workflow completed!")
            print(f"   Status: {result['status'].value}")
            print(f"   Progress: {result['progress']:.1f}%")
            print(f"   Tasks completed: {len(result['results'])}")
            
            if result['started_at'] and result['completed_at']:
                duration = result['completed_at'] - result['started_at']
                print(f"   Duration: {duration.total_seconds():.1f} seconds")
            
            return True
            
        except Exception as e:
            print(f"❌ Workflow failed: {e}")
            return False
    
    def show_system_status(self):
        """Display current system status."""
        if not self.coordinator:
            print("❌ System not initialized. Run 'setup' command first.")
            return
        
        print("📊 Wellspring System Status")
        print("=" * 40)
        
        status = self.coordinator.get_system_status()
        
        print(f"Database connected: {status['database_connected']}")
        print(f"Active workflows: {status['active_workflows']}")
        print(f"Task queue size: {status['task_queue_size']}")
        print(f"Last update: {status['timestamp']}")
        
        print(f"\n🤖 Agent Status:")
        for name, info in status['agents'].items():
            status_icon = "🟢" if info['status'] == 'idle' else "🔄" if info['status'] == 'running' else "⚪"
            print(f"  {status_icon} {name}: {info['status']}")
            if info['current_task']:
                print(f"      Current task: {info['current_task']}")
            if info['performance_metrics']:
                metrics = info['performance_metrics']
                print(f"      Performance: {metrics}")
    
    def create_sample_files(self):
        """Create sample files for testing."""
        print("📝 Creating sample files for testing...")
        
        # Sample chapter content with em dashes and quotes
        sample_content = """Chapter 1: Setting the Vision for Behavioral Health Facilities

"The foundation of successful behavioral health facility development lies in comprehensive planning and stakeholder alignment" — Brian V Jones, BHSME

Introduction

This chapter explores the critical first steps—vision development and strategic planning—that determine project success.

The development process includes several key phases:
1. Concept planning and vision development  
2. Stakeholder alignment and team building
3. Site analysis and feasibility studies
4. Financial planning and budget development

Research indicates that 75% of behavioral health projects succeed when proper due diligence is conducted during the planning phase.

Key Components

The following components are essential—site selection, design coordination, and regulatory compliance. Each component requires specialized expertise and careful coordination between multiple stakeholders.

"Proper planning prevents poor performance, especially in complex healthcare projects" — Healthcare Design Institute

Budget allocation typically follows this pattern:
- Land acquisition and site preparation: 20-25% of total budget
- Design and professional services: 15-20% 
- Construction and build-out: 50-60%
- Equipment, furniture, and technology: 10-15%
- Contingency and project management: 5-10%

According to the National Institute of Mental Health, there is a critical shortage of behavioral health infrastructure—affecting over 2.5 million Americans who lack access to appropriate care facilities.

Development Timeline

The typical development timeline includes these phases—initial planning (3-6 months), design and permitting (6-12 months), and construction (12-18 months). However, complex projects may require additional time for specialized components.

Studies show that facilities designed with patient-centered approaches achieve 30% better treatment outcomes and 25% higher staff satisfaction rates.

Conclusion

Success in behavioral health facility development requires—careful planning, expert coordination, and unwavering commitment to quality. The investment in proper upfront planning—while significant—pays dividends throughout the project lifecycle.
"""
        
        # Create sample input file
        input_dir = self.project_root / "em_dash_replacement" / "input"
        sample_file = input_dir / "sample_chapter_1.txt"
        
        with open(sample_file, 'w', encoding='utf-8') as f:
            f.write(sample_content)
        
        print(f"✅ Created sample file: {sample_file}")
        
        # Create another sample with different content
        sample_content_2 = """Chapter 2: Strategic Planning and Feasibility Analysis

"The key to successful behavioral health facility development lies in rigorous feasibility analysis and stakeholder engagement" — Dr. Sarah Mitchell, Healthcare Planning Consultant

Overview

This chapter covers the essential elements—feasibility studies, market analysis, and financial planning—that form the foundation of successful projects.

Market Analysis Components

The market analysis should include:
• Current service capacity and gaps
• Population demographics and growth projections  
• Competitive landscape assessment
• Regulatory environment analysis
• Payer mix and reimbursement trends

Financial Feasibility

According to industry studies, 68% of behavioral health facility projects exceed initial budget projections—primarily due to inadequate upfront analysis.

The financial feasibility study must address:
1. Capital requirements and funding sources
2. Operating revenue projections
3. Staffing and operational costs
4. Break-even analysis and ROI calculations
5. Risk assessment and mitigation strategies

"Without proper financial planning, even the best-intentioned projects can fail to serve their communities" — Journal of Healthcare Finance

Stakeholder Engagement

Effective stakeholder engagement—community leaders, healthcare providers, and regulatory bodies—is critical for project success. Research shows that projects with comprehensive stakeholder engagement have 40% higher success rates.

Key Performance Indicators

Monitor these critical metrics—occupancy rates, patient satisfaction scores, staff retention rates, and financial performance. Industry benchmarks suggest:
- Target occupancy rate: 85-90%
- Patient satisfaction: 4.5+ out of 5.0
- Staff turnover: Less than 15% annually
- Operating margin: 5-10% for sustainable operations

Implementation Timeline

The strategic planning phase typically requires 4-6 months—including market research, financial modeling, and stakeholder consultations. This investment in planning reduces downstream risks and improves project outcomes.
"""
        
        sample_file_2 = input_dir / "sample_chapter_2.txt"
        with open(sample_file_2, 'w', encoding='utf-8') as f:
            f.write(sample_content_2)
        
        print(f"✅ Created sample file: {sample_file_2}")
        print(f"\n📁 Sample files created in: {input_dir}")
        
        return True

def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Wellspring AI-Assisted Book Production System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s setup                                    # Initialize the system
  %(prog)s status                                   # Show system status
  %(prog)s create-samples                           # Create sample test files
  %(prog)s analyze chapter1.txt                     # Analyze em dashes
  %(prog)s process chapter1.txt --no-dry-run        # Process em dashes
  %(prog)s research chapter1.txt                    # Run deep research
  %(prog)s workflow em_dash_replacement chapter1.txt # Run full workflow
        """
    )
    
    parser.add_argument('command', choices=[
        'setup', 'status', 'create-samples', 'analyze', 'process', 'research', 'workflow'
    ], help='Command to execute')
    
    parser.add_argument('file', nargs='?', help='Input file for processing commands')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--chapter', '-c', help='Chapter name for context')
    parser.add_argument('--confidence', '-conf', type=float, default=0.8, help='Confidence threshold (0.0-1.0)')
    parser.add_argument('--dry-run', action='store_true', default=True, help='Run in dry-run mode (default)')
    parser.add_argument('--no-dry-run', action='store_true', help='Disable dry-run mode')
    parser.add_argument('--workflow-type', choices=['em_dash_replacement', 'deep_research', 'full_book_processing'], 
                       default='em_dash_replacement', help='Type of workflow to run')
    
    args = parser.parse_args()
    
    # Initialize CLI
    cli = WellspringCLI()
    
    # Handle commands
    if args.command == 'setup':
        success = cli.setup_system()
        sys.exit(0 if success else 1)
    
    elif args.command == 'status':
        cli.show_system_status()
        sys.exit(0)
    
    elif args.command == 'create-samples':
        success = cli.create_sample_files()
        sys.exit(0 if success else 1)
    
    elif args.command == 'analyze':
        if not args.file:
            print("❌ File argument required for analyze command")
            sys.exit(1)
        success = cli.analyze_em_dashes(args.file, args.chapter)
        sys.exit(0 if success else 1)
    
    elif args.command == 'process':
        if not args.file:
            print("❌ File argument required for process command")
            sys.exit(1)
        
        dry_run = not args.no_dry_run  # Default to dry run unless --no-dry-run is specified
        success = cli.process_em_dashes(args.file, args.output, dry_run, args.confidence)
        sys.exit(0 if success else 1)
    
    elif args.command == 'research':
        if not args.file:
            print("❌ File argument required for research command")
            sys.exit(1)
        success = cli.run_deep_research(args.file, args.chapter)
        sys.exit(0 if success else 1)
    
    elif args.command == 'workflow':
        if not args.file:
            print("❌ File argument required for workflow command")
            sys.exit(1)
        
        input_data = {
            'input_files': [args.file],
            'confidence_threshold': args.confidence,
            'dry_run': not args.no_dry_run,
            'chapter_name': args.chapter
        }
        
        success = asyncio.run(cli.run_full_workflow(args.workflow_type, input_data))
        sys.exit(0 if success else 1)
    
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()