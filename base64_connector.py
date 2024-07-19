import base64
class base64:
    def encode_to_base64(input_string):
        return base64.b64encode(input_string.encode("utf-8"))
    def decode_from_base64(input_string):
        return base64.b64decode(input_string).decode("utf-8")

