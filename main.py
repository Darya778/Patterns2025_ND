import connexion
from flask import request
from Src.Services.reference_service import reference_service
from flask import request, jsonify
from Src.Dtos.nomenclature_dto import nomenclature_dto
from Src.Dtos.range_dto import range_dto
from Src.Dtos.category_dto import category_dto
from Src.Dtos.storage_dto import storage_dto


app = connexion.FlaskApp(__name__)

"""
Проверить доступность REST API
"""
@app.route("/api/accessibility", methods=['GET'])
def formats():
    return "SUCCESS"


ref_svc = reference_service()

@app.route("/api/<string:reference_type>", methods=['GET'])
def get_references(reference_type):
    item_id = request.args.get('id', None)
    try:
        result = ref_svc.get(reference_type, item_id)
        out = []
        for r in result:
            if hasattr(r, "to_dto"):
                out.append(r.to_dto().__dict__)
            else:
                out.append(r.__dict__)
        return jsonify(out), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/<string:reference_type>", methods=['PUT'])
def put_reference(reference_type):
    payload = request.get_json()
    try:
        dto_class_map = {
            "nomenclature": nomenclature_dto,
            "range": range_dto,
            "group": category_dto,
            "storage": storage_dto
        }
        key = reference_type.lower()
        dto_cls = None
        if key.startswith("nomen"):
            dto_cls = nomenclature_dto
        elif key.startswith("range"):
            dto_cls = range_dto
        elif key.startswith("group") or key.startswith("category"):
            dto_cls = category_dto
        elif key.startswith("storage"):
            dto_cls = storage_dto
        else:
            return jsonify({"error": "unsupported reference type"}), 400

        dto = dto_cls()
        for k, v in (payload or {}).items():
            if hasattr(dto, k):
                setattr(dto, k, v)

        model = ref_svc.add(reference_type, dto)
        return jsonify({"id": getattr(model, "unique_code", None)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/<string:reference_type>/<string:item_id>", methods=['PATCH'])
def patch_reference(reference_type, item_id):
    payload = request.get_json()
    try:
        updated = ref_svc.update(reference_type, item_id, payload or {})
        return jsonify({"id": getattr(updated, "unique_code", None)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/<string:reference_type>/<string:item_id>", methods=['DELETE'])
def delete_reference(reference_type, item_id):
    try:
        ref_svc.delete(reference_type, item_id)
        return '', 204
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port = 8080)
