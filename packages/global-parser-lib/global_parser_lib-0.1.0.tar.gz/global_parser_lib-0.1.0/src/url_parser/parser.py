

from typing import Optional
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from langdetect import detect
from pymongo import MongoClient
import hashlib
import datetime
from fastapi import APIRouter
import os
import chardet
from src.utils.classifers.sustainability_hf import classify_sustainability_batch
from src.parser.file import parse_pdf
import requests
import tempfile
router = APIRouter()

# MongoDB setup
MONGODB_URI=os.getenv('MONGODB_URI')
client = MongoClient(MONGODB_URI)  # Update with your MongoDB URI if needed
# Global variables
db = client["WebCrawlerDB"]  # Single persistent database
collection = db["WebContent"]  # Collection for individual URL records
master_collection = db["MasterRecord"]  # Collection for the master record
sent_from = None

# Initialize sent_from variable
def initialize_sent_from(sent=None):
    global sent_from
    sent_from = sent

# Global statistics tracking
total_sublinks = 0
fetched_sublinks = 0
error_count = 0
saved_count = 0
skipped_urls = []

RELEVANT_TOPICS = [
    "renewable", "energy", "carbon", "waste", "hydrogen", "climate",
    "urban", "sustainability", "electric", "recycling", "battery",
    "water", "wind", "green", "storage", "startup"
]

HF_TOKEN=os.getenv("HF_TOKEN")
API_URL = os.getenv("VAIA_SUSTAINABILITY_CLASSIFIER_API_URL")
headers = {
	"Accept" : "application/json",
	"Authorization": f"Bearer {HF_TOKEN}",
	"Content-Type": "application/json" 
}
# Utility Functions
def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.scheme) and bool(parsed.netloc)

def generate_content_hash(content):#
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    print(response)
    return response

def is_english(text):
    try:
        return detect(text) == 'en'
    except:
        return False

def is_relevant_content(content): #Sustainability Classifier
    content_lower = content.lower()
    for topic in RELEVANT_TOPICS:
        if topic in content_lower:
            return True
    return False

def get_aggregated_data_all_chunks(url):#
    try:
        master_record = master_collection.find_one({"url": url})
        if not master_record or not master_record.get("all_data"):
            raise ValueError(f"No aggregated data found for the URL: {url}")
        return master_record["all_data"]
    except Exception as e:
        print(f"Error while fetching aggregated data: {e}")
        return "No data"

# Fetch Function
async def fetch(session, url, retries=3):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    timeout = aiohttp.ClientTimeout(total=15)
    for attempt in range(retries):
        try:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    raw_content = await response.read()
                    detected_encoding = chardet.detect(raw_content)['encoding'] or 'utf-8'
                    return {"content": raw_content.decode(detected_encoding, errors='ignore'), "access": "permitted"}
                elif response.status == 403:
                    return {"content": None, "access": "restricted"}
                print(f"Attempt {attempt + 1}: Failed to fetch {url} with status {response.status}")
        except Exception as e:
            print(f"Error fetching {url} on attempt {attempt + 1}: {e}")
    return {"content": None, "access": "restricted"}  # Assuming any persistent failure is a restriction


