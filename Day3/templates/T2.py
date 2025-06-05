from flask import Flask, render_template, request
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

app = Flask(__name__)


role_prompt = {
    "counselor": "You are a career counselor helping students choose their future.",
    "resume": "You are a resume advisor providing feedback on resume content and structure.",
    "interview": "You are an interview coach giving mock interview responses and tips."
}

@app.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    user_input = ""
    selected_role = "counselor"


    if request.method == "POST":
        selected_role = request.form.get("role")
        user_input = request.form.get("user_input")

        if user_input:
          
            model = ChatOllama(model="llama3", temperature=0.7)


            messages = [
                SystemMessage(content=role_prompt[selected_role]),
                HumanMessage(content=user_input)
            ]


            response = model.invoke(messages)
            response_text = response.content

    return render_template("index.html", response=response_text, user_input=user_input, role=selected_role)

if __name__ == "__main__":
    app.run(debug=True)

