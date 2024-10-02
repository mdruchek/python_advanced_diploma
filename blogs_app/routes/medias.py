import os
from datetime import datetime

from flask import Blueprint, request, current_app, jsonify
from werkzeug.utils import secure_filename

from blogs_app import database
from blogs_app import models


bp = Blueprint('medias', __name__, url_prefix='/api/medias')

@bp.route('/', methods=('POST',))
def upload_medias():
    db = database.get_db()
    api_key = request.headers.get('Api-Key')
    file = request.files['file']
    filename_full = secure_filename(file.filename)
    if file and allowed_file(file.filename):
        static_folder = os.path.join(current_app.instance_path ,current_app.config['UPLOAD_FOLDER'])
        user_folder = os.path.join(static_folder, api_key)
        if not os.path.exists(static_folder):
            os.makedirs(static_folder)
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
        filename_full = rename_file(filename_full)
        file_path = os.path.join(user_folder, filename_full)
        file.save(file_path)

        file_obj = models.Media(url=file_path)
        db.add(file_obj)
        db.commit()
        return jsonify(
            {
                'result': True,
                'media_id': file_obj.id
            }
        )


def allowed_file(filename_full):
    return '.' in filename_full and filename_full.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']

def rename_file(filename_full):
    filename, extension = filename_full.split('.')
    filename = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    return f'{filename}.{extension}'
