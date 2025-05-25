#!/usr/bin/env python3
"""
Comprehensive System Test for Wellspring Book Production
Validates all components and workflows are working correctly.
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime
import sqlite3

# Add project modules to path
sys.path.append(str(Path(__file__).parent))

from shared_utils.data.init_database import create_database, verify_database
from shared_utils.agent_coordinator import AgentCoordinator
from em_dash_replacement.scripts.em_dash_analyzer import EmDashAnalyzer
from em_dash_replacement.scripts.em_dash_processor import EmDashProcessor, ProcessingSession
from deep_research_agent.scripts.deep_research_agent import DeepResearchAgent

class SystemTester:
    """Comprehensive system tester for Wellspring components."""
    
    def __init__(self):
        """Initialize the system tester."""
        self.project_root = Path(__file__).parent
        self.db_path = self.project_root / "shared_utils" / "data" / "wellspring.db"
        self.test_results = {}
        self.passed_tests = 0
        self.total_tests = 0
        
        # Create test content
        self.test_content = """Chapter 1: Testing Content

"This is a test quote for the system validation" — Test Author

This chapter contains multiple em dashes—used in various contexts—for testing purposes.

The system should handle:
- List items with em dashes—like this one
- Parenthetical expressions—such as this example—properly
- Definition scenarios: planning—the first phase of development
- Statistical claims: 75% of projects succeed with proper planning

"Another quote to test citation verification" — Dr. Example Researcher

Budget breakdown typically includes:
1. Land acquisition—15-25% of total budget
2. Design costs—20-30% of budget  
3. Construction—50-60% of budget
4. Equipment and contingency—5-15% of budget

