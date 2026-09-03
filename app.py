from flask import Flask, request, session, redirect
import secrets
import random

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)


@app.route("/")
def roulette():
    user_guess = request.args.get("guess")
    user_bet = request.args.get("bet")
    bet_type = request.args.get("bet_type")

    if "balance" not in session:
        session["balance"] = 1000
    if "total_lost" not in session:
        session["total_lost"] = 0
    if "total_balance" not in session:
        session["total_balance"] = 10000
    balance = session["balance"]
    total_lost = session["total_lost"]
    total_balance = session["total_balance"]

    if total_balance<=0:
        session["lose"]=True
        return redirect("/lose")
    if balance <= 0:
        return f"""
    <style>
    body {{
            background-color: black;
            color: red;
            text-align: center;
            font-family: Sans-serif;
        }}
    h1 {{
            font-family: atop-font;
            padding: 5px;
            font-size: 40px;
    }}
    h2 {{
            font-family: atop-font;
            padding: 10px;
            font-size: 40px;
    }}
    </style>
    <meta http-equiv="refresh" content="5;url=/reset">
    <h1>TAKE 1000 MORE DOLLARS FROM YOUR BANK ACCOUNT</h1>
    <h2>SO FAR, YOU'VE LOST {total_lost}$ TO GAMBLING!</h2>
    <h3>Current money in your bank account: {total_balance}$</h3>
    """

    if bet_type == "number" and user_guess is None:
        result = "Please enter a number sir"
    elif not user_bet:
        result = "<h2>Please enter a bet sir</h2>"
    else:
        try:
            user_bet = int(user_bet)
        except (ValueError, TypeError):
            user_bet = -1

        if bet_type == "number":
            try:
                user_guess = int(user_guess)
            except (ValueError, TypeError):
                user_guess = -1

        if user_bet > balance:
            result = "<h1>You're just a dirty hacker, aren't you?-sans</h1>"
            balance -= balance
        elif user_bet < 0:
            result = "<h1>Yeah, get out of here-sans</h1>"
            balance -= balance
        elif bet_type == "number" and (user_guess is None or user_guess < 0 or user_guess > 36):
            result = "<h1>You didn't do anything at all, did you?-sans</h1>"
            balance -= 0.25 * balance
        else:
            roulette_number = random.randint(0, 36)

            red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
            black_numbers = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]

            if roulette_number == 0:
                color = "GREEN"
            elif roulette_number in red_numbers:
                color = "RED"
            else:
                color = "BLACK"

            if bet_type == "number":
                won = roulette_number == user_guess
                payout = 35
            elif bet_type == "red":
                won = roulette_number in red_numbers
                payout = 1
            elif bet_type == "black":
                won = roulette_number in black_numbers
                payout = 1
            elif bet_type == "green":
                won = roulette_number == 0
                payout = 35
            elif bet_type == "high":
                won = 19 <= roulette_number <= 36
                payout = 1
            elif bet_type == "low":
                won = 1 <= roulette_number <= 18
                payout = 1
            else:
                payout = 0
                won = False

            if won:
                result = "<h1>YOU WON</h1>"
                balance += payout * user_bet
                session["total_lost"] -= user_bet
                session["total_balance"] += user_bet
            else:
                result = "<h2>YOU LOST</h2>"
                balance -= user_bet
                session["total_lost"] += user_bet
                session["total_balance"] -= user_bet

            result += f"""
                 <h1>Bet type: {bet_type}</h1>
                 <h1>Your number: {user_guess}</h1>
                 <h1>Number rolled: {roulette_number}</h1>
                 <h1>Color: {color}</h1>
                 """

            session["balance"] = balance

    return f"""
    <head>
        <link rel="icon" type="image/png" href="/static/favicon.png">
    </head>
    <style>
        body {{
            background-color: black;
            color: red;
            text-align: center;
            font-family: Sans-serif;
        }}
        h1 {{
            font-size: 50px;
            font-family: atop-font;
        }}
        h2 {{
            font-size: 40px;
            font-family: "Courier New";
        }}
        button {{
            background-color: Black;
            color: white;
            border-radius: 10px;
            padding: 15px 15px;
            font-size: 13px;
            transition: 0.75s;
            border: 2px solid black;
            box-shadow: 0 0 15px red;
            font-family: Trebuchet MS;
        }}
        button:hover {{
            background-color: red;
            color: white;
            transform: scale(1.2);
            box-shadow: 0 0 15px white;
            border: 2px solid black;
        }}
        select {{
            background-color: Red;
            color: black;
            border-radius: 10px;
            padding: 15px 15px;
            font-size: 13px;
            transition: 0.75s;
            border: 2px solid black;
            box-shadow: 0 0 15px red;
            font-family: Trebuchet MS;
        }}
        select:hover {{
            background-color: red;
            color: white;
            transform: scale(1.2);
            box-shadow: 0 0 15px white;
            border: 2px solid black;
            cursor: pointer;
        }}
        select:focus {{
            box-shadow: 0 0 30px red;
        }}
    </style>

    <h1>ROULETTE</h1>
    <h2>Balance: {balance}$</h2>

    <form action="/" method="get">
        <h2>Bet Type</h2>
        <select name="bet_type">
            <option value="number">Number</option>
            <option value="red">Red</option>
            <option value="black">Black</option>
            <option value="green">Green</option>
            <option value="high">High</option>
            <option value="low">Low</option>
        </select>

        <br><br>
        <h2>Pick a number</h2>
        <input type="number" name="guess" min="0" max="36">

        <br><br>
        <h2>Bet an amount of money</h2>
        <label for="bet">Bet: $<span id="betValue">100</span></label>
        <input type="range" id="bet" name="bet" min="1" max="{max(1, int(balance))}" value="100" oninput="document.getElementById('betValue').textContent=this.value">

        <br><br>
        <button type="submit">ROLL</button>
    </form>

    {result}
    """


