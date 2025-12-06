import connexion
from flask import request
from Src.Logics.logging_service import emit, logging_service
from Src.Core.observe_service import observe_service

app = connexion.FlaskApp(__name__)
log_service = logging_service()


"""
Проверить доступность REST API
"""
@app.route("/api/accessibility", methods=['GET'])
def formats():
    emit('INFO', 'API /api/accessibility called', {
        'method': request.method,
        'path': request.path,
        'body': request.get_json(silent=True)
    })
    return "SUCCESS"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port = 8080)
    emit('INFO', 'Server started')
