from extensions import db


def calculate_monthly_performance(user_id, month, year):

        result = db.session.execute(
            "CALL calculateMonthlyPerformance(:user_id, :month, :year)",
            {
                "user_id": user_id,
                "month": month,
                "year": year
            }
        )
        data = result.fetchone()
        db.session.commit()

        if data:
            return {
                "userId": data._mapping["userId"],
                "month": data._mapping["month"],
                "year": data._mapping["year"],
                "totalScore": float(data._mapping["totalScore"]),
                "rating": data._mapping["rating"]
            }, True

        return {"message": "No data returned"}, False
