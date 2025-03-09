# explanation.py

import os
import openai
from dotenv import load_dotenv

# Load environment variables (make sure OPENAI_API_KEY is set in your .env file)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_reasoning_summary(user_text, supporting_texts, challenging_text, temperature=0.7):
    """
    Generates a reasoning summary for the provided claim using GPT-3.5-turbo.

    Args:
        user_text (str): The user's claim.
        supporting_texts (list of str): A list of texts from supporting sources.
        challenging_text (str): The text from a challenging source.
        temperature (float): Optional temperature parameter for the model (default is 0.7).

    Returns:
        str: A concise reasoning summary produced by GPT.
    """
    # Combine the supporting texts into one block, separated by newlines
    supporting_combined = "\n\n".join(supporting_texts)

    # Build the GPT prompt
    prompt = (
            "You are a fact-checking assistant. Below is the user's claim, "
            "followed by excerpts from two supporting sources and one challenging source. "
            "Explain in clear terms how these sources support or refute the claim.\n\n"
            f"User's claim:\n{user_text}\n\n"
            "Supporting sources:\n" + supporting_combined + "\n\n"
                                                            "Challenging source:\n" + challenging_text + "\n\n"
                                                                                                         "Please provide a concise reasoning summary."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a factual, neutral assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        reasoning_text = response["choices"][0]["message"]["content"].strip()
        return reasoning_text
    except Exception as e:
        return f"Error generating reasoning summary: {e}"



# Example usage if running this file directly for testing
if __name__ == "__main__":
    user_claim = "The government has announced a new tax reform."
    supporting = [
        "According to the official press release, a tax reform was introduced to stimulate economic growth.",
        "Reputable news outlets reported detailed policy changes supporting the tax reform."
    ]
    challenging = "An independent analysis suggests that the proposed tax reform is unlikely to have any significant impact, contradicting official statements."
    summary = generate_reasoning_summary(user_claim, supporting, challenging)
    print("Generated Reasoning Summary:")
    print(summary)
