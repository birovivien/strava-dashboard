from fastapi import APIRouter
from backend.database import query

router = APIRouter()

@router.get("/activities")
def get_activities():
    rows = query("SELECT * FROM activities ORDER BY start_date DESC")
    return rows

@router.get("/stats/weekly-distance")
def weekly_distance():
    rows = query("""
        SELECT
            DATE_TRUNC('week', start_date) AS week,
            sport_type,
            ROUND(CAST(SUM(distance) / 1000 AS numeric), 2) AS total_km
        FROM activities
        GROUP BY week, sport_type
        ORDER BY week DESC
    """)
    return rows

@router.get("/stats/monthly-avg-hr")
def monthly_avg_hr():
    rows = query ("""
                  SELECT
    DATE_TRUNC('month', start_date) AS month,
    sport_type,
    ROUND(CAST(AVG(average_heartrate) AS numeric), 1) AS avg_hr
FROM activities
WHERE average_heartrate IS NOT NULL
GROUP BY month, sport_type
ORDER BY month DESC
    """)
    return rows