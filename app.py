
from dotenv import load_dotenv
import os
from groq import Groq
from flask import Flask, request, jsonify, render_template_string

# ============================================================
# STEP 1: CONFIGURATION
# ============================================================

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if api_key:
    print("API key loaded successfully")
else:
    raise ValueError(
        "GROQ_API_KEY not found. Please check your .env file."
    )

client = Groq(api_key=api_key)
MODEL = "openai/gpt-oss-20b"

app = Flask(__name__)

# ============================================================
# STEP 2: YOUR ORIGINAL AI FUNCTIONS
# ============================================================

def ask_ai(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000,
    )

    return response.choices[0].message.content


def generate_ideas(topic):
    prompt = f"""
    you are a content planning assistant.
    Generate 5 unique and creative content ideas for the topic:{topic}
    Explain each idea in 2-3 sentences.
    Use a numbered list.
    """

    ideas = ask_ai(prompt)
    return ideas


def create_article(topic, ideas):
    prompt = f"""
    you are a professional content writer.
    Topic: {topic}
    use these ideas to write a informative article.
    {ideas}

    Requirements:
    - Write a suitable title.
    - Use simple englih.
    - Include an introduction.
    - Eplain the ideass using headings and subheadings.
    - Include a concluion.
    - Keep the article beginner friendly.
    """

    article = ask_ai(prompt)
    return article


def create_summary(article):
    prompt = f"""
    you are a expert content summarizer.

    Summarize the following article into 5 important bullet points.

    use simple english.
    preserve the article's main meaning.

    Article:
    {article}
    """

    summary = ask_ai(prompt)
    return summary


def create_linkedin_post(topic, summary):
    prompt = f"""
    you are a professional social media content writer.
    Create a LinkedIn post about the topic: {topic}
    Use this summary as the source material:
    {summary}

    Requirements:
    - Start with a engaging opening.
    - Ue imple and profesional english.
    - Keep the post concie.
    - Add a call to action.
    - Add 3 relevant hashtags.
    - Do not invent fact or statistics.
    """

    post = ask_ai(prompt)
    return post


# ============================================================
# STEP 3: HTML, CSS AND JAVASCRIPT IN ONE FILE
# ============================================================

