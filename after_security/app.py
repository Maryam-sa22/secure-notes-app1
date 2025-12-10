from flask import Flask, render_template, request, redirect, url_for, session
from security import hash_password, verify_password

app = Flask(__name__)
# Stronger secret key (should be environment variable in real apps)
app.secret_key = "use-a-strong-random-secret-key-here-123456789"

# User with hashed password
USER = {
    "username": "admin",
    "password": hash_password("123456")
}

notes = []


@app.after_request
def add_security_headers(response):
    # Basic security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response


@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            error = "Username and password are required."
        elif username == USER["username"] and verify_password(USER["password"], password):
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password"

    return render_template("login.html", error=error)


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    global notes

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if title and content:
            notes.append({"title": title, "content": content})

    return render_template("dashboard.html", notes=notes, user=session["user"])


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
