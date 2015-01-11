import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)


class Rlist():
    def __init__(self, lname, alist):
        self.lname = lname
        self.alist = alist
        self.create()

    def create(self):
        for thing in self.alist:
            r.rpush(self.lname, thing)
        return True

    def get(self, start=0, end=-1):
        f = r.lrange(self.lname, start, end)
        for i in range(len(f)):
            f[i] = f[i].decode('utf-8')
            f[i] = int(f[i]) if f[i].isdigit() else f[i]
        return f

    def append(self, alist):
        if isinstance(alist, list):
            for thing in alist:
                r.rpush(self.lname, thing)
        else:
            r.rpush(self.lname, alist)
        return True

    def delete(self):
        r.delete(self.lname)
        return True


### sorry no dict['key'] notation 
### instead dot notation dict.key
class RDict():
    def __init__(self, **kwargs):
        
        self.name = kwargs['name']
        kwargs.pop('name')
        
        for key, value in kwargs.items():
            setattr(self, key, value)
        
        self.create(kwargs)

    def create(self,kwargs):
        for key, value in kwargs.items():
            r.hset(self.name, key, value)
        return True

    def pop(self, key):
        value = r.hget(self.name, key).decode('utf-8')
        if value.isdigit():
            value = int(value)
        r.hdel(self.name, key)
        return value

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
            r.hset(self.name,key,value) 
        return True

    def delete(self):
        r.delete(self.name)
        return True

    def keys(self):
        keys = r.hkeys(self.name)
        for i,j in enumerate(keys):
            keys[i] = j.decode('utf-8')
        return keys
    
    def values(self):
        values = r.hvals(self.name)
        for i,j in enumerate(values):
            values[i] = j.decode('utf-8')
        return values


########  tests ##########
# my_list = ["j", "ssttuu", "ds", "sup", "why", 100]
# list_name = "try2"
# test = Rlist(list_name, my_list)
# test.append(5000)
# test.delete()
# test = RDict(name='158dict', adolfo="reyes", wtf='now')
# result = test.pop('adolfo')
# test.update(boss="adolfo")
# test.delete()
# print(test)
# print(test.keys())
# print(test.values())
# test['boss']
# test.delete()
# print(test.boss)
# print(test.get())