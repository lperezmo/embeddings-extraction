#--------------------------------------------------------#
# Import Libraries
#--------------------------------------------------------#
import os
import numpy as np
from time import sleep
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity

#--------------------------------------------------------#
# OpenAI Client - no need to pass api key
# as long as it's an env variable named OPENAI_API_KEY
# You can create in script as 
#       os.environ['OPENAI_API_KEY'] = 'your_key_here'
#--------------------------------------------------------#
client = OpenAI()

#--------------------------------------------------------#
# Define function to get top-k results
#--------------------------------------------------------#

def get_top_k_results_text(df, query_text, embed_model='text-embedding-3-small', n=3):
    # create embeddings (try-except added to avoid RateLimitError)
    # Added a max of 5 retries
    max_retries = 2
    retry_count = 0
    done = False

    while not done and retry_count < max_retries:
        try:
            res = client.embeddings.create(input=query_text, model=embed_model)
            done = True
        except Exception as e:
            # print(f"Error creating embeddings for batch {i}: {e}")
            retry_count += 1
            sleep(5)
    query_embedding = res.data[0].embedding

    # Compute cosine similarity
    similarities = cosine_similarity([query_embedding], list(df['embedding']))
    
    # Find top-k indices and metadata
    top_k_indices = np.argsort(similarities[0])[-n:][::-1]
    top_k_results = df.iloc[top_k_indices]

    # Join the text of the top-k results
    joined_text = ' '.join(list(top_k_results['text']))

    return joined_text

#--------------------------------------------------------#
# Context-Augmented Query
#--------------------------------------------------------#

def retrieve(query, df, limit_of_context = 3750, embed_model = 'text-embedding-3-small'):
    """
    Retrieve relevant contexts from the dataset and build a prompt for the question answering model.

    Parameters
    ----------
    query : str
        The query to answer.
    df : pandas.DataFrame
        The DataFrame containing the embedding vectors and metadata.
    limit_of_context : int
        The maximum number of characters to use for the context.
    embed_model : str
        The embedding model to use.
    
    Returns
    -------
    prompt : str
        The prompt to use for the question answering model.
    """
    # get relevant contexts
    contexts = get_top_k_results_text(df, query, embed_model=embed_model, n=3)

    # Limit the number of characters
    contexts = contexts[:limit_of_context]

    # build our prompt with the retrieved contexts included
    prompt = (
        f"Answer the question based on the context below.\n\n"+
        f"Context:\n {contexts}\n\n"+f"Question: {query}\nAnswer:"
    )
    return prompt