HTML_PAGE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Content House | AI Generator</title>

    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        :root {
            --bg: #0b1020;
            --panel: #121a2e;
            --panel-light: #18233a;
            --border: #293650;
            --text: #edf2ff;
            --muted: #9caac3;
            --accent: #8b7cff;
            --accent2: #5c9dff;
            --success: #52d6a1;
        }

        body {
            font-family: Inter, "Segoe UI", Arial, sans-serif;
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
        }

        button, input {
            font: inherit;
        }

        .app {
            display: flex;
            min-height: 100vh;
        }

        /* Sidebar */

        .sidebar {
            width: 245px;
            flex-shrink: 0;
            padding: 28px 18px;
            background: #0e1527;
            border-right: 1px solid var(--border);
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 0 8px;
            margin-bottom: 42px;
        }

        .brand h2 {
            font-size: 16px;
            letter-spacing: 0.2px;
        }

        .brand small {
            display: block;
            color: var(--muted);
            margin-top: 4px;
            font-size: 11px;
        }

        .nav-label {
            color: #71809c;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 1.6px;
            padding: 0 12px;
            margin-bottom: 12px;
        }

        .nav-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 13px 12px;
            margin-bottom: 7px;
            border-radius: 10px;
            color: var(--muted);
            font-size: 13px;
        }

        .nav-item.active {
            background: #222b48;
            color: white;
            border: 1px solid #354165;
        }

        .nav-item span {
            font-size: 17px;
        }

        .sidebar-bottom {
            margin-top: 55px;
            padding: 17px;
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 13px;
        }

        .sidebar-bottom p {
            font-size: 12px;
            line-height: 1.6;
            color: var(--muted);
            margin-top: 8px;
        }

        .status {
            color: var(--success);
            font-size: 12px;
            margin-top: 12px;
        }

        /* Main layout */

        .main {
            flex: 1;
            min-width: 0;
            padding: 32px 38px 60px;
            max-width: 1500px;
        }

        .topbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 20px;
            margin-bottom: 38px;
        }

        .eyebrow {
            color: var(--accent);
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 1.8px;
            text-transform: uppercase;
            margin-bottom: 9px;
        }

        h1 {
            font-size: clamp(25px, 3vw, 34px);
            letter-spacing: -1px;
        }

        .topbar p {
            color: var(--muted);
            margin-top: 9px;
            font-size: 13px;
            line-height: 1.6;
        }

        .model-badge {
            border: 1px solid var(--border);
            background: var(--panel);
            padding: 11px 15px;
            border-radius: 10px;
            font-size: 11px;
            color: #c8d4ef;
            white-space: nowrap;
        }

        .model-badge span {
            color: var(--success);
            margin-right: 7px;
        }

        /* Input panel */

        .generator {
            background: linear-gradient(140deg, #18233c, #12192c);
            border: 1px solid #34405d;
            border-radius: 18px;
            padding: 28px;
            margin-bottom: 28px;
        }

        .generator h2 {
            font-size: 18px;
            margin-bottom: 8px;
        }

        .generator > p {
            color: var(--muted);
            font-size: 13px;
            line-height: 1.6;
            margin-bottom: 23px;
        }

        .input-label {
            display: block;
            color: #d9e2f5;
            font-size: 12px;
            font-weight: 700;
            margin-bottom: 10px;
        }

        .input-row {
            display: flex;
            gap: 12px;
        }

        .topic-input {
            flex: 1;
            min-width: 0;
            background: #0c1325;
            color: white;
            border: 1px solid #354361;
            border-radius: 10px;
            padding: 15px 16px;
            outline: none;
            transition: border 0.2s;
        }

        .topic-input:focus {
            border-color: var(--accent);
        }

        .topic-input::placeholder {
            color: #71809c;
        }

        .primary-btn {
            border: none;
            background: linear-gradient(110deg, #8b7cff, #628cff);
            color: white;
            padding: 14px 20px;
            border-radius: 10px;
            font-weight: 700;
            font-size: 12px;
            cursor: pointer;
            transition: opacity 0.2s, transform 0.2s;
            white-space: nowrap;
        }

        .primary-btn:hover {
            transform: translateY(-1px);
        }

        button:disabled {
            opacity: 0.55;
            cursor: not-allowed;
            transform: none;
        }

        .helper {
            color: #8290aa;
            font-size: 11px;
            margin-top: 12px;
        }

        /* Workflow */

        .section-heading {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 15px;
            margin-bottom: 17px;
        }

        .section-heading h2 {
            font-size: 17px;
        }

        .section-heading p {
            color: var(--muted);
            font-size: 12px;
            margin-top: 6px;
        }

        .clear-btn {
            background: transparent;
            border: 1px solid var(--border);
            color: #bac7df;
            padding: 9px 13px;
            border-radius: 8px;
            font-size: 11px;
            cursor: pointer;
        }

        .clear-btn:hover, .copy-btn:hover {
            background: #26314b;
        }

        .workflow {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 12px;
            margin-bottom: 28px;
        }

        .step {
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 13px;
            padding: 17px;
            min-width: 0;
            transition: border 0.2s;
        }

        .step.running {
            border-color: var(--accent);
        }

        .step.done {
            border-color: #286e59;
        }

        .step-number {
            color: var(--accent);
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 1px;
        }

        .step h3 {
            font-size: 12px;
            margin: 13px 0 7px;
        }

        .step p {
            color: var(--muted);
            font-size: 11px;
            line-height: 1.5;
        }

        .step-state {
            margin-top: 14px;
            color: #8290aa;
            font-size: 10px;
        }

        .step.done .step-state {
            color: var(--success);
        }

        /* Results */

        .results {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 16px;
        }

        .result-card {
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 14px;
            min-width: 0;
            overflow: hidden;
        }

        .result-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            padding: 17px 19px;
            border-bottom: 1px solid var(--border);
        }

        .result-title {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 13px;
            font-weight: 700;
        }

        .result-icon {
            display: grid;
            place-items: center;
            width: 32px;
            height: 32px;
            background: var(--panel-light);
            border-radius: 9px;
            font-size: 15px;
        }

        .copy-btn {
            background: #202b43;
            border: 1px solid #34415c;
            color: #c5d0e7;
            border-radius: 7px;
            padding: 7px 10px;
            font-size: 10px;
            cursor: pointer;
        }

        .result-content {
            padding: 19px;
            color: #c5d0e3;
            font-size: 12px;
            line-height: 1.85;
            min-height: 200px;
            max-height: 430px;
            overflow-y: auto;
            overflow-wrap: anywhere;
            white-space: pre-wrap;
        }

        .result-content.empty {
            color: #71809c;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            min-height: 200px;
        }

        .result-content:focus {
            outline: 1px solid var(--accent);
            outline-offset: -2px;
        }

        .error-message {
            display: none;
            background: #361e2a;
            border: 1px solid #824258;
            color: #ffbdcb;
            border-radius: 10px;
            padding: 13px 15px;
            margin-bottom: 20px;
            font-size: 12px;
            line-height: 1.6;
            overflow-wrap: anywhere;
        }

        .loading-indicator {
            display: none;
            color: #c9c0ff;
            font-size: 12px;
            margin-top: 15px;
        }

        .spinner {
            display: inline-block;
            width: 13px;
            height: 13px;
            border: 2px solid #50577a;
            border-top-color: #b0a6ff;
            border-radius: 50%;
            animation: spin 0.7s linear infinite;
            vertical-align: middle;
            margin-right: 8px;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        footer {
            color: #6f7d98;
            font-size: 11px;
            text-align: center;
            margin-top: 35px;
        }

        @media (max-width: 1100px) {
            .sidebar {
                width: 205px;
            }

            .main {
                padding: 28px 22px 45px;
            }

            .workflow {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
        }

        @media (max-width: 720px) {
            .sidebar {
                display: none;
            }

            .main {
                padding: 23px 15px 35px;
            }

            .topbar {
                align-items: flex-start;
                flex-direction: column;
                margin-bottom: 25px;
            }

            .generator {
                padding: 20px;
            }

            .input-row {
                flex-direction: column;
            }

            .primary-btn {
                width: 100%;
            }

            .results {
                grid-template-columns: 1fr;
            }

            .workflow {
                gap: 9px;
            }

            .step {
                padding: 13px;
            }

            .model-badge {
                white-space: normal;
            }
        }
    </style>
</head>

<body>
<div class="app">

    <aside class="sidebar">
        <div class="brand">
            <div class="brand-icon"></div>
            <div>
                <h2>Content House</h2>
                <small>AI-powered workspace</small>
            </div>
        </div>

        <div class="nav-label">WORKSPACE</div>

        <div class="nav-item active">
            <span>✦</span> Content Generator
        </div>

        <div class="sidebar-bottom">
            <strong style="font-size:12px;">Your AI workflow</strong>
            <p>Turn one topic into ideas, an article, a summary and a professional LinkedIn post.</p>
            <div class="status">● Groq integration configured</div>
        </div>
    </aside>

    <main class="main">

        <header class="topbar">
            <div>
                <div class="eyebrow">AI Content Workspace</div>
                <h1>Create your content smarter.</h1>
                <p>One topic. Four stages. A complete content package.</p>
            </div>

            <div class="model-badge">
                <span>●</span> Groq API &nbsp;|&nbsp; GPT-OSS-20B
            </div>
        </header>

        <section class="generator">
            <h2>What do you want to write about?</h2>
            <p>Enter your topic and let the AI generate a complete set of content for you.</p>

            <form id="contentForm">
                <label class="input-label" for="topic">ENTER YOUR CONTENT TOPIC</label>

                <div class="input-row">
                    <input
                        type="text"
                        id="topic"
                        class="topic-input"
                        placeholder="e.g. The future of artificial intelligence"
                        maxlength="500"
                        required
                    >

                    <button type="submit" class="primary-btn" id="generateBtn">
                        ✦ Generate Content
                    </button>
                </div>

                <div class="helper">
                    Generates 5 ideas, an article, a 5-point summary and a LinkedIn post in just 5 seconds.
                </div>

                <div class="loading-indicator" id="loadingIndicator">
                    <span class="spinner"></span>
                    <span id="loadingText">Preparing your content...</span>
                </div>
            </form>
        </section>

        <div class="error-message" id="errorMessage" role="alert"></div>

        <section>
            <div class="section-heading">
                <div>
                    <h2>Your generation pipeline</h2>
                    <p>Follow each stage of your AI content workflow.</p>
                </div>

                <button type="button" class="clear-btn" id="clearBtn">
                    ↺ Clear workspace
                </button>
            </div>

            <div class="workflow">
                <div class="step" id="step1">
                    <div class="step-number">STEP 01</div>
                    <h3>Generate Ideas</h3>
                    <p>Explore five creative content angles.</p>
                    <div class="step-state" id="state1">○ Waiting</div>
                </div>

                <div class="step" id="step2">
                    <div class="step-number">STEP 02</div>
                    <h3>Write Article</h3>
                    <p>Turn the ideas into a beginner-friendly article.</p>
                    <div class="step-state" id="state2">○ Waiting</div>
                </div>

                <div class="step" id="step3">
                    <div class="step-number">STEP 03</div>
                    <h3>Summarize</h3>
                    <p>Extract five important takeaways.</p>
                    <div class="step-state" id="state3">○ Waiting</div>
                </div>

                <div class="step" id="step4">
                    <div class="step-number">STEP 04</div>
                    <h3>LinkedIn Post</h3>
                    <p>Create a concise professional social post.</p>
                    <div class="step-state" id="state4">○ Waiting</div>
                </div>
            </div>
        </section>

        <section>
            <div class="section-heading">
                <div>
                    <h2>Generated content</h2>
                    <p id="resultSubtitle">Your results will appear here.</p>
                </div>
            </div>

            <div class="results">

                <article class="result-card">
                    <div class="result-header">
                        <div class="result-title">
                            <div class="result-icon">✧</div>
                            Content Ideas
                        </div>
                        <button class="copy-btn" data-copy="ideas">Copy</button>
                    </div>
                    <div class="result-content empty" id="ideas" aria-live="polite">
                        Your five content ideas will appear here.
                    </div>
                </article>

                <article class="result-card">
                    <div class="result-header">
                        <div class="result-title">
                            <div class="result-icon">▤</div>
                            Article
                        </div>
                        <button class="copy-btn" data-copy="article">Copy</button>
                    </div>
                    <div class="result-content empty" id="article" aria-live="polite">
                        Your complete article will appear here.
                    </div>
                </article>

                <article class="result-card">
                    <div class="result-header">
                        <div class="result-title">
                            <div class="result-icon">≡</div>
                            Summary
                        </div>
                        <button class="copy-btn" data-copy="summary">Copy</button>
                    </div>
                    <div class="result-content empty" id="summary" aria-live="polite">
                        Your five-point summary will appear here.
                    </div>
                </article>

                <article class="result-card">
                    <div class="result-header">
                        <div class="result-title">
                            <div class="result-icon">in</div>
                            LinkedIn Post
                        </div>
                        <button class="copy-btn" data-copy="linkedin_post">Copy</button>
                    </div>
                    <div class="result-content empty" id="linkedin_post" aria-live="polite">
                        Your LinkedIn post will appear here.
                    </div>
                </article>

            </div>
        </section>

        <footer>
            Content House &nbsp;·&nbsp; Powered by Flask and Groq
        </footer>

    </main>
</div>

<script>
    const form = document.getElementById("contentForm");
    const topicInput = document.getElementById("topic");
    const generateBtn = document.getElementById("generateBtn");
    const clearBtn = document.getElementById("clearBtn");
    const loadingIndicator = document.getElementById("loadingIndicator");
    const loadingText = document.getElementById("loadingText");
    const errorMessage = document.getElementById("errorMessage");
    const resultSubtitle = document.getElementById("resultSubtitle");

    const resultIds = [
        "ideas",
        "article",
        "summary",
        "linkedin_post"
    ];

    const stepNames = [
        "Generating ideas...",
        "Creating your article...",
        "Summarizing the article...",
        "Writing your LinkedIn post..."
    ];

    let isGenerating = false;
    let currentRequest = null;

    function setStep(number, status) {
        const card = document.getElementById("step" + number);
        const state = document.getElementById("state" + number);

        card.classList.remove("running", "done");

        if (status === "running") {
            card.classList.add("running");
            state.textContent = "◌ In progress";
        } else if (status === "done") {
            card.classList.add("done");
            state.textContent = "✓ Completed";
        } else if (status === "error") {
            state.textContent = "! Failed";
        } else {
            state.textContent = "○ Waiting";
        }
    }

    function setLoading(loading) {
        isGenerating = loading;
        generateBtn.disabled = loading;
        clearBtn.disabled = loading;
        topicInput.disabled = loading;

        generateBtn.textContent = loading
            ? "Generating..."
            : "✦ Generate Content";

        loadingIndicator.style.display = loading ? "block" : "none";
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = "block";
    }

    function clearError() {
        errorMessage.textContent = "";
        errorMessage.style.display = "none";
    }

    function resetResults() {
        const placeholders = {
            ideas: "Your five content ideas will appear here.",
            article: "Your complete article will appear here.",
            summary: "Your five-point summary will appear here.",
            linkedin_post: "Your LinkedIn post will appear here."
        };

        resultIds.forEach(id => {
            const element = document.getElementById(id);
            element.textContent = placeholders[id];
            element.classList.add("empty");
        });

        for (let i = 1; i <= 4; i++) {
            setStep(i, "waiting");
        }

        resultSubtitle.textContent = "Your results will appear here.";
    }

    form.addEventListener("submit", async function(event) {
        event.preventDefault();

        if (isGenerating) return;

        const topic = topicInput.value.trim();

        if (!topic) {
            showError("Please enter a topic before generating content.");
            topicInput.focus();
            return;
        }

        clearError();
        resetResults();
        setLoading(true);

        let activeStep = 1;

        currentRequest = new AbortController();

        try {
            const response = await fetch("/generate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ topic: topic }),
                signal: currentRequest.signal
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Unable to generate content.");
            }

            const results = [
                data.ideas,
                data.article,
                data.summary,
                data.linkedin_post
            ];

            for (let i = 0; i < 4; i++) {
                activeStep = i + 1;

                loadingText.textContent = stepNames[i];
                setStep(activeStep, "running");

                // Display each result only after the complete chain
                // has returned from the server.
                const element = document.getElementById(resultIds[i]);
                element.textContent = results[i] || "No content returned.";
                element.classList.remove("empty");

                setStep(activeStep, "done");
            }

            resultSubtitle.textContent =
                "Content generated successfully for: " + topic;

        } catch (error) {
            if (error.name === "AbortError") {
                return;
            }

            showError(error.message || "Something went wrong.");

            if (activeStep >= 1 && activeStep <= 4) {
                setStep(activeStep, "error");
            }

        } finally {
            currentRequest = null;
            setLoading(false);
        }
    });

    clearBtn.addEventListener("click", function() {
        if (isGenerating) return;

        topicInput.value = "";
        clearError();
        resetResults();
        topicInput.focus();
    });

    document.querySelectorAll("[data-copy]").forEach(button => {
        button.addEventListener("click", async function() {
            const id = this.dataset.copy;
            const element = document.getElementById(id);

            if (element.classList.contains("empty")) {
                showError("Generate content before copying a result.");
                return;
            }

            try {
                await navigator.clipboard.writeText(element.textContent);

                const originalText = this.textContent;
                this.textContent = "Copied!";

                setTimeout(() => {
                    this.textContent = originalText;
                }, 1500);

            } catch (error) {
                showError(
                    "Clipboard access failed. Select and copy the text manually."
                );
            }
        });
    });
</script>

</body>
</html>
"""


# ============================================================
# STEP 4: FLASK ROUTES
# ============================================================

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)


@app.route("/generate", methods=["POST"])
def generate_content():
    data = request.get_json(silent=True) or {}
    topic = data.get("topic", "").strip()

    if not topic:
        return jsonify({
            "error": "Please enter a valid topic."
        }), 400

    if len(topic) > 500:
        return jsonify({
            "error": "Topic must not exceed 500 characters."
        }), 400

    try:
        # Chain 1: Generate ideas
        print("\nSTEP 1: Generating content ideas...")
        ideas = generate_ideas(topic)

        # Chain 2: Create article
        print("\nSTEP 2: Creating an article...")
        article = create_article(topic, ideas)

        # Chain 3: Summarize article
        print("\nSTEP 3: Creating summary...")
        summary = create_summary(article)

        # Chain 4: Create LinkedIn post
        print("\nSTEP 4: Creating LinkedIn post...")
        linkedin_post = create_linkedin_post(topic, summary)

        print("\nPrompt chaining completed successfully!")

        return jsonify({
            "ideas": ideas,
            "article": article,
            "summary": summary,
            "linkedin_post": linkedin_post
        })

    except Exception as error:
        # Keep the detailed error in the terminal for debugging.
        app.logger.exception("Content generation failed")

        return jsonify({
            "error": (
                "Content generation failed. Please check your Groq "
                "API key, model availability, internet connection, "
                "and terminal logs. Details: " + str(error)
            )
        }), 500


# ============================================================
# STEP 5: START THE FLASK APPLICATION
# ============================================================

if __name__ == "__main__":
    app.run(debug=True, port=5000)
