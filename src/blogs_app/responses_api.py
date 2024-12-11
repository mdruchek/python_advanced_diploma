"""Ответы API."""


class ResponsesAPI:
    """Класс ответов API веб приложения.

    Methods:
        result_true: успешный результат
        error_not_found: ошибка 'объект не найден'
        error_user_not_found: ошибка 'пользователь с данным api_key не найден'
        error_forbidden: ошибка 'доступ запрещён'
    """

    @classmethod
    def result_true(cls, additional_fields: set = set) -> dict:
        """Ответ 'Успешный результат'.

        Parameters:
            additional_fields: дополнительные поля для включения в возвращаемый словарь

        Returns:
            Ответ
        """
        response = {'result': True}
        response.update(additional_fields)
        return response

    @classmethod
    def error_not_found(cls, message):
        """Ответ 'Ошибка, объект не найден'.

        Parameters:
            message: поясняющее сообщение

        Returns:
            Ответ
        """
        return {
            'result': False,
            'error_type': 'Not found',
            'error_message': message,
        }

    @classmethod
    def error_user_not_found(cls, api_key: str) -> dict:
        """Ответ 'Ошибка, пользователь с данным api_key не найден'.

        Parameters:
            api_key: api_key пользователя

        Returns:
            Ответ
        """
        return {
            'result': False,
            'error_type': 'Not found',
            'error_message': 'Access is denied. User with api-key {api_key} not found'.format(api_key=api_key),
        }

    @classmethod
    def error_forbidden(cls, message: str) -> dict:
        """Ответ 'Ошибка, доступ запрещён'.

        Parameters:
            message: поясняющее сообщение

        Returns:
            Ответ
        """
        return {
            'result': False,
            'error_type': 'Forbidden',
            'error_message': message,
        }
