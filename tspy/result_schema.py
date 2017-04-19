

class ResultField(object):

    pass


class ResultSchema(object):

    __summary_fields = list()

    def __new__(cls, *args, **kwargs):
        print("NEW CALLED!")
        for attr, value in cls.__dict__.items():
            print(attr, value)
        if hasattr(cls, 'Meta'):
            print("HAS META!")
            meta = cls.Meta
            if hasattr(meta, 'summary_fields'):
                print("SUMMARY FIELDS!")
                print(meta.summary_fields)
                cls.__summary_fields = meta.summary_fields
        return object.__new__(cls)

    def summary(self):
        print(self.__summary_fields)
        

class LinearFit(ResultSchema):

    jimothy = ResultField()

    class Meta:
        summary_fields = ['jimothy']


lin_fit = LinearFit()

lin_fit.summary()