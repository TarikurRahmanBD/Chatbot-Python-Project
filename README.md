# Chatbot Python Project

## Project Overview

This project is a simple chatbot application built with Python. It provides a friendly chat interface where users can ask basic questions, receive bot responses, and interact with a small rule-based and model-based conversational system.

The project includes:
- A graphical chat window built with Tkinter
- A trained chatbot model file
- Intent and response data stored in JSON
- A training script for rebuilding the model

This project is ideal for beginners who want to learn how chatbot applications work in Python.

---

## Features

- Interactive chatbot interface
- Basic greeting and support responses
- Question-answer support for common topics
- Project-related and developer-related responses
- Easy to run locally on Windows
- Includes training script for model retraining

---

## Project Structure

The repository contains the following important files:

- [chatgui.py](chatgui.py) – Main chatbot application with GUI
- [train_chatbot.py](train_chatbot.py) – Script used to train the chatbot model
- [intents.json](intents.json) – Contains the chatbot intents and responses
- [chatbot_model.h5](chatbot_model.h5) – Pretrained chatbot model
- [words.pkl](words.pkl) and [classes.pkl](classes.pkl) – Vocabulary and class files used by the model
- [test_chatbot.py](test_chatbot.py) – Simple test script for basic chatbot verification

---

## How to Install & Run

### 1. Clone or open the project
Open the project folder in your terminal or VS Code workspace.

### 2. Create a virtual environment
```bash
python -m venv .venv
```

### 3. Activate the virtual environment
On Windows:
```bash
.venv\Scripts\activate
```

### 4. Install dependencies
```bash
pip install nltk numpy tensorflow keras
```

### 5. Download NLTK data (optional, for training)
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet')"
```

### 6. Run the chatbot
```bash
python chatgui.py
```

### 7. Retrain the model (optional)
If you want to rebuild the chatbot model:
```bash
python train_chatbot.py
```

---

## Usage

Once the application starts:
1. Type a message in the chat box.
2. Click the Send button.
3. The bot will respond based on its built-in patterns and trained model.

---

## About the Developer

Name: Tarikur Rahman

GitHub: https://github.com/tarikurrahmanbd

Portfolio: https://yourtarikur.netlify.app/

Social/Handle: tarikurrahman08

Email: tarikurrahman2008@gmail.com

---

## License

This project is licensed under the MIT License.

You are free to use, modify, and share this project with proper attribution.

---

## Conclusion

This project is a beginner-friendly chatbot application that demonstrates how Python can be used to build simple conversational AI systems. It is a great starting point for learning NLP, model training, and GUI-based application development.
