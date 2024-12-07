from app.db.models import EditableDocument


class Institution(EditableDocument):
    pass

    class Settings:
        validate_on_save = True
