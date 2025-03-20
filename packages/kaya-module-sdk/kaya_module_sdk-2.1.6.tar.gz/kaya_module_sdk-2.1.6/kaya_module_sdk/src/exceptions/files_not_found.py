class FilesNotFoundException(Exception):
    message: str
    error_code: int

    def __init__(self, msg: str, err_code: int = 4):
        super().__init__(msg)
        self.message = msg
        self.error_code = err_code

    def __str__(self):
        return f"Error {self.error_code}: {self.message}"