# Content Extraction and Processing
async def get_content_from_url_async_su(url, depth=2, visited=None, master_record=None, main_domain=None):
    global total_sublinks, fetched_sublinks, error_count, saved_count

    if visited is None:
        visited = set()

    if main_domain is None:
        main_domain = urlparse(url).netloc

    if url in visited or depth <= 0:
        return ""

    if not is_valid_url(url):
        print(f"Invalid URL skipped: {url}")
        skipped_urls.append(url)
        return ""

    visited.add(url)

    if master_record is None:
        master_record = master_collection.find_one({"url": url}) or {
            "url": url,
            "all_data": "",
            "hash": "",
            "sublinks": [],
            "pdf_links": [],  # Initialize pdf_links array
            "LastUpdated": datetime.datetime.utcnow(),
            "access": "unknown"  # Initialize access status
        }
        if "_id" not in master_record:
            master_record["_id"] = master_collection.insert_one(master_record).inserted_id

    async with aiohttp.ClientSession() as session:
        result = await fetch(session, url)
        html = result["content"]
        access_status = result["access"]
        
        # Update master record with access status
        master_record["access"] = access_status
        master_collection.update_one({"_id": master_record["_id"]}, {"$set": {"access": access_status}})
        is_pdf = url.lower().endswith('.pdf')
        
        if not html:
            error_count += 1
            print(f"Not able to extract html. Access status: {access_status}")
            
            # Even with no HTML, create a record with the access status
            record = {
                "URL": url,
                "Content": "",
                "ContentHash": generate_content_hash(""),
                "LastCrawled": datetime.datetime.utcnow(),
                "Score": 0,
                "access": access_status,
            }
            collection.insert_one(record)
            saved_count += 1
            
            return ""

        soup = BeautifulSoup(html, 'html.parser')
        content_sections = []
        score = 0

        # Find and store PDF links
        pdf_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(url, href)
            if full_url.lower().endswith('.pdf'):
                pdf_links.append(full_url)
                if "pdf_links" not in master_record:
                    master_record["pdf_links"] = []
                if full_url not in master_record["pdf_links"]:
                    master_record["pdf_links"].append(full_url)
                    # Update MongoDB with new PDF link
                    master_collection.update_one(
                        {"_id": master_record["_id"]},
                        {"$addToSet": {"pdf_links": full_url}}
                    )
                    
                    # Process PDF content
                    try:
                        # Download PDF content
                        async with session.get(full_url) as pdf_response:
                            if pdf_response.status == 200:
                                # Create a temporary file to store the PDF
                                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
                                    temp_pdf.write(await pdf_response.read())
                                    temp_pdf_path = temp_pdf.name

                                try:
                                    
                                    pdf_content = parse_pdf(temp_pdf_path)
                                    
                                    # Store PDF content in WebContent collection
                                    pdf_record = {
                                        "URL": full_url,
                                        "Content": pdf_content,
                                        "ContentHash": generate_content_hash(pdf_content),
                                        "LastCrawled": datetime.datetime.utcnow(),
                                        "Score": score,
                                        "access": "permitted",
                                        "is_pdf": True,
                                        "source_url": url  # Store the URL where this PDF was found
                                    }
                                    collection.insert_one(pdf_record)
                                    
                                   
                                    warmup_payload = {
                                    "inputs": ["warmup"],
                                    "parameters": {"candidate_labels": ["sustainability-related", "not sustainability-related"]}
                                    }
                                    warmup_completed = False
                                    while not warmup_completed:
                                        try:
                                            print("Sending warmup query...")
                                            response = (query(warmup_payload))
                                            if str(response) == "<Response [200]>":
                                                warmup_completed = True
                                                print("Warmup completed.")
                                            else:
                                                print(f"Warmup failed: {response}. Retrying...")
                                        except Exception as e:
                                            print(f"Warmup query failed: {e}. Retrying...")
                                    sustainabilty_relevant, pdf_score = classify_sustainability_batch([pdf_content[:1000]])
                                    
                                    if sustainabilty_relevant:
                                        # Update the record with sustainability score
                                        collection.update_one(
                                            {"_id": pdf_record["_id"]},
                                            {"$set": {"Score": pdf_score}}
                                        )
                                        
                                        # Add PDF content to the master record's all_data
                                        pdf_section = f"\nPDF Document: {os.path.basename(full_url)}\n{'=' * 50}\n{pdf_content}\n{'=' * 50}\n"
                                        master_record["all_data"] += pdf_section
                                        
                                        # If we're building combined_content, add the PDF content to it
                                        if 'combined_content' in locals():
                                            combined_content += pdf_section
                                        else:
                                            combined_content = pdf_section
                                        
                                        # Update master record with the new content
                                        master_collection.update_one(
                                            {"_id": master_record["_id"]},
                                            {"$set": {"all_data": master_record["all_data"]}}
                                        )
                                    
                                finally:
                                    # Clean up temporary PDF file
                                    try:
                                        os.unlink(temp_pdf_path)
                                    except Exception as e:
                                        print(f"Error deleting temporary PDF file: {e}")
                    except Exception as pdf_error:
                        print(f"Error processing PDF {full_url}: {pdf_error}")

        # Only check for sustainability relevance if depth > 0 (not the initial URL)
        check_relevance = (depth < 2 and sent_from != "vaia_client")
        
        if sent_from != "vaia_client":
            # Extract text for classification
            paragraphs = soup.find_all("p")
            paragraph_text = " ".join([p.get_text(strip=True) for p in paragraphs])
            
            # Try alternative text extraction methods if needed
            if not paragraph_text:
                headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                heading_text = " ".join([h.get_text(strip=True) for h in headings])
                paragraph_text = heading_text
            
            if not paragraph_text:
                content_divs = [div for div in soup.find_all('div') if div.get_text(strip=True)]
                div_text = " ".join([div.get_text(strip=True) for div in content_divs[:10]])
                paragraph_text = div_text
            
            if not paragraph_text:
                paragraph_text = soup.get_text(strip=True)
            
            # If we still have no text, handle empty content
            if not paragraph_text:
                print(f"No text content found in {url}")
                record = {
                    "URL": url,
                    "Content": "",
                    "ContentHash": generate_content_hash(""),
                    "LastCrawled": datetime.datetime.utcnow(),
                    "Score": 0,
                    "access": access_status
                }
                collection.insert_one(record)
                saved_count += 1
                return "empty"
            
            # Skip relevance check for initial URL (depth=2)
            if check_relevance:
                # Classify content for sustainability relevance
                classification_text = paragraph_text[:1000]
                print(f"Checking relevance for URL {url} (depth {depth})")
                
                # Run the warmup
                warmup_payload = {
                    "inputs": ["warmup"],
                    "parameters": {"candidate_labels": ["sustainability-related", "not sustainability-related"]}
                }
                warmup_completed = False
                while not warmup_completed:
                    try:
                        print("Sending warmup query...")
                        response = (query(warmup_payload))
                        if str(response) == "<Response [200]>":
                            warmup_completed = True
                            print("Warmup completed.")
                        else:
                            print(f"Warmup failed: {response}. Retrying...")
                    except Exception as e:
                        print(f"Warmup query failed: {e}. Retrying...")
                
                # Check sustainability relevance
                sustainabilty_relevant, score = classify_sustainability_batch([classification_text])
                print(f"Score: {score}")
                print("Sustainability Relevant:", sustainabilty_relevant)
                
                # Skip non-relevant content
                if not sustainabilty_relevant:
                    print(f"Skipping {url}: content not relevant to sustainability.")
                    record = {
                        "URL": url,
                        "Content": "",
                        "ContentHash": generate_content_hash(""),
                        "LastCrawled": datetime.datetime.utcnow(),
                        "Score": score,
                        "access": access_status,
                        "skipped_reason": "not sustainability relevant"
                    }
                    collection.insert_one(record)
                    saved_count += 1
                    return "empty"
            else:
                print(f"Skipping relevance check for initial URL {url} (depth {depth})")
            
            # Extract structured content
            for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                heading_text = heading.get_text(strip=True)
                if heading_text and is_english(heading_text):
                    section_text = []
                    sibling = heading.find_next_sibling()
                    while sibling and sibling.name not in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                        if sibling.name == 'p':
                            paragraph_text = sibling.get_text(strip=True)
                            if is_english(paragraph_text):
                                section_text.append(paragraph_text)
                        sibling = sibling.find_next_sibling()
                    if section_text:
                        content_sections.append(f"{heading_text}\n{'-' * len(heading_text)}\n" + "\n".join(section_text))

            combined_content = "\n\n".join(content_sections)

        else:
            all_text = soup.get_text()
            print(soup.get_text())
            combined_content = all_text
            
        if combined_content.strip():
            content_hash = generate_content_hash(combined_content)
            record = {
                "URL": url,
                "Content": combined_content,
                "ContentHash": content_hash,
                "LastCrawled": datetime.datetime.utcnow(),
                "Score": score,
                "access": access_status,
                "is_pdf": is_pdf,

            }
            collection.insert_one(record)
            saved_count += 1

            if content_hash != master_record.get("hash"):
                sublink_obj = {"Id": record["_id"], "url": url, "data": combined_content, "hash": content_hash}
                master_record["all_data"] += f"\n\n{combined_content}"
                master_record["sublinks"].append(sublink_obj)
                master_record["hash"] = content_hash
                master_record["LastUpdated"] = datetime.datetime.utcnow()
                master_collection.update_one({"_id": master_record["_id"]}, {"$set": master_record})

        links = [
            (urljoin(url, link['href']), depth - 1)
            for link in soup.find_all('a', href=True)
            if urljoin(url, link['href']).startswith('http') and urljoin(url, link['href']) not in visited
        ]

        if links:
            tasks = [get_content_from_url_async_su(link[0], link[1], visited, master_record, main_domain) for link in links]
            await asyncio.gather(*tasks)
    
    print(combined_content if 'combined_content' in locals() else "No content")
    return combined_content if 'combined_content' in locals() and combined_content.strip() else "empty"

async def start_crawl_async(url, depth=2):#
    print(f"Starting immediate crawl for {url}")
    await get_content_from_url_async_su(url, depth)
    print("Immediate crawl completed.")

async def extract_text_from_url(url,frequency:Optional[str]=None,sent_from:Optional[str]=None):
    print(f"Starting crawl for {url} with frequency {frequency} from {sent_from}")
    initialize_sent_from(sent=sent_from)
    if sent_from=="vaia_client":
        print("Sent from vaia_client")
        await start_crawl_async(url, depth=0)
    else:
        print("Sent from training")
        await start_crawl_async(url, depth=2)    
    text= get_aggregated_data_all_chunks(url)
    return text