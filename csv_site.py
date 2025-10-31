from flask import Flask, render_template, send_file
import pandas as pd
import matplotlib.pyplot as plt
import base64

app = Flask(__name__)

def generate_plot(csv_file):
    data = pd.read_csv(test.csv)
    data['Average Grade'] = data.mean(axis=1)
    plt.switch_backend('Agg')
    plt.figure(figsize=(10, 6))
    plt.bar(data['Name'], data['Average Grade'], color='skyblue')
    plt.xlabel('Students')
    plt.ylabel('Average Grade')
    plt.title('Average Grades of Students')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('static/average_grades.png')

@app.route('/')
def index():
    generate_plot()
    fig = 'static/average_grades.png'
    return render_template('index.html', fig=fig)

app.route('/static/<path:filename>')
def serve_static(filename):
    return send_file(f'static/{filename}')

if __name__ == '__main__':
    app.run(debug=True)