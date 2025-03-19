class ApiException(Exception):
    def __init__(self, status=None, reason=None, http_resp=None):
        if http_resp:
            self.status = http_resp.status_code
            self.reason = http_resp.reason
            self.response = http_resp
            self.headers = http_resp.headers  # Store the headers
            self.body = http_resp.data()  # Store the body (or use http_resp.content for binary)
        else:
            self.status = status
            self.reason = reason
            self.response = None
            self.headers = None
            self.body = None

    def __str__(self):
        """Custom error messages for exception"""
        error_message = "({0})\nReason: {1}\n".format(self.status, self.reason)

        # Check if headers exist before including them in the message
        if self.headers:
            error_message += "HTTP response headers: {0}\n".format(self.headers)

        # Check if body exists before including it in the message
        if self.body:
            error_message += "HTTP response body: {0}\n".format(self.body)

        return error_message
