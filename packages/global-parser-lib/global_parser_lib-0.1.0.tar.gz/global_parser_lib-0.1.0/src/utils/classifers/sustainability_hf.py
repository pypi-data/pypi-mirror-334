import requests
import os
from dotenv import load_dotenv
import logging
import httpx
import asyncio
from fastapi import HTTPException
from src.config import GlobalConfig
load_dotenv()

def get_headers(config: GlobalConfig = None):
	if not config:
		config = GlobalConfig()
	if not config.huggingface or not config.huggingface.token:
		raise ValueError("Hugging Face token not configured")
	return {
		"Accept": "application/json",
		"Authorization": f"Bearer {config.huggingface.token}",
		"Content-Type": "application/json" 
	}

def query(payload, config: GlobalConfig = None):
	if not config:
		config = GlobalConfig()
	if not config.huggingface or not config.huggingface.sustainability_classifier_url:
		raise ValueError("Sustainability classifier URL not configured")
	headers = get_headers(config)
	response = requests.post(config.huggingface.sustainability_classifier_url, headers=headers, json=payload)
	return response

def classify_sustainability(text: str, config: GlobalConfig = None):
	payload = {
		"inputs": text,
		"parameters": {"candidate_labels": ["sustainability-related", "not sustainability-related"]},
	}
	response = query(payload, config)
	return response[0]["labels"][0] == "sustainability-related"

def classify_sustainability_batch(texts: list, batch_size=10, config: GlobalConfig = None):
	if not config:
		config = GlobalConfig()
	results = []
	warmup_payload = {
		"inputs": ["warmup"],
		"parameters": {"candidate_labels": ["sustainability-related", "not sustainability-related"]}
	}
	warmup_completed = False
	while not warmup_completed:
		try:
			print("Sending warmup query...")
			response = query(warmup_payload, config)
			if str(response) == "<Response [200]>":
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
			response = query(payload, config)
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

async def check_api_health(max_retries=10, retry_delay=10, config: GlobalConfig = None):
	if not config:
		config = GlobalConfig()
	if not config.huggingface or not config.huggingface.sustainability_classifier_url:
		raise ValueError("Sustainability classifier URL not configured")
		
	headers = get_headers(config)
	async with httpx.AsyncClient() as client:
		for attempt in range(max_retries):
			try:
				test_payload = {
					"inputs": "test",
					"parameters": {"candidate_labels": ["sustainability-related", "not sustainability-related"]}
				}
				response = await client.post(
					config.huggingface.sustainability_classifier_url, 
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

async def warm_up_endpoint(session, max_retries=10, delay=15, config: GlobalConfig = None):
	if not config:
		config = GlobalConfig()
	if not config.huggingface or not config.huggingface.sustainability_classifier_url:
		raise ValueError("Sustainability classifier URL not configured")
		
	headers = get_headers(config)
	for attempt in range(max_retries):
		async with session.get(config.huggingface.sustainability_classifier_url, headers=headers) as response:
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