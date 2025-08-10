# app.py
from flask import Flask, render_template, request, redirect, url_for, session
import yaml
import os

app = Flask(__name__, template_folder='templates')
app.secret_key = 'vernon-scroll-secret'  # 🕯️ Required for session handling

# 📜 Load scroll from YAML
def load_scroll(path='scrolls/vernon-scroll.yaml'):
    if not os.path.exists(path):
        raise FileNotFoundError(f"🕯️ Scroll not found at: {path}")
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
        if 'scroll' not in data:
            raise KeyError("📜 Jiinga’s scroll lacks a 'scroll' key. Check the YAML structure.")
        return data['scroll']

# 🏠 Home route
@app.route('/')
def index():
    try:
        scroll = load_scroll()
    except Exception as e:
        return f"⚠️ Scroll loading error: {e}", 500

    session['lineage'] = []
    session['step_index'] = 0
    session['branch_steps'] = None
    session['main_index'] = 0

    debug = request.args.get('debug')
    if debug:
        print("🧪 Debug mode active")
        print(f"Starting scroll at index {session['step_index']}")
        print("Lineage:", session['lineage'])

    return render_template('index.html', title=scroll_data['title'], caption=scroll_data['caption'])

# 🧭 Step route
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

       if response:
    current_step = steps[index]

    # Handle branching response
    if question:
        lineage.append(f"Q: {question} → {response.capitalize()}")
        session['lineage'] = lineage

        branch_key = f"if_{response}"
        if branch_key in current_step:
            session['branch_steps'] = current_step[branch_key]
            session['step_index'] = 0
            session['main_index'] = index + 1
            return redirect(url_for('step'))

    # Handle non-branching "next"
    index += 1
    session['step_index'] = index

    if branch_steps and index >= len(branch_steps):
        session['branch_steps'] = None
        index = session.get('main_index', 0)
        session['step_index'] = index

    return redirect(url_for('step'))

        index += 1
        session['step_index'] = index

        if branch_steps and index >= len(branch_steps):
            session['branch_steps'] = None
            index = session.get('main_index', 0)
            session['step_index'] = index

        return redirect(url_for('step'))

    if not branch_steps:
        session['main_index'] = index

    if index < len(steps):
        current_step = steps[index]
        return render_template('scroll.html', step=current_step, index=index, lineage=lineage)
    else:
        return redirect(url_for('complete'))

# 🏁 Completion route
@app.route('/complete')
def complete():
    lineage = session.get('lineage', [])
    return render_template('complete.html', lineage=lineage)

# 🧬 Lineage route
@app.route('/lineage')
def lineage_view():
    lineage = session.get('lineage', [])
    return render_template('lineage.html', lineage=lineage)

# 🔄 Reset route
@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

# 🚀 Run ritual
if __name__ == '__main__':
    app.run(debug=True)


