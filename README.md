# 🤖 PySeraph - AI Academic Assistant for Students

**PySeraph** is an AI-powered desktop assistant built using Python to help students reduce academic stress and save time by automating common academic tasks.

Whether you're preparing for a viva, building a mini-project, or generating documentation — PySeraph is your personal academic companion.

---

## 🚀 Features

- 🎤 Voice-activated commands
- 📰 Get latest news using NewsAPI
- 🌦️ Weather updates via OpenWeather API
- 📄 Auto-generate PDFs for projects, assignments, and reports
- 📊 Auto-create PowerPoint presentations from topic prompts
- 🎤 Viva question & answer generator
- 📚 Mini project ideas + sample runnable code
- 🌐 Chat via integrated DeepSeek AI or Ollama LLM
- 📨 Email sending feature
- 📅 Academic utility tools (coming soon)

---

## 🧠 Tech Stack

- Python 3
- DeepSeek AI / Ollama (Open-source LLM)
- NewsAPI.org
- OpenWeatherMap API
- Pyttsx3 / SpeechRecognition
- Tkinter (optional GUI)
- FPDF / python-pptx
- smtplib (Email)

---

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/PySeraph.git
cd PySeraph

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the assistant
python main.py
