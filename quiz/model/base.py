from quiz.extensions import db


class ModelMixin:
    """
    扩展model
    """
    _hide_columns = set()  # 序列化时隐藏的字段

    @property
    def columns(self):
        all_columns = {c.name for c in self.__table__.columns}
        yield from all_columns - self._hide_columns

    def __iter__(self):
        yield from ((c, getattr(self, c)) for c in self.columns)

    def __repr__(self):
        return f'<{self.__class__.__name__}>'


class Model(ModelMixin, db.Model):
    __abstract__ = True

