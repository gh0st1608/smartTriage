from flask import Blueprint, request, jsonify
from app.models.triage_model import triage, URGENCY_LEVELS
from app.utils.helpers import snake_to_camel
from datetime import datetime

predict_bp = Blueprint('predict_bp', __name__)

@predict_bp.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json

        if not data or 'Data' not in data or 'Triaje' not in data['Data']:
            return jsonify({"status": "error", "message": "Estructura inválida"}), 400

        raw_triaje_data = data['Data']['Triaje']
        triaje_data = {
            snake_to_camel(k): v for k, v in raw_triaje_data.items()
        }

        missing_vars = [var for var in triage.variables if var not in triaje_data]
        if missing_vars:
            return jsonify({"status": "error", "message": f"Faltan: {', '.join(missing_vars)}"}), 400

        triaje_data_clean = {
            var: str(triaje_data[var]).strip().capitalize() for var in triage.variables
        }

        invalid_values = [var for var in triage.variables if triaje_data_clean[var] not in ['Si', 'No']]
        if invalid_values:
            return jsonify({"status": "error", "message": f"Valores inválidos: {', '.join(invalid_values)}"}), 400

        nivel = triage.predict(triaje_data_clean)

        return jsonify({
            "status": "success",
            "data": {
                "nivel_triaje": nivel,
                "detalle": URGENCY_LEVELS[nivel],
                "timestamp": datetime.now().isoformat()
            }
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500