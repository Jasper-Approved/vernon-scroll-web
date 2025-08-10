# app.py
from flask import Flask, render_template, request, redirect, url_for, session
import yaml

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Required for session handling

def load_scroll():
    with open('scrolls/vernon-scroll.yaml', 'r') as f:
        return yaml.safe_load(f)['scroll']

@app.route('/')
def index():
    scroll = load_scroll()
    return render_template('index.html', title=scroll['title'], caption=scroll['caption'])

@app.route('/step', methods=['GET', 'POST'])
def step():
    scroll = load_scroll()
    main_steps = scroll['remedy']['steps']
    branch_steps = session.get('branch_steps')
    lineage = session.get('lineage', [])
    index = session.get('step_index', 0)

    steps = branch_steps if branch_steps else main_steps

    if request.method == 'POST':
        response = request.form.get('response')
        question = request.form.get('question')

        if response and question:
            lineage.append(f"Q: {question} → {response.capitalize()}")
            session['lineage'] = lineage

            current_step = steps[index]
            branch_key = f"if_{response}"
            if branch_key in current_step:
                session['branch_steps'] = current_step[branch_key]
                session['step_index'] = 0
                session['main_index'] = index + 1
                return redirect(url_for('step'))

        index += 1
        session['step_index'] = index

        if branch_steps and index >= len(branch_steps):
            session['branch_steps'] = None
            index = session.get('main_index', 0)
            session['step_index'] = index

        return redirect(url_for('step'))

    if index < len(steps):
        current_step = steps[index]
        return render_template('step.html', step=current_step, index=index, lineage=lineage)
    else:
        return redirect(url_for('complete'))

@app.route('/complete')
def complete():
    lineage = session.get('lineage', [])
    return render_template('complete.html', lineage=lineage)

if __name__ == '__main__':
    app.run(debug=True)

