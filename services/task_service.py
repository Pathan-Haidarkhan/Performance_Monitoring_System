from datetime import datetime

from dto.response.taskResponse import TaskStatusResponseDTO
from models import TaskMaster
from models import TaskAssignments
from models import TaskStatusMaster
from models import TaskActivityLogs
from dto.response.taskResponse import TaskResponseDTO
from utils.security import current_user, current_user_role
from extensions import db
from .performance_event_service import trigger_performance_event

class TaskService:


    @staticmethod
    def createTask(dto):

        currentUser = current_user()
        task = TaskMaster(
            title=dto.title,
            description=dto.description,
            priority=dto.priority,
            createdBy= currentUser
        )
        db.session.add(task)
        db.session.commit()

        return { 'message': 'Task created successfully', 'taskId' : task.id } , True , 200


    @staticmethod
    def updateTask(task_id, dto):
        task = TaskMaster.query.get(task_id)
        if not task:
            return { 'message': 'Task not found', 'taskId' : task_id } , False, 400

        task.title = dto.title,
        task.description = dto.description,
        task.priority = dto.priority

        db.session.commit()
        return { 'message': 'Task Updated successfully', 'taskId' : task.id } , True , 200


    @staticmethod
    def deleteTask(task_id):
        task = TaskMaster.query.get(task_id)
        if not task:
            return { 'message': 'Task not found', 'taskId' : task_id } , False, 400

        db.session.delete(task)
        db.session.commit()
        return { 'message': 'Task Deleted successfully', 'taskId' : task.id } , True , 200


    @staticmethod
    def assignTask(dto):

        getTask = TaskMaster.query.get(dto.taskId)
        currentUser = current_user()
        if getTask is not None:
            assignment = TaskAssignments(
                taskId= dto.taskId,
                assignedTo=dto.assignedTo,
                assignedBy=currentUser,
                statusId=dto.statusId,
                dueDate=dto.dueDate,
                progressPercent=0
            )
            db.session.add(assignment)
            db.session.commit()

            log = TaskActivityLogs(
                assignmentId=assignment.id,
                progressPercent=0,
                updatedBy=currentUser,
                remarks=dto.remarks
            )
            db.session.add(log)
            db.session.commit()

            return { 'message': 'Task assign successfully', 'assignmentId': assignment.id }, True, 200

        return {'message': 'Task not found'}, False, 400


    @staticmethod
    def getTask(taskId):

        getTask = TaskMaster.query.get(taskId)
        if getTask is not None:
            data  = TaskResponseDTO.model_validate(getTask).model_dump(exclude_none=True)
            return {'message': 'Get task details successfully' , 'data': data}, True, 200
        return {'message': 'Task not found'}, False, 400


    @staticmethod
    def updateTaskStatus(dto):

        assignment  = TaskAssignments.query.get(dto.assignmentId)
        oldStatusId = assignment.statusId
        oldProgress = assignment.progressPercent
        currentUser = current_user()
        currentRole = current_user_role()

        if not assignment:
            return {'message': 'Task Assignment not found'}, False, 404

        if currentRole == "EMPLOYEE" and assignment.assignedTo != currentUser:
            return {'message': 'You cannot update this task'}, False, 403

        status  = TaskStatusMaster.query.get(assignment.statusId)

        if status.isFinal and currentRole == "EMPLOYEE":
            return  {'message': 'Task Already completed'}, False, 400

        if dto.progressPercent == 100:
            final_status = TaskStatusMaster.query.filter_by(isFinal=True).first()

            if not final_status:
                return {'message': 'Final status not configured'}, False, 500

            assignment.statusId = final_status.id
            assignment.progressPercent = dto.progressPercent
            assignment.completedDate = datetime.now()

        else:
            new_status = TaskStatusMaster.query.get(dto.statusId)
            if not new_status:
                return {'message': 'Invalid status'}, False, 400

            if currentRole == "EMPLOYEE" and new_status.isFinal:
                return {'message': 'Employees cannot set final status'}, False, 403

            assignment.statusId = new_status.id
            assignment.progressPercent = dto.progressPercent

        log = TaskActivityLogs(
            assignmentId= assignment.id,
            progressPercent= dto.progressPercent,
            remarks= dto.remarks,
            updatedBy= currentUser
        )
        db.session.add(log)

        trigger_performance_event(assignment,oldStatusId,dto.matricId,oldProgress)
        db.session.commit()

        return { 'message': 'Task Assignment status updated successfully'} , True , 200


    @staticmethod
    def reAssignTask(dto):

        assignment = TaskAssignments.query.get(dto.assignmentId)
        currentUser = current_user()

        if not assignment:
            return {'message': 'Task Assignment not found'}, False, 400

        status = TaskStatusMaster.query.get(assignment.statusId)
        if status.isFinal:
            return {'message': 'Task Already completed'}, False, 400

        assignment.assignedTo= dto.newUserId

        activity = TaskActivityLogs(
            assignmentId=assignment.id,
            progressPercent=dto.progressPercent,
            remarks=dto.remarks,
            updatedBy= currentUser
        )

        db.session.add(activity)
        db.session.commit()
        return { 'message': 'Task reassigned successfully'} , True , 200



    @staticmethod
    def createStatus(dto):
        status = TaskStatusMaster(
            statusName=dto.statusName,
            isFinal=dto.isFinal
        )
        db.session.add(status)
        db.session.commit()
        return { 'message': 'Task Status Created successfully', 'status_id': status.id} , True , 200



    @staticmethod
    def updateStatus(status_id, dto):
        status = TaskStatusMaster.query.get(status_id)
        if not status:
            return {'message': 'Task Status not found'}, False, 400

        status.statusName =  dto.statusName
        status.isFinal = dto.isFinal
        db.session.commit()
        return { 'message': 'Status updated successfully', 'statusId': status.id} , True , 200



    @staticmethod
    def deleteStatus(status_id):
        status = TaskStatusMaster.query.get(status_id)
        if not status:
            return {'message': 'Task Status not found'}, False, 400

        db.session.delete(status)
        db.session.commit()
        return { 'message': 'Status deleted successfully', 'statusId': status.id} , True , 200


    @staticmethod
    def getAllStatus():
        statuses = TaskStatusMaster.query.all()
        status_list = [ TaskStatusResponseDTO.model_validate(s).model_dump(exclude_none=True) for s in statuses  ]

        return {'message': 'Get All Status successfully', 'data': status_list}, True, 200













