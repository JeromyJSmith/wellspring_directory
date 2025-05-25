# 📍 Wellspring Em Dash Replacement - Change Log & Output Destinations

## 🗂️ **Primary Output Locations**

### 1. **Database-Based Change Logs** (PRIMARY TRACKING)

**Location**: `shared_utils/data/wellspring.db`

#### Key Tables for Change Tracking:

- **`typography_sessions`** - Comprehensive session logs
  - Session name, input/output files, processing statistics
  - Start/completion times, processing duration
  - Error logs and status tracking

- **`agent_logs`** - Detailed agent activity logs
  - Individual agent actions and performance metrics
  - Input/output data payloads
  - Execution times and memory usage

- **`em_dash_patterns`** - Individual replacement tracking
  - Original text, context, replacement details
  - Confidence scores and manual review flags
  - Chapter locations and timestamps

- **`workflow_status`** - High-level workflow progress
  - Overall processing status and progress percentages
  - Agent assignments and coordination
  - Error messages and completion estimates

### 2. **File-Based Outputs**

**Location**: `em_dash_replacement/output/`

#### Current Files:

- **`analysis_report.json`** - Analysis results from Google ADK agents
  - Total em dashes found, confidence scores
  - Agent status and model information
  - Pattern analysis and suggestions

- **`dry_run_output.txt`** - Preview of proposed changes
  - Before/after text comparisons
  - Replacement rules and reasoning
  - Statistics on changes made

### 3. **Structured Log Directories**

#### **`em_dash_replacement/logs/`**

- **Purpose**: File-based processing logs
- **Current Status**: Ready (contains `__init__.py`)
- **Future Use**: Session logs, error logs, performance metrics

#### **`em_dash_replacement/changelog/`**

- **Purpose**: Human-readable change summaries
- **Current Status**: Ready (empty directory)
- **Future Use**: Markdown change summaries, version history

---

## 🔄 **Processing Flow & Logging**

```
Input File → Google ADK Agents → Multiple Log Destinations
    ↓
1. Real-time analysis → Database (agent_logs)
2. Session tracking → Database (typography_sessions) 
3. Pattern storage → Database (em_dash_patterns)
4. Results export → Files (output/*.json, *.txt)
5. Change summary → Files (changelog/*.md)
```

---

## 📊 **Current Status** (After Latest Run)

### Database Logs ✅

- **Typography Sessions**: Ready to log processing sessions
- **Agent Logs**: Ready to track individual agent actions
- **Em Dash Patterns**: Ready to store replacement details
- **Workflow Status**: Ready to track overall progress

### File Outputs ✅

- **Analysis Report**: `analysis_report.json` (4.1KB, 164 lines)
- **Dry Run Output**: `dry_run_output.txt` (1.6KB, 25 lines)
- **Processing Statistics**: 26 em dashes found, 5 replacements proposed

### Google ADK Integration ✅

- **Model**: `gemini-2.5-flash-preview-05-20`
- **Agents Active**: 3 (analyzer, processor, coordinator)
- **Database Connection**: `shared_utils/data/wellspring.db`

---

## 🎯 **Key Benefits of This Structure**

1. **Complete Audit Trail**: Every change is tracked in the database
2. **Human-Readable Outputs**: JSON/TXT files for review
3. **Agent Coordination**: Logs show how agents work together
4. **Performance Monitoring**: Execution times and metrics tracked
5. **Error Handling**: Failed operations logged with details
6. **Rollback Capability**: Backup files created before changes

---

## 📖 **Accessing the Logs**

### Via Python Package:

```python
from wellspring_book_production.em_dash_replacement import get_logs, get_output_files
from shared_utils.data import database_connection

# Get file-based logs
logs = get_logs()
outputs = get_output_files()

# Query database logs
# (Database queries via SQLite or agent tools)
```

### Via Database:

```sql
-- View recent typography sessions
SELECT * FROM typography_sessions ORDER BY started_at DESC LIMIT 10;

-- View agent activity
SELECT * FROM agent_logs WHERE agent_name = 'em_dash_processor' ORDER BY logged_at DESC;

-- View replacement patterns
SELECT * FROM em_dash_patterns WHERE confidence_score > 0.8;
```

---

**🎉 All systems operational for comprehensive change tracking!**