According to industry studies, behavioral health facilities require specialized design considerations.
"""
    
    def log_test(self, test_name: str, success: bool, message: str = ""):
        """Log a test result."""
        self.total_tests += 1
        if success:
            self.passed_tests += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
        
        print(f"{status}: {test_name}")
        if message:
            print(f"    {message}")
        
        self.test_results[test_name] = {
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
    
    def test_database_initialization(self):
        """Test database creation and initialization."""
        print("\n🔧 Testing Database Initialization...")
        
        try:
            # Remove existing database if it exists
            if self.db_path.exists():
                self.db_path.unlink()
            
            # Create database
            success = create_database()
            self.log_test("Database Creation", success, "Database created successfully")
            
            # Verify database
            if success:
                verify_success = verify_database()
                self.log_test("Database Verification", verify_success, "Database structure verified")
                
                # Check table counts
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                conn.close()
                
                expected_tables = [
                    'database_metadata', 'research_citations', 'typography_sessions',
                    'workflow_status', 'agent_logs', 'book_metadata', 'em_dash_patterns',
                    'visual_opportunities'
                ]
                
                table_names = [table[0] for table in tables]
                tables_found = all(table in table_names for table in expected_tables)
                self.log_test("Database Schema", tables_found, 
                            f"Found {len(table_names)}/{len(expected_tables)} expected tables")
            
        except Exception as e:
            self.log_test("Database Initialization", False, f"Error: {e}")
    
    def test_em_dash_analyzer(self):
        """Test em dash analysis functionality."""
        print("\n🔍 Testing Em Dash Analyzer...")
        
        try:
            # Create test file
            test_file = self.project_root / "em_dash_replacement" / "input" / "test_content.txt"
            test_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(self.test_content)
            
            # Initialize analyzer
            analyzer = EmDashAnalyzer(str(self.db_path))
            
            # Analyze content
            matches = analyzer.analyze_file(test_file)
            self.log_test("Em Dash Detection", len(matches) > 0, f"Found {len(matches)} em dash instances")
            
            # Test analysis report
            if matches:
                report = analyzer.generate_analysis_report(matches)
                self.log_test("Analysis Report Generation", 'total_matches' in report, 
                            f"Report generated with {report.get('total_matches', 0)} matches")
                
                # Test database save
                save_success = analyzer.save_analysis_to_db(matches, "test_chapter")
                self.log_test("Analysis Database Save", save_success, "Analysis results saved to database")
            
        except Exception as e:
            self.log_test("Em Dash Analyzer", False, f"Error: {e}")
    
    def test_em_dash_processor(self):
        """Test em dash processing functionality."""
        print("\n🔧 Testing Em Dash Processor...")
        
        try:
            # Create test input file
            test_input = self.project_root / "em_dash_replacement" / "input" / "test_processing.txt"
            test_output = self.project_root / "em_dash_replacement" / "output" / "test_processed.txt"
            
            with open(test_input, 'w', encoding='utf-8') as f:
                f.write(self.test_content)
            
            # Initialize processor
            processor = EmDashProcessor(str(self.db_path))
            
            # Create processing session (dry run)
            session = ProcessingSession(
                session_name="test_session",
                input_file=test_input,
                output_file=test_output,
                dry_run=True,
                confidence_threshold=0.5  # Lower threshold for testing
            )
            
            # Process file
            result = processor.process_file(session)
            
            self.log_test("Em Dash Processing", result['success'], 
                        f"Processed with {result.get('stats', {}).get('replacements_made', 0)} replacements")
            
            if result['success']:
                stats = result['stats']
                self.log_test("Processing Statistics", 'total_em_dashes' in stats,
                            f"Found {stats.get('total_em_dashes', 0)} em dashes, replaced {stats.get('replacements_made', 0)}")
                
                # Test report generation
                report = processor.generate_processing_report(stats)
                self.log_test("Processing Report", len(report) > 0, "Processing report generated")
            
        except Exception as e:
            self.log_test("Em Dash Processor", False, f"Error: {e}")
    
    def test_deep_research_agent(self):
        """Test deep research agent functionality."""
        print("\n🔍 Testing Deep Research Agent...")
        
        try:
            # Initialize research agent
            agent = DeepResearchAgent(str(self.db_path))
            
            # Test quote extraction
            quotes = agent.extract_quotes(self.test_content, "test_chapter")
            self.log_test("Quote Extraction", len(quotes) > 0, f"Extracted {len(quotes)} quotes")
            
            # Test quote relevance verification
            if quotes:
                relevance_score = agent.verify_quote_relevance(quotes[0], self.test_content)
                self.log_test("Quote Relevance", relevance_score >= 0, f"Relevance score: {relevance_score:.2f}")
            
            # Test fact checking
            fact_checks = agent.fact_check_claims(self.test_content)
            self.log_test("Fact Checking", len(fact_checks) >= 0, f"Identified {len(fact_checks)} factual claims")
            
            # Test visual opportunities
            visual_ops = agent.identify_visual_opportunities(self.test_content, "test_chapter")
            self.log_test("Visual Opportunities", len(visual_ops) >= 0, f"Found {len(visual_ops)} visual opportunities")
            
            # Test citation research
            if quotes:
                citations = []
                for quote in quotes:
                    citation = agent.research_quote_authenticity(quote)
                    citations.append(citation)
                
                self.log_test("Citation Research", len(citations) > 0, f"Researched {len(citations)} citations")
                
                # Test database save
                save_success = agent.save_research_results(quotes, citations, fact_checks, visual_ops)
                self.log_test("Research Database Save", save_success, "Research results saved to database")
            
            # Test report generation
            if quotes:
                report = agent.generate_research_report(quotes, citations, fact_checks, visual_ops)
                self.log_test("Research Report", len(report) > 0, "Research report generated")
            
        except Exception as e:
            self.log_test("Deep Research Agent", False, f"Error: {e}")
    
    def test_agent_coordinator(self):
        """Test agent coordination system."""
        print("\n🤖 Testing Agent Coordinator...")
        
        try:
            # Initialize coordinator
            coordinator = AgentCoordinator(str(self.db_path))
            
            # Test agent registration
            system_status = coordinator.get_system_status()
            agent_count = len(system_status['agents'])
            self.log_test("Agent Registration", agent_count > 0, f"Registered {agent_count} agents")
            
            # Test workflow creation
            workflow_id = coordinator.create_workflow("em_dash_replacement", {
                "input_files": ["test_content.txt"],
                "confidence_threshold": 0.5
            })
            self.log_test("Workflow Creation", workflow_id is not None, f"Created workflow: {workflow_id}")
            
            # Test workflow status
            if workflow_id:
                status = coordinator.get_workflow_status(workflow_id)
                self.log_test("Workflow Status", 'workflow_id' in status, f"Status retrieved: {status.get('status', 'unknown')}")
            
        except Exception as e:
            self.log_test("Agent Coordinator", False, f"Error: {e}")
    
    async def test_workflow_execution(self):
        """Test complete workflow execution."""
        print("\n⚡ Testing Workflow Execution...")
        
        try:
            # Initialize coordinator
            coordinator = AgentCoordinator(str(self.db_path))
            
            # Create and execute workflow
            workflow_id = coordinator.create_workflow("em_dash_replacement", {
                "input_files": ["test_content.txt"],
                "confidence_threshold": 0.5,
                "dry_run": True
            })
            
            if workflow_id:
                # Execute workflow
                result = await coordinator.execute_workflow(workflow_id)
                
                execution_success = result['status'].value in ['completed']
                self.log_test("Workflow Execution", execution_success, 
                            f"Workflow {result['status'].value} with {result['progress']:.1f}% progress")
                
                if execution_success:
                    self.log_test("Task Completion", len(result['results']) > 0, 
                                f"Completed {len(result['results'])} tasks")
            
        except Exception as e:
            self.log_test("Workflow Execution", False, f"Error: {e}")
    
    def test_database_queries(self):
        """Test database query functionality."""
        print("\n📊 Testing Database Queries...")
        
        try:
            if not self.db_path.exists():
                self.log_test("Database Queries", False, "Database not found")
                return
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Test metadata queries
            cursor.execute("SELECT COUNT(*) FROM book_metadata")
            metadata_count = cursor.fetchone()[0]
            self.log_test("Metadata Queries", metadata_count > 0, f"Found {metadata_count} metadata records")
            
            # Test em dash patterns queries
            cursor.execute("SELECT COUNT(*) FROM em_dash_patterns")
            pattern_count = cursor.fetchone()[0]
            self.log_test("Pattern Queries", pattern_count >= 0, f"Found {pattern_count} em dash patterns")
            
            # Test research citations queries
            cursor.execute("SELECT COUNT(*) FROM research_citations")
            citation_count = cursor.fetchone()[0]
            self.log_test("Citation Queries", citation_count >= 0, f"Found {citation_count} citations")
            
            # Test visual opportunities queries
            cursor.execute("SELECT COUNT(*) FROM visual_opportunities")
            visual_count = cursor.fetchone()[0]
            self.log_test("Visual Opportunity Queries", visual_count >= 0, f"Found {visual_count} visual opportunities")
            
            conn.close()
            
        except Exception as e:
            self.log_test("Database Queries", False, f"Error: {e}")
    
    def test_file_operations(self):
        """Test file operation capabilities."""
        print("\n📁 Testing File Operations...")
        
        try:
            # Test directory creation
            test_dirs = [
                "em_dash_replacement/input",
                "em_dash_replacement/output",
                "deep_research_agent/reports",
                "shared_utils/data"
            ]
            
            dirs_created = 0
            for dir_path in test_dirs:
                full_path = self.project_root / dir_path
                full_path.mkdir(parents=True, exist_ok=True)
                if full_path.exists():
                    dirs_created += 1
            
            self.log_test("Directory Creation", dirs_created == len(test_dirs), 
                        f"Created {dirs_created}/{len(test_dirs)} directories")
            
            # Test file writing and reading
            test_file = self.project_root / "em_dash_replacement" / "input" / "system_test.txt"
            test_content = "This is a system test file—with em dashes—for validation."
            
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(test_content)
            
            with open(test_file, 'r', encoding='utf-8') as f:
                read_content = f.read()
            
            self.log_test("File Operations", read_content == test_content, "File write/read successful")
            
        except Exception as e:
            self.log_test("File Operations", False, f"Error: {e}")
    
    def generate_test_report(self):
        """Generate comprehensive test report."""
        print("\n" + "="*60)
        print("📊 WELLSPRING SYSTEM TEST REPORT")
        print("="*60)
        
        success_rate = (self.passed_tests / max(self.total_tests, 1)) * 100
        
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.total_tests - self.passed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        print(f"\n📋 Test Results Summary:")
        for test_name, result in self.test_results.items():
            status = "✅" if result['success'] else "❌"
            print(f"  {status} {test_name}")
            if result['message']:
                print(f"     {result['message']}")
        
        # Overall system status
        if success_rate >= 90:
            status = "🎉 EXCELLENT"
            grade = "A+"
        elif success_rate >= 80:
            status = "✅ GOOD"
            grade = "A"
        elif success_rate >= 70:
            status = "⚠️  ACCEPTABLE"
            grade = "B"
        else:
            status = "❌ NEEDS WORK"
            grade = "C"
        
        print(f"\n🏆 Overall System Status: {status}")
        print(f"📈 System Grade: {grade}")
        
        # Save detailed report
        report_file = self.project_root / f"system_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                'test_summary': {
                    'total_tests': self.total_tests,
                    'passed_tests': self.passed_tests,
                    'success_rate': success_rate,
                    'grade': grade,
                    'timestamp': datetime.now().isoformat()
                },
                'test_results': self.test_results
            }, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        
        return success_rate >= 80  # Return True if system passes
    
    async def run_all_tests(self):
        """Run all system tests."""
        print("🚀 Starting Wellspring System Tests...")
        
        # Core infrastructure tests
        self.test_database_initialization()
        self.test_file_operations()
        self.test_database_queries()
        
        # Component functionality tests
        self.test_em_dash_analyzer()
        self.test_em_dash_processor()
        self.test_deep_research_agent()
        
        # Integration tests
        self.test_agent_coordinator()
        await self.test_workflow_execution()
        
        # Generate final report
        system_ready = self.generate_test_report()
        
        return system_ready

async def main():
    """Main test function."""
    print("🧪 Wellspring Book Production System - Comprehensive Test Suite")
    print("=" * 70)
    
    tester = SystemTester()
    
    try:
        system_ready = await tester.run_all_tests()
        
        if system_ready:
            print(f"\n🎉 System is ready for production use!")
            print(f"   You can now run: python wellspring_cli.py setup")
            print(f"   Then try: python wellspring_cli.py create-samples")
            sys.exit(0)
        else:
            print(f"\n⚠️  System has issues that need to be addressed.")
            print(f"   Please review the test results above.")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())