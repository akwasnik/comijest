from flask import jsonify
from ..services.diagnose_service import DiagnoseService


class DiagnoseController:
    def diagnose():
        illnes = DiagnoseService.diagnose()
        return jsonify({ "message": f'You have {illnes}'})