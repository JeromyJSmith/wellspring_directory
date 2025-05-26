#!/usr/bin/env python3
"""
Visual Opportunities Generator with Batch Prompt System
Generates 3 visual options per opportunity with deep research prompts for cost-effective batch processing.
"""

import re
import json
import sqlite3
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class VisualOption:
    """Represents a single visual option with research prompt."""
    chart_type: str  # 'bar', 'line', 'pie', 'table', 'card', 'progress'
    shadcn_component: str  # Specific shadcn UI component
    data_structure: str  # Expected data format
    research_prompt: str  # Batch processing prompt
    complexity_score: int  # 1-10 implementation difficulty
    priority_score: int  # 1-10 importance for book

@dataclass 
class VisualOpportunity:
    """Enhanced visual opportunity with 3 options and batch prompts."""
    location: str
    content_data: str
    original_text: str
    chapter_section: str
    page_estimate: int
    visual_options: List[VisualOption]
    batch_research_id: str
    
class VisualOpportunitiesGenerator:
    """Generates visual opportunities with batch research prompts."""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = Path(__file__).parent.parent.parent / "shared_utils" / "data" / "wellspring.db"
        self.db_path = Path(db_path)
        self.shadcn_chart_templates = self._load_chart_templates()
    
    def _load_chart_templates(self) -> Dict[str, Dict]:
        """Load shadcn UI chart component templates."""
        return {
            'budget_breakdown': {
                'component': 'BarChart',
                'data_format': 'array of {category: string, amount: number, percentage: number}',
                'implementation': '''
<ChartContainer config={chartConfig} className="h-[300px] w-full">
  <BarChart data={budgetData}>
    <CartesianGrid vertical={false} />
    <XAxis dataKey="category" />
    <ChartTooltip content={<ChartTooltipContent />} />
    <Bar dataKey="amount" fill="var(--chart-1)" radius={4} />
  </BarChart>
</ChartContainer>'''
            },
            'project_timeline': {
                'component': 'LineChart', 
                'data_format': 'array of {phase: string, duration: number, cost: number}',
                'implementation': '''
<ChartContainer config={chartConfig} className="h-[300px] w-full">
  <LineChart data={timelineData}>
    <CartesianGrid strokeDasharray="3 3" />
    <XAxis dataKey="phase" />
    <YAxis />
    <ChartTooltip content={<ChartTooltipContent />} />
    <Line type="monotone" dataKey="duration" stroke="var(--chart-1)" />
  </LineChart>
</ChartContainer>'''
            },
            'resource_allocation': {
                'component': 'PieChart',
                'data_format': 'array of {name: string, value: number, fill: string}',
                'implementation': '''
<ChartContainer config={chartConfig} className="h-[300px] w-full">
  <PieChart>
    <Pie data={resourceData} cx="50%" cy="50%" outerRadius={80} 
         dataKey="value" fill="var(--chart-1)" />
    <ChartTooltip content={<ChartTooltipContent />} />
  </PieChart>
</ChartContainer>'''
            },
            'requirements_checklist': {
                'component': 'DataTable',
                'data_format': 'array of {requirement: string, status: string, priority: string}',
                'implementation': '''
<DataTable 
  columns={checklistColumns} 
  data={requirementsData}
  className="border rounded-lg"
/>'''
            },
            'kpi_dashboard': {
                'component': 'Card',
                'data_format': 'array of {title: string, value: number, change: number, unit: string}',
                'implementation': '''
<div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
  {kpiData.map((kpi) => (
    <Card key={kpi.title}>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="text-sm font-medium">{kpi.title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{kpi.value}{kpi.unit}</div>
      </CardContent>
    </Card>
  ))}
</div>'''
            }
        }
    
    def analyze_content_for_visuals(self, content: str, chapter_name: str) -> List[VisualOpportunity]:
        """Analyze content and generate visual opportunities with 3 options each."""
        opportunities = []
        
        # Enhanced pattern detection for behavioral health content
        visual_patterns = [
            {
                'pattern': r'budget[^.]{20,200}(\d+(?:,\d{3})*|\d+%)[^.]{0,100}',
                'type': 'budget_analysis',
                'priority': 9
            },
            {
                'pattern': r'phase[s]?[^.]{20,200}(?:timeline|schedule|duration)[^.]{0,100}',
                'type': 'project_timeline', 
                'priority': 8
            },
            {
                'pattern': r'(\d+%[^.]{10,100})|(?:percent|percentage)[^.]{20,100}',
                'type': 'percentage_data',
                'priority': 7
            },
            {
                'pattern': r'(?:steps?|requirements?|checklist)[^.]{20,200}',
                'type': 'process_checklist',
                'priority': 8
            },
            {
                'pattern': r'(?:components?|elements?|factors?)[^.]{20,200}',
                'type': 'component_breakdown',
                'priority': 6
            },
            {
                'pattern': r'comparison[^.]{20,200}',
                'type': 'comparative_analysis',
                'priority': 7
            }
        ]
        
        for i, pattern_info in enumerate(visual_patterns):
            matches = re.finditer(pattern_info['pattern'], content, re.IGNORECASE)
            for match in matches:
                data_content = match.group(0).strip()
                
                # Generate 3 visual options for this opportunity
                visual_options = self._generate_three_options(
                    data_content, 
                    pattern_info['type'],
                    pattern_info['priority']
                )
                
                opportunity = VisualOpportunity(
                    location=f"{chapter_name} - Line {content[:match.start()].count('\n') + 1}",
                    content_data=data_content,
                    original_text=data_content,
                    chapter_section=chapter_name,
                    page_estimate=content[:match.start()].count('\n') // 25 + 1,
                    visual_options=visual_options,
                    batch_research_id=f"batch_{chapter_name}_{i}_{datetime.now().strftime('%Y%m%d')}"
                )
                opportunities.append(opportunity)
        
        logger.info(f"Generated {len(opportunities)} visual opportunities with {len(opportunities) * 3} total options")
        return opportunities
    
    def _generate_three_options(self, data_content: str, content_type: str, priority: int) -> List[VisualOption]:
        """Generate 3 different visual options for each opportunity."""
        options = []
        
        # Analyze content to determine best chart types
        has_numbers = bool(re.search(r'\d+', data_content))
        has_percentages = bool(re.search(r'\d+%', data_content))
        has_categories = len(re.findall(r'\b(?:and|or|including)\b', data_content, re.IGNORECASE)) > 0
        has_timeline = bool(re.search(r'(?:phase|step|stage|before|after|during)', data_content, re.IGNORECASE))
        
        # Option 1: Primary recommendation (highest visual impact)
        if content_type == 'budget_analysis':
            options.append(VisualOption(
                chart_type='bar',
                shadcn_component='BarChart with CartesianGrid',
                data_structure=self.shadcn_chart_templates['budget_breakdown']['data_format'],
                research_prompt=f"""
DEEP RESEARCH PROMPT 1: Budget Breakdown Analysis
Content: {data_content}

Research Task: Create a comprehensive budget breakdown chart for behavioral health facility development.

Required Analysis:
1. Extract all cost categories and amounts from the content
2. Research industry standard budget allocations for similar projects
3. Find 3-5 authoritative sources on behavioral health facility budgeting
4. Calculate percentage distributions and identify any unusual allocations
5. Provide benchmarking data from similar projects

Output Format: JSON with structure matching: {self.shadcn_chart_templates['budget_breakdown']['data_format']}
Citations Required: Include source URLs, publication dates, and relevance scores
Implementation: {self.shadcn_chart_templates['budget_breakdown']['implementation']}
""",
                complexity_score=6,
                priority_score=priority
            ))
        
        # Option 2: Alternative visualization (different perspective)
        if has_percentages or has_categories:
            options.append(VisualOption(
                chart_type='pie',
                shadcn_component='PieChart with Tooltip',
                data_structure=self.shadcn_chart_templates['resource_allocation']['data_format'],
                research_prompt=f"""
DEEP RESEARCH PROMPT 2: Resource Allocation Visualization
Content: {data_content}

Research Task: Create a resource allocation pie chart showing proportional distributions.

Required Analysis:
1. Identify all categorical data and their relationships
2. Research optimal resource allocation ratios for behavioral health projects
3. Find industry benchmarks and best practices (3-5 authoritative sources)
4. Calculate proportional distributions and identify optimization opportunities
5. Compare against regulatory requirements and guidelines

Output Format: JSON with structure matching: {self.shadcn_chart_templates['resource_allocation']['data_format']}
Citations Required: Include regulatory sources, industry standards, expert opinions
Implementation: {self.shadcn_chart_templates['resource_allocation']['implementation']}
""",
                complexity_score=4,
                priority_score=priority - 1
            ))
        
        # Option 3: Data table/checklist (actionable format)
        options.append(VisualOption(
            chart_type='table',
            shadcn_component='DataTable with sorting/filtering',
            data_structure=self.shadcn_chart_templates['requirements_checklist']['data_format'],
            research_prompt=f"""
DEEP RESEARCH PROMPT 3: Interactive Requirements Checklist
Content: {data_content}

Research Task: Create a comprehensive, actionable checklist/table for project implementation.

Required Analysis:
1. Break down content into specific, actionable requirements
2. Research regulatory compliance requirements and industry standards
3. Find 3-5 authoritative checklists from government agencies or professional organizations
4. Assign priority levels and implementation timelines
5. Cross-reference with current 2024 regulatory requirements

Output Format: JSON with structure matching: {self.shadcn_chart_templates['requirements_checklist']['data_format']}
Citations Required: Government regulations, professional standards, compliance guides
Implementation: {self.shadcn_chart_templates['requirements_checklist']['implementation']}
""",
            complexity_score=5,
            priority_score=priority
        ))
        
        # Ensure we always have 3 options (fill with KPI cards if needed)
        while len(options) < 3:
            options.append(VisualOption(
                chart_type='card',
                shadcn_component='KPI Cards Grid',
                data_structure=self.shadcn_chart_templates['kpi_dashboard']['data_format'],
                research_prompt=f"""
DEEP RESEARCH PROMPT {len(options) + 1}: KPI Dashboard Cards
Content: {data_content}

Research Task: Extract key performance indicators and create dashboard cards.

Required Analysis:
1. Identify measurable metrics and KPIs from the content
2. Research industry-standard KPIs for behavioral health facility development
3. Find benchmarking data from 3-5 authoritative industry reports
4. Calculate baseline values and industry comparisons
5. Determine appropriate measurement units and tracking methods

Output Format: JSON with structure matching: {self.shadcn_chart_templates['kpi_dashboard']['data_format']}
Citations Required: Industry reports, benchmarking studies, performance standards
Implementation: {self.shadcn_chart_templates['kpi_dashboard']['implementation']}
""",
                complexity_score=3,
                priority_score=max(priority - 2, 1)
            ))
        
        return options[:3]  # Always return exactly 3 options
    
    def save_opportunities_with_batch_prompts(self, opportunities: List[VisualOpportunity]) -> bool:
        """Save visual opportunities with batch research prompts to database."""
        if not self.db_path.exists():
            logger.error(f"Database not found: {self.db_path}")
            return False
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create enhanced visual opportunities table if not exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS visual_opportunities_enhanced (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    location_description TEXT,
                    content_data TEXT,
                    original_text TEXT,
                    chapter_section TEXT,
                    page_estimate INTEGER,
                    batch_research_id TEXT,
                    visual_option_1_type TEXT,
                    visual_option_1_component TEXT,
                    visual_option_1_prompt TEXT,
                    visual_option_1_complexity INTEGER,
                    visual_option_1_priority INTEGER,
                    visual_option_2_type TEXT,
                    visual_option_2_component TEXT,
                    visual_option_2_prompt TEXT,
                    visual_option_2_complexity INTEGER,
                    visual_option_2_priority INTEGER,
                    visual_option_3_type TEXT,
                    visual_option_3_component TEXT,
                    visual_option_3_prompt TEXT,
                    visual_option_3_complexity INTEGER,
                    visual_option_3_priority INTEGER,
                    implementation_status TEXT DEFAULT 'pending',
                    selected_option INTEGER DEFAULT NULL,
                    created_at TEXT
                )
            """)
            
            # Insert opportunities with all 3 options
            for opp in opportunities:
                cursor.execute("""
                    INSERT INTO visual_opportunities_enhanced 
                    (location_description, content_data, original_text, chapter_section, page_estimate,
                     batch_research_id, visual_option_1_type, visual_option_1_component, visual_option_1_prompt,
                     visual_option_1_complexity, visual_option_1_priority, visual_option_2_type, 
                     visual_option_2_component, visual_option_2_prompt, visual_option_2_complexity,
                     visual_option_2_priority, visual_option_3_type, visual_option_3_component,
                     visual_option_3_prompt, visual_option_3_complexity, visual_option_3_priority, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    opp.location, opp.content_data, opp.original_text, opp.chapter_section,
                    opp.page_estimate, opp.batch_research_id,
                    opp.visual_options[0].chart_type, opp.visual_options[0].shadcn_component,
                    opp.visual_options[0].research_prompt, opp.visual_options[0].complexity_score,
                    opp.visual_options[0].priority_score,
                    opp.visual_options[1].chart_type, opp.visual_options[1].shadcn_component,
                    opp.visual_options[1].research_prompt, opp.visual_options[1].complexity_score,
                    opp.visual_options[1].priority_score,
                    opp.visual_options[2].chart_type, opp.visual_options[2].shadcn_component,
                    opp.visual_options[2].research_prompt, opp.visual_options[2].complexity_score,
                    opp.visual_options[2].priority_score,
                    datetime.now().isoformat()
                ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Saved {len(opportunities)} enhanced visual opportunities")
            return True
            
        except Exception as e:
            logger.error(f"Error saving opportunities: {e}")
            return False
    
    def generate_batch_prompts_report(self, opportunities: List[VisualOpportunity]) -> str:
        """Generate comprehensive report with all batch prompts for cost-effective processing."""
        report = []
        report.append("=" * 80)
        report.append("📊 VISUAL OPPORTUNITIES BATCH RESEARCH REPORT")
        report.append("=" * 80)
        
        total_prompts = len(opportunities) * 3
        report.append(f"\n🎯 EXECUTIVE SUMMARY:")
        report.append(f"  • Total Visual Opportunities: {len(opportunities)}")
        report.append(f"  • Total Research Prompts: {total_prompts}")
        report.append(f"  • Estimated API Cost Savings: {total_prompts * 0.75:.2f} USD (vs live prompts)")
        report.append(f"  • shadcn UI Components Required: {len(set(opt.shadcn_component for opp in opportunities for opt in opp.visual_options))}")
        
        # Group by chart type for better organization
        chart_type_counts = {}
        for opp in opportunities:
            for opt in opp.visual_options:
                chart_type_counts[opt.chart_type] = chart_type_counts.get(opt.chart_type, 0) + 1
        
        report.append(f"\n📈 CHART TYPE BREAKDOWN:")
        for chart_type, count in sorted(chart_type_counts.items()):
            report.append(f"  • {chart_type.title()} Charts: {count}")
        
        report.append(f"\n🔬 BATCH RESEARCH PROMPTS:")
        report.append("=" * 50)
        
        for i, opp in enumerate(opportunities, 1):
            report.append(f"\n📍 OPPORTUNITY {i}: {opp.location}")
            report.append(f"Content: {opp.content_data[:100]}...")
            report.append(f"Batch ID: {opp.batch_research_id}")
            
            for j, option in enumerate(opp.visual_options, 1):
                report.append(f"\n  🎨 OPTION {j}: {option.chart_type.upper()} CHART")
                report.append(f"  Component: {option.shadcn_component}")
                report.append(f"  Complexity: {option.complexity_score}/10")
                report.append(f"  Priority: {option.priority_score}/10")
                report.append(f"  \n  📝 RESEARCH PROMPT:")
                report.append("  " + "-" * 40)
                for line in option.research_prompt.strip().split('\n'):
                    report.append(f"  {line}")
                report.append("  " + "-" * 40)
        
        report.append(f"\n💡 IMPLEMENTATION STRATEGY:")
        report.append(f"  1. Process all batch prompts simultaneously (cost savings)")
        report.append(f"  2. Review research results and select best option per opportunity")
        report.append(f"  3. Implement shadcn UI components in InDesign export workflow")
        report.append(f"  4. Generate comprehensive citations report")
        
        report.append("=" * 80)
        
        return '\n'.join(report)

def main():
    """Main function to demonstrate visual opportunities generation."""
    print("🎨 Visual Opportunities Generator with Batch Research")
    print("=" * 60)
    
    generator = VisualOpportunitiesGenerator()
    
    # Sample content for testing
    sample_content = """
Chapter 2: Budget Planning and Resource Allocation

The development budget for behavioral health facilities typically includes several key components:

1. Land acquisition costs: 15-25% of total project budget
2. Design and soft costs: 20-30% including architecture, engineering, permits
3. Construction hard costs: 50-60% for actual building construction  
4. FF&E and contingency: 10-15% for fixtures, furniture, equipment

Studies show that 75% of successful projects maintain strict budget discipline throughout all phases of development. The six phases of development include concept planning, site analysis, design development, permitting, construction, and commissioning.

Resource allocation must consider staffing requirements, with clinical spaces requiring specialized equipment and technology infrastructure. Comparison studies indicate that facilities with integrated design approaches achieve 30% better patient outcomes while maintaining cost efficiency.

Budget components require careful analysis including:
- Site preparation and utilities: $200,000 - $500,000
- Clinical equipment: $1.5M - $3M depending on service lines
- Technology infrastructure: $300,000 - $800,000
- Contingency funds: 5-10% of total construction costs
"""
    
    # Generate visual opportunities
    print("🔍 Analyzing content for visual opportunities...")
    opportunities = generator.analyze_content_for_visuals(sample_content, "Chapter 2")
    
    # Generate batch prompts report
    print("📊 Generating batch research prompts...")
    report = generator.generate_batch_prompts_report(opportunities)
    print(report)
    
    # Save to database
    if generator.db_path.exists():
        generator.save_opportunities_with_batch_prompts(opportunities)
        print(f"\n✅ Opportunities saved to database: {generator.db_path}")
    else:
        print(f"\n⚠️  Database not found - run init_database.py first")
    
    print(f"\n🎉 Generated {len(opportunities)} opportunities with {len(opportunities) * 3} research prompts!")

if __name__ == "__main__":
    main()
