from  flask import Blueprint, jsonify, request
from dto.request.performanceRequest import PerformanceMetricCreateDTO, PerformanceMetricUpdateDTO
from services.performance_service import PerformanceService
from utils.security import role_required
from utils.apiResponse import api_response
from flask_jwt_extended import jwt_required


metric_routes = Blueprint('metric_routes', __name__,url_prefix='/matric/performance')

@metric_routes.route('/createMetric', methods=['POST'])
@jwt_required
@role_required('ADMIN')
def createMetric():

    dto = PerformanceMetricCreateDTO(**request.json)
    response, success, status = PerformanceService.createMatric(dto)
    return api_response(
        success=success,
        message=response['message'],
        data=response,
        status_code=status
    )

@metric_routes.route('/updateMetric/<int:metricId>', methods=['PUT'])
@jwt_required
@role_required('ADMIN')
def updateMetric(metricId):
    dto = PerformanceMetricUpdateDTO(**request.json)
    response, success, status = PerformanceService.update_metric(metricId,dto)
    return api_response(
        success=success,
        message=response['message'],
        data=response,
        status_code=status
    )


@metric_routes.route('/getAllMetric', methods=['GET'])
@jwt_required
@role_required('ADMIN')
def getAllMetric():
    response, success, status = PerformanceService.getAllMetrics()
    return api_response(
        success=success,
        message=response['message'],
        data=response,
        status_code=status
    )

@metric_routes.route('/deleteMetric/<int:metricId>', methods=['DELETE'])
@jwt_required
@role_required('ADMIN')
def deleteMetric(metricId):
    response, success, status = PerformanceService.deleteMetric(metricId)
    return api_response(
        success=success,
        message=response['message'],
        data=response,
        status_code=status
    )