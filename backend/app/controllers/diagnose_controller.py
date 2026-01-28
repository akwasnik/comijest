from flask import jsonify, request
from ..services.diagnose_service import DiagnoseService


class DiagnoseController:
    def diagnose():
        payload = request.get_json(silent=True) or {}

        symptoms = payload.get("symptoms", [])
        userinput = (payload.get("userinput") or "").strip()

        # łączenie w jeden ciąg (PL)
        parts = []
        if userinput:
            parts.append(userinput)
        if symptoms:
            parts.append(", ".join(symptoms))
        text_pl = ", ".join(parts).strip()

        if not text_pl:
            return jsonify({"error": "Brak objawów lub opisu"}), 400

        result = DiagnoseService.diagnose(text_pl, top_k=5)
        return jsonify(result)