from flask import Blueprint

from ..controllers.diagnose_controller import DiagnoseController
from ..extensions import limiter
diagnose_bp = Blueprint("diagnose", __name__)

diagnose_bp.post("/diagnose", endpoint="diagnose")((DiagnoseController.diagnose))
