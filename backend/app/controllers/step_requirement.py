from flask import request, session
from app.controllers.common import json_response
from flask import Blueprint
from app.pkgs.tools.i18b import getI18n
from app.pkgs.prompt.prompt import clarifyRequirement
from app.pkgs.knowledge.app_info import getAppArchitecture
from app.models.requirement import Requirement
from config import REQUIREMENT_STATUS_InProgress

bp = Blueprint('step_requirement', __name__, url_prefix='/step_requirement')

@bp.route('/clarify', methods=['POST'])
@json_response
def clarify():
    _ = getI18n("controllers")
    userPrompt = request.json.get('user_prompt')
    globalContext = request.json.get('global_context')
    userName = session["username"]
    taskID = request.json.get('task_id')

    appID = session[userName]['memory']['task_info']['app_id']

    if len(appID) == 0 or not appID:
        raise Exception(_("Please select the application you want to develop."))
    
    Requirement.update_requirement(requirement_id=taskID, original_requirement=userPrompt, status=REQUIREMENT_STATUS_InProgress)
    
    appArchitecture, _ = getAppArchitecture(appID)
    msg, success = clarifyRequirement(userPrompt, globalContext, appArchitecture)

    if success:
        return {'message': msg, 'memory': session[userName]['memory']}
    else:
        raise Exception(_("Failed to clarify requirement."))
