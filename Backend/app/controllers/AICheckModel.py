from app.services.autoDetectCheck import auto_detect_and_check

def aiChecker_model(message, user_text, bot):
    # First, attempt to analyze the input with the auto_detect_and_check function
    result = auto_detect_and_check(user_text)

    if not result:
        bot.send_message(message.chat.id, "Error: Could not analyze the input. Please check the URL or file path.")
        return

    # Determine the type of input based on the API response.
    # We assume that if the "report" has a "confidence" field directly, it might be a voice file.
    input_type = 'image'
    if "report" in result and "confidence" in result["report"]:
        input_type = 'voice'

    # Begin building the output message
    output = "===== AIorNOT ANALYSIS RESULTS =====\n"

    if input_type == 'image':
        verdict = result["report"].get("verdict", "N/A")
        output += f"Verdict: {verdict.upper()}\n"

        # Include AI vs. Human confidence scores if available
        if "ai" in result["report"] and "confidence" in result["report"]["ai"]:
            ai_confidence = result["report"]["ai"]["confidence"]
            human_confidence = result["report"]["human"]["confidence"]
            output += f"AI confidence: {ai_confidence:.2%}\n"
            output += f"Human confidence: {human_confidence:.2%}\n"

            # If there is a generator breakdown, include that information.
            if "generator" in result["report"]:
                output += "\nAI Generator Analysis:\n"
                for generator, details in result["report"]["generator"].items():
                    generator_name = generator.replace("_", " ").title()
                    confidence = details.get("confidence", 0)
                    is_detected = details.get("is_detected", False)
                    status = "DETECTED" if is_detected else "Not Detected"
                    output += f"  {generator_name}: {status} (confidence: {confidence:.2%})\n"

        # Include any facet information (e.g. quality or NSFW checks)
        if "facets" in result:
            output += "\nImage Quality Checks:\n"
            for facet, details in result["facets"].items():
                is_detected = details.get("is_detected", False)
                if facet == "quality":
                    quality_status = "PASS" if is_detected else "FAIL"
                    output += f"  Image Quality: {quality_status}\n"
                elif facet == "nsfw":
                    nsfw_status = "Not Detected" if not is_detected else "Detected"
                    output += f"  NSFW Content: {nsfw_status}\n"

    elif input_type == 'voice':
        verdict = result["report"].get("verdict", "N/A")
        confidence = result["report"].get("confidence", 0)
        duration = result["report"].get("duration", 0)
        output += f"Verdict: {verdict.upper()}\n"
        output += f"Confidence: {confidence:.2%}\n"
        output += f"Audio Duration: {duration} seconds\n"

    else:
        output += "Unknown input type.\n"

    output += f"\nReport ID: {result.get('id', 'N/A')}\n"
    output += f"Created At: {result.get('created_at', 'N/A')}\n"
    output += "===================================="

    # Send the analysis result to the Telegram chat
    bot.send_message(message.chat.id, output)
