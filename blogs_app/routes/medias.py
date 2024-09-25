import os

from flask import Blueprint, request, current_app, jsonify
from werkzeug.utils import secure_filename

from blogs_app import database
from blogs_app import models


bp = Blueprint('medias', __name__, url_prefix='/api/medias')

@bp.route('/', methods=('POST',))
def upload_medias():
    db = database.get_db()
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_url = os.path.join(current_app.instance_path ,current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_url)

        file_obj = models.Media(url=file_url)
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
