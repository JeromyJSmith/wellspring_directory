# 🚀 Wellspring OpenAI Batch Processing System

A comprehensive batch processing system for OpenAI API that handles the visual research prompts from the Wellspring Manual project. This system reduces API costs by 50% compared to real-time processing while providing robust job management and monitoring capabilities.

## 📋 Features

- **Cost Efficient**: 50% cost reduction using OpenAI Batch API
- **Robust Processing**: Handles up to 24-hour batch jobs with automatic monitoring
- **REST API**: FastAPI endpoint for easy integration
- **Complete Workflow**: Submit, monitor, and process results automatically
- **Error Handling**: Comprehensive error handling and logging
- **Result Processing**: Automatic organization and analysis of batch results

## 🏗️ Architecture

```
batch_prompts/
├── openai_batch_processor.py    # Core batch processing class
├── batch_endpoint.py            # FastAPI REST endpoint
├── example_usage.py            # Usage examples and demos
├── setup_batch_processing.sh   # Installation script
├── README.md                   # This documentation
├── input/                      # Input JSONL files directory
├── output/                     # Results and processed data
└── logs/                       # Processing logs
```

## 🚀 Quick Start

### 1. Setup

```bash
# Make setup script executable and run it
chmod +x setup_batch_processing.sh
./setup_batch_processing.sh
```

### 2. Configure API Key

Set your OpenAI API key in your environment:

```bash
export OPENAI_API_KEY='sk-proj-your-key-here'
```

Or add it to your `.env` file:

```
OPENAI_API_KEY=sk-proj-your-key-here
```

### 3. Basic Usage

#### CLI Usage
```bash
# Process the visual batch prompts directly
python openai_batch_processor.py --input /path/to/visual_batch_prompts.json

# Monitor existing job
python openai_batch_processor.py --monitor-only batch_job_id

# List all jobs
python openai_batch_processor.py --list-jobs
```

#### Python API Usage
```python
from openai_batch_processor import WellspringBatchProcessor

# Initialize processor
processor = WellspringBatchProcessor()

# Run complete workflow
results = processor.run_complete_batch_workflow(
    "/path/to/visual_batch_prompts.json"
)

print(f"Processed {results['total_results']} results")
```

#### REST API Usage
```bash
# Start the API server
python batch_endpoint.py

# Server runs on http://localhost:8000
# API docs available at http://localhost:8000/docs
```

## 📖 Detailed Usage

### Processing Visual Batch Prompts

The system is specifically designed to handle the Wellspring visual batch prompts JSON file:

```python
# Load your visual batch prompts
input_file = "/Users/ojeromyo/Desktop/wellspring_directory/em_dash_replacement/changelog/visual_batch_prompts_20250526_171050.json"

processor = WellspringBatchProcessor()
results = processor.run_complete_batch_workflow(input_file)
```

### Monitoring Jobs

```python
# Check job status
status = processor.get_batch_status("batch_job_id")
print(f"Status: {status['status']}")

# Monitor until completion
completed_job = processor.monitor_batch_job("batch_job_id")
```

### Processing Results

The system automatically organizes results by section and prompt type:

```python
# Results structure
{
    "total_results": 9,
    "results_by_section": {
        "Development Budget Components": {
            "data_extraction_prompt": {
                "response": "Statistical analysis...",
                "usage": {"total_tokens": 1500},
                "model": "gpt-4o-mini"
            },
            "design_specification_prompt": {...},
            "content_optimization_prompt": {...}
        },
        "Six Phases of Development Life Cycle": {...},
        "DHCS Compliance Requirements": {...}
    },
    "timestamp": "2025-01-27T12:00:00"
}
```

## 🌐 REST API Endpoints

### Submit Batch Job
```http
POST /batch/submit
Content-Type: application/json

{
    "json_file_path": "/path/to/visual_batch_prompts.json",
    "description": "Wellspring Visual Research Batch"
}
```

### Monitor Job Status
```http
GET /batch/{job_id}/status
```

### Get Results
```http
GET /batch/{job_id}/results
```

### List All Jobs
```http
GET /batch/list
```

### Complete Workflow
```http
POST /batch/process-complete
Content-Type: application/json

{
    "json_file_path": "/path/to/visual_batch_prompts.json"
}
```

## 💰 Cost Analysis

Using OpenAI's Batch API provides significant cost savings:

- **Real-time API**: $0.0150 per 1K tokens (gpt-4o-mini)
- **Batch API**: $0.0075 per 1K tokens (gpt-4o-mini)
- **Savings**: 50% cost reduction

For the Wellspring visual batch prompts (9 prompts, ~2000 tokens each):
- Real-time cost: ~$0.27
- Batch cost: ~$0.135
- **Savings: $0.135 (50%)**

## 🔧 Configuration

### Environment Variables

