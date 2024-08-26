from flask import Flask, request
from flask_cors import CORS
import json

import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

from modules.test import test

@app.route("/api/test", methods=["GET"])
def api_get_test():
    print("Handling get test...")
    return test()


def main():
    print("Starting backend...")


if __name__ == "__main__":
    flask.run(app, debug=True, port=5000)
