---
title: "dataclasses in python"
date: 2023-04-19T10:14:00-06:00
draft: true
categories: ["Technical"]
---

For classes in python see here. One of the best articles written on this. 

[https://aayushmnit.com/posts/2022-12-20-PythonFundamentals/Python OOPs Fundamentals.html](https://aayushmnit.com/posts/2022-12-20-PythonFundamentals/Python%20OOPs%20Fundamentals.html)

why dataclasses

1. no boilerplate code
2. if primarily to store data
3. type hinting
4. 

```python
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

p1 = Point(1, 2)
p2 = Point(1, 2)
print(p1)  # Point(x=1, y=2)
print(p1 == p2)  # True
```

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

p1 = Point(1, 2)
p2 = Point(1, 2)
print(p1)  # Point(x=1, y=2)
print(p1 == p2)  # True
```

## desert

mainly for mainly focused on 

1. serialization and deserialization.
2. validation

```python
from dataclasses import dataclass
import desert
import marshmallow

@dataclass
class User:
    id: int
    name: str

# Automatically generate a marshmallow schema
UserSchema = desert.schema(User)

# Serialize the data
user = User(id=1, name="John Doe")
serialized_data = UserSchema().dump(user)
print(serialized_data)  # {'id': 1, 'name': 'John Doe'}

# Deserialize the data
serialized_data = {'id': 1, 'name': 'John Doe'}
deserialized_user = UserSchema().load(serialized_data)
print(deserialized_user)  # User(id=1, name='John Doe')
```

In this example, **`desert`**
 simplifies the process of generating a schema for the **`User`**
 dataclass, as well as serializing and deserializing data. Without **`desert`**
, you would need to manually create a **`marshmallow`**
 schema for the **`User`**
 dataclass and define the fields and their types.
