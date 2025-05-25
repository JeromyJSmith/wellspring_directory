#!/usr/bin/env python3
"""
Session Management for Google ADK Em Dash Agents
Provides session persistence and state management for agent workflows.
"""

import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AgentSession:
    """Represents an agent session."""
    session_id: str
    agent_name: str
    session_type: str  # 'analysis', 'processing', 'workflow'
    status: str  # 'active', 'paused', 'completed', 'failed'
    created_at: datetime
    last_activity: datetime
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    progress_data: Dict[str, Any]
    configuration: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'session_id': self.session_id,
            'agent_name': self.agent_name,
            'session_type': self.session_type,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'last_activity': self.last_activity.isoformat(),
            'input_data': self.input_data,
            'output_data': self.output_data,
            'progress_data': self.progress_data,
            'configuration': self.configuration
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentSession':
        """Create from dictionary."""
        return cls(
            session_id=data['session_id'],
            agent_name=data['agent_name'],
            session_type=data['session_type'],
            status=data['status'],
            created_at=datetime.fromisoformat(data['created_at']),
            last_activity=datetime.fromisoformat(data['last_activity']),
            input_data=data['input_data'],
            output_data=data['output_data'],
            progress_data=data['progress_data'],
            configuration=data['configuration']
        )

class WellspringSessionService:
    """Custom session service for Wellspring Google ADK agents."""
    
    def __init__(self, db_path: str = None):
        """Initialize session service."""
        if db_path is None:
            db_path = Path(__file__).parent.parent.parent / "shared_utils" / "data" / "wellspring.db"
        
        self.db_path = Path(db_path)
        self.active_sessions: Dict[str, AgentSession] = {}
        self.session_timeout = timedelta(hours=2)  # 2 hour timeout
        
        # Initialize database tables if needed
        self._initialize_session_tables()
        
        # Load active sessions from database
        self._load_active_sessions()
        
        logger.info(f"WellspringSessionService initialized with {len(self.active_sessions)} active sessions")
    
    def _initialize_session_tables(self):
        """Initialize session tables in database."""
        if not self.db_path.exists():
            logger.warning(f"Database not found: {self.db_path}")
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create agent_sessions table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS agent_sessions (
                    session_id TEXT PRIMARY KEY,
                    agent_name TEXT NOT NULL,
                    session_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    last_activity TEXT NOT NULL,
                    input_data TEXT,
                    output_data TEXT,
                    progress_data TEXT,
                    configuration TEXT,
                    expires_at TEXT
                )
            """)
            
            # Create session_state table for detailed state storage
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS session_state (
                    session_id TEXT,
                    state_key TEXT,
                    state_value TEXT,
                    updated_at TEXT,
                    PRIMARY KEY (session_id, state_key),
                    FOREIGN KEY (session_id) REFERENCES agent_sessions (session_id)
                )
            """)
            
            conn.commit()
            conn.close()
            
            logger.info("Session tables initialized")
            
        except Exception as e:
            logger.error(f"Error initializing session tables: {e}")
    
    def _load_active_sessions(self):
        """Load active sessions from database."""
        if not self.db_path.exists():
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Load sessions that haven't expired
            cursor.execute("""
                SELECT session_id, agent_name, session_type, status, created_at, 
                       last_activity, input_data, output_data, progress_data, configuration
                FROM agent_sessions
                WHERE status IN ('active', 'paused') 
                AND datetime(expires_at) > datetime('now')
            """)
            
            rows = cursor.fetchall()
            
            for row in rows:
                session_data = {
                    'session_id': row[0],
                    'agent_name': row[1],
                    'session_type': row[2],
                    'status': row[3],
                    'created_at': row[4],
                    'last_activity': row[5],
                    'input_data': json.loads(row[6]) if row[6] else {},
                    'output_data': json.loads(row[7]) if row[7] else {},
                    'progress_data': json.loads(row[8]) if row[8] else {},
                    'configuration': json.loads(row[9]) if row[9] else {}
                }
                
                session = AgentSession.from_dict(session_data)
                self.active_sessions[session.session_id] = session
            
            conn.close()
            logger.info(f"Loaded {len(self.active_sessions)} active sessions from database")
            
        except Exception as e:
            logger.error(f"Error loading active sessions: {e}")
    
    def create_session(
        self,
        session_id: str,
        agent_name: str,
        session_type: str,
        input_data: Dict[str, Any],
        configuration: Optional[Dict[str, Any]] = None
    ) -> AgentSession:
        """Create a new agent session."""
        try:
            now = datetime.now()
            
            session = AgentSession(
                session_id=session_id,
                agent_name=agent_name,
                session_type=session_type,
                status='active',
                created_at=now,
                last_activity=now,
                input_data=input_data,
                output_data={},
                progress_data={},
                configuration=configuration or {}
            )
            
            # Store in memory
            self.active_sessions[session_id] = session
            
            # Persist to database
            self._persist_session(session)
            
            logger.info(f"Created session {session_id} for agent {agent_name}")
            return session
            
        except Exception as e:
            logger.error(f"Error creating session: {e}")
            raise
    
    def get_session(self, session_id: str) -> Optional[AgentSession]:
        """Get an existing session."""
        session = self.active_sessions.get(session_id)
        
        if session:
            # Check if session has expired
            if datetime.now() - session.last_activity > self.session_timeout:
                self._expire_session(session_id)
                return None
            
            # Update last activity
            session.last_activity = datetime.now()
            self._persist_session(session)
        
        return session
    
    def update_session(
        self,
        session_id: str,
        output_data: Optional[Dict[str, Any]] = None,
        progress_data: Optional[Dict[str, Any]] = None,
        status: Optional[str] = None
    ) -> bool:
        """Update an existing session."""
        try:
            session = self.active_sessions.get(session_id)
            if not session:
                logger.warning(f"Session not found: {session_id}")
                return False
            
            # Update session data
            if output_data:
                session.output_data.update(output_data)
            
            if progress_data:
                session.progress_data.update(progress_data)
            
            if status:
                session.status = status
            
            session.last_activity = datetime.now()
            
            # Persist changes
            self._persist_session(session)
            
            logger.debug(f"Updated session {session_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating session: {e}")
            return False
    
    def complete_session(self, session_id: str, final_output: Dict[str, Any]) -> bool:
        """Mark a session as completed."""
        try:
            session = self.active_sessions.get(session_id)
            if not session:
                logger.warning(f"Session not found: {session_id}")
                return False
            
            session.status = 'completed'
            session.output_data.update(final_output)
            session.last_activity = datetime.now()
            
            # Persist final state
            self._persist_session(session)
            
            # Remove from active sessions
            del self.active_sessions[session_id]
            
            logger.info(f"Completed session {session_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error completing session: {e}")
            return False
    
    def fail_session(self, session_id: str, error_message: str) -> bool:
        """Mark a session as failed."""
        try:
            session = self.active_sessions.get(session_id)
            if not session:
                logger.warning(f"Session not found: {session_id}")
                return False
            
            session.status = 'failed'
            session.output_data['error_message'] = error_message
            session.last_activity = datetime.now()
            
            # Persist final state
            self._persist_session(session)
            
            # Remove from active sessions
            del self.active_sessions[session_id]
            
            logger.info(f"Failed session {session_id}: {error_message}")
            return True
            
        except Exception as e:
            logger.error(f"Error failing session: {e}")
            return False
    
    def pause_session(self, session_id: str) -> bool:
        """Pause a session."""
        try:
            session = self.active_sessions.get(session_id)
            if not session:
                logger.warning(f"Session not found: {session_id}")
                return False
            
            session.status = 'paused'
            session.last_activity = datetime.now()
            
            self._persist_session(session)
            
            logger.info(f"Paused session {session_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error pausing session: {e}")
            return False
    
    def resume_session(self, session_id: str) -> bool:
        """Resume a paused session."""
        try:
            session = self.active_sessions.get(session_id)
            if not session:
                logger.warning(f"Session not found: {session_id}")
                return False
            
            if session.status != 'paused':
                logger.warning(f"Session {session_id} is not paused (status: {session.status})")
                return False
            
            session.status = 'active'
            session.last_activity = datetime.now()
            
            self._persist_session(session)
            
            logger.info(f"Resumed session {session_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error resuming session: {e}")
            return False
    
    def list_sessions(
        self,
        agent_name: Optional[str] = None,
        session_type: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[AgentSession]:
        """List sessions with optional filtering."""
        sessions = list(self.active_sessions.values())
        
        if agent_name:
            sessions = [s for s in sessions if s.agent_name == agent_name]
        
        if session_type:
            sessions = [s for s in sessions if s.session_type == session_type]
        
        if status:
            sessions = [s for s in sessions if s.status == status]
        
        return sessions
    
    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions."""
        try:
            expired_count = 0
            now = datetime.now()
            
            expired_session_ids = []
            for session_id, session in self.active_sessions.items():
                if now - session.last_activity > self.session_timeout:
                    expired_session_ids.append(session_id)
            
            for session_id in expired_session_ids:
                self._expire_session(session_id)
                expired_count += 1
            
            logger.info(f"Cleaned up {expired_count} expired sessions")
            return expired_count
            
        except Exception as e:
            logger.error(f"Error cleaning up expired sessions: {e}")
            return 0
    
    def get_session_statistics(self) -> Dict[str, Any]:
        """Get session statistics."""
        try:
            stats = {
                'active_sessions': len(self.active_sessions),
                'by_agent': {},
                'by_type': {},
                'by_status': {},
                'oldest_session': None,
                'newest_session': None
            }
            
            if self.active_sessions:
                sessions = list(self.active_sessions.values())
                
                # Group by agent
                for session in sessions:
                    agent = session.agent_name
                    stats['by_agent'][agent] = stats['by_agent'].get(agent, 0) + 1
                
                # Group by type
                for session in sessions:
                    session_type = session.session_type
                    stats['by_type'][session_type] = stats['by_type'].get(session_type, 0) + 1
                
                # Group by status
                for session in sessions:
                    status = session.status
                    stats['by_status'][status] = stats['by_status'].get(status, 0) + 1
                
                # Find oldest and newest
                oldest = min(sessions, key=lambda s: s.created_at)
                newest = max(sessions, key=lambda s: s.created_at)
                
                stats['oldest_session'] = {
                    'session_id': oldest.session_id,
                    'created_at': oldest.created_at.isoformat(),
                    'agent_name': oldest.agent_name
                }
                
                stats['newest_session'] = {
                    'session_id': newest.session_id,
                    'created_at': newest.created_at.isoformat(),
                    'agent_name': newest.agent_name
                }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting session statistics: {e}")
            return {}
    
    def _persist_session(self, session: AgentSession):
        """Persist session to database."""
        if not self.db_path.exists():
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            expires_at = session.last_activity + self.session_timeout
            
            cursor.execute("""
                INSERT OR REPLACE INTO agent_sessions 
                (session_id, agent_name, session_type, status, created_at, last_activity,
                 input_data, output_data, progress_data, configuration, expires_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session.session_id,
                session.agent_name,
                session.session_type,
                session.status,
                session.created_at.isoformat(),
                session.last_activity.isoformat(),
                json.dumps(session.input_data),
                json.dumps(session.output_data),
                json.dumps(session.progress_data),
                json.dumps(session.configuration),
                expires_at.isoformat()
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error persisting session: {e}")
    
    def _expire_session(self, session_id: str):
        """Expire a session."""
        try:
            if session_id in self.active_sessions:
                session = self.active_sessions[session_id]
                session.status = 'expired'
                self._persist_session(session)
                del self.active_sessions[session_id]
                
                logger.info(f"Expired session {session_id}")
        
        except Exception as e:
            logger.error(f"Error expiring session: {e}")

# Global session service instance
SESSION_SERVICE = WellspringSessionService()

# Convenience functions
def create_analysis_session(session_id: str, input_data: Dict[str, Any]) -> AgentSession:
    """Create an analysis session."""
    return SESSION_SERVICE.create_session(session_id, "em_dash_analyzer", "analysis", input_data)

def create_processing_session(session_id: str, input_data: Dict[str, Any]) -> AgentSession:
    """Create a processing session."""
    return SESSION_SERVICE.create_session(session_id, "em_dash_processor", "processing", input_data)

def create_workflow_session(session_id: str, input_data: Dict[str, Any]) -> AgentSession:
    """Create a workflow session."""
    return SESSION_SERVICE.create_session(session_id, "em_dash_coordinator", "workflow", input_data)

def get_session_by_id(session_id: str) -> Optional[AgentSession]:
    """Get session by ID."""
    return SESSION_SERVICE.get_session(session_id)

def update_session_progress(session_id: str, progress_data: Dict[str, Any]) -> bool:
    """Update session progress."""
    return SESSION_SERVICE.update_session(session_id, progress_data=progress_data)

def complete_session_with_results(session_id: str, results: Dict[str, Any]) -> bool:
    """Complete session with results."""
    return SESSION_SERVICE.complete_session(session_id, results)

if __name__ == "__main__":
    # Demo session management
    print("🗂️  Wellspring Session Management Demo")
    print("=" * 50)
    
    # Get statistics
    stats = SESSION_SERVICE.get_session_statistics()
    print(f"\n📊 Session Statistics:")
    print(f"  • Active sessions: {stats['active_sessions']}")
    print(f"  • By agent: {stats['by_agent']}")
    print(f"  • By type: {stats['by_type']}")
    print(f"  • By status: {stats['by_status']}")
    
    # Create demo session
    demo_session = create_analysis_session(
        "demo_session_001",
        {"file_path": "sample.txt", "confidence_threshold": 0.8}
    )
    
    print(f"\n✅ Created demo session: {demo_session.session_id}")
    print(f"  • Agent: {demo_session.agent_name}")
    print(f"  • Type: {demo_session.session_type}")
    print(f"  • Status: {demo_session.status}")
    
    # Update session
    update_session_progress("demo_session_001", {"progress": 50, "step": "analyzing"})
    print(f"  • Updated progress: 50%")
    
    # Complete session
    complete_session_with_results("demo_session_001", {"patterns_found": 25, "confidence": 0.85})
    print(f"  • Session completed")
    
    print(f"\n🎉 Session management demo completed!")