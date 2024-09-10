import os
from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from get_spec import plot_spec, get_spec

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'  # Defina o caminho correto
app.config['UPLOAD_FILENAME'] = 'actual_audio.wav'
app.config['ALLOWED_EXTENSIONS'] = {'wav'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    border_time = float(request.form['border_time'])
    start_time = float(request.form['start_time'])-border_time
    end_time = float(request.form['end_time'])+border_time

    if file and allowed_file(file.filename):
        filename = secure_filename(app.config['UPLOAD_FILENAME'])
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Gerar o espectrograma
        D = get_spec(file_path, start_time, end_time)
        output_image_path = plot_spec(D, start_time, end_time, output_folder=app.config['UPLOAD_FOLDER'])

        return send_file(output_image_path, mimetype='image/png')

    return redirect(request.url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
