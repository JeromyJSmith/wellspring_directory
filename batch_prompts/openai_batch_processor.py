#!/usr/bin/env python3
"""
OpenAI Batch Processing System for Wellspring Visual Research
=====================================

This module handles batch processing of visual research prompts using OpenAI's Batch API.
It can process the visual batch prompts generated for the Wellspring Manual and submit them
efficiently as batch jobs, reducing costs by 50% compared to real-time API calls.

Author: BHSME Team
Version: 1.0.0
"""

import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import logging

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("OpenAI SDK not installed. Run: pip install openai --upgrade")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WellspringBatchProcessor:
    """
    OpenAI Batch Processing Manager for Wellspring Visual Research
    
    Handles the complete workflow:
    1. Load visual batch prompts from JSON
    2. Format them for OpenAI Batch API
    3. Submit batch jobs
    4. Monitor job status
    5. Download and process results
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the batch processor
        
        Args:
            api_key: OpenAI API key (defaults to environment variable)
        """
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI SDK not available. Install with: pip install openai --upgrade")
        
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.batch_jobs: Dict[str, Dict] = {}
        
        # Create output directories
        self.setup_directories()
    
    def setup_directories(self):
        """Create necessary directories for batch processing"""
        self.base_dir = Path("/Users/ojeromyo/Desktop/wellspring_directory/batch_prompts")
        self.input_dir = self.base_dir / "input"
        self.output_dir = self.base_dir / "output"
        self.logs_dir = self.base_dir / "logs"
        
        for directory in [self.input_dir, self.output_dir, self.logs_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def load_visual_batch_prompts(self, json_file_path: str) -> Dict[str, Any]:
        """
        Load the visual batch prompts JSON file
        
        Args:
            json_file_path: Path to the visual batch prompts JSON file
            
        Returns:
            Parsed JSON data containing batch prompts
        """
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Loaded visual batch prompts from {json_file_path}")
            return data
        except Exception as e:
            logger.error(f"Error loading batch prompts: {e}")
            raise
    
    def format_prompts_for_batch_api(self, batch_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Convert Wellspring batch prompts to OpenAI Batch API format
        
        Args:
            batch_data: The visual batch prompts data
            
        Returns:
            List of formatted tasks for OpenAI Batch API
        """
        tasks = []
        
        # Extract prompt sets from the batch data
        prompt_sets = batch_data.get("batch_prompts", {}).get("prompt_sets", [])
        
        for prompt_set in prompt_sets:
            section = prompt_set.get("section", "")
            research_prompts = prompt_set.get("research_prompts", {})
            
            # Create tasks for each type of research prompt
            for prompt_type, prompt_content in research_prompts.items():
                if prompt_content and prompt_content.strip():
                    custom_id = f"{section}_{prompt_type}_{int(time.time())}"
                    
                    task = {
                        "custom_id": custom_id,
                        "method": "POST",
                        "url": "/v1/chat/completions",
                        "body": {
                            "model": "gpt-4o-mini",
                            "temperature": 0.3,
                            "max_tokens": 2000,
                            "messages": [
                                {
                                    "role": "system",
                                    "content": "You are a professional research assistant specializing in behavioral health facility development. Provide detailed, well-cited responses with specific data points and actionable insights."
                                },
                                {
                                    "role": "user",
                                    "content": prompt_content.strip()
                                }
                            ]
                        }
                    }
                    tasks.append(task)
        
        logger.info(f"Formatted {len(tasks)} tasks for batch processing")
        return tasks
    
    def create_batch_file(self, tasks: List[Dict[str, Any]], filename: str = None) -> str:
        """
        Create a JSONL file for batch processing
        
        Args:
            tasks: List of formatted tasks
            filename: Optional custom filename
            
        Returns:
            Path to the created JSONL file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"wellspring_batch_tasks_{timestamp}.jsonl"
        
        file_path = self.input_dir / filename
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                for task in tasks:
                    f.write(json.dumps(task) + '\n')
            
            logger.info(f"Created batch file: {file_path}")
            return str(file_path)
        
        except Exception as e:
            logger.error(f"Error creating batch file: {e}")
            raise
    
    def upload_batch_file(self, file_path: str) -> str:
        """
        Upload the batch file to OpenAI
        
        Args:
            file_path: Path to the JSONL batch file
            
        Returns:
            File ID from OpenAI
        """
        try:
            with open(file_path, 'rb') as f:
                batch_file = self.client.files.create(
                    file=f,
                    purpose="batch"
                )
            
            logger.info(f"Uploaded batch file. File ID: {batch_file.id}")
            return batch_file.id
        
        except Exception as e:
            logger.error(f"Error uploading batch file: {e}")
            raise
    
    def create_batch_job(self, file_id: str, description: str = "Wellspring Visual Research Batch") -> Dict[str, Any]:
        """
        Create a batch job with the uploaded file
        
        Args:
            file_id: OpenAI file ID
            description: Description for the batch job
            
        Returns:
            Batch job object
        """
        try:
            batch_job = self.client.batches.create(
                input_file_id=file_id,
                endpoint="/v1/chat/completions",
                completion_window="24h",
                metadata={
                    "description": description,
                    "project": "wellspring-manual",
                    "created_by": "wellspring-batch-processor"
                }
            )
            
            self.batch_jobs[batch_job.id] = {
                "job": batch_job,
                "created_at": datetime.now(),
                "description": description
            }
            
            logger.info(f"Created batch job: {batch_job.id}")
            return batch_job
        
        except Exception as e:
            logger.error(f"Error creating batch job: {e}")
            raise
    
    def monitor_batch_job(self, job_id: str, check_interval: int = 60) -> Dict[str, Any]:
        """
        Monitor a batch job until completion
        
        Args:
            job_id: Batch job ID
            check_interval: Seconds between status checks
            
        Returns:
            Final batch job status
        """
        logger.info(f"Monitoring batch job: {job_id}")
        
        while True:
            try:
                batch_job = self.client.batches.retrieve(job_id)
                status = batch_job.status
                
                logger.info(f"Job {job_id} status: {status}")
                
                if status in ["completed", "failed", "expired", "cancelled"]:
                    return batch_job
                
                time.sleep(check_interval)
                
            except Exception as e:
                logger.error(f"Error monitoring batch job: {e}")
                time.sleep(check_interval)
    
    def download_results(self, batch_job: Dict[str, Any]) -> str:
        """
        Download batch job results
        
        Args:
            batch_job: Completed batch job object
            
        Returns:
            Path to downloaded results file
        """
        if not batch_job.output_file_id:
            raise ValueError("No output file available for this batch job")
        
        try:
            result = self.client.files.content(batch_job.output_file_id).content
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            result_filename = f"wellspring_batch_results_{timestamp}.jsonl"
            result_path = self.output_dir / result_filename
            
            with open(result_path, 'wb') as f:
                f.write(result)
            
            logger.info(f"Downloaded results to: {result_path}")
            return str(result_path)
        
        except Exception as e:
            logger.error(f"Error downloading results: {e}")
            raise
    
    def process_results(self, results_file_path: str) -> Dict[str, Any]:
        """
        Process and analyze batch results
        
        Args:
            results_file_path: Path to the results JSONL file
            
        Returns:
            Processed results data
        """
        results = []
        
        try:
            with open(results_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        result = json.loads(line.strip())
                        results.append(result)
            
            # Organize results by section and prompt type
            processed_results = {
                "total_results": len(results),
                "results_by_section": {},
                "timestamp": datetime.now().isoformat(),
                "raw_results": results
            }
            
            for result in results:
                custom_id = result.get("custom_id", "")
                if "_" in custom_id:
                    parts = custom_id.split("_")
                    if len(parts) >= 2:
                        section = parts[0]
                        prompt_type = parts[1]
                        
                        if section not in processed_results["results_by_section"]:
                            processed_results["results_by_section"][section] = {}
                        
                        processed_results["results_by_section"][section][prompt_type] = {
                            "custom_id": custom_id,
                            "response": result.get("response", {}).get("body", {}).get("choices", [{}])[0].get("message", {}).get("content", ""),
                            "usage": result.get("response", {}).get("body", {}).get("usage", {}),
                            "model": result.get("response", {}).get("body", {}).get("model", "")
                        }
            
            # Save processed results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            processed_filename = f"wellspring_processed_results_{timestamp}.json"
            processed_path = self.output_dir / processed_filename
            
            with open(processed_path, 'w', encoding='utf-8') as f:
                json.dump(processed_results, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Processed results saved to: {processed_path}")
            return processed_results
        
        except Exception as e:
            logger.error(f"Error processing results: {e}")
            raise
    
    def run_complete_batch_workflow(self, json_file_path: str) -> Dict[str, Any]:
        """
        Run the complete batch processing workflow
        
        Args:
            json_file_path: Path to the visual batch prompts JSON file
            
        Returns:
            Final processed results
        """
        logger.info("Starting complete batch processing workflow")
        
        try:
            # Step 1: Load visual batch prompts
            batch_data = self.load_visual_batch_prompts(json_file_path)
            
            # Step 2: Format prompts for batch API
            tasks = self.format_prompts_for_batch_api(batch_data)
            
            if not tasks:
                logger.warning("No valid tasks found to process")
                return {"error": "No valid tasks found"}
            
            # Step 3: Create batch file
            batch_file_path = self.create_batch_file(tasks)
            
            # Step 4: Upload to OpenAI
            file_id = self.upload_batch_file(batch_file_path)
            
            # Step 5: Create batch job
            batch_job = self.create_batch_job(file_id, "Wellspring Visual Research Batch Processing")
            
            # Step 6: Monitor job
            completed_job = self.monitor_batch_job(batch_job.id)
            
            if completed_job.status != "completed":
                logger.error(f"Batch job failed with status: {completed_job.status}")
                return {"error": f"Batch job failed: {completed_job.status}"}
            
            # Step 7: Download results
            results_file_path = self.download_results(completed_job)
            
            # Step 8: Process results
            processed_results = self.process_results(results_file_path)
            
            logger.info("Batch processing workflow completed successfully")
            return processed_results
        
        except Exception as e:
            logger.error(f"Error in batch workflow: {e}")
            raise
    
    def get_batch_status(self, job_id: str) -> Dict[str, Any]:
        """
        Get current status of a batch job
        
        Args:
            job_id: Batch job ID
            
        Returns:
            Job status information
        """
        try:
            batch_job = self.client.batches.retrieve(job_id)
            return {
                "id": batch_job.id,
                "status": batch_job.status,
                "created_at": batch_job.created_at,
                "completed_at": batch_job.completed_at,
                "failed_at": batch_job.failed_at,
                "request_counts": batch_job.request_counts.__dict__ if batch_job.request_counts else None,
                "metadata": batch_job.metadata
            }
        except Exception as e:
            logger.error(f"Error getting batch status: {e}")
            raise
    
    def list_batch_jobs(self) -> List[Dict[str, Any]]:
        """
        List all batch jobs
        
        Returns:
            List of batch job information
        """
        try:
            batches = self.client.batches.list()
            return [
                {
                    "id": batch.id,
                    "status": batch.status,
                    "created_at": batch.created_at,
                    "completed_at": batch.completed_at,
                    "metadata": batch.metadata
                }
                for batch in batches.data
            ]
        except Exception as e:
            logger.error(f"Error listing batch jobs: {e}")
            raise


def main():
    """
    CLI interface for the batch processor
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="Wellspring OpenAI Batch Processor")
    parser.add_argument("--input", "-i", required=True, help="Path to visual batch prompts JSON file")
    parser.add_argument("--api-key", help="OpenAI API key (or set OPENAI_API_KEY env var)")
    parser.add_argument("--monitor-only", help="Monitor existing batch job by ID")
    parser.add_argument("--list-jobs", action="store_true", help="List all batch jobs")
    parser.add_argument("--status", help="Get status of specific batch job")
    
    args = parser.parse_args()
    
    try:
        processor = WellspringBatchProcessor(api_key=args.api_key)
        
        if args.list_jobs:
            jobs = processor.list_batch_jobs()
            print(f"Found {len(jobs)} batch jobs:")
            for job in jobs:
                print(f"  {job['id']}: {job['status']} (created: {job['created_at']})")
        
        elif args.status:
            status = processor.get_batch_status(args.status)
            print(f"Batch Job Status: {json.dumps(status, indent=2)}")
        
        elif args.monitor_only:
            completed_job = processor.monitor_batch_job(args.monitor_only)
            print(f"Job completed with status: {completed_job.status}")
            
            if completed_job.status == "completed":
                results_path = processor.download_results(completed_job)
                processed_results = processor.process_results(results_path)
                print(f"Results processed. Total: {processed_results['total_results']}")
        
        else:
            # Run complete workflow
            results = processor.run_complete_batch_workflow(args.input)
            if "error" not in results:
                print(f"Batch processing completed successfully!")
                print(f"Total results: {results['total_results']}")
                print(f"Sections processed: {list(results['results_by_section'].keys())}")
            else:
                print(f"Error: {results['error']}")
    
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())