"""
Initialize database and create tables
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.core.database import init_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Initialize database"""
    logger.info("🔄 Initializing database...")
    
    try:
        # Ensure data directory exists
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        logger.info(f"✅ Data directory: {data_dir.absolute()}")
        
        # Initialize database
        db = init_db()
        logger.info("✅ Database initialized successfully")
        
        # Test database
        stats = db.get_feedback_stats()
        logger.info(f"✅ Database test passed")
        logger.info(f"   Total feedback: {stats['total_feedback']}")
        
        logger.info("\n✅ Database initialization complete!")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

# """
# Initialize database and create necessary directories
# """
# import sys
# from pathlib import Path

# # Add parent directory to path
# sys.path.insert(0, str(Path(__file__).parent.parent))

# from backend.core.database import Database
# from backend.core.config import settings
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# def init_database():
#     """Initialize database and create tables"""
#     logger.info("🚀 Initializing database...")
    
#     # Create data directory if it doesn't exist
#     data_dir = Path("data")
#     data_dir.mkdir(exist_ok=True)
#     logger.info(f"✅ Created data directory: {data_dir}")
    
#     # Initialize database
#     db = Database()
#     logger.info("✅ Database tables created")
    
#     # Test database connection
#     stats = db.get_feedback_stats()
#     logger.info(f"✅ Database connection verified")
#     logger.info(f"   Total feedback: {stats['total_feedback']}")
    
#     return True


# def create_directories():
#     """Create necessary directories"""
#     directories = [
#         "data",
#         "data/qdrant_storage",
#         "logs"
#     ]
    
#     for dir_path in directories:
#         Path(dir_path).mkdir(parents=True, exist_ok=True)
#         logger.info(f"✅ Created directory: {dir_path}")


# def verify_knowledge_base():
#     """Verify knowledge base file exists"""
#     kb_path = Path("data/math_knowledge_base.json")
    
#     if not kb_path.exists():
#         logger.warning(f"⚠️  Knowledge base not found at {kb_path}")
#         logger.info("   It will be created with default data on first run")
#         return False
    
#     import json
#     with open(kb_path, 'r') as f:
#         kb_data = json.load(f)
    
#     logger.info(f"✅ Knowledge base verified: {len(kb_data)} problems")
#     return True


# def main():
#     """Main initialization function"""
#     logger.info("=" * 60)
#     logger.info("MathAI Database Initialization")
#     logger.info("=" * 60)
    
#     try:
#         # Create directories
#         create_directories()
        
#         # Initialize database
#         init_database()
        
#         # Verify knowledge base
#         verify_knowledge_base()
        
#         logger.info("=" * 60)
#         logger.info("✅ Initialization complete!")
#         logger.info("=" * 60)
#         logger.info("")
#         logger.info("Next steps:")
#         logger.info("1. Start backend: cd backend && python main.py")
#         logger.info("2. Start frontend: cd frontend && npm run dev")
#         logger.info("")
        
#         return True
        
#     except Exception as e:
#         logger.error(f"❌ Initialization failed: {e}")
#         import traceback
#         traceback.print_exc()
#         return False


# if __name__ == "__main__":
#     success = main()
#     sys.exit(0 if success else 1)