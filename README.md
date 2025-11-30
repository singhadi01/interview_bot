# AI Interview Bot 

A Django-powered interview assistant that uses **Llama (HuggingFace API)** and **speech recognition** to run automated mock interviews and generate professional feedback — built using only **basic HTML & CSS (No JavaScript)**.

---

## Features

- Accepts **Job Description** input and **PDF Resume upload**
- Generates **10 relevant interview questions** using Llama 3.1 (8B-Instruct)
- Records answers from microphone using **Google Speech Recognition**
- Detects **5 seconds of silence** to mark answer completion
- Plays a **beep sound** when answer recording begins
- Displays **Interview Instructions + Feedback on the same page**
- Template-based flow, pure **Django + HTML + CSS**, no frontend JS

---

## 🛠 Tech Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS |
| Backend | Django 5 |
| LLM | meta-llama/Llama-3.1-8B-Instruct via HuggingFace API |
| Questions Schema | LangChain Structured Output |
| Interview Workflow | LangGraph |
| Voice Input | SpeechRecognition |
| TTS Output | Custom `tts_play()` |
| PDF extraction | PyPDFLoader |

---
## Project Structure
```
Interview_bot/
│── interview/ # Django app
│── backend.py # LangGraph pipeline
│── templates/
│ └── interview.html
│── static/
│ └── beep.wav (optional)
│── manage.py
│── requirements.txt
│── .gitignore
│── README.md
```
---

---

## ⚙ Installation & Local Run

```sh
# Clone repo
git clone https://github.com/singhadi01/interview_bot

# Create & activate environment
python -m venv myenv
myenv\Scripts\activate  # Windows
# source myenv/bin/activate  # Mac/Linux
#make .env file and put the huggingface api in that file

# Install dependencies
pip install -r requirements.txt

# Run server
python manage.py runserver


