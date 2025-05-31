from flask import Flask, redirect, url_for, session
from flask_dance.contrib.google import make_google_blueprint, google
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecret")

# 🔑 Google OAuth 설정
app.config["OAUTHLIB_INSECURE_TRANSPORT"] = True  # 로컬 테스트용
google_bp = make_google_blueprint(
    client_id=os.environ.get("GOOGLE_OAUTH_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET"),
    redirect_to="welcome"
)
app.register_blueprint(google_bp, url_prefix="/login")

# 🔐 로그인 후 이동할 라우트
@app.route("/welcome")
def welcome():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v1/userinfo")
    user_info = resp.json()
    return f"안녕하세요, {user_info['email']} 님!"

# 홈 라우트
@app.route("/")
def index():
    return '<a href="/login/google">구글로 로그인</a>'

if __name__ == "__main__":
    app.run(debug=True)
