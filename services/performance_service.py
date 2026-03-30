from models import PerformanceMaster
from extensions import db
from dto.response.performanceResponse import  PerformanceMetricResponseDTO

class PerformanceService:

    @staticmethod
    def createMatric(dto):

        existing = PerformanceMaster.query.filter_by(metricName=dto.metricName).first()
        if existing:
            return {"message": "Metric already exists"}, False, 400

        metric = PerformanceMaster(
            metricName=dto.metricName,
            metricWeight=dto.metricWeight,
            description=dto.description,
        )

        db.session.add(metric)
        db.session.commit()

        return {"message": "Metric created", 'metricId': metric.id}, True, 200

    @staticmethod
    def getAllMetrics():
        metrics = PerformanceMaster.query.filter_by(isActive=True).all()
        data = [PerformanceMetricResponseDTO.model_validate(metric).model_dump(exclude_none=True) for metric in metrics]
        return {'message': 'Get All metrics successfully', 'data': data}, True, 200

    @staticmethod
    def update_metric(metricId, dto):
        metric = PerformanceMaster.query.get(metricId)

        if not metric:
            return {"message": "Metric not found"}, False, 404

        dtoData = dto.model_validate().model_dump(exclude_none=True)

        for key, value in dtoData.items():
            setattr(metric, key, value)

        db.session.commit()

        return {"message": "Metric Updated successfully", 'updatedMetricId': metric.id} , True, 200

    @staticmethod
    def deleteMetric(metricId):
        metric = PerformanceMaster.query.get(metricId)

        if not metric:
            return {"message": "Metric not found"}, False, 404

        db.session.delete(metric)
        db.session.commit()

        return {"message": "Metric deleted"}, True, 200





