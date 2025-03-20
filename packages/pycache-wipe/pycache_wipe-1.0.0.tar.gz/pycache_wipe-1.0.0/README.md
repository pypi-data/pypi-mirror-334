# pycache-wipe

**pycache-wipe** is a lightweight, production-ready Python utility that helps you keep your project directories clean by safely and efficiently deleting all `__pycache__` folders.

These `__pycache__` folders are generated automatically by Python to store bytecode-compiled files. Over time, they can clutter your workspace and may not be necessary to keep in production or deployment environments.

---

## Features

- 🌊 **Simple & Intuitive CLI**: Minimal commands with clear flags.
- 🔒 **Safe Deletion**: Only targets `__pycache__` directories, nothing else.
- 🔄 **Two Modes**: Choose between local (current directory) deletion or recursive deletion.
- 🌟 **Robust Error Handling**: Graceful failure and informative messages.

---

## Installation

Install via pip:

```
pip install pycache-wipe
```

---

## Usage

### Delete all `__pycache__` folders **recursively** (in current and subdirectories):

```
pycache-wipe -r
```

### Delete only the `__pycache__` folder **in the current directory**:

```
pycache-wipe -l
```

---

## Example Output

```
Recursively deleting all __pycache__ directories...
✅ Deleted: /your/project/path/__pycache__
✅ Deleted: /your/project/path/submodule/__pycache__
🎉 Finished pycache-wipe operation.
```

---

## Why Use pycache-wipe?

- Keep your project folder clean.
- Reduce unnecessary clutter before committing to version control.
- Easily integrate into deployment or CI/CD scripts.
- No more manual deletion!

---

## License

MIT License


