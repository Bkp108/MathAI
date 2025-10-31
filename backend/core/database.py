"""
Database connection and session management
"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import json
import logging
from pathlib import Path

from core.config import settings

logger = logging.getLogger(__name__)


class Database:
    """SQLite database manager"""

    # def __init__(self, db_path: str = None):
    #     self.db_path = db_path or settings.DATABASE_URL.replace("sqlite:///", "")
    #     self._ensure_tables()

    def __init__(self, db_path: str = None):
        # Resolve db_path
        self.db_path = db_path or settings.DATABASE_URL.replace(
            "sqlite:///", "")

        # Ensure parent directory exists
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)  # creates folder if missing

        self._ensure_tables()

    def _get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)

    def _ensure_tables(self):
        """Create tables if they don't exist"""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Feedback table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                query TEXT NOT NULL,
                solution TEXT NOT NULL,
                rating INTEGER,
                comment TEXT,
                improved_solution TEXT,
                model_used TEXT,
                source TEXT,
                confidence REAL
            )
        ''')

        # Chat history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                metadata TEXT
            )
        ''')

        # Analytics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                event_type TEXT NOT NULL,
                event_data TEXT,
                session_id TEXT
            )
        ''')

        conn.commit()
        conn.close()
        logger.info("✅ Database tables initialized")

    # ========== Feedback Operations ==========

    def save_feedback(
        self,
        query: str,
        solution: str,
        rating: int = None,
        comment: str = None,
        improved_solution: str = None,
        model_used: str = None,
        source: str = None,
        confidence: float = None
    ) -> int:
        """Save feedback to database"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO feedback (
                timestamp, query, solution, rating, comment,
                improved_solution, model_used, source, confidence
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            query,
            solution,
            rating,
            comment,
            improved_solution,
            model_used,
            source,
            confidence
        ))

        feedback_id = cursor.lastrowid
        conn.commit()
        conn.close()

        logger.info(f"✅ Feedback saved with ID: {feedback_id}")
        return feedback_id

    def get_feedback_stats(self) -> Dict:
        """Get feedback statistics"""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Total feedback
        cursor.execute("SELECT COUNT(*) FROM feedback")
        total = cursor.fetchone()[0]

        # Average rating
        cursor.execute(
            "SELECT AVG(rating) FROM feedback WHERE rating IS NOT NULL")
        avg_rating = cursor.fetchone()[0] or 0

        # Rating distribution
        cursor.execute("""
            SELECT rating, COUNT(*) as count
            FROM feedback
            WHERE rating IS NOT NULL
            GROUP BY rating
            ORDER BY rating DESC
        """)
        rating_dist = {row[0]: row[1] for row in cursor.fetchall()}

        # Recent feedback
        cursor.execute("""
            SELECT timestamp, query, rating, comment
            FROM feedback
            ORDER BY timestamp DESC
            LIMIT 10
        """)
        recent = [
            {
                'timestamp': row[0],
                'query': row[1],
                'rating': row[2],
                'comment': row[3]
            }
            for row in cursor.fetchall()
        ]

        conn.close()

        return {
            'total_feedback': total,
            'average_rating': round(avg_rating, 2),
            'rating_distribution': rating_dist,
            'recent_feedback': recent
        }

    def get_positive_feedback(self, min_rating: int = 4) -> List[Dict]:
        """Get positive feedback for learning"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT query, solution, improved_solution, rating, comment
            FROM feedback
            WHERE rating >= ? AND improved_solution IS NOT NULL
            ORDER BY rating DESC, timestamp DESC
        """, (min_rating,))

        results = [
            {
                'query': row[0],
                'solution': row[1],
                'improved_solution': row[2],
                'rating': row[3],
                'comment': row[4]
            }
            for row in cursor.fetchall()
        ]

        conn.close()
        return results

    # ========== Chat History ==========

    def save_message(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: Dict = None
    ) -> int:
        """Save chat message"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO chat_history (session_id, timestamp, role, content, metadata)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            session_id,
            datetime.now().isoformat(),
            role,
            content,
            json.dumps(metadata) if metadata else None
        ))

        message_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return message_id

    def get_chat_history(
        self,
        session_id: str,
        limit: int = 50
    ) -> List[Dict]:
        """Get chat history for a session"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT timestamp, role, content, metadata
            FROM chat_history
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (session_id, limit))

        messages = [
            {
                'timestamp': row[0],
                'role': row[1],
                'content': row[2],
                'metadata': json.loads(row[3]) if row[3] else None
            }
            for row in cursor.fetchall()
        ]

        conn.close()
        return list(reversed(messages))

    # ========== Analytics ==========

    def log_event(
        self,
        event_type: str,
        event_data: Dict = None,
        session_id: str = None
    ):
        """Log analytics event"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO analytics (timestamp, event_type, event_data, session_id)
            VALUES (?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            event_type,
            json.dumps(event_data) if event_data else None,
            session_id
        ))

        conn.commit()
        conn.close()

    def get_analytics(self, days: int = 7) -> Dict:
        """Get analytics for last N days"""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Total queries
        cursor.execute("""
            SELECT COUNT(*)
            FROM chat_history
            WHERE role = 'user'
            AND timestamp >= datetime('now', '-' || ? || ' days')
        """, (days,))
        total_queries = cursor.fetchone()[0]

        # Events by type
        cursor.execute("""
            SELECT event_type, COUNT(*) as count
            FROM analytics
            WHERE timestamp >= datetime('now', '-' || ? || ' days')
            GROUP BY event_type
        """, (days,))
        events = {row[0]: row[1] for row in cursor.fetchall()}

        conn.close()

        return {
            'period_days': days,
            'total_queries': total_queries,
            'events': events
        }


# Global database instance
def init_db():
    """Initialize database"""
    db = Database()
    return db


# Create global instance
db = Database()
