# VerifAI Bot

VerifAI is an AI-driven Telegram bot desgined to combat misinfomration in private messaging apps such as Telegram. Developed for TechFest 2025, VerifAI utilizes Natural Language Processing and AI-Powered image analysis to detect falsehoods

---
## The Problem: Why VerifAi
65% of adults in Singapore struggle to differentiate between real and fake online content. With false information spreading effortlessly through a single forward button, online falsehoods proliferate at an alarming rate. Meanwhile, existing fact-checking tools remain slow, unreliable, and require tedious manual verification. 

## The VerifAI solution 
VerifAI mitigates misinfomration by providing instant, automated fact-checking directly through a Telegram bot. VerifAI aims to combat misinformation by combining text analysis techniques with AI-driven image detection. The two models work independently to assess the credibility of claims and likelihood of AI generated images respectively.

- **Model 1: Claim Verification**  
  Uses natural language processing to extract keywords from an input claim, finds credible sources via Google Custom Search, scrapes content from various formats (HTML, XML, PDF), embeds both the claim and the sourced content, and then compares their vector representations to assess reliability.
  **Features**:
  - **TF-IDF Keyword Extraction:** Identifies key terms from the input claim.
  - **Google Custom Search Integration:** Uses extracted keywords to locate credible online sources.
  - **Content Scraping:** Retrieves text content from various formats (HTML, XML, PDF).
  - **Embedding & Vector Comparison:** Embeds both the claim and scraped content to compare similarity and determine credibility.
  - **Reliability Score** Provides a reliability score using cosine similarity
  - **Explanation of Reliability Score** Compares top sources with original claim and leverages OpenAI GPT4-o to provide users with an in-depth explanation of reliability score

- **Model 2: AI Generator Image Detector**
  With the rise of AI-generated images and online falsehood, manipulated content are harder to detect. VerifAI allows user to verify images, seperating real images from AI images.
  **Features**:
  - **AI-Genereated Image Detection** Determines whether an image is AI-generate and provides a statistical analysis
  - **Heatmap Visualization** Highlights manipulated areas in AI-generated images for better transparency

---

## Tech Stack 
![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white)
| **Category**                 | **Technology Used**                           |
|------------------------------|----------------------------------------------|
| **Programming Language**     | Python 3.x                                   |
| **Natural Language Processing** | `scikit-learn`, `TF-IDF`, `spaCy`    |
| **Web Scraping & Data Extraction** | `BeautifulSoup4`, `pdfminer.six` |
| **AI Image Analysis**        | OpenCV, TensorFlow, PyTorch                 |
| **API Integrations**         | Google Custom Search API, Telegram API      |
| **Bot Framework**            | Python Telegram Bot API                      |
| **Deployment**               | Flask             |


- **Programming Language:** Python 3.x
- **Libraries & Tools:**
  - `scikit-learn` (for TF-IDF and vector operations)
  - `requests` (for HTTP requests)
  - `BeautifulSoup4` (for HTML/XML scraping)
  - PDF parsing libraries (e.g., `pdfminer.six` or similar)
  - Pre-trained models or APIs for AI image detection (as applicable)
  - Google Custom Search API client (ensure you have valid API credentials)
- **Other:** Internet connectivity for API requests and content scraping

---

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/FakeInfoDetector.git
   cd FakeInfoDetector
   ```

2. **Install Dependencies:**
   Create a virtual environment (optional but recommended) and install required packages:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Set Up API Credentials:**
    - Obtain your Google Custom Search API key and set up a Custom Search Engine.
    - Configure your environment variables or update the configuration file (e.g., `config.json`) with your API credentials.


---


*Note: This project is developed for hackathon demonstration purposes. Further improvements and rigorous testing are needed before considering production deployment.*
```
