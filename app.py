from flask import Flask, render_template, request, jsonify, redirect, session
import os
from supabase import create_client, Client
from flask_cors import CORS
from supabase_auth.errors import AuthApiError
app = Flask(__name__)
CORS(app)
app.secret_key = "supersecretkey"
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpyeGx0bGV0YWp0eXFsdHpjc3ByIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzcyODE5MiwiZXhwIjoyMDkzMzA0MTkyfQ.ntWyrb5jlOiReeXSofLkEsZCtnf6HigRt_CXbLFKB80"
url = "https://jrxltletajtyqltzcspr.supabase.co"
database = create_client(url, api_key)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/<path:file_path>")
def show_page(file_path):
    return render_template(f"{file_path}")
    
@app.route("/api/score<int:num>", methods = ["POST"])
def score_quiz(num):
    extra = int(num)
    result = request.get_json()
    correct_answers = []
    user_answers = result.get("answers", [])
    quiz = result.get("quiz_id", 1)
    
    correct = 0 
    norm = extra < 90
    bound = extra + 10 if extra < 90 else extra + 6
    
    for i in range(extra, bound):
        data = database.table("Quiz_answers").select("*").eq('id', i).execute()
        correct_answer = data.data[0]["correct_ans"]
        if correct_answer == user_answers[data.data[0]["quest_num"]-1]:
            correct += 1
        correct_answers.append(correct_answer)
    
    return jsonify({"score": correct, "correct_answers": correct_answers})

@app.route("/render_login")
def render_login():
    return render_template("SignIn.html")

@app.route("/sign", methods = ["POST"])
def sign_up():
    creds = request.get_json()
    email = creds["email"]
    password = creds["password"]
    try:
        result = database.auth.sign_up({"email": email, "password": password})
        return jsonify({"error": None})
    except Exception as e:
        return jsonify({"error": "Sign Up Failed", "exc": str(e)})

    # if result.user:
    #     database.table("User_data").insert({
    #         "user_id": result.user.email,
    #         "q1": None,
    #         "q2": None,
    #         "q3": None,
    #         "q4": None,
    #         "q5": None,
    #         "q6": None,
    #         "q7": None,
    #         "q8": None,
    #         "q9": None,
    #         "q10": None,
    #         "q11": None
    #         }).execute()
    #     return redirect("/render_login")
    # else:
    #     return {"error": "Signup failed"}, 400
    

@app.route("/login", methods=["POST"])
def login():
    creds = request.get_json()
    
    if not creds:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    email = creds.get("email")
    password = creds.get("password")

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    try:
        result = database.auth.sign_in_with_password({"email": email, "password": password})
        return jsonify({"error": None}), 200

    except AuthApiError as auth_err:
        return jsonify({"error": "Error: Incorrect Credentials", "exc": str(auth_err)}), 401

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "exc": str(e)}), 500
    
    # if result.user:
    #     session['user'] = result.user.email

    #     # Check if user data exists
    #     curr = database.table("User_data").select("*").eq("user_id", session['user']).execute()
    #     if not curr.data or len(curr.data) == 0:
    #         database.table("User_data").insert([{
    #            "user_id": session['user'],
    #             "q1": None,
    #             "q2": None,
    #             "q3": None,
    #             "q4": None,
    #             "q5": None,
    #             "q6": None,
    #             "q7": None,
    #             "q8": None,
    #             "q9": None,
    #             "q10": None,
    #             "q11": None
    #         }]).execute()
            

    

@app.route("/logout", methods = ["POST"])
def logout():
    session.clear()
    return redirect("/render_login")

if __name__ ==  "__main__":
    app.run(debug=True)