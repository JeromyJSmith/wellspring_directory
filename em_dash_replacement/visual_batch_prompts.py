#!/usr/bin/env python3
"""
Enhanced Visual Opportunities System for Wellspring Book
Generates 3 batch prompt options for cost-effective infographic research

Based on shadcn UI chart components and Brian's requirements from transcript
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any

class VisualBatchPromptGenerator:
    """
    Generates 3 different visual research prompts for each statistical opportunity
    in the Wellspring manuscript to enable cost-effective batch processing
    """
    
    def __init__(self):
        self.shadcn_charts = {
            "bar_chart": "Budget breakdowns, phase comparisons, performance metrics",
            "line_chart": "Project timelines, cost trends, compliance over time", 
            "pie_chart": "Budget allocation, resource distribution, stakeholder breakdown",
            "data_table": "Comprehensive checklists, requirements, compliance matrices",
            "progress_indicator": "Project completion status, milestone tracking",
            "card_layout": "KPI dashboards, key metrics, summary statistics",
            "area_chart": "Cumulative data, trend analysis, capacity over time",
            "scatter_plot": "Correlation analysis, cost vs outcome, risk assessment"
        }
        
        self.visual_opportunities = []
        self.batch_prompts = []
        
    def analyze_content_for_visual_opportunities(self, content_section: str, section_title: str) -> List[Dict]:
        """
        Analyze a content section and identify 3 different visual presentation options
        """
        opportunities = []
        
        # Statistical patterns that suggest visualization needs
        stat_indicators = [
            "percent", "%", "million", "billion", "cost", "budget", "timeline",
            "phase", "requirement", "compliance", "deadline", "facility", 
            "patient", "bed", "capacity", "funding", "grant", "DHCS", "B-CHIP"
        ]
        
        # Check if section contains statistical content
        has_stats = any(indicator in content_section.lower() for indicator in stat_indicators)
        
        if has_stats:
            # Generate 3 different visual approaches
            opportunities = [
                {
                    "option": 1,
                    "approach": "Data-Driven Dashboard",
                    "chart_type": "card_layout + bar_chart",
                    "description": f"KPI dashboard for {section_title} with key metrics and comparative bar charts",
                    "shadcn_components": ["Card", "Progress", "Bar Chart"],
                    "citation_focus": "Statistical sources, government data, industry benchmarks"
                },
                {
                    "option": 2, 
                    "approach": "Process Flow Visualization",
                    "chart_type": "data_table + progress_indicator",
                    "description": f"Step-by-step process table for {section_title} with progress tracking",
                    "shadcn_components": ["Table", "Progress", "Badge"],
                    "citation_focus": "Regulatory requirements, best practices, case studies"
                },
                {
                    "option": 3,
                    "approach": "Trend & Analysis",
                    "chart_type": "line_chart + area_chart", 
                    "description": f"Time-series analysis and trend visualization for {section_title}",
                    "shadcn_components": ["Line Chart", "Area Chart", "Tooltip"],
                    "citation_focus": "Historical data, projections, comparative analysis"
                }
            ]
            
        return opportunities
    
    def generate_batch_research_prompts(self, visual_opportunity: Dict) -> Dict[str, str]:
        """
        Generate 3 batch research prompts for a visual opportunity
        Optimized for cost-effective processing
        """
        section = visual_opportunity.get("section_title", "Unknown Section")
        chart_type = visual_opportunity.get("chart_type", "general")
        
        prompts = {
            "data_extraction_prompt": f"""
            BATCH RESEARCH TASK: Extract quantitative data for "{section}" visualization
            
            OBJECTIVE: Find statistical data, percentages, costs, timelines, and metrics
            related to {section} in behavioral health facility development.
            
            OUTPUT FORMAT:
            - Data points with specific numbers
            - Source citations (author, publication, date)
            - Data reliability score (1-10)
            - Suggested chart type: {chart_type}
            
            FOCUS AREAS:
            1. Regulatory compliance statistics
            2. Cost benchmarks and budget breakdowns  
            3. Timeline and milestone data
            4. Performance metrics and KPIs
            
            CITATION REQUIREMENTS: Include full source attribution for all statistics
            """,
            
            "design_specification_prompt": f"""
            BATCH DESIGN TASK: Create visual specification for "{section}" infographic
            
            OBJECTIVE: Design professional chart layout using shadcn UI components
            for behavioral health development manual.
            
            OUTPUT FORMAT:
            - shadcn UI component specifications
            - Color scheme (dark blue/gold per brand guidelines)
            - Layout dimensions and spacing
            - Typography specifications
            - Accessibility considerations
            
            REQUIREMENTS:
            1. Professional manual/textbook aesthetic
            2. Brian V Jones author voice alignment
            3. Print-ready resolution specifications
            4. Responsive design for digital formats
            
            COMPONENTS: {visual_opportunity.get('shadcn_components', [])}
            """,
            
            "content_optimization_prompt": f"""
            BATCH CONTENT TASK: Optimize information architecture for "{section}"
            
            OBJECTIVE: Structure content for maximum comprehension and retention
            following adult learning principles and Brian's "dense but digestible" approach.
            
            OUTPUT FORMAT:
            - Content hierarchy and information flow
            - Key message prioritization
            - Supporting detail organization  
            - Call-to-action placement
            - Cross-reference opportunities
            
            CRITERIA:
            1. Support multiple learning styles (visual, auditory, kinesthetic)
            2. Break up dense paragraphs as requested by Brian
            3. Maintain subject matter expert authority
            4. Enable quick reference and scanning
            
            INTEGRATION: Links to other manual sections and external resources
            """
        }
        
        return prompts
    
    def create_change_log_entry(self, visual_opportunities: List[Dict]) -> Dict[str, Any]:
        """
        Create comprehensive change log entry with all visual options and prompts
        """
        timestamp = datetime.now().isoformat()
        
        change_log = {
            "timestamp": timestamp,
            "change_type": "visual_enhancement_batch_research",
            "total_opportunities": len(visual_opportunities),
            "visual_options": visual_opportunities,
            "batch_prompts": {
                "prompt_sets": [],
                "total_prompts": 0,
                "estimated_cost_savings": "70-80% vs live API calls"
            },
            "shadcn_ui_integration": {
                "available_components": list(self.shadcn_charts.keys()),
                "implementation_notes": "Using shadcn UI for professional chart aesthetics",
                "brand_compliance": "Dark blue/gold color scheme per Brian's specifications"
            },
            "processing_workflow": {
                "step_1": "Batch prompt execution",
                "step_2": "Citation compilation and verification", 
                "step_3": "Visual design specification",
                "step_4": "InDesign integration via automation scripts"
            }
        }
        
        # Generate prompts for each opportunity
        for opportunity in visual_opportunities:
            prompts = self.generate_batch_research_prompts(opportunity)
            
            prompt_set = {
                "section": opportunity.get("section_title"),
                "visual_options": opportunity.get("visual_options", []),
                "research_prompts": prompts,
                "expected_outputs": [
                    "Statistical data with citations",
                    "Visual design specifications", 
                    "Content optimization recommendations"
                ]
            }
            
            change_log["batch_prompts"]["prompt_sets"].append(prompt_set)
        
        change_log["batch_prompts"]["total_prompts"] = len(change_log["batch_prompts"]["prompt_sets"]) * 3
        
        return change_log
    
    def save_change_log(self, change_log: Dict[str, Any], output_path: str = None):
        """
        Save the change log to the em_dash_replacement changelog directory
        """
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"/Users/ojeromyo/Desktop/wellspring_directory/em_dash_replacement/changelog/visual_batch_prompts_{timestamp}.json"
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(change_log, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Change log saved: {output_path}")
        return output_path

# Example usage for demonstration
if __name__ == "__main__":
    generator = VisualBatchPromptGenerator()
    
    # Sample content sections from Brian's requirements
    sample_sections = [
        {
            "section_title": "Development Budget Components",
            "content": "The development budget includes fundamental land acquisition costs, soft costs for design and professionals, hard costs for construction, and contingency planning with F,F&E requirements."
        },
        {
            "section_title": "Six Phases of Development Life Cycle", 
            "content": "Phase One: Concept Planning, Phase Two: Due Diligence, Phase Three: Design Development, Phase Four: Permitting, Phase Five: Construction, Phase Six: Activation and occupancy with specific timelines and milestones."
        },
        {
            "section_title": "DHCS Compliance Requirements",
            "content": "B-CHIP funding requires compliance with 18 specific certifications, sunset dates of June 30, 2026 for Round 3, December 2026 for Rounds 4-5, with performance metrics and reporting requirements."
        }
    ]
    
    # Process each section for visual opportunities
    all_opportunities = []
    for section in sample_sections:
        opportunities = generator.analyze_content_for_visual_opportunities(
            section["content"], 
            section["section_title"]
        )
        
        if opportunities:
            all_opportunities.append({
                "section_title": section["section_title"],
                "visual_options": opportunities
            })
    
    # Generate comprehensive change log with batch prompts
    change_log = generator.create_change_log_entry(all_opportunities)
    
    # Save to changelog directory
    output_file = generator.save_change_log(change_log)
    
    print(f"""
    🎯 VISUAL BATCH PROMPT SYSTEM GENERATED!
    
    📊 Summary:
    - {len(all_opportunities)} content sections analyzed
    - {change_log['batch_prompts']['total_prompts']} research prompts generated
    - 3 visual options per section using shadcn UI
    - Comprehensive citations and design specs included
    
    💰 Cost Savings: {change_log['batch_prompts']['estimated_cost_savings']}
    
    📁 Output: {output_file}
    
    🚀 Ready for batch processing execution!
    """)
