class ResponsesAPI:
    @classmethod
    def result_true(cls, additional_fields={}):
        response = {'result': True}
        response.update(additional_fields)
        return response

    @classmethod
    def error_not_found(cls, message):
        return {
                'result': False,
                'error_type': 'Not found',
                'error_massage': message,
        }

    @classmethod
    def error_forbidden(cls, message):
        return {
            'result': False,
            'error_type': 'Forbidden',
            'error_massage': message,
        }