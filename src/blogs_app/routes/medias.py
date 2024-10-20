import os
from datetime import datetime

from flask import Blueprint, request, current_app, jsonify, Response
from sqlalchemy.orm import Session
from werkzeug.utils import secure_filename

from blogs_app import database
from blogs_app.models import Media

bp = Blueprint('medias', __name__, url_prefix='/api/medias')

@bp.route('/', methods=('POST',))
def upload_medias() -> Response:
    """
    Ендпоинт загрузки фото
    """

    db: Session = database.get_session()
    api_key: str = request.headers.get('Api-Key')
    file = request.files['file']
    filename_full: str = secure_filename(file.filename)

    if file and allowed_file(file.filename):
        static_folder: str = os.path.join(current_app.instance_path ,current_app.config['UPLOAD_FOLDER'])
        user_folder: str = os.path.join(static_folder, api_key)

        if not os.path.exists(static_folder):
            os.makedirs(static_folder)

        if not os.path.exists(user_folder):
            os.makedirs(user_folder)

        filename_full: str = rename_file(filename_full)
        file_path: str = os.path.join(user_folder, filename_full)
        file.save(file_path)

        file_obj: Media = Media(url=os.path.join(current_app.config['UPLOAD_FOLDER'], api_key, filename_full))
        db.add(file_obj)
        db.commit()
        return jsonify(
            {
                'result': True,
                'media_id': file_obj.id
            }
        )

    return jsonify(
        {
            'result': False,
            'error_type': 'File is not supported',
            'error_massage': 'This file extension is prohibited for downloading. Only .jpeg and .jpg are allowed.',
        }
    )


def allowed_file(filename_full: str) -> bool:
    """
    Функция проверки расширения файла

    :param filename_full: имяфайла с расширением
    :type filename_full: str

    :return: является ли расширение файла допустимым
    :rtype: bool
    """

    return '.' in filename_full and filename_full.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']

def rename_file(filename_full: str) -> str:
    """
    Функция переименования загруженного файла

    :param filename_full: имя файла с расширением
    :type filename_full: str

    :return: новое имя файла
    :rtype: str
    """

    filename, extension = filename_full.split('.')
    filename = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    return f'{filename}.{extension}'
