from orm_models import sql_control

class Filed:
    def __init__(self,name,type,primary_key,default):
        self.name = name
        self.type = type
        self.primary_key = primary_key
        self.default = default

class IntegerField(Filed):
    def __init__(self,name,type="int",primary_key=False,default=0):
        super().__init__(name,type,primary_key,default)

class StringField(Filed):
    def __init__(self,name,type="varchar(256)",primary_key=False,default=None):
        super().__init__(name,type,primary_key,default)

class Mymeta(type):
    def __new__(cls, class_name,base_class,class_attr):
        if class_name == "Models":
            return type.__new__(cls, class_name,base_class,class_attr)
        
        table_name = class_attr.get("table_name",class_name)
        primary_key = None
        mappings = {}
        for k,v in class_attr.items():
             if isinstance(v,Filed):
                 mappings[k]=v

                 if v.primary_key:
                    if primary_key:
                        raise Exception("只能有一个主键")

                    primary_key = v.name
        if not primary_key:
            raise Exception("必须有一个主键")

        for k in mappings.keys():
            class_attr.pop(k)

        class_attr["table_name"] = table_name
        class_attr["primary_key"] = primary_key
        class_attr["mappings"] = mappings
        return type.__new__(cls, class_name,base_class,class_attr)
    


class Models(dict,metaclass=Mymeta):
    sql_obj = sql_control.SQLControl()

    def __getattr__(self, item):
        return self.get(item)
    
    def __setattr__(self, key, value):
        self[key] = value

    @classmethod
    def select_sql(cls,**kwargs):
        if not kwargs:
            sql = f"select * from {cls.table_name}"
            res = cls.sql_obj.select(sql)
            return res
        else:
            key = list(kwargs.keys())[0]
            value = kwargs.get(key)
            # select * from xx where key = value
            sql = f"select * from {cls.table_name} where {key} = %s"
            res = cls.sql_obj.select(sql,value)
        return [cls(**i) for i in res]
