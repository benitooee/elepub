# app.py
import os
from flask import Flask, render_template, send_from_directory, url_for
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

STATIC_DIR = os.path.join(app.root_path, 'static')
os.makedirs(STATIC_DIR, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')


@app.route("/analysis")
def analysis():
    pie_url = url_for('static', filename='plots/pie_chart.png')
    budget_overall_url = url_for('static', filename='plots/budget_overall.png')
    budget_person_url = url_for('static', filename='plots/budget_by_person.png')
    heatmap_url = url_for('static', filename='plots/heatmap_activity_vs_alone.png')

    return render_template(
        "analysis.html",
        pie_url=pie_url,
        budget_overall_url=budget_overall_url,
        budget_person_url=budget_person_url,
        heatmap_url=heatmap_url
    )


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(STATIC_DIR, filename)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
