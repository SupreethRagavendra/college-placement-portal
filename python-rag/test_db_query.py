import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

# Connect to database
conn = psycopg2.connect(
    host=os.getenv('SUPABASE_DB_HOST'),
    port=os.getenv('SUPABASE_DB_PORT'),
    database=os.getenv('SUPABASE_DB_NAME'),
    user=os.getenv('SUPABASE_DB_USER'),
    password=os.getenv('SUPABASE_DB_PASSWORD')
)

cursor = conn.cursor()

print("=== ALL ACTIVE ASSESSMENTS ===")
cursor.execute("""
    SELECT id, name, category, total_time, is_active, deleted_at
    FROM assessments 
    WHERE is_active = true
    ORDER BY id
""")

rows = cursor.fetchall()
print(f"Found {len(rows)} assessments:")
for row in rows:
    print(f"ID: {row[0]}, Name: {row[1]}, Category: {row[2]}, Time: {row[3]}, Active: {row[4]}, Deleted: {row[5]}")

print("\n=== AVAILABLE FOR STUDENT 52 (WITH SOFT DELETE CHECK) ===")
cursor.execute("""
    SELECT a.id, a.name, a.category, a.total_time
    FROM assessments a
    WHERE a.is_active = true
    AND a.deleted_at IS NULL
    AND (a.start_date IS NULL OR a.start_date <= NOW())
    AND (a.end_date IS NULL OR a.end_date >= NOW())
    AND a.id NOT IN (
        SELECT assessment_id 
        FROM student_assessments 
        WHERE student_id = %s
    )
    ORDER BY a.created_at DESC
""", (52,))

rows = cursor.fetchall()
print(f"Found {len(rows)} assessments for student 52:")
for row in rows:
    print(f"ID: {row[0]}, Name: {row[1]}, Category: {row[2]}, Time: {row[3]}")

conn.close()

