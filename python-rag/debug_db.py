"""
Debug script to test database connection and data retrieval
"""
import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_database_connection():
    """Test database connection"""
    try:
        conn = psycopg2.connect(
            host=os.getenv('SUPABASE_DB_HOST', 'your-supabase-host.supabase.co'),
            port=os.getenv('SUPABASE_DB_PORT', '5432'),
            database=os.getenv('SUPABASE_DB_NAME', 'postgres'),
            user=os.getenv('SUPABASE_DB_USER', 'postgres'),
            password=os.getenv('SUPABASE_DB_PASSWORD', 'your-database-password')
        )
        print("✓ Database connection successful")
        return conn
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return None

def test_student_context(conn, student_id=1):
    """Test student context retrieval"""
    try:
        cursor = conn.cursor()
        
        # Get student info
        cursor.execute("""
            SELECT id, name, email
            FROM users 
            WHERE id = %s
        """, (student_id,))
        
        student_row = cursor.fetchone()
        if student_row:
            print(f"✓ Student info: ID={student_row[0]}, Name={student_row[1]}, Email={student_row[2]}")
        else:
            print("⚠ No student found with ID 1")
            
            # List all students
            cursor.execute("""
                SELECT id, name, email
                FROM users 
                ORDER BY id
                LIMIT 10
            """)
            
            student_rows = cursor.fetchall()
            if student_rows:
                print("Available students:")
                for row in student_rows:
                    print(f"  ID={row[0]}, Name={row[1]}, Email={row[2]}")
            else:
                print("No students found in database")
        
        # Get available assessments
        cursor.execute("""
            SELECT id, name, description, category, total_time, duration
            FROM assessments 
            WHERE is_active = true
            AND (start_date IS NULL OR start_date <= NOW())
            AND (end_date IS NULL OR end_date >= NOW())
            ORDER BY created_at DESC
        """)
        
        assessment_rows = cursor.fetchall()
        print(f"✓ Found {len(assessment_rows)} available assessments")
        
        for i, row in enumerate(assessment_rows[:3]):  # Show first 3
            print(f"  {i+1}. {row[1]} ({row[3]}) - {row[4] or row[5] or 30} minutes")
        
        if len(assessment_rows) > 3:
            print(f"  ... and {len(assessment_rows) - 3} more")
        
        cursor.close()
        return True
        
    except Exception as e:
        print(f"✗ Student context retrieval failed: {e}")
        return False

def main():
    """Main function"""
    print("Testing RAG database connection and data retrieval...")
    print("=" * 50)
    
    conn = test_database_connection()
    if not conn:
        return
    
    success = test_student_context(conn)
    conn.close()
    
    if success:
        print("\n✓ All tests passed!")
    else:
        print("\n✗ Some tests failed!")

if __name__ == "__main__":
    main()