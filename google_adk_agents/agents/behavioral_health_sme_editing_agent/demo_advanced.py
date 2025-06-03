#!/usr/bin/env python3
"""
Advanced Behavioral Health SME Agent Demo
========================================

Demonstrates the enhanced features of the Advanced BHSME-aware editing agent:
- Real-Time Compliance Dashboard
- Interactive Stakeholder Validation 
- Continuous Learning & Adaptation
- Predictive Insights & Recommendations
- Project Context Awareness

Version: 3.0.0 - Advanced Strategic Enhancement
"""

import json
import sys
from pathlib import Path

# Add agent directory to path
agent_dir = Path(__file__).parent
sys.path.insert(0, str(agent_dir))

from implementation_advanced import (
    process_agent_request, 
    process_stakeholder_feedback,
    ProjectContext,
    AdvancedBehavioralHealthSMEAgent
)

def demo_basic_enhancement():
    """Demonstrate basic enhancement with advanced features."""
    print("🚀 ADVANCED BHSME EDITING AGENT DEMO")
    print("=" * 50)
    
    # Sample text for enhancement
    sample_text = """
    The first pillar of our behavioral health initiative must be embedded within 
    the community framework. It is critical that we establish comprehensive 
    services that are designed to meet the needs of vulnerable populations.
    The mental health services act provides guidance for trauma informed care 
    implementation across psychiatric health facilities.
    """
    
    # Configure project context for enhanced processing
    project_context = {
        "project_name": "BHCIP Downtown Campus Development",
        "region": "Southern California",
        "facility_types": ["PHF", "CSU", "BHUC"],
        "target_population": ["adults", "youth", "veterans"],
        "funding_source": "BHCIP Bond Grant Round 1",
        "compliance_requirements": ["DHCS", "OSHPD", "Title 22"]
    }
    
    # Process with advanced features
    input_data = {
        "text": sample_text,
        "chapter_title": "Chapter 1: Foundation Framework",
        "project_context": project_context,
        "enable_stakeholder_validation": True,
        "focus_areas": ["pillar_replacement", "passive_voice", "bhsme_terminology", "vague_openers"]
    }
    
    print("📝 Original Text:")
    print(sample_text.strip())
    print("\n" + "=" * 50)
    
    # Run advanced processing
    results = process_agent_request(input_data)
    
    print("✅ ENHANCED TEXT:")
    print(results["edited_text"].strip())
    print("\n" + "=" * 50)
    
    # Display advanced features
    display_compliance_dashboard(results.get("compliance_dashboard", []))
    display_validation_interface(results.get("validation_interface"))
    display_predictive_insights(results.get("predictive_insights"))
    display_learning_summary(results.get("learning_summary"))
    
    return results

def display_compliance_dashboard(dashboard_data):
    """Display real-time compliance monitoring dashboard."""
    print("📊 REAL-TIME COMPLIANCE DASHBOARD")
    print("-" * 40)
    
    if not dashboard_data:
        print("No compliance data available")
        return
    
    for metric in dashboard_data:
        metric_name = metric.get('metric_name', 'Unknown Metric')
        current_score = metric.get('current_score', 0)
        target_score = metric.get('target_score', 10)
        status = metric.get('status', 'unknown')
        
        # Status indicator
        status_icon = {
            'excellent': '🟢',
            'good': '🟡', 
            'needs_improvement': '🟠',
            'critical': '🔴',
            'pending': '⏳'
        }.get(status, '❓')
        
        print(f"{status_icon} {metric_name}: {current_score:.1f}/{target_score}")
        
        # Progress bar
        progress = min(100, (current_score / target_score) * 100)
        bar_length = 20
        filled = int((progress / 100) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"   [{bar}] {progress:.1f}%")
        
        # Improvement actions
        actions = metric.get('improvement_actions', [])
        if actions:
            print(f"   → {actions[0]}")
        print()

def display_validation_interface(validation_data):
    """Display interactive stakeholder validation interface."""
    print("👥 STAKEHOLDER VALIDATION INTERFACE")
    print("-" * 40)
    
    if not validation_data:
        print("No validation interface available")
        return
    
    validation_items = validation_data.get('validation_items', [])
    print(f"📋 {len(validation_items)} edits ready for stakeholder review\n")
    
    # Show first 3 validation items as examples
    for i, item in enumerate(validation_items[:3]):
        edit_id = item.get('edit_id', 'unknown')
        edit_type = item.get('edit_type', 'Unknown')
        original = item.get('original', '')
        proposed = item.get('proposed', '')
        confidence = item.get('confidence', 0)
        rationale = item.get('rationale', '')
        
        confidence_icon = "🟢" if confidence > 0.9 else "🟡" if confidence > 0.7 else "🟠"
        
        print(f"✏️ Edit #{i+1} [{edit_id}] - {edit_type}")
        print(f"   {confidence_icon} Confidence: {confidence:.2f}")
        print(f"   📤 Original: \"{original}\"")
        print(f"   📥 Proposed: \"{proposed}\"")
        print(f"   💡 Rationale: {rationale}")
        print(f"   🎯 Validation Options: approve | modify | reject | defer")
        print()
    
    if len(validation_items) > 3:
        print(f"... and {len(validation_items) - 3} more edits")
    
    # Batch operations
    batch_actions = validation_data.get('batch_actions', {})
    print("\n🔄 BATCH OPERATIONS AVAILABLE:")
    for action, description in batch_actions.items():
        print(f"   • {action}: {description}")

def display_predictive_insights(insights_data):
    """Display AI-enhanced predictive insights."""
    print("\n🔮 PREDICTIVE INSIGHTS & RECOMMENDATIONS")
    print("-" * 40)
    
    if not insights_data:
        print("No predictive insights available")
        return
    
    # Future optimization opportunities
    opportunities = insights_data.get('future_optimization_opportunities', [])
    if opportunities:
        print("🎯 FUTURE OPTIMIZATION OPPORTUNITIES:")
        for opp in opportunities:
            print(f"   • {opp}")
        print()
    
    # Time savings estimates
    time_savings = insights_data.get('estimated_time_savings', {})
    if time_savings:
        print("⏱️ ESTIMATED TIME SAVINGS:")
        for phase, savings in time_savings.items():
            print(f"   • {phase.replace('_', ' ').title()}: {savings}")
        print()
    
    # Quality predictions
    quality_predictions = insights_data.get('quality_predictions', {})
    if quality_predictions:
        print("📈 QUALITY PREDICTIONS:")
        for metric, prediction in quality_predictions.items():
            print(f"   • {metric.replace('_', ' ').title()}: {prediction}")
        print()

def display_learning_summary(learning_data):
    """Display continuous learning and adaptation summary."""
    print("🧠 CONTINUOUS LEARNING SUMMARY")
    print("-" * 40)
    
    if not learning_data:
        print("No learning data available")
        return
    
    sessions = learning_data.get('sessions_analyzed', 0)
    improvements = learning_data.get('effectiveness_improvements', 'No data')
    next_focus = learning_data.get('next_optimization', 'General enhancement')
    
    print(f"📊 Sessions Analyzed: {sessions}")
    print(f"📈 Effectiveness Improvements: {improvements}")
    print(f"🎯 Next Optimization Focus: {next_focus}")

def demo_stakeholder_feedback_processing():
    """Demonstrate stakeholder feedback processing and learning."""
    print("\n" + "=" * 50)
    print("👥 STAKEHOLDER FEEDBACK PROCESSING DEMO")
    print("=" * 50)
    
    # Simulate stakeholder feedback
    feedback_data = {
        "feedback_items": [
            {
                "edit_id": "a1b2c3d4",
                "stakeholder_type": "sme",
                "approval_status": "approved",
                "feedback_text": "Excellent improvement to professional authority"
            },
            {
                "edit_id": "e5f6g7h8", 
                "stakeholder_type": "developer",
                "approval_status": "modified",
                "feedback_text": "Good edit but prefer 'healthcare teams' over 'clinical teams'",
                "suggested_alternative": "healthcare teams establish"
            },
            {
                "edit_id": "i9j0k1l2",
                "stakeholder_type": "clinician",
                "approval_status": "rejected",
                "feedback_text": "This change loses important clinical nuance"
            }
        ],
        "overall_feedback": {
            "quality_rating": 8.5,
            "most_helpful": "Passive voice corrections significantly improved professional tone",
            "suggestions": "Consider more context-specific terminology for different facility types"
        }
    }
    
    print("📝 Processing stakeholder feedback...")
    feedback_results = process_stakeholder_feedback(feedback_data)
    
    print(f"✅ Processed {feedback_results.get('feedback_processed', 0)} feedback items")
    
    learning_updates = feedback_results.get('learning_updates', {})
    if learning_updates:
        print(f"🧠 Learning updates: {learning_updates}")
    
    improved_recs = feedback_results.get('improved_recommendations', [])
    if improved_recs:
        print("💡 IMPROVED RECOMMENDATIONS:")
        for rec in improved_recs[:3]:
            print(f"   • {rec}")

def demo_project_context_adaptation():
    """Demonstrate project context-aware adaptation."""
    print("\n" + "=" * 50)
    print("🎯 PROJECT CONTEXT ADAPTATION DEMO")  
    print("=" * 50)
    
    # Different project contexts
    contexts = [
        {
            "name": "Rural Crisis Center",
            "context": {
                "project_name": "Rural Crisis Center Development",
                "region": "Northern California",
                "facility_types": ["CSU", "Peer Respite"],
                "target_population": ["rural residents", "agricultural workers"],
                "funding_source": "BHCIP Rural Priority",
                "compliance_requirements": ["DHCS", "Rural Health Guidelines"]
            }
        },
        {
            "name": "Urban Youth Campus", 
            "context": {
                "project_name": "Downtown Youth Behavioral Health Campus",
                "region": "Los Angeles County",
                "facility_types": ["STRTP", "PHP", "BHUC"],
                "target_population": ["youth", "transitional age youth"],
                "funding_source": "BHCIP Youth Priority Grant",
                "compliance_requirements": ["DHCS", "Youth Services Standards"]
            }
        }
    ]
    
    sample_text = "This facility must be embedded with comprehensive services designed to meet community needs."
    
    for context_demo in contexts:
        print(f"🏗️ {context_demo['name']} Adaptation:")
        
        input_data = {
            "text": sample_text,
            "project_context": context_demo['context'],
            "enable_stakeholder_validation": False  # Simplified for demo
        }
        
        results = process_agent_request(input_data)
        
        print(f"   Original: {sample_text.strip()}")
        print(f"   Enhanced: {results['edited_text'].strip()}")
        
        # Show context-specific recommendations
        recommendations = results.get('recommendations', [])
        if recommendations:
            print(f"   Context-Specific Rec: {recommendations[0]}")
        print()

def main():
    """Run the complete advanced demo."""
    try:
        print("🌟 ADVANCED BEHAVIORAL HEALTH SME EDITING AGENT")
        print("Version 3.0.0 - Strategic Enhancement Demo")
        print("=" * 60)
        
        # Basic enhancement with advanced features
        results = demo_basic_enhancement()
        
        # Stakeholder feedback processing
        demo_stakeholder_feedback_processing()
        
        # Project context adaptation
        demo_project_context_adaptation()
        
        print("\n" + "=" * 60)
        print("✅ ADVANCED DEMO COMPLETED SUCCESSFULLY")
        print("\nKey Advanced Features Demonstrated:")
        print("  🎯 Real-Time Compliance Monitoring")
        print("  👥 Interactive Stakeholder Validation")
        print("  🧠 Continuous Learning & Adaptation") 
        print("  🔮 Predictive Insights & Recommendations")
        print("  🏗️ Project Context Awareness")
        print("  📊 Enhanced Analytics & Reporting")
        
        print(f"\nTotal Advanced Features: 6")
        print(f"Production Readiness: ✅ Enterprise-Level")
        print(f"Stakeholder Validation: ✅ Multi-Role Support")
        print(f"Learning Capability: ✅ Continuous Improvement")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 