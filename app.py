import os
import socket

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify(
        message="NCP Developer Tools 배포 연습용 Flask 앱 - 파이프라인 자동 배포 테스트",
        version=os.environ.get("APP_VERSION", "v1"),
        code_revision="v3-canary-test",
        hostname=socket.gethostname(),
    )


@app.route("/healthz")
def healthz():
    return "ok", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
