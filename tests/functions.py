def checking_by_api_error_type(json_data, error_type: str, error_message):
    assert json_data['result'] is False
    assert json_data['error_type'] == error_type
    assert json_data['error_message'] == error_message