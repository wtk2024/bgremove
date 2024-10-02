from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from rembg import remove
from PIL import Image
import os

app = Flask(__name__)

# Folder to store uploaded and edited images
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files['image']

    if image.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the uploaded image
    filename = secure_filename(image.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(file_path)

    # Open the image using Pillow
    input_image = Image.open(file_path)

    # Remove background using rembg
    output_image = remove(input_image)

    # Save the output image
    output_filename = f"edited_{filename}"
    output_file_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
    with open(output_file_path, 'wb') as f:
        f.write(output_image)

    # Return the URL of the edited image
    edited_image_url = f"/static/uploads/{output_filename}"
    return jsonify({"edited_image_url": edited_image_url})

if __name__ == '__main__':
    # Bind to the PORT environment variable or use 5000 as a default
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
