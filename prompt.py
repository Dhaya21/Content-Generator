# First create a virtual enviironment folder and activate it ---- this creates a seperate workplace
# Create .env file --> used for strong API key
# Create •gitignore file --> secure the •env file
# install required packages --› python-dotenv , groq --> pip install
# check pakages are installed --› pip list
# Create a python file for build application
# --------------------------------------------------------------------------------------------------

# step 1: Import Required pakages
from dotenv import load_dotenv
import os
from groq import Groq

# Load the environment variable in our python file
load_dotenv()

# -------------------------------------------------------------------------------

# Get the environment variable & store it in the pyton variable
api_key = os.getenv("GROQ_API_KEY")

# ------------------------------------------------------------------------------
# sCheck api_key is loaded successfully or not
if api_key:
    print("API key loaded successfully")
if not api_key:
    print("API key not found")

# ------------------------------------------------------------------------------
# Create the client
client = Groq(api_key=api_key)

# Choose the model that is currently available in the groq account
# If this model is unavailable,check the models page in Groq account
MODEL = "openai/gpt-oss-20b"


# ===============================================================================
# STEP-2: CREATE A RESUAABLE AI FUNCTION
# ==============================================================================
def ask_ai(prompt):
    # Send the prompt to the groq chat compilation API
    response = client.chat.completions.create(
        model=MODEL,
        # Provide the prompt as a user message
        messages=[{"role": "user", "content": prompt}],
        # Control how creative the AI respose can be.
        temperature=0.7,
        # Limit the maximum response length.
        max_tokens=1000,
    )

    # Extract and return the AI generated text.
    return response.choices[0].message.content


# ===============================================================================
# STEP-3: GENERATE IDEAS
# ===============================================================================
def generate_ideas(topic):
    # Create a prompt that asks the AI to generate ideas.
    prompt = f"""
    you are a content planning assistant.
    Generate 5 unique and creative content ideas for the topic:{topic}
    Explain each idea in 2-3 sentences.
    Use a numbered list.
    """
    # Send the prompt to Groq and get the AI generated reponse.
    ideas = ask_ai(prompt)
    # Return the ideas to the next stage.
    return ideas


# ===============================================================================
# STEP-4: CREATE AN ARTICLE
# ===============================================================================
def create_article(topic, ideas):
    # Insert the ideas from step-3 into the next prompt
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

    # Send the new prompt to Groq.
    article = ask_ai(prompt)

    # Return the article to the next stage.
    return article


# ===============================================================================
# STEP-5: SUMMARIZE THE ARTICLE
# ===============================================================================


def create_summary(article):
    # Pass the complete article to the AI for summarization.
    prompt = f"""
    you are a expert content summarizer.

    Summarize the following article into 5 important bullet points.
    
    use simple english.
    preserve the article's main meaning.

    Article:
    {article}
    """
    # Ask Groq to summarize the article.
    summary = ask_ai(prompt)
    # Return the summary to the next stage.
    return summary


# ===============================================================================
# STEP-6: CREATE A LINKEDIN POST
# ===============================================================================
def create_linkedin_post(topic, summary):
    # Use the summary to create a LinkedIn post.
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
    # Send the prompt to Groq.
    post = ask_ai(prompt)
    # Return the final LinkedIn post.
    return post


# ===============================================================================
# STEP-7: RUN THE PROMPT CHAIN
# ===============================================================================
def main():
    # Ask the user for a topic.
    topic = input("Enter a topic: ").strip()

    # Stop if the user does not enter a topic
    if not topic:
        print("Please enter a valid topic.")
        return
    try:
        # Chain 1:
        # Generate ideas from user's topic.
        print("\nSTEP 1: Generating content ideas...")
        ideas = generate_ideas(topic)

        # Display the generated ideas.
        print("\n===== Generated Ideas =====")
        print(ideas)

        # Chain 2:
        # Pass the ideas to the article generation function.
        print("\nSTEP 2: Creating an article...")
        article = create_article(topic, ideas)

        # Display the generated article.
        print("\n===== Article =====")
        print(article)

        # Chain 3:
        # Pass the article to the summary function.
        print("\nSTEP 3: Creating summary...")
        summary = create_summary(article)

        # Display the generated summary.
        print("\n===== Summary =====")
        print(summary)

        # Chain 4:
        # Pass the summary to the LinkedIn post function.
        print("\nSTEP 4: Creating LinkedIn post...")
        linkedin_post = create_linkedin_post(topic, summary)

        # Display the final LinkedIn post.
        print("\n===== LinkedIn Post =====")
        print(linkedin_post)

        # Confirm that all stages completed successfully.
        print("\nprompt chaining completed successfully!")

    except Exception as error:
        # Display an error if an API request or another step fails.
        print("\nSomething went wrong.")
        print("Error: error")


# Run main() only when this file is executed directly.
if __name__ == "__main__":
    main()
