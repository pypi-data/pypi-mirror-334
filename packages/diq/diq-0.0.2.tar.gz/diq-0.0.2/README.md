# **Diq: A Pythonic Object Serializer**
[![PyPI](https://img.shields.io/pypi/v/diq.svg)](https://pypi.org/project/diq/) [![License](https://img.shields.io/github/license/Jyonn/diq)](https://opensource.org/licenses/MIT)

**Diq** is a lightweight and flexible Python library that enables easy serialization of class instances into dictionaries. It supports renaming fields dynamically, custom serialization logic, and automatic attribute extraction.

---

## **✨ Features**
- 🔹 Convert class instances into dictionaries with `dictify()`
- 🔹 **Rename attributes** dynamically using `field->new_name`
- 🔹 **Custom serialization** via `_dictify_{field}()` methods
- 🔹 **Automatic attribute detection** (no need to list fields manually)
- 🔹 **Lightweight and dependency-free**

---

## **📦 Installation**
```bash
pip install diq
```

## **🚀 Quick Start**

### 1️⃣ Basic Usage

```python
from diq import Dictify

class User(Dictify):
    def __init__(self, username, email):
        self.username = username
        self.email = email

user = User("john_doe", "john@example.com")
print(user.dictify())  # {'username': 'john_doe', 'email': 'john@example.com'}
```

### 2️⃣ Select Specific Fields

```python
print(user.dictify("username"))  
# {'username': 'john_doe'}
```

### 3️⃣ Rename Fields

print(user.dictify("username->user", "email->contact"))
# {'user': 'john_doe', 'contact': 'john@example.com'}

### 4️⃣ Custom Serialization for Specific Fields

```python
from datetime import datetime

from diq import Dictify

class User(Dictify):
    def __init__(self, username, created_at):
        self.username = username
        self.created_at = created_at

    def _dictify_created_at(self):
        return self.created_at.strftime('%Y-%m-%d')

user = User("john_doe", datetime(2025, 3, 15))
print(user.dictify())  
# {'username': 'john_doe', 'created_at': '2025-03-15'}
```

## **📝 License**

Diq is released under the **MIT License**.

## **🤝 Contributing**

Contributions are welcome! Feel free to submit issues or pull requests.

## **📮 Contact**

- GitHub: https://github.com/Jyonn/diq
- PyPI: https://pypi.org/project/diq
