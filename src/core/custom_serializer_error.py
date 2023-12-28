""" Custom Serializers Errors """


class SerializerErrorParser:
    """
    SerializerErrorParser : Serializer error Parser Class Used to split the serializer errors in 
    two parts key and Values, key define the error of key and value define what is the
    error in this Key.
    # {'email': ['Enter a valid e-mail address.'], 'created': ['This field is required.']}
    """

    def __init__(self, un_error_message):
        self.error_message = un_error_message

    def __call__(self):
        return self.serializer_error_parser()

    def serializer_error_parser(self):
        """
        manipulate the serializer error for api response
        return: key and error
        """
        try:
            # manipulate serializer error
            if isinstance(self.error_message, dict):
                error_keys = list(self.error_message.keys())
                if len(error_keys) > 0:
                    return error_keys[0], self.error_message[error_keys[0]][0]
                return None, None

            if isinstance(self.error_message, list):
                error_list = list(filter(lambda x: list(x.keys()), self.error_message))
                if error_list:
                    error_parse = error_list[0]
                    error_keys = list(error_parse.keys())
                    if len(error_keys) > 0:
                        return error_keys[0], error_parse[error_keys[0]][0]
                    return None, None

        except Exception as exception_error:
            print(exception_error)
            return None, None
