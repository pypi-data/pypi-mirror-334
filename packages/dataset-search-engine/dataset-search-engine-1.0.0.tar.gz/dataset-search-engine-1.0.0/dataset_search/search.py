import requests
from bs4 import BeautifulSoup
from transformers import AutoModel, AutoTokenizer
from fuzzywuzzy import fuzz
import json
import os
import torch
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DatasetSearchEngine:
    def __init__(self, kaggle_api_key="your_api_key_here", relevance_threshold=0.3, source_filter=None):
        self.hf_api_url = "https://huggingface.co/api/datasets"
        self.kaggle_api_url = "https://www.kaggle.com/datasets"
        self.google_dataset_search_url = "https://datasetsearch.research.google.com/search?query="
        self.kaggle_api_key = kaggle_api_key
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.relevance_threshold = relevance_threshold
        self.source_filter = source_filter
        
        self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        self.model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2").to(self.device)
    
    def fetch_huggingface_datasets(self):
        try:
            response = requests.get(self.hf_api_url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Failed to fetch Hugging Face datasets: {e}")
            return []
    
    def fetch_kaggle_datasets(self):
        if not self.kaggle_api_key:
            logging.warning("Kaggle API key is missing. Skipping Kaggle datasets.")
            return []
        
        headers = {"Authorization": f"Bearer {self.kaggle_api_key}"}
        try:
            response = requests.get(self.kaggle_api_url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Failed to fetch Kaggle datasets: {e}")
            return []
    
    def fetch_google_datasets(self, query):
        try:
            search_url = self.google_dataset_search_url + query.replace(" ", "+")
            response = requests.get(search_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            return [link.get("href") for link in soup.find_all("a") if "dataset" in str(link.get("href"))]
        except requests.RequestException as e:
            logging.error(f"Failed to fetch Google datasets: {e}")
            return []
    
    def encode_text(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True).to(self.device)
        with torch.no_grad():
            embeddings = self.model(**inputs).last_hidden_state.mean(dim=1)
        return embeddings.cpu().numpy().flatten()
    
    def compute_similarity(self, query_embedding, text_embedding):
        return float(np.dot(query_embedding, text_embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(text_embedding)))
    
    def search_datasets(self, query):
        logging.info(f"Searching datasets for query: {query}")
        
        hf_datasets = self.fetch_huggingface_datasets()
        kaggle_datasets = self.fetch_kaggle_datasets()
        google_datasets = self.fetch_google_datasets(query)
        
        query_embedding = self.encode_text(query)
        results = []
        
        for dataset in hf_datasets:
            dataset_text = dataset.get("id", "") + " " + dataset.get("description", "")
            dataset_embedding = self.encode_text(dataset_text)
            similarity = self.compute_similarity(query_embedding, dataset_embedding)
            if similarity >= self.relevance_threshold:
                results.append({"source": "Hugging Face", "name": dataset["id"], "description": dataset.get("description", "No description available"), "score": similarity})
        
        for dataset in kaggle_datasets:
            dataset_text = dataset.get("title", "") + " " + dataset.get("description", "")
            dataset_embedding = self.encode_text(dataset_text)
            similarity = self.compute_similarity(query_embedding, dataset_embedding)
            if similarity >= self.relevance_threshold:
                results.append({"source": "Kaggle", "name": dataset["title"], "description": dataset.get("description", "No description available"), "score": similarity})
        
        for dataset in google_datasets:
            similarity = float(fuzz.partial_ratio(query.lower(), dataset.lower()) / 100)
            if similarity >= self.relevance_threshold:
                results.append({"source": "Google Dataset Search", "name": dataset, "description": "No description available", "score": similarity})
        
        results = sorted(results, key=lambda x: x["score"], reverse=True)
        
        if self.source_filter:
            results = [res for res in results if res["source"] == self.source_filter]
        
        return results

if __name__ == "__main__":
    search_engine = DatasetSearchEngine(kaggle_api_key="d6e7b438128d0a673eea44ece0cf1a83")
    query = input("Enter your dataset search query: ")
    results = search_engine.search_datasets(query)
    print(json.dumps(results, indent=4))
