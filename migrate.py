import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv

load_dotenv()

local_conn = psycopg2.connect(os.getenv("DATABASE_URL"))
railway_conn = psycopg2.connect("postgresql://postgres:sVxDVNJbuubHzGqQrTNDgkyyQzsyuRGj@zephyr.proxy.rlwy.net:53854/railway")

print("Connected to both databases!")

local_cur = local_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
local_cur.execute("SELECT * FROM activities")
activities = local_cur.fetchall()
print(f"Found {len(activities)} activities locally")

railway_cur = railway_conn.cursor()

for i, activity in enumerate(activities):
    railway_cur.execute("""
        INSERT INTO activities (
            id, name, sport_type, start_date, distance,
            moving_time, elapsed_time, total_elevation_gain,
            average_speed, max_speed, average_heartrate, average_watts
        ) VALUES (
            %(id)s, %(name)s, %(sport_type)s, %(start_date)s, %(distance)s,
            %(moving_time)s, %(elapsed_time)s, %(total_elevation_gain)s,
            %(average_speed)s, %(max_speed)s, %(average_heartrate)s, %(average_watts)s
        ) ON CONFLICT (id) DO NOTHING
    """, activity)
    railway_conn.commit()
    print(f"Inserted {i + 1}/{len(activities)}: {activity['name']}")

print("Migration complete!")

local_cur.close()
local_conn.close()
railway_cur.close()
railway_conn.close()