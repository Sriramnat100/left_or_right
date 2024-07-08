from flask import Flask, render_template, request, redirect, url_for, session
from backend import Opener, Chatbot

loader = Opener("questions.json")
chatter = Chatbot()

app = Flask(__name__)
app.secret_key = ''

@app.route("/")
def home():
    questions = loader.get_qs()
    return render_template("main.html", questions=questions)

@app.route("/demographics")
def demographics():
    return render_template("demographics.html")
    
@app.route("/submit_demo", methods=['POST'])
def submit_demo():
    demographics_data = {
    'age': request.form.get('age'),
    'gender': request.form.get('gender'),
    'ethnicity': request.form.get('ethnicity'),
    'education': request.form.get('education'),
    'income': request.form.get('income'),
    'occupation': request.form.get('occupation'),
    'marital_status': request.form.get('marital-status'),
    'location': request.form.get('location'),
    'religion': request.form.get('religion'),
    'voting_history': request.form.get('voting-history')
}
    
    demo_party = chatter.chat(demographics_data)
    session['demo_party'] = demo_party

    return redirect(url_for('results_demo'))
    

@app.route("/results_demo")
def results_demo():
    
    demo_party=session.get('demo_party')
    return render_template('results_demo.html', demo_party=demo_party)
    


@app.route("/submit", methods=['POST'])
def submit():
    resulting_hash = {}

    for index in range(1,21):
        resulting_hash[f"user-response-{index}"] = request.form.get(f"user-recommend-{index}")
        resulting_hash[f"user-pref-{index}"] = request.form.get(f"importance-{index}")

    
    booleans = loader.get_vals()
    analyzation = loader.analyzer(resulting_hash, booleans)
    session['analyzation'] = analyzation

    return redirect(url_for('results'))



@app.route("/results")
def results():
    analyzation = session.get('analyzation')
    return render_template('results.html', analyzation=analyzation)

if __name__ == "__main__":
    app.run(debug=True)