```bash
# Required
OPENAI_API_KEY=sk-proj-your-key-here

# Optional
PORT=8000                    # API server port
LOG_LEVEL=INFO              # Logging level
BATCH_CHECK_INTERVAL=60     # Job monitoring interval (seconds)
```

### Batch Processing Settings

```python
# Customize in openai_batch_processor.py
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_TEMPERATURE = 0.3
DEFAULT_MAX_TOKENS = 2000
COMPLETION_WINDOW = "24h"
```

## 📊 Monitoring and Logging

The system provides comprehensive logging:

- **File Logs**: Stored in `logs/` directory
- **Console Output**: Real-time progress updates
- **API Logs**: Endpoint access and error logs

### Log Levels
- `INFO`: General operation info
- `WARNING`: Non-critical issues
- `ERROR`: Error conditions
- `DEBUG`: Detailed debugging info

## 🔍 Examples

### Example 1: Submit and Monitor
```python
from openai_batch_processor import WellspringBatchProcessor

processor = WellspringBatchProcessor()

# Submit job
batch_data = processor.load_visual_batch_prompts("prompts.json")
tasks = processor.format_prompts_for_batch_api(batch_data)
batch_file_path = processor.create_batch_file(tasks)
file_id = processor.upload_batch_file(batch_file_path)
batch_job = processor.create_batch_job(file_id)

print(f"Job submitted: {batch_job.id}")

# Monitor (will wait until completion)
completed_job = processor.monitor_batch_job(batch_job.id)
print(f"Job completed with status: {completed_job.status}")
```

### Example 2: Process Results
```python
# Download and process results
if completed_job.status == "completed":
    results_file = processor.download_results(completed_job)
    processed_results = processor.process_results(results_file)
    
    print(f"Total results: {processed_results['total_results']}")
    
    # Access specific section results
    development_results = processed_results['results_by_section']['Development Budget Components']
    data_response = development_results['data_extraction_prompt']['response']
    print(f"Data extraction result: {data_response[:200]}...")
```

### Example 3: API Integration
```python
import requests

# Submit via API
response = requests.post("http://localhost:8000/batch/submit", json={
    "json_file_path": "/path/to/prompts.json",
    "description": "My batch job"
})

job_id = response.json()["job_id"]

# Check status
status_response = requests.get(f"http://localhost:8000/batch/{job_id}/status")
print(f"Status: {status_response.json()['status']}")
```

## 🛠️ Development

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/ -v
```

### Adding New Features

1. **Extend the processor**: Add methods to `WellspringBatchProcessor`
2. **Add API endpoints**: Extend `batch_endpoint.py`
3. **Update examples**: Add usage examples to `example_usage.py`

### Custom Prompt Formatting

To handle different prompt formats, override the `format_prompts_for_batch_api` method:

```python
class CustomBatchProcessor(WellspringBatchProcessor):
    def format_prompts_for_batch_api(self, batch_data):
        # Custom formatting logic
        tasks = []
        # ... your logic here
        return tasks
```

## 🚨 Error Handling

Common issues and solutions:

### API Key Issues
```
Error: OpenAI API key not found
Solution: Set OPENAI_API_KEY environment variable
```

### File Not Found
```
Error: File not found: /path/to/prompts.json
Solution: Check file path and permissions
```

### Job Failed
```
Error: Batch job failed with status: failed
Solution: Check job details and OpenAI status page
```

### Rate Limits
```
Error: Rate limit exceeded
Solution: Batch API has different limits; wait and retry
```

## 📈 Performance

### Batch Size Recommendations
- **Small batches** (1-10 prompts): Process immediately
- **Medium batches** (10-100 prompts): Use batch API
- **Large batches** (100+ prompts): Split into multiple jobs

### Timing Expectations
- **Job submission**: 1-5 seconds
- **Job processing**: 5 minutes to 24 hours
- **Result download**: 1-10 seconds
- **Result processing**: 1-30 seconds

## 🔐 Security

- **API Keys**: Never commit API keys to version control
- **File Permissions**: Ensure proper file permissions for logs and results
- **Network Security**: Use HTTPS in production
- **Input Validation**: All inputs are validated before processing

## 📞 Support

For issues or questions:

1. Check the logs in `logs/` directory
2. Review the example usage in `example_usage.py`
3. Consult OpenAI Batch API documentation
4. Contact the BHSME team

## 📝 License

MIT License - See LICENSE file for details.

## 🚀 Next Steps

1. **Run the setup script**: `./setup_batch_processing.sh`
2. **Set your API key**: `export OPENAI_API_KEY='your-key'`
3. **Try the examples**: `python example_usage.py`
4. **Process your data**: Use your visual batch prompts JSON file
5. **Monitor results**: Check the output directory for processed results

---

**Happy Batch Processing! 🎉**