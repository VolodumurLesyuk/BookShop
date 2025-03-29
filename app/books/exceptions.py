from fastapi import HTTPException, status

class BookAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Книга з таким заголовком уже існує."
        )

class FileParseException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не вдалося розпарсити файл. Перевірте формат або дані."
        )