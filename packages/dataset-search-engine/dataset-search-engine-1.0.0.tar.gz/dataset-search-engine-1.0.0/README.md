# DataScouter

DataScouter is a Python library for searching datasets across Hugging Face, Kaggle, and Google Dataset Search using semantic similarity and fuzzy matching.

## Features

- **Multi-Source Search**: Fetch datasets from Hugging Face, Kaggle, and Google Dataset Search.
- **Semantic Search**: Leverages NLP embeddings for improved relevance.
- **Fuzzy Matching**: Enhances search results using string similarity techniques.
- **Optimized Performance**: Utilizes PyTorch for efficient similarity calculations.
- **API Key Support**: Supports authentication for Kaggle dataset access.

## Installation

Install DataScouter via pip:

```sh
pip install datascouter
```

Ensure you have the required dependencies:

```sh
pip install requests beautifulsoup4 transformers fuzzywuzzy torch numpy
```

## Usage

### Basic Search

```python
from datascouter import DataScouter

# Initialize DataScouter
search_engine = DataScouter(kaggle_api_key="your_kaggle_api_key")

# Search for datasets related to 'climate change'
results = search_engine.search_datasets("climate change")

# Print results
for dataset in results:
    print(f"{dataset['source']}: {dataset['name']} - {dataset['description']} (Score: {dataset['score']})")
```

### Using Environment Variable for Kaggle API Key

Instead of passing the API key directly, set it as an environment variable:

```sh
export KAGGLE_API_KEY="your_kaggle_api_key"
```

Then initialize DataScouter without the API key:

```python
search_engine = DataScouter()
```

## How It Works

1. Fetches dataset metadata from Hugging Face, Kaggle, and Google Dataset Search.
2. Uses sentence-transformers to generate embeddings for semantic similarity.
3. Applies fuzzy matching to refine search results.
4. Filters and ranks datasets based on relevance threshold.

## API Reference

### `DataScouter`

#### Initialization

```python
DataScouter(kaggle_api_key=None, relevance_threshold=0.3, source_filter=None)
```

- `kaggle_api_key` (*str*, optional): API key for accessing Kaggle datasets.
- `relevance_threshold` (*float*, default=0.3): Minimum similarity score required for results.
- `source_filter` (*str*, optional): Filter results by a specific source ("Hugging Face", "Kaggle", "Google Dataset Search").

#### `search_datasets`

```python
search_datasets(query: str) -> list
```

- `query` (*str*): Search term for datasets.
- **Returns**: A list of matching datasets sorted by relevance.

## Contributing

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-xyz`.
3. Commit changes: `git commit -m 'Added new feature'`.
4. Push to your branch: `git push origin feature-xyz`.
5. Submit a Pull Request.

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

## Support

If you find DataScouter useful, consider starring the repository on GitHub. For issues, create a GitHub issue or contact us at **your.email@example.com**.
