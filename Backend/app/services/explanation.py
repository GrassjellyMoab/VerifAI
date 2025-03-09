# explanation.py
from flask import Blueprint, request, jsonify
import os
from openai import OpenAI
from dotenv import load_dotenv

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Load environment variables (make sure OPENAI_API_KEY is set in your .env file)
load_dotenv()
explanation_blueprint = Blueprint("explanation_blueprint", __name__)

@explanation_blueprint.route("/", methods=["POST"])
def reasoning_route():
    """
    Args:
        user_text (str): The user's claim.
        supporting_texts (list of str): A list of texts from supporting sources.
        challenging_text (str): The text from a challenging source.
        temperature (float): Optional temperature parameter for the model (default is 0.7).

    Returns:
        str: A concise reasoning summary produced by GPT.
    """

    data = request.get_json()
    user_text = data.get("user_text")
    supporting_texts = data.get("supporting_texts", [])
    min_score = data.get("min_score")
    max_score = data.get("max_score")
    temperature = data.get("temperature")

    # Combine the supporting texts into one block, separated by newlines
    supporting_combined = "\n\n".join(supporting_texts)

    # print(supporting_texts)
    # Build the GPT prompt
    prompt = (
        "You are a fact-checking assistant for a Telegram bot, responsible for verifying the reliability of user claims. "
        "Based on supporting sources and credibility scores, determine whether the claim is highly reliable, unreliable, ambiguous, or false and provide a brief reasoning (2-3 sentences) in clear and simple language.\n\n"
        
        "### Reliability Scoring Guide:\n"
        "- Highly unreliable (min score < -0.3): Sources contradict the claim.\n"
        "- Unreliable (max score < 0.50): No credible sources support the claim.\n"
        "- Ambiguous (max score 0.50 - 0.55): Some support, but evidence is weak.\n"
        "- Reliable (max score > 0.55): Strong evidence from credible sources.\n\n"
        
        f"User's Claim: {user_text}\n\n"
        f"Supporting Sources:\n{supporting_combined}\n\n"
        
        "### Instructions for Your Response:\n"
        "- Start with the verdict (e.g., 'This claim is highly reliable/unreliable/ambiguous because...')\n"
        "- Explain the reasoning in simple and concise terms (2-3 sentences).\n"
        "- Mention supporting or contradicting sources where relevant.\n"
        "- Keep the tone clear and user-friendly—avoid technical jargon, and do not mention the numerical score in the response at all, the users dont need to see the exact score in the response.\n\n"
        
        "### Example Response:\n"
        "'Highly Reliable. This claim is widely reported by multiple credible news sources, including The Straits Times, confirming that Donald Trump is the current president of the USA.'"
    )

    try:
        response = client.chat.completions.create(model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a factual, neutral assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature)
        reasoning_text = response.choices[0].message.content.strip()
        return jsonify({"reasoning_summary": reasoning_text})
    except Exception as e:
        return jsonify({"error": f"Error generating reasoning summary: {e}"}), 500
