import copy

from tspy.result_field import ResultField, FloatField, TableField


class ResultSchemaBase(type):

    def __new__(mcs, name, bases, attrs):
        fields = {}
        summary_title = None
        summary_fields = None
        for key, value in attrs.items():
            if isinstance(value, ResultField):
                fields[key] = value
            if key == 'Meta':
                if hasattr(value, 'summary_title'):
                    summary_title = value.summary_title
                summary_fields = value.summary_fields
        for base in bases:
            if hasattr(base, '_fields'):
                fields.update(base._fields)
        attrs['_fields'] = fields
        if summary_title is not None:
            attrs['summary_title'] = summary_title
        attrs['summary_fields'] = summary_fields
        return type.__new__(mcs, name, bases, attrs)


class ResultSchema(object, metaclass=ResultSchemaBase):

    __metaclass__ = ResultSchemaBase

    _fields = dict()
    summary_title = "Result summary"
    summary_fields = tuple()

    def __new__(cls, *args, **kwargs):
        """
                for attr, value in cls.__dict__.items():
            print(attr, value)
        if hasattr(cls, 'Meta'):
            print("HAS META!")
            meta = cls.Meta
            if hasattr(meta, 'summary_fields'):
                print("SUMMARY FIELDS!")
                print(meta.summary_fields)
                cls.__summary_fields = meta.summary_fields
        """
        return object.__new__(cls)

    def __init__(self):
        self.fields = list()

    @property
    def result_fields(self):
        for attr, value in self.__dict__.items():
            print(attr)
            if isinstance(value, ResultField):
                print("Yielding result field!")
                yield value

    def summary(self):
        print(self.summary_title)
        for summary_field in self.summary_fields:
            print(self._fields[summary_field].summary_str)

