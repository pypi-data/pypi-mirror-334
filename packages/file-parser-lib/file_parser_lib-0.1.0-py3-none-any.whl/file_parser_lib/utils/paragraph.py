import os
import re
import requests
from dotenv import load_dotenv
from utils.validSentence import is_valid_sentence_v2
from utils.classifers.sustainability_hf import query,classify_sustainability_batch
load_dotenv()

HF_TOKEN=os.getenv("HF_TOKEN")
API_URL = os.getenv("VAIA_SUSTAINABILITY_CLASSIFIER_API_URL")

headers = {
	"Accept" : "application/json",
	"Authorization": f"Bearer {HF_TOKEN}",
	"Content-Type": "application/json" 
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    print(response)
    return response
def filtering_paragraphs(text: str, useSustainabilityClassifier: bool, max_words: int = 500):
    def clean_sentence(sentence):
        """Remove numbered list markers like 1., 2., 25., etc."""
        return re.sub(r'^\s*\d+\.\s*', '', sentence).strip()

    # Split the text into paragraphs based on double newlines
    initial_paragraphs = [para.strip() for para in text.split('\n\n') if para.strip()]
    
    # Final list to store processed paragraphs
    final_paragraphs = []

    # Warm up the classifier if required
    if useSustainabilityClassifier:
        warmup_payload = {
            "inputs": ["warmup"],
            "parameters": {"candidate_labels": ["sustainability-related", "not sustainability-related"]}
        }
        warmup_completed = False

        while not warmup_completed:
            try:
                print("Sending warmup query...")
                response=(query(warmup_payload))
                if str(response) == "<Response [200]>":  # Check if response matches expected success string
                    warmup_completed = True
                    print("Warmup completed.")
                else:
                    print(f"Warmup failed: {response}. Retrying...")
            except Exception as e:
                print(f"Warmup query failed: {e}. Retrying...")

    # Process each paragraph
    for paragraph in initial_paragraphs:
        # If paragraph is longer than max_words, split it
        if len(paragraph.split()) > max_words:
            sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', paragraph)
            
            current_paragraph = []
            current_word_count = 0

            for sentence in sentences:
                cleaned_sentence = clean_sentence(sentence)

                # Skip empty sentences
                if not cleaned_sentence:
                    continue

                # Restore punctuation if missing
                if not cleaned_sentence.endswith(('.', '?', '!')):
                    cleaned_sentence += '.'

                # Check sentence validity and sustainability classification
                if not is_valid_sentence_v2(cleaned_sentence):
                    print(f"Invalid sentence: {cleaned_sentence}")
                    continue
                if useSustainabilityClassifier and not classify_sustainability_batch([cleaned_sentence]):
                    print(f"Non-sustainability text found: {cleaned_sentence}")
                    continue

                sentence_words = len(cleaned_sentence.split())

                # If adding this sentence exceeds max_words, finalize the current paragraph
                if current_word_count + sentence_words > max_words:
                    final_paragraphs.append(' '.join(current_paragraph))
                    current_paragraph = []
                    current_word_count = 0

                # Add the sentence to the current paragraph
                current_paragraph.append(cleaned_sentence)
                current_word_count += sentence_words

            # Add the last paragraph if any sentences remain
            if current_paragraph:
                final_paragraphs.append(' '.join(current_paragraph))

        else:
            # If paragraph is within the word limit, keep it as is
            final_paragraphs.append(paragraph)

    return final_paragraphs