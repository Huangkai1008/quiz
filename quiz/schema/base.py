from jsonschema import Draft4Validator, draft4_format_checker

from quiz.exceptions import ValidateException


class Schema:
    _schema = None

    def __init__(self, instance):
        """
        schema / instance
        先验证instance符合schema, 再去做instance的入库等操作
        """
        self.instance = instance

    @property
    def schema(self):
        return self.schema

    def validate(self):
        """验证实例 validate the instance with the schema"""
        _validator = Draft4Validator(self._schema, format_checker=draft4_format_checker)

        errors = sorted(_validator.iter_errors(self.instance), key=lambda e: e.path)
        for error in errors:
            raise ValidateException(error.message)


class SchemaMixin:
    """
    扩展schema
    """
    pass
