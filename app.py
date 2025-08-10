# app.py
from flask import Flask, render_template, request, redirect, url_for
import yaml

app = Flask(__name__)

with open('scrolls/vernon-scroll.yaml', 'r') as f:
    scroll_data = yaml.safe_load(f)['scroll']
steps = scroll_data['remedy']['steps']

@app.route('/')
def index():
    return render_template('index.html', title=scroll_data['title'], caption=scroll_data['caption'])

@app.route('/scroll/<int:step_index>', methods=['GET', 'POST'])
def scroll(step_index):
    current_step = steps[step_index] if step_index < len(steps) else None
    if request.method == 'POST':
        response = request.form.get('response')
        # Handle branching logic here
        return redirect(url_for('scroll', step_index=step_index + 1))
    return render_template('scroll.html', step=current_step, step_index=step_index)

@app.route('/complete')
def complete():
    return render_template('complete.html')

if __name__ == '__main__':
    app.run(debug=True)
