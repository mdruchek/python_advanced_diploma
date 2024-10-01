import os
from fileinput import filename

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
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        static_folder = os.path.join(current_app.instance_path ,current_app.config['UPLOAD_FOLDER'])
        user_folder = os.path.join(static_folder, api_key)
        if not os.path.exists(static_folder):
            os.makedirs(static_folder)
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
        file_path = os.path.exists(os.path.join(user_folder, filename))
        if os.path.exists(file_path):

        file_path = os.path.join(user_folder, filename)
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


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']

def rename_file(file_path):

        name, extension = file.filename.rsplit('.')
        while True:
            name += '_'
            filename = f'{name}.{extension}'
            if not os.path.exists(os.path.join(user_folder, filename)):
                break
