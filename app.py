from flask import Flask, render_template, jsonify, request
from acescience import generate_response, ai_check_answer

app = Flask(__name__)

# Session data
session_data = {
    "current_question": None,
    "answer": None,
    "explanation": None,
    "asked_questions": set()
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/resources")
def resources():
    return render_template("resources.html")

@app.route("/quiz")
def quiz():
    return render_template("quiz.html")

@app.route("/ask_question", methods=["POST", "GET"])
def ask_question():
    retries = 3
    while retries > 0:
        response = generate_response("['Question', 'Answer', 'Explanation']")
        try:
            parsed_response = eval(response)
            question, answer, explanation = parsed_response
            if question in session_data["asked_questions"]:
                retries -= 1
                continue
            session_data["current_question"] = question
            session_data["answer"] = answer
            session_data["explanation"] = explanation
            session_data["asked_questions"].add(question)
            return jsonify({"question": question})
        except Exception:
            retries -= 1
    return jsonify({"error": "Failed to generate a question. Try again."})

@app.route("/check_answer", methods=["POST"])
def check_answer():
    data = request.get_json()  # Parse JSON payload
    user_answer = data.get('user_answer')
    correct_answer = session_data.get("answer", "").lower()
    result = "Correct" if user_answer == correct_answer else "Incorrect"
    return jsonify({"result": result})

@app.route("/show_explanation", methods=["POST"])
def show_explanation():
    explanation = session_data.get("explanation", "No explanation available.")
    return jsonify({"explanation": explanation})

if __name__ == "__main__":
    app.run(debug=True)