# Embedding Extraction for Context-Augmented Queries

This repository contains code for extracting text fragments, converting them into embeddings, and using them in context-augmented queries. By using embeddings, you can represent and compare text in a mathematical way, enabling efficient search and retrieval of relevant information from your dataset.

## Repository Structure

> For the version that works best with OpenAI's newer SDK (version > 1.0.0), see scripts in folder `Newer OpenAI SDK`. For legacy versions see `Older OpenAI SDK`.

- `extract_text.py`: Script for extracting text from all HTML or PDF documents present in a given folder.
- `preprocess_text.py`: Script to break up the data into chunks and clean it up.
- `create_embeddings.py`: Script for converting the extracted text fragments into embeddings using pre-trained models.
- `context_augmented_queries.py`: Script for performing context-augmented queries on the embeddings.

## Setup and Installation

1. Clone this repository:

```
git clone https://github.com/lperezmo/embedding-extraction.git
```


2. Install required dependencies:

```
pip install -r requirements.txt
```

## Functionality

1. Extract raw text from your data sources using the `extract_text.py` script.

2. Clean up the text data and break into text fragments from your data sources using the `preprocess_text.py` script.

3. Create embeddings for the extracted text fragments using the `create_embeddings.py` script.

4. Create context-augmented queries based on the embeddings using the `context_augmented_queries.py` script.

## Usage

1. Copy into the folder you are working on and import into your work environment, whether that is a Python script, a jupyter notebook, a Dash application, or a Streamlit application.

2. -OR- Just copy and paste the functions into your code.😊


## Customization

You can customize the text extraction, embedding generation, and context-augmented query process by modifying the respective scripts to suit your specific use case.

## Contributing

Contributions to this repository are welcome! Feel free to open a pull request or create an issue if you encounter any problems or have suggestions for improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
