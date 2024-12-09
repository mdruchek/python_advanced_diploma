class ResponsesAPI:
    """
    Класс ответов API веб приложения

    Methods:
        result_true: успешный результат
        error_not_found: ошибка 'объект не найден'
        error_forbidden: ошибка 'доступ запрещён'
    """

    @classmethod
    def result_true(cls, additional_fields={}):
        """
        Отвут 'Успешный результат'

        :param additional_fields: дополнительные поля для включения в возвращаемый словарь
        :type additional_fields: dict

        :return response: ответ
        :rtype response: dict
        """

        response = {'result': True}
        response.update(additional_fields)
        return response

    @classmethod
    def error_not_found(cls, message):
        """
        Ответ 'Ошибка, объект не найден'

        :param message: поясняющее сообщение
        :type message: str

        :return: ответ
        :rtype: dict
        """

        return {
                'result': False,
                'error_type': 'Not found',
                'error_message': message,
        }

    @classmethod
    def error_user_not_found(cls, api_key):
        """
        Ответ 'Ошибка, пользователь с данным api_key не найден'

        :param api_key: api_key пользователя
        :type api_key: str

        :return: ответ
        :rtype: dict
        """

        return {
                'result': False,
                'error_type': 'Not found',
                'error_message': 'Access is denied. User with api-key {api_key} not found'.format(api_key=api_key),
        }

    @classmethod
    def error_forbidden(cls, message):
        """
        Ответ 'Ошибка, доступ запрещён'

        :param message: поясняющее сообщение
        :type message: str

        :return: ответ
        :rtype: dict
        """

        return {
            'result': False,
            'error_type': 'Forbidden',
            'error_message': message,
        }
