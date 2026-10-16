# ✨ AI Content Generator using Groq and Flask

An AI-powered content generation web application built using **Python, Flask, HTML, CSS, JavaScript, and the Groq API**. The application transforms a single topic into five creative content ideas, a beginner-friendly article, a concise summary, and a professional LinkedIn post using a sequential AI prompt chain.

## 🚀 Features

- **Content Idea Generation:** Generates five unique content ideas based on the user's topic.
- **Article Creation:** Converts the generated ideas into an informative article with a title, introduction, headings, and conclusion.
- **Article Summarization:** Extracts five important points from the generated article.
- **LinkedIn Post Generation:** Creates a concise LinkedIn post with an engaging opening, a call to action, and three relevant hashtags.
- **Interactive Web Interface:** Provides a modern dashboard built with HTML, CSS, and JavaScript.
- **Copy to Clipboard:** Allows users to copy individual outputs.
- **Clear Workspace:** Resets the generated content and input field.
- **Error Handling:** Displays error messages when content generation fails.
- **Secure API Configuration:** Uses environment variables to protect the Groq API key.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Flask | Web application framework |
| Groq API | AI-powered text generation |
| GPT-OSS-20B | Language model configured in the application |
| HTML | Web page structure |
| CSS | Responsive dashboard styling |
| JavaScript | User interactions and API requests |
| python-dotenv | Loads environment variables |

## ⚙️ How It Works

The application follows a sequential AI prompt chain:

1. **Topic Input:** The user enters a content topic.
2. **Idea Generation:** The AI generates five creative content ideas.
3. **Article Writing:** The generated ideas are used to write an informative article.
4. **Summarization:** The article is summarized into five key points.
5. **LinkedIn Post Creation:** The summary is used to generate a professional LinkedIn post.
6. **Display Results:** All four outputs are displayed in the web interface.

## 📁 Project Structure

```text
Groq_Content_Generator/
│
├── app.py              # Flask application and AI prompt chain
├── .env                # Secret API key (not uploaded)
├── .env.example        # Example environment configuration
├── .gitignore          # Files excluded from Git
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## 📋 Prerequisites

Before running the project, make sure you have:

- Python 3.10 or a compatible version.
- pip, the Python package installer.
- A Groq account and a valid API key.
- Git, if you want to upload the project to GitHub.

## 🔧 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

Replace `YOUR_USERNAME` and `YOUR_REPOSITORY` with your actual GitHub details.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```cmd
.venv\Scripts\activate.bat
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available yet, install the packages manually:

```bash
pip install flask python-dotenv groq
```

### 5. Configure the API key

Create a `.env` file in the project root directory:

```env
GROQ_API_KEY=your_actual_groq_api_key
```

Replace the placeholder with your API key from the Groq developer console.

**Security:** Never upload your `.env` file or share your API key publicly.

### 6. Run the application

```bash
python app.py
```

### 7. Open the web interface

Open your browser and visit:

http://127.0.0.1:5000

Enter a topic and click **Generate Content** to start the AI prompt chain.

## 🔐 Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | API key used to authenticate requests to Groq |

The application loads the API key using `python-dotenv`, keeping credentials separate from the application code.

## 📌 Example Use Case

**Input topic:** The Future of Artificial Intelligence

**Expected outputs:**

- Five content ideas related to artificial intelligence.
- An informative article explaining the topic.
- A summary containing five key points.
- A LinkedIn post with a call to action and relevant hashtags.

The generated output depends on the topic, model availability, and AI response.

## ⚠️ Limitations

- An active internet connection is required to communicate with the Groq API.
- API usage is subject to the account's applicable limits and availability.
- The configured model must be available to the Groq account.
- Generated content may contain inaccuracies and should be reviewed before publication.
- The application currently generates content sequentially and does not permanently save results.
- The Flask development server is intended for local development, not production deployment.

## 🔮 Future Enhancements

- Download generated articles as PDF or text files.
- Save and retrieve previous content generations.
- Add user authentication.
- Support additional social media platforms.
- Add options for article length, writing tone, and target audience.
- Deploy the application to a cloud hosting platform.

## 👨‍💻 Author

**Your Name**

GitHub: https://github.com/YOUR_USERNAME

## 📄 License

This project is
