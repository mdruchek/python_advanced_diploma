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
                'error_massage': message,
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
            'error_massage': message,
        }
