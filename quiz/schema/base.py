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

    def __getitem__(self, item):
        return self.instance[item]

    @property
    def schema(self):
        return self._schema

    @property
    def fields(self):
        yield from self._schema.get('properties')

    def validate(self):
        """验证实例 validate the instance with the schema"""

        _validator = Draft4Validator(self._schema, format_checker=draft4_format_checker)

        errors = sorted(_validator.iter_errors(self.instance), key=lambda e: e.path)
        for error in errors:
            raise ValidateException(error.message)

        self.validate_field()

    def validate_field(self):
        """验证其他字段"""
        for field in self.fields:
            validate_field = getattr(self, f'validate_{field}', None)
            if validate_field:
                validate_field()
