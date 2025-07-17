
# Arithmetic Expression Evaluator with GUI

This is a Python app that lets you enter arithmetic expressions and see how they are processed step by step. It shows:

- Postfix notation (Reverse Polish Notation)
- Three-address code (used in compilers)
- Step-by-step breakdown of how the expression is evaluated

The app has a graphical interface built with PyQt5 and uses a dark theme for better readability.

---

## Features

- Supports arithmetic, relational, and logical operators
- Expression validation with error handling
- Converts to postfix using the Shunting Yard algorithm
- Generates simple intermediate code (three-address code)
- Shows all processing steps in a clean tabbed interface
- Dark-themed GUI with icons and progress animation

---

## How to Use

### 1. Clone the project

```bash
git clone https://github.com/yourusername/Arithmetic-Expression-Evaluator-with-GUI.git
cd Arithmetic-Expression-Evaluator-with-GUI
````

### 2. Set up the environment

It's a good idea to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install the required packages

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python gui_app.py
```

---

## Example Input

You can enter something like:

```
3 + 4 * 2 / (1 - 5) ** 2
```

And the app will show:

* The postfix form of the expression
* The generated three-address code
* Each step of how the expression was processed

---

## Dependencies

The app uses:

```
PyQt5==5.15.9
qdarkstyle==3.2.0
QtAwesome==1.2.1
pygments==2.16.1
graphviz==0.20.1
python-dotenv==1.0.0
```


```
