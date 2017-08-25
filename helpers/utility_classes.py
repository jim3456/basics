class EnumBase(object):
    '''
    for performance purposes, objects with simple class variables are used throught the library instead of enums
    using this object exposes classmethods to transform the string representation to and from the interal integer representation
    '''
    @classmethod
    def tostring(cls, value):
        return dict([(v,k) for k,v in cls.__dict__.items() if type(v)==int])[value]

    @classmethod
    def fromstring(cls, name):
        return cls.__dict__[name]
    
    @classmethod
    def all_values(cls):
        return sorted([i for i in cls.__dict__.values() if type(i)==int])