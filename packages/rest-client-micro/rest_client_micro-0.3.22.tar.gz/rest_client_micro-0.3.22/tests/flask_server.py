from flask import Flask, json, Response
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

companies = [{"id": 1, "name": "Company One"},
             {"id": 2, "name": "Company Two"}]

api = Flask(__name__)
auth = HTTPBasicAuth()
users = {
    "user": generate_password_hash("secretpass")
}


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


@api.route("/auth", methods=['GET'])
@auth.login_required
def index():
    return Response(f"{auth.current_user()}", status=200, mimetype='application/json')


@api.route('/200', methods=['GET'])
def get_200():
    return Response("", status=200, mimetype='application/json')


@api.route('/201', methods=['GET'])
def get_201():
    return Response("", status=201, mimetype='application/json')


@api.route('/companies', methods=['GET'])
def get_companies():
    return json.dumps(companies)


@api.route('/', methods=['GET'])
def get_index():
    return Response("", status=200, mimetype='application/json')


def run_server():
    api.run(port=3876)


if __name__ == '__main__':
    api.run(port=3876)
