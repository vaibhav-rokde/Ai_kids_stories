"""
Migration script to add version support to stories table
Run this once to update existing database
"""
from sqlalchemy import text
from app.core.database import engine, Base, init_db
from app.models.story import Story, StoryVersion
from app.models.user import User


def migrate():
    """Add current_version column and create story_versions table"""
    print("Starting migration...")

    with engine.connect() as connection:
        # Check if current_version column exists
        try:
            result = connection.execute(text("SELECT current_version FROM stories LIMIT 1"))
            result.close()
            print("✓ current_version column already exists")
        except Exception:
            # Add current_version column to stories table
            print("Adding current_version column to stories table...")
            connection.execute(text(
                "ALTER TABLE stories ADD COLUMN current_version INTEGER DEFAULT 1"
            ))
            connection.commit()
            print("✓ Added current_version column")

        # Create story_versions table if not exists
        print("Creating story_versions table if not exists...")
        Base.metadata.create_all(bind=engine)
        print("✓ story_versions table ready")

    print("\n✅ Migration completed successfully!")
    print("You can now use version tracking features.")


if __name__ == "__main__":
    migrate()
