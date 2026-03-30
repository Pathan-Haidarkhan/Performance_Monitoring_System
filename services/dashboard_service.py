import calendar

from sqlalchemy import text

from dto.response.performanceResponse import PerformanceSummaryDTO, PerformanceCalculationDTO
from extensions import db
from utils.security import current_user, current_user_role


class DashboardService:

    @staticmethod
    def GetMyPerformanceMetrics(month, year):

        userId = current_user()

        getSummary = db.session.execute(text("""
               SELECT totalScore, rating
               FROM PerformanceSummary
               WHERE userId = :uid
               AND month = :m
               AND year = :y
           """), {"uid": userId, "m": month, "y": year}).fetchone()

        getMetrics = db.session.execute(text("""
                SELECT metricId, calculatedScore
                FROM PerformanceCalculations
                WHERE userId = :uid
                AND month = :m
                AND year = :y
            """), {"uid": userId, "m": month, "y": year}).fetchall()

        data = {
            'summary': PerformanceSummaryDTO.model_validate(getSummary).model_dump(exclude_none=True),
            'metrics': [PerformanceCalculationDTO.model_validate(m).model_dump(exclude_none=True) for m in getMetrics]
        }
        return {'message': 'Performance Data get successfully', 'data': data}, True, 200

    @staticmethod
    def teamPerformance(month, year):

        managerId = current_user()

        results = db.session.execute(text("""
               SELECT u.id, u.firstName, u.lastName, ps.totalScore, ps.rating
               FROM UserMaster u
               JOIN PerformanceSummary ps ON ps.userId = u.id
               WHERE u.managerId = :mid
               AND ps.month = :m
               AND ps.year = :y
               ORDER BY ps.totalScore DESC
           """), {"mid": managerId, "m": month, "y": year}).fetchall()

        data = [dict(row) for row in results]
        return {'message': 'get Team Performance Data successfully', 'data': data}, True, 200

    @staticmethod
    def companyPerformance(month, year):

        stats = db.session.execute(text("""
               SELECT 
                   COUNT(*) as totalEmployees,
                   AVG(totalScore) as averageScore,
                   MAX(totalScore) as highestScore,
                   MIN(totalScore) as lowestScore
               FROM PerformanceSummary
               WHERE month = :m
               AND year = :y
           """), {"m": month, "y": year}).fetchone()

        return {'message': 'get Company Performance Data successfully', 'data': dict(stats)}, True, 200

    @staticmethod
    def topPerformers(month, year):

        results = db.session.execute(text("""
                SELECT u.name, ps.totalScore, ps.rating
                FROM PerformanceSummary ps
                JOIN UserMaster u ON u.id = ps.userId
                WHERE ps.month = :m
                AND ps.year = :y
                ORDER BY ps.totalScore DESC
                LIMIT 5
            """), {"m": month, "y": year}).fetchall()

        data = [dict(row) for row in results]
        return {'message': 'get Top Performers Data successfully', 'data': data}, True, 200

    @staticmethod
    def performanceTrend(months, userId):

        currentuser = current_user()
        role = current_user_role()

        if role == "EMPLOYEE":
            result = db.session.execute(text("""
                   SELECT year, month, totalScore
                   FROM PerformanceSummary
                   WHERE userId = :uid
                   ORDER BY year DESC, month DESC
                   LIMIT :limit
               """), {"uid": currentuser, "limit": months}).fetchall()

            data = format_trend_result(result)
            return {'message': 'get Trend data successfully', 'data': {"type": "personal_trend", **data}}, True, 200

        elif role == "MANAGER":

            if userId:
                employee = db.session.execute(text("""
                                SELECT id FROM UserMaster
                                WHERE id = :eid AND managerId = :mid
                            """), {"eid": userId, "mid": currentuser}).fetchone()

                if not employee:
                    return {'message': 'User Can''t Access data'}, False, 401

                result = db.session.execute(text("""
                                   SELECT year, month, totalScore
                                   FROM PerformanceSummary
                                   WHERE userId = :uid
                                   ORDER BY year DESC, month DESC
                                   LIMIT :limit
                               """), {"uid": userId, "limit": months}).fetchall()

                data = format_trend_result(result)
                return {'message': 'get Employee''s Trend data successfully',
                        'data': {"type": "employee_trend", **data}}, True, 200

            result = db.session.execute(text("""
                        SELECT ps.year, ps.month, AVG(ps.totalScore) as avgScore
                        FROM PerformanceSummary ps
                        JOIN UserMaster u ON u.id = ps.userId
                        WHERE u.managerId = :mid
                        GROUP BY ps.year, ps.month
                        ORDER BY ps.year DESC, ps.month DESC
                        LIMIT :limit
                    """), {"mid": currentuser, "limit": months}).fetchall()

            data = format_trend_result(result)
            return {'message': 'Team average trend fetched successfully',
                    'data': {"type": "team_average_trend", **data}}, True, 200

        elif role == "ADMIN":

            if userId:
                result = db.session.execute(text("""
                        SELECT year, month, totalScore
                        FROM PerformanceSummary
                        WHERE userId = :uid
                        ORDER BY year DESC, month DESC
                        LIMIT :limit
                    """), {"uid": userId, "limit": months}).fetchall()

                data = format_trend_result(result)
                return {'message': 'Employee trend fetched successfully',
                        'data': {"type": "employee_trend_by_admin", **data}}, True, 200

            result = db.session.execute(text("""
                    SELECT year, month, AVG(totalScore) as avgScore
                    FROM PerformanceSummary
                    GROUP BY year, month
                    ORDER BY year DESC, month DESC
                    LIMIT :limit
                """), {"limit": months}).fetchall()

            data = format_trend_result(result)

            return {'message': 'Company trend fetched successfully',
                    'data': {"type": "company_average_trend", **data}}, True, 200

    @staticmethod
    def companyRanking(month, year):

        result = db.session.execute(text("""
                SELECT 
                    u.id,
                    u.name,
                    p.totalScore,
                    p.rating
                FROM PerformanceSummary p
                JOIN UserMaster u ON u.id = p.userId
                WHERE p.month = :month AND p.year = :year
                ORDER BY p.totalScore DESC
            """), {"month": month, "year": year})

        data = result.fetchall()

        response = []
        rank = 1

        for row in data:
            response.append({
                "rank": rank,
                "employee": row.name,
                "score": row.totalScore,
                "rating": row.rating,
            })
            rank += 1
        return {'message': 'get Company ranking table', 'data': response}, True, 200

    @staticmethod
    def ratingDistribution(month, year):

        result = db.session.execute(text("""
                SELECT 
                    rating,
                    COUNT(*) as total
                FROM PerformanceSummary
                WHERE month = :month AND year = :year
                GROUP BY rating
                ORDER BY FIELD(rating,'EXCELLENT','GOOD','AVERAGE','POOR')
            """), {"month": month, "year": year})

        rows = result.fetchall()

        labels = []
        values = []

        for r in rows:
            labels.append(r.rating)
            values.append(r.total)

        return {'message': 'get Company ranking distribuion',
                'data': { "labels": labels, "values": values}}, True, 200


def format_trend_result(result, score_field="totalScore"):
    if not result:
        return {
            "labels": [],
            "values": [],
            "growthPercentage": 0,
            "trendDirection": "Stable"
        }

    # Reverse for chronological order
    result = list(reversed(result))

    labels = []
    values = []

    for row in result:
        month_name = calendar.month_abbr[row.month]
        labels.append(f"{month_name} {row.year}")
        values.append(float(getattr(row, score_field)))

    growth = 0
    direction = "Stable"

    if len(values) >= 2:
        current = values[-1]
        previous = values[-2]

        if previous != 0:
            growth = round(((current - previous) / previous) * 100, 2)

        if growth > 0:
            direction = "Improving"
        elif growth < 0:
            direction = "Declining"

    return {
        "labels": labels,
        "values": values,
        "growthPercentage": growth,
        "trendDirection": direction
    }
