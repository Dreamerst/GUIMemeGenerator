class ApiRequestError(Exception):
    def __init__(self):
        self.message = f"Ошибка запроса к API"
        super().__init__(self.message)
