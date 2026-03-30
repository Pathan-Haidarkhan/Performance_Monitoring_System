from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from services.dashboard_service import DashboardService
from utils.apiResponse import api_response
from utils.security import role_required

dashboard_routes = Blueprint('dashboard_routes', __name__, url_prefix='/api/dashboard')


@dashboard_routes.route('/myPerformance', methods=['GET'])
@jwt_required()
@role_required('EMPLOYEE')
def myPerformance():
    Month = request.args.get("month", type=int)
    Year = request.args.get("year", type=int)

    responseDto, success, status = DashboardService.GetMyPerformanceMetrics(month=Month, year=Year)

    return api_response(
        message=responseDto['message'],
        data=responseDto['data'],
        success=success,
        status_code=status
    )


@dashboard_routes.route('/teamPerformance', methods=['GET'])
@jwt_required()
@role_required('MANAGER')
def teamPerformance():
    Month = request.args.get("month", type=int)
    Year = request.args.get("year", type=int)

    responseDto, success, status = DashboardService.teamPerformance(month=Month, year=Year)

    return api_response(
        message=responseDto['message'],
        data=responseDto['data'],
        success=success,
        status_code=status
    )


@dashboard_routes.route('/companyPerformance', methods=['GET'])
@jwt_required()
@role_required('ADMIN')
def companyPerformance():
    Month = request.args.get("month", type=int)
    Year = request.args.get("year", type=int)

    responseDto, success, status = DashboardService.companyPerformance(month=Month, year=Year)

    return api_response(
        message=responseDto['message'],
        data=responseDto['data'],
        success=success,
        status_code=status
    )


@dashboard_routes.route('/topPerformers', methods=['GET'])
@jwt_required()
@role_required('ADMIN')
def topPerformers():
    Month = request.args.get("month", type=int)
    Year = request.args.get("year", type=int)

    responseDto, success, status = DashboardService.topPerformers(month=Month, year=Year)

    return api_response(
        message=responseDto['message'],
        data=responseDto['data'],
        success=success,
        status_code=status
    )


@dashboard_routes.route('/performanceTrend', methods=['GET'])
@jwt_required()
@role_required(["ADMIN", "MANAGER", "EMPLOYEE"])
def performanceTrend():
    Months = request.args.get("months", 6, type=int)
    user_id = request.args.get("userId", type=int)

    responseDto, success, status = DashboardService.performanceTrend(months=Months, userId=user_id)

    return api_response(
        message=responseDto['message'],
        data=responseDto['data'],
        success=success,
        status_code=status
    )


@dashboard_routes.route('/companyRanking', methods=['GET'])
@jwt_required()
@role_required('ADMIN')
def companyRanking():
    Month = request.args.get("month", type=int)
    Year = request.args.get("year", type=int)

    responseDto, success, status = DashboardService.companyRanking(months=Month, year=Year)

    return api_response(
        message=responseDto['message'],
        data=responseDto['data'],
        success=success,
        status_code=status
    )

@dashboard_routes.route('/ratingDistribution', methods=['GET'])
@jwt_required()
@role_required('ADMIN')
def ratingDistribution():
    Month = request.args.get("month", type=int)
    Year = request.args.get("year", type=int)

    responseDto, success, status = DashboardService.ratingDistribution(months=Month, year=Year)

    return api_response(
        message=responseDto['message'],
        data=responseDto['data'],
        success=success,
        status_code=status
    )
