from datetime import date
from models import PerformanceLogs, PerformanceMaster
from extensions import db


def trigger_performance_event(assignment, old_status, metricId, old_progress):

    today = date.today()

    metricDetail = PerformanceMaster.query.filter_by(id=metricId).first()

    if assignment.progressPercent == 100 and old_progress  < 100 and  old_status != assignment.statusId:


        if not log_exists(assignment.userId,assignment.id,metricDetail.id):
            completion_log = PerformanceLogs(
                userId=assignment.userId,
                assignmentId=assignment.id,
                metricId=metricDetail.id,
                metricValue=metricDetail.metricWeight,
                logDate=today
            )
            db.session.add(completion_log)


        if assignment.dueDate >= today:

            if not log_exists(assignment.userId,assignment.id,metricDetail.id):
                ontime_log = PerformanceLogs(
                    userId=assignment.userId,
                    assignmentId=assignment.id,
                    metricId=metricDetail.id,
                    metricValue=metricDetail.metricWeight,
                    logDate=today
                )
                db.session.add(ontime_log)
        else:
            if not log_exists(assignment.userId, assignment.id, metricDetail.id):
                overdue_log = PerformanceLogs(
                    userId=assignment.userId,
                    assignmentId=assignment.id,
                    metricId=metricDetail.id,
                    metricValue=metricDetail.metricWeight,
                    logDate=today
                )
                db.session.add(overdue_log)


    elif assignment.progressPercent > old_progress:

        progress_diff = assignment.progressPercent - old_progress

        partial_score = (progress_diff / 100) * metricDetail.metricWeight

        progress_log = PerformanceLogs(
            userId=assignment.userId,
            assignmentId=assignment.id,
            metricId=metricDetail.id,
            metricValue=round(partial_score, 2),
            logDate=today
        )
        db.session.add(progress_log)



def log_exists(user_id, assignment_id, metric_id):
    return PerformanceLogs.query.filter_by(
        userId=user_id,
        assignmentId=assignment_id,
        metricId=metric_id
    ).first()


