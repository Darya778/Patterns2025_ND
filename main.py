import connexion
from flask import request

app = connexion.FlaskApp(__name__)

"""
Проверить доступность REST API
"""
@app.route("/api/accessibility", methods=['GET'])
def formats():
    return "SUCCESS"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port = 8080)
