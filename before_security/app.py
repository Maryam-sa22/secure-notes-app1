from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "demo-key-without-security"

notes = []

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        # VERSION 1 - NO SECURITY
        # يدخل مباشرة بدون تحقق
        session["user"] = username if username else "Guest"
        return redirect(url_for("dashboard"))

    return render_template("login.html")  # نفس التصميم

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
