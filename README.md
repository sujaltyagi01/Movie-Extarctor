# 🎬 Movie Extractor – AI-Powered Movie & Series Finder

Movie Extractor is a Generative AI-powered application that identifies movies and TV series based on user-provided descriptions. Users can enter a storyline, character description, or memorable scene, and the application uses an LLM to help identify the matching movie or series.

## 🚀 Live Demo

**Try the application here:**

[Movie Extractor – Live Application](https://movie-extarctor-dqg24d2amchq462zyt6nsz.streamlit.app/)

## ✨ Features

- **AI-Powered Identification:** Uses Generative AI to identify movies and TV series from natural language descriptions.
- **Natural Language Input:** Accepts descriptions of storylines, scenes, characters, and other memorable details.
- **LLM Integration:** Uses Groq-powered language models through LangChain.
- **Interactive Interface:** Provides a simple and user-friendly interface built with Streamlit.
- **Structured Output:** Uses structured data handling to organize the extracted information.

## 🛠️ Tech Stack

- **Programming Language:** Python
- **Frontend:** Streamlit
- **LLM Provider:** Groq API
- **Framework:** LangChain
- **Data Validation:** Pydantic
- **Environment Management:** Python Dotenv

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Movie-Extractor
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment:

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

Create a `.env` file in the project root directory:

```env
GROQ_API_KEY=your_groq_api_key
```

Get your API key from [Groq Console](https://console.groq.com/).

### 5. Run the Application

Run the Streamlit application using its main UI file:

```bash
streamlit run app.py
```

Replace `app.py` with your actual main Streamlit filename if different.

## 🔐 Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | API key used to access Groq LLM services |

**Important:** Never upload your `.env` file or expose your API key on GitHub.

## 📂 Project Structure

```text
Movie-Extractor/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

Update this structure according to your actual project files.

## 🌐 Deployment

The application is deployed using **Streamlit Community Cloud**.

[![Streamlit](https://img.shields.io/badge/Streamlit-Live%20App-red?logo=streamlit)](https://movie-extarctor-dqg24d2amchq462zyt6nsz.streamlit.app/)

## 👨‍💻 Author

**Sujal Tyagi**

B.Tech – Computer Science & Technology (Data Science)

Interested in Generative AI, Python, Full-Stack Development, and building AI-powered applications.

---

⭐ If you find this project interesting, feel free to explore the live application!
