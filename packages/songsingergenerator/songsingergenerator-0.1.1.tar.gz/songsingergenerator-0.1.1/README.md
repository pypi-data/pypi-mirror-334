
# 🎵 Song Singer Generator

[![The latest build/test workflow run](https://github.com/software-students-spring2025/3-python-package-solapis/actions/workflows/ci.yml/badge.svg)](https://github.com/software-students-spring2025/3-python-package-solapis/actions/workflows/ci.yml) 

---

**Song Singer Generator** is a Python package that allows you to create and manage song collections by genre and artist. It enables developers to:
- Add new artists and songs  
- Search for specific names  
- Generate random songs and singers  

---

## 📦 **Package on PyPI**
👉 [**Visit the PyPI Page**](https://pypi.org/project/songsingergenerator/0.1.0/)  

---

## 🚀 **Installation**  
You can install the package directly from PyPI:

```bash
pip install songsingergenerator
```
---

## 💡 **How to Use**  
Here's how you can import and use the package in your Python project:

### ➡️ **Importing the package:**
```python
from songsingergenerator import generator
```

### ➡️ **Example Code:**
Example for adding a new singer and song:
```python
from songsingergenerator.generator import addSinger, randomSong, randomSinger, findSinger

# Add a singer and their songs
addSinger("Adele", "pop", ["Hello", "Someone Like You", "Rolling in the Deep"])

# Get a random song from the 'pop' genre
print(randomSong("pop"))

# Get a random singer from the 'pop' genre
print(randomSinger("pop"))

# Find a singer containing the word 'Adele'
print(findSinger("Adele"))
```

---

## 🛠️ **Available Functions**
| Function | Description | Example |
|----------|-------------|---------|
| `addSinger(singer, genre, songs)` | Adds a new singer and their songs to the collection. | `addSinger("Adele", "pop", ["Hello"])` |
| `randomSong(genre=None)` | Returns a random song from a specific genre (or any genre if none is specified). | `randomSong("pop")` |
| `randomSinger(genre=None)` | Returns a random singer from a specific genre. | `randomSinger("pop")` |
| `findSinger(inWord)` | Searches for singers whose names contain the specified substring. | `findSinger("Adele")` |

---

## 🏗️ **Contributing**  
We welcome contributions! Here’s how to get started:

### 1. **Clone the repository**:
```bash
git clone https://github.com/software-students-spring2025/3-python-package-solapis.git
```

### 2. **Set up the virtual environment**:
We use **Pipenv** for managing dependencies:

- Install Pipenv:
```bash
pip install pipenv
```

- Install dependencies:
```bash
pipenv install --dev
```

### 3. **Activate the environment**:
Activate the Pipenv virtual environment:
```bash
pipenv shell
```

### 4. **Build the package**:
Use `build` to create package artifacts:
```bash
pipenv run python -m build
```

### 5. **Run tests**:
Use `pytest` to run tests:
```bash
pipenv run pytest tests/
```

---

## 👥 **Team**
| Name | GitHub Profile |
|------|----------------|
| **Yang Hu** | [@younghu312](https://github.com/younghu312) |
| **Ziqi Huang** | [@RyanH0417](https://github.com/RyanH0417) |
| **Zirui Han** | [@ZiruiHan](https://github.com/ZiruiHan) |
| **Zichao Jin** | [@ZichaoJin](https://github.com/ZichaoJin) |

---

## 🌐 **Running the Project**
To run the project locally:
1. Clone the repository.
2. Set up the virtual environment with Pipenv.
3. Run the test suite to make sure everything is working:
```bash
pipenv run pytest tests/
```

4. Import the package and use it as described in the **How to Use** section.

