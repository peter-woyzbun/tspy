


class String(object):

    def __init__(self, name):
        self.name = name
        self.value = None

    def __set__(self, instance, value):
        self.value = value

    def __get__(self, instance, owner):
        return "%s: %s" % (self.name, self.value)

    def __str__(self):
        return "%s: %s" % (self.name, self.value)


class SchemaClass(object):

    p_value = String(name='p-value')



schema = SchemaClass()

schema.p_value = '0.004'

print(str(schema.p_value))