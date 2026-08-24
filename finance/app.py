import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Uygulama Yapılandırması
app = Flask(__name__)

# Özel filtre (Para birimi formatı için)
app.jinja_env.filters["usd"] = usd

# Oturum yapılandırması (Dosya sistemi kullanarak)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Veritabanı bağlantısı
db = SQL("sqlite:///finance.db")

@app.after_request
def after_request(response):
    """Yanıtların önbelleğe alınmadığından emin olun"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    """Hisse senedi portföyünü göster"""
    # Kullanıcının sahip olduğu aktif hisseleri çek
    stocks = db.execute("SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0", session["user_id"])

    # Kullanıcının nakit parasını çek
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    total_value = cash
    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["price"] = quote["price"]
        stock["value"] = stock["price"] * stock["total_shares"]
        total_value += stock["value"]

    return render_template("index.html", stocks=stocks, cash=cash, total_value=total_value)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Hisse senedi satın al"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol", 400)

        quote = lookup(symbol)
        if not quote:
            return apology("invalid symbol", 400)

        try:
            shares = int(shares)
            if shares <= 0:
                return apology("shares must be positive", 400)
        except ValueError:
            return apology("shares must be an integer", 400)

        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        total_cost = quote["price"] * shares

        if user_cash < total_cost:
            return apology("can't afford", 400)

        # Bakiyeyi güncelle ve işlemi kaydet
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   session["user_id"], quote["symbol"], shares, quote["price"])

        flash("Bought!")
        return redirect("/")
    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """İşlem geçmişini göster"""
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ? ORDER BY transacted DESC", session["user_id"])
    return render_template("history.html", transactions=transactions)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Kullanıcı girişi"""
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Kullanıcı çıkışı"""
    session.clear()
    return redirect("/")

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Hisse senedi fiyatını sorgula"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol", 400)

        quote = lookup(symbol)

        if not quote:
            return apology("invalid symbol", 400)

        # Sonucu göstermek için quoted.html şablonunu kullan
        return render_template("quoted.html", quote=quote)
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Yeni kullanıcı kaydı"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username", 400)
        elif not password or not confirmation:
            return apology("must provide password", 400)
        elif password != confirmation:
            return apology("passwords do not match", 400)

        hash = generate_password_hash(password)
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        except:
            return apology("username already exists", 400)

        # Kayıt sonrası otomatik giriş yap
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Hisse senedi sat"""
    stocks = db.execute("SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares_input = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol", 400)
        if not shares_input:
            return apology("must provide shares", 400)

        shares = int(shares_input)
        user_shares_row = db.execute("SELECT SUM(shares) as total FROM transactions WHERE user_id = ? AND symbol = ?",
                                     session["user_id"], symbol)
        user_shares = user_shares_row[0]["total"] if user_shares_row else 0

        if shares > user_shares:
            return apology("too many shares", 400)

        quote = lookup(symbol)
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", (quote["price"] * shares), session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   session["user_id"], symbol, -shares, quote["price"])

        flash("Sold!")
        return redirect("/")
    else:
        return render_template("sell.html", stocks=stocks)
