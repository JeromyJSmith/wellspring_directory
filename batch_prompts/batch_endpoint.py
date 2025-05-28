#!/usr/bin/env python3
"""
Wellspring Batch Processing Endpoint
==================================

FastAPI endpoint for OpenAI batch processing integration.
Provides REST API for submitting and monitoring batch jobs.

Author: BHSME Team
Version: 1.0.0
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import json
import os
from pathlib import Path
import logging

try:
    from openai_batch_processor import WellspringBatchProcessor
    PROCESSOR_AVAILABLE = True
except ImportError:
    PROCESSOR_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Wellspring Batch Processing API",
    description="OpenAI Batch Processing endpoint for Wellspring Visual Research",
    version="1.0.0"
)

# Global processor instance
processor: Optional[WellspringBatchProcessor] = None


class BatchSubmissionRequest(BaseModel):
    """Request model for batch submission"""
    json_file_path: str
    description: Optional[str] = "Wellspring Visual Research Batch"
    api_key: Optional[str] = None


class BatchStatusResponse(BaseModel):
    """Response model for batch status"""
    id: str
    status: str
    created_at: Optional[int] = None
    completed_at: Optional[int] = None
    failed_at: Optional[int] = None
    request_counts: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class BatchResultsResponse(BaseModel):
    """Response model for batch results"""
    total_results: int
    results_by_section: Dict[str, Any]
    timestamp: str


@app.on_event("startup")
async def startup_event():
    """Initialize the batch processor on startup"""
    global processor
    
    if not PROCESSOR_AVAILABLE:
        logger.warning("OpenAI batch processor not available")
        return
    
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            processor = WellspringBatchProcessor(api_key=api_key)
            logger.info("Batch processor initialized successfully")
        else:
            logger.warning("OPENAI_API_KEY not found in environment")
    except Exception as e:
        logger.error(f"Failed to initialize batch processor: {e}")


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "service": "Wellspring Batch Processing API",
        "version": "1.0.0",
        "status": "active" if processor else "unavailable",
        "endpoints": {
            "submit_batch": "/batch/submit",
            "monitor_batch": "/batch/{job_id}/status",
            "list_batches": "/batch/list",
            "download_results": "/batch/{job_id}/results"
        }
    }


@app.post("/batch/submit")
async def submit_batch(request: BatchSubmissionRequest, background_tasks: BackgroundTasks):
    """
    Submit a new batch processing job
    
    Args:
        request: Batch submission request with file path and options
        background_tasks: FastAPI background tasks for async processing
        
    Returns:
        Job submission confirmation with job ID
    """
    if not processor:
        raise HTTPException(status_code=503, detail="Batch processor not available")
    
    # Validate file exists
    if not Path(request.json_file_path).exists():
        raise HTTPException(status_code=404, detail=f"File not found: {request.json_file_path}")
    
    try:
        # Load and validate the JSON file
        batch_data = processor.load_visual_batch_prompts(request.json_file_path)
        
        # Format prompts for batch API
        tasks = processor.format_prompts_for_batch_api(batch_data)
        
        if not tasks:
            raise HTTPException(status_code=400, detail="No valid tasks found in the batch file")
        
        # Create and upload batch file
        batch_file_path = processor.create_batch_file(tasks)
        file_id = processor.upload_batch_file(batch_file_path)
        
        # Create batch job
        batch_job = processor.create_batch_job(file_id, request.description)
        
        return {
            "success": True,
            "job_id": batch_job.id,
            "status": batch_job.status,
            "task_count": len(tasks),
            "estimated_completion": "24 hours",
            "message": "Batch job submitted successfully"
        }
        
    except Exception as e:
        logger.error(f"Error submitting batch: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to submit batch: {str(e)}")


@app.get("/batch/{job_id}/status")
async def get_batch_status(job_id: str) -> BatchStatusResponse:
    """
    Get the status of a batch job
    
    Args:
        job_id: OpenAI batch job ID
        
    Returns:
        Current job status information
    """
    if not processor:
        raise HTTPException(status_code=503, detail="Batch processor not available")
    
    try:
        status_info = processor.get_batch_status(job_id)
        return BatchStatusResponse(**status_info)
        
    except Exception as e:
        logger.error(f"Error getting batch status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get batch status: {str(e)}")


@app.get("/batch/list")
async def list_batch_jobs():
    """
    List all batch jobs
    
    Returns:
        List of all batch jobs with their statuses
    """
    if not processor:
        raise HTTPException(status_code=503, detail="Batch processor not available")
    
    try:
        jobs = processor.list_batch_jobs()
        return {
            "total_jobs": len(jobs),
            "jobs": jobs
        }
        
    except Exception as e:
        logger.error(f"Error listing batch jobs: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list batch jobs: {str(e)}")


@app.get("/batch/{job_id}/results")
async def get_batch_results(job_id: str):
    """
    Download and process batch job results
    
    Args:
        job_id: OpenAI batch job ID
        
    Returns:
        Processed batch results
    """
    if not processor:
        raise HTTPException(status_code=503, detail="Batch processor not available")
    
    try:
        # Check job status first
        status_info = processor.get_batch_status(job_id)
        
        if status_info["status"] != "completed":
            raise HTTPException(
                status_code=400, 
                detail=f"Job not completed. Current status: {status_info['status']}"
            )
        
        # Get the batch job object
        batch_job = processor.client.batches.retrieve(job_id)
        
        # Download and process results
        results_file_path = processor.download_results(batch_job)
        processed_results = processor.process_results(results_file_path)
        
        return processed_results
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting batch results: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get batch results: {str(e)}")


@app.post("/batch/{job_id}/monitor")
async def monitor_batch_job(job_id: str, background_tasks: BackgroundTasks):
    """
    Start monitoring a batch job until completion
    
    Args:
        job_id: OpenAI batch job ID
        background_tasks: FastAPI background tasks for async monitoring
        
    Returns:
        Monitoring confirmation
    """
    if not processor:
        raise HTTPException(status_code=503, detail="Batch processor not available")
    
    def monitor_job():
        """Background task to monitor the job"""
        try:
            completed_job = processor.monitor_batch_job(job_id)
            logger.info(f"Job {job_id} completed with status: {completed_job.status}")
            
            if completed_job.status == "completed":
                # Auto-download and process results
                results_file_path = processor.download_results(completed_job)
                processed_results = processor.process_results(results_file_path)
                logger.info(f"Results processed for job {job_id}. Total: {processed_results['total_results']}")
                
        except Exception as e:
            logger.error(f"Error monitoring job {job_id}: {e}")
    
    # Add monitoring task to background
    background_tasks.add_task(monitor_job)
    
    return {
        "success": True,
        "job_id": job_id,
        "message": "Monitoring started in background"
    }


@app.post("/batch/process-complete")
async def process_complete_workflow(request: BatchSubmissionRequest):
    """
    Run the complete batch processing workflow (submit + monitor + process)
    
    Args:
        request: Batch submission request
        
    Returns:
        Complete processed results
    """
    if not processor:
        raise HTTPException(status_code=503, detail="Batch processor not available")
    
    # Validate file exists
    if not Path(request.json_file_path).exists():
        raise HTTPException(status_code=404, detail=f"File not found: {request.json_file_path}")
    
    try:
        # Run complete workflow
        results = processor.run_complete_batch_workflow(request.json_file_path)
        
        if "error" in results:
            raise HTTPException(status_code=500, detail=results["error"])
        
        return results
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in complete workflow: {e}")
        raise HTTPException(status_code=500, detail=f"Workflow failed: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "processor_available": processor is not None,
        "openai_configured": bool(os.getenv("OPENAI_API_KEY"))
    }


if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment or default to 8000
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        "batch_endpoint:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )