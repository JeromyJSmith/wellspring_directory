#!/usr/bin/env python3
"""Quick status checker for the batch job"""

from openai_batch_processor import WellspringBatchProcessor
from datetime import datetime

def check_job_status():
    job_id = 'batch_683506cc77cc8190b47611aeff3f7024'
    
    p = WellspringBatchProcessor()
    s = p.get_batch_status(job_id)
    
    print('🎯 DETAILED JOB STATUS:')
    print('=' * 40)
    print(f'🆔 Job ID: {s["id"]}')
    print(f'📊 Status: {s["status"]}')
    print(f'📅 Created: {datetime.fromtimestamp(s["created_at"])}')
    
    if s['request_counts']:
        counts = s['request_counts']
        completed = counts.get('completed', 0)
        total = counts.get('total', 0)
        failed = counts.get('failed', 0)
        progress = (completed / total * 100) if total > 0 else 0
        
        print(f'📈 Progress: {completed}/{total} ({progress:.1f}%)')
        print(f'✅ Completed: {completed}')
        print(f'❌ Failed: {failed}')
        print(f'⏳ Remaining: {total - completed}')
    
    print()
    print('📋 WHAT THIS MEANS:')
    print('• OpenAI is actively processing your research prompts')
    print('• Each task generates AI analysis for your visual opportunities')
    print('• Expected completion: Within 24 hours')
    print('• No action needed - just wait for completion!')
    
    return s

if __name__ == "__main__":
    check_job_status()