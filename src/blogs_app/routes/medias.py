"""Модуль загрузки медиа."""

import os
from datetime import datetime
from typing import Optional

from flask import Blueprint, Response, current_app, jsonify, request
from sqlalchemy import select
from sqlalchemy.orm import Session
from werkzeug.utils import secure_filename

from blogs_app import database
from blogs_app.models import Media, User
from blogs_app.responses_api import ResponsesAPI

bp = Blueprint('medias', __name__, url_prefix='/api/medias')


@bp.route('/', methods=('POST',))
def upload_medias() -> tuple[Response, int]:
    """Ендпоинт загрузки фото.

    Returns:
        HTTP ответ и HTTP статус

    ---
    tags:
        - medias

    parameters:
        - in: header
          name: Api-Key
          required: true

    requestBody:
        content:
            image/jpeg:
                schema:
                    type: string
                    format: binary

    responses:
        201:
            description: Фото загружено
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            result:
                                type: boolean
                                example: True
                            media_id:
                                type: integer
        403:
            description: Пользователь с данным api-key не найден или
                пользователь пытается удалить подписку на самого себя
            content:
                application/json:
                    schema:
                        properties:
                            result:
                                type: boolean
                                example: False
                            error_type:
                                type: string
                                example: Forbidden
                            error_message:
                                type: string
                                example: error_message
        415:
            description: Формат медиафайла не поддерживается
            content:
                application/json:
                    schema:
                        properties:
                            result:
                                type: boolean
                                example: False
                            error_type:
                                type: string
                                example: File is not supported
                            error_message:
                                type: string
                                example: This file extension is prohibited for downloading.
                                    Only .jpeg and .jpg are allowed.
    """
    db: Session = database.get_session()
    api_key: str = request.headers.get('Api-Key')

    user: Optional[User] = (
        db.execute(
            select(User).
            where(User.api_key == api_key),
        ).
        scalar()
    )

    if not user:
        return jsonify(
            ResponsesAPI.error_forbidden(
                'Access is denied. User with api-key {api_key} not found'.format(api_key=api_key),
            ),
        ), 403

    photo = request.files['file']
    filename_full: str = secure_filename(photo.filename)

    if photo and allowed_file(photo.filename):
        static_folder: str = os.path.join(current_app.instance_path, current_app.config['UPLOAD_FOLDER'])
        user_folder: str = os.path.join(static_folder, api_key)

        if not os.path.exists(static_folder):
            os.makedirs(static_folder)

        if not os.path.exists(user_folder):
            os.makedirs(user_folder)

        filename_full: str = rename_file(filename_full)
        file_path: str = os.path.join(user_folder, filename_full)
        photo.save(file_path)

        file_obj: Media = Media(
            url=os.path.join(
                current_app.config['UPLOAD_FOLDER'],
                api_key,
                filename_full,
            ),
        )

        db.add(file_obj)
        db.commit()
        return jsonify(
            {
                'result': True,
                'media_id': file_obj.id,
            },
        ), 201

    return jsonify(
        {
            'result': False,
            'error_type': 'File is not supported',
            'error_massage': 'This file extension is prohibited for downloading. Only .jpeg and .jpg are allowed.',
        },
    ), 415


def allowed_file(filename_full: str) -> bool:
    """
    Функция проверки расширения файла.

    Parameters:
        filename_full: имя файла с расширением

    Returns:
        Является ли расширение файла допустимым
    """
    file_extension = filename_full.rsplit('.', 1)[1]
    return '.' in filename_full and file_extension in current_app.config['ALLOWED_EXTENSIONS']


def rename_file(filename_full: str) -> str:
    """
    Функция переименования загруженного файла.

    Parameters:
        filename_full: имя файла с расширением

    Returns:
        Новое имя файла
    """
    filename, extension = filename_full.split('.')
    filename = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    return '{filename}.{extension}'.format(filename=filename, extension=extension)
