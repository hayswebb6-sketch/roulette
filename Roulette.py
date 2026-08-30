from flask import Flask, request, session, redirect
import secrets
import random


app=Flask(__name__)
app.secret_key=secrets.token_hex(32)


@app.route("/")
def roulette():
    user_guess=request.args.get("guess")
    user_bet=request.args.get("bet")
    
    if "balance" not in session:                          
        session["balance"]=1000
        
    
    balance=session["balance"]
    
    if not user_guess:
        result=""
 
    elif not user_bet:
        result="<h2>Please enter a bet sir</h2>"
        
    else:
        user_guess=int(user_guess)
        user_bet=int(user_bet)
            
        if user_guess < 0 or user_guess > 36:
            result="<h1>You didn't do anything at all, did you?-sans</h1>"
            balance-=0.25*balance
            
        elif user_bet>balance:
            result="<h1>You're just a dirty hacker, aren't you?-sans</h1>"
            balance-=balance
           
        elif user_bet<0:
            result="<h1>Yeah, get outta here-sans</h1>"
            balance-=balance
            
        else:
            roulette_number=random.randint(0,36)
        
            if roulette_number==user_guess:
                result="<h1>YOU WON</h1>"
                balance += 35 * user_bet
            else:
                result="<h2>YOU LOST</h2>"
                balance-=user_bet
            result += f""" 
                 <h1>Your number:{user_guess}</h1>
                 <h1>Number rolled: {roulette_number}</h1>
                 """
            session["balance"]=balance    
    return  f"""
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
     </style>
     
     <h1>ROULETTE</h1>
     
     <h2>Balance: {balance}$</h2>
    
     
     <form action="/" method="get">
         <h2>Pick a number</h2>
         
         <input type="number" name="guess" min="0" max="36">
         
         
         <br><br>
         
         <h2>Bet an amount of money</h2>
         
         <label for="bet">Bet: $<span id="betValue">100</span></label>
            
         <input
         
         type="range"
         
         id="bet"
         
         name="bet"
         
         min="1"
         
         max={balance}
         
         value="100"
         
         oninput="document.getElementById( 'betValue' ).textContent=this.value"
         
         >
         <br><br>
         
         <button type="submit">ROLL</button>
    </form>
     
     
    {result} 
    """
  
@app.route("/reset")
def reset():
    session["balance"]=1000
    return redirect("/")

@app.route("/no_money")
def no_money():
    session ["balance"]=0
    return redirect("/")

@app.route("/jackpot")
def jackpot():
    session["balance"]=100000000
    return redirect("/")

@app.route("/double")
def double():
    session["balance"]*=2
    return redirect("/")
    
@app.route("/half")
def half():
    session["balance"]/=2
    return redirect("/")

@app.route("/bankrupt")
def bankrupt():
    session ["balance"]=0
    return redirect("/")

@app.route("/goat")
def goat():
    return """
<img src="/static/goat.png" style="width: 100%; height: auto;">
"""
@app.route("/ypdamin", methods=["GET","POST"])
def ypdamin():
    if "failed_attempts" not in session:
        session["failed_attempts"] = 0
        
        
    
    if request.method=="POST":
        code=request.form.get("code")
        
        if code  == "152014":
            session["admin"]=True
            session["failed_attempts"] = 0
            return redirect("/admin")
        
            """
            <h1>ADMIN PANEL</h1>
            <h5>dirbpy -u http://127.0.0.1:5001 -f routes.txt --no-duplicate</h5>
            <h5>ngrok http 5001</h5>
            """
        else:
            session["failed_attempts"] += 1
                
            if session["failed_attempts"]>=5:
                return redirect ("/goat")
             
            return redirect("/ypdamin")
            
        return "<h1> Wrong Code</h1>"
    
    return """
    <form method="post">
    <input type="password" name="code">
    <button type="submit"  name="submit">ENTER</button>
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
    <p>It's a beautiful day outside. Birds are singing, flowers are blooming... On days like these, kids like you... Should be burning in hell.</p>
    """
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

