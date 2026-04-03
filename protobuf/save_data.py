import example_pb2

#创建一个Person对象
person = example_pb2.Person()
person.name = "alice"
person.age = 30
person.hobbies.extend(["painting", "dancing"])

#序列化对象并写入文件
with open("person_data.data", "wb") as f:
    print(f"Serializing data to {person.SerializeToString()}")
    f.write(person.SerializeToString())


#从文件中读取数据并反序列化对象
with open("person_data.data", "rb") as f:
    data = f.read()
    new_person = example_pb2.Person()
    new_person.ParseFromString(data)

    print(f"Name: {new_person.name}")
    print(f"Age: {new_person.age}")
    print(f"Hobbies: {new_person.hobbies}")