@app.route("/reset")
def reset():
    session["total_balance"] = 10000
    session["total_lost"] = 0
    session["balance"] = 1000
    session["lose"] = False
    return redirect("/")


@app.route("/no_money")
def no_money():
    session["balance"] = 0
    return redirect("/")

@app.route("/double")
def double():
    session["balance"] *= 2
    return redirect("/")


@app.route("/half")
def half():
    session["balance"] /= 2
    return redirect("/")


@app.route("/bankrupt")
def bankrupt():
    session["balance"] = 0
    return redirect("/")


@app.route("/goat")
def goat():
    return """
    <img src="/static/goat.png" style="width: 100%; height: auto;">
    """


@app.route("/ypdamin", methods=["GET", "POST"])
def ypdamin():
    if "failed_attempts" not in session:
        session["failed_attempts"] = 0

    if request.method == "POST":
        code = request.form.get("code")

        if code == "152014":
            session["admin"] = True
            session["failed_attempts"] = 0
            return redirect("/admin")
        else:
            session["failed_attempts"] += 1

            if session["failed_attempts"] >= 5:
                return redirect("/goat")

            return redirect("/ypdamin")

    return """
    <style>
    body {
            background-color: black;
            color: red;
            text-align: center;
            font-family: Sans-serif;
        }
            
    
    h1 {
            font-family: atop-font;
            padding: 15px;
    }
    h2 {
            font-family: atop-font;
            padding: 10px;
    }
    </style>
    <form method="post">
        <input type="password" name="code">
        <button type="submit" name="submit">ENTER</button>
    </form>
    """


@app.route("/admin")
def admin():
    if not session.get("admin"):
        return "STOP HACKING", 403

    return """
    <h1>ADMIN PANEL</h1>
    <p>I don't know how you made it here, but it's a work in progress.</p>
    """


@app.route("/sans")
def sans():
    return """
    <style>
    body {
            background-color: black;
            color: red;
            text-align: center;
            font-family: Sans-serif;
        }
            
    
    h1 {
            font-family: atop-font;
            padding: 15px;
    }
    h2 {
            font-family: atop-font;
            padding: 10px;
    }
    </style>
    <p>It's a beautiful day outside. Birds are singing, flowers are blooming... On days like these, kids like you... Should be burning in hell.</p>
    """
@app.route("/lose")
def lose():
    if not session.get("lose"):
        return "STOP TRYING TO LOSE", 403
    return """
    <style>
    body {
            background-color: black;
            color: red;
            text-align: center;
            font-family: Sans-serif;
        }
            
    
    h1 {
            font-family: atop-font;
            padding: 15px;
    }
    h2 {
            font-family: atop-font;
            padding: 10px;
    }
    </style>
            
    
    <h1>YOU LOST</h1>
    <a
    href="/reset"><h2>You happen to get 11,000 more dollars in the mail from a mysterious person, and decide to go to the casino to play roulette</h2>
    </a>
    """
    
@app.route("/emu")
def emu():
    return """
    <img src="/static/emu.png" style="width: 100%; height: auto;">
    """

@app.route("/lottery")
def lottery():    
    roulette_number=random.randint(0,100)
    payout=100000
    if "balance" not in session:
        session["balance"]=1000
    elif "total_lost" not in session:
        session["total_lost"] = 0
    
    session["balance"]=balance
    
    elif roulette_number==0:
        session["balance"] += payout
        result="<h1>YOU WON THE LOTTERY!!!</h1>"
    else:
        session["balance"]=0
        session["total_lost"]=balance
        result= """
        <h1>YOU LOST</h1>
        <h5>YOU ALSO LOST ALL OF YOUR MONEY</h5>
        """
    return f"""
    <style>
    body {{
            background-color: black;
            color: red;
            text-align: center;
            font-family: Sans-serif;
        }}
            
    
    h1 {{
            font-family: atop-font;
            padding: 15px;
            text-size: 50px;
    }}
    h2 {{
            font-family: atop-font;
            padding: 10px;
    }}
    </style>
    {result}
    <button
        onclick="location.href='/'">PRESS TO GO BACK TO HOME PAGE
    </button>
    """   

@app.route("/random_money")
def random_money():     
     if "balance" not in session:
         session["balance"]=1000    
     session["balance"]=random.randint(0,5000)
     return redirect("/")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
