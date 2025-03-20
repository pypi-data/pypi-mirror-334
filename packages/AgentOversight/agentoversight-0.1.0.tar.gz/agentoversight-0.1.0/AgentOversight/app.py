from flask import Flask, render_template, request
from AgentOversight.agent_logic import AgentOversight

app = Flask(__name__)

oversight = AgentOversight(
    openai_api_key="your-openai-key",
    deepseek_api_key="your-deepseek-key",
    grok_api_key="your-grok-key"
)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        model_name = request.form["model"]
        input_text = request.form["input"]
        rules_input = request.form["rules"]
        auto_correct = request.form.get("auto_correct") == "on"
        
        oversight.set_rules(rules_input)
        result = oversight.process_input(model_name, input_text, auto_correct=auto_correct)

        return render_template("index.html", 
                              model=model_name,
                              input=input_text,
                              rules=rules_input,
                              auto_correct=auto_correct,
                              **result)
    return render_template("index.html")

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()