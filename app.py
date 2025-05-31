from flask import Flask, redirect, url_for, session, render_template_string
from authlib.integrations.flask_client import OAuth
import os

# 환경 설정
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev_key_for_local_use")  # 로컬 테스트용 기본값

# Google OAuth 설정
app.config["GOOGLE_CLIENT_ID"] = os.getenv("GOOGLE_CLIENT_ID")
app.config["GOOGLE_CLIENT_SECRET"] = os.getenv("GOOGLE_CLIENT_SECRET")
app.config["SECRET_KEY"] = app.secret_key
app.config["SESSION_COOKIE_NAME"] = "google-login-session"
app.config["GOOGLE_DISCOVERY_URL"] = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id=app.config["GOOGLE_CLIENT_ID"],
    client_secret=app.config["GOOGLE_CLIENT_SECRET"],
    access_token_url="https://oauth2.googleapis.com/token",
    access_token_params=None,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params=None,
    api_base_url="https://www.googleapis.com/oauth2/v2/",
    userinfo_endpoint="https://www.googleapis.com/oauth2/v2/userinfo",
    client_kwargs={"scope": "openid email profile"},
)

# 홈 페이지
@app.route("/")
def index():
    user = session.get("user")
    if user:
        return render_template_string("""
            <h2>✅ 로그인 성공!</h2>
            <p>환영합니다, <strong>{{ email }}</strong>!</p>
            <a href="/logout">🚪 로그아웃</a>
        """, email=user["email"])
    return '<a href="/login">🔐 구글 로그인</a>'

# 로그인 라우트
@app.route("/login")
def login():
    redirect_uri = url_for("authorize", _external=True)
    return google.authorize_redirect(redirect_uri)

# 콜백 라우트
@app.route("/login/google/authorized")
def authorize():
    token = google.authorize_access_token()
    resp = google.get("userinfo")
    user_info = resp.json()
    session["user"] = user_info
    return redirect("/")

# 로그아웃 라우트
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

# 실행
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
