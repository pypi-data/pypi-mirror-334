import requests
import os
from dotenv import load_dotenv
import logging
import httpx
import asyncio
from fastapi import HTTPException
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = os.getenv("VAIA_SUSTAINABILITY_CLASSIFIER_API_URL")


headers = {
	"Accept" : "application/json",
	"Authorization": f"Bearer {HF_TOKEN}",
	"Content-Type": "application/json" 
}


def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response


def classify_sustainability(text: str):
    payload = {
        "inputs": text,
        "parameters": {"candidate_labels": ["sustainability-related", "not sustainability-related"]},
    }
    response = query(payload)
    return response[0]["labels"][0] == "sustainability-related"


def classify_sustainability_batch(texts: list, batch_size=10):
    results = []
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
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        payload = {
            "inputs": batch,
            "parameters": {"candidate_labels": ["sustainability-related", "not sustainability-related"]}
        }
        try:
            response = query(payload)
        except Exception as e:
            print(f"Error during query:{e}")
            continue
        
        for item in response:
            try:
                print(item)
                if item["scores"][0] and item["scores"][0] > 0.75:
                    results.append(item['sequence'])
                else:
                    print(f"Non-sustainability text found: {item['sequence']}")
            except Exception as e:
                print(f"Error processing item:{e}")
                continue

    print(results)
    
    return results


async def check_api_health(max_retries=10, retry_delay=10):
    async with httpx.AsyncClient() as client:
        for attempt in range(max_retries):
            try:
                test_payload = {
                    "inputs": "test",
                    "parameters": {"candidate_labels": ["sustainability-related", "not sustainability-related"]}
                }
                response = await client.post(
                    API_URL, 
                    headers=headers, 
                    json=test_payload, 
                    timeout=10
                )
                if response.status_code == 200:
                    logging.info("API is warm")
                    return True
            except (httpx.TimeoutException, httpx.RequestError) as e:
                logging.info(f"API not ready (attempt {attempt + 1}/{max_retries}), waiting {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
    return False


async def warm_up_endpoint(session, max_retries=10, delay=15):
    for attempt in range(max_retries):
        async with session.get(API_URL, headers=headers) as response:
            if response.status == 200:
                print("Endpoint is warm.")
                return True
            elif response.status == 503:
                print(f"Endpoint cold, attempt {attempt + 1} to warm it up...")
                await asyncio.sleep(delay)
            else:
                error_message = await response.text()
                print(f"Error while warming up: {error_message}")
                raise HTTPException(status_code=response.status, detail="Error warming up summarization API")

    raise HTTPException(status_code=503, detail="Failed to warm up the summarization API after several attempts")