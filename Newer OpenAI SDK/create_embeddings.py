#-------------------------------------#
# Import libraries
#-------------------------------------#
import os
import datetime
import pandas as pd
from time import sleep
from openai import OpenAI
from tqdm.auto import tqdm

#--------------------------------------------------------#
# OpenAI Client - no need to pass api key
# as long as it's an env variable named OPENAI_API_KEY
# You can create in script as 
#       os.environ['OPENAI_API_KEY'] = 'your_key_here'
#--------------------------------------------------------#
client = OpenAI()

#----------------------------------------------#
# Create embeddings and append to DataFrame
#----------------------------------------------#

def create_and_append_embeddings(new_data, embed_model = 'text-embedding-3-small'):
    batch_size = 100  # how many embeddings we create and insert at once

    # Create an empty DataFrame (INITIALIZE AT THE BEGINNING OF THE PROCESS ONLY)
    columns = ['file', 'text', 'title', 'headings', 'images', 'folder', 'embedding']
    # df = pd.DataFrame(columns=columns)

    for i in tqdm(range(0, len(new_data), batch_size)):
        # find end of batch
        i_end = min(len(new_data), i+batch_size)
        meta_batch = new_data[i:i_end]
        # get ids (files)
        ids_batch = [x['file'] for x in meta_batch]
        # get texts to encode
        texts = [x['text'] for x in meta_batch]

        # create embeddings (try-except added to avoid RateLimitError)
        # Added a max of 5 retries
        max_retries = 2
        retry_count = 0
        done = False

        while not done and retry_count < max_retries:
            try:
                res = openai.embeddings.create(input=texts, model=embed_model)
                done = True
            except Exception as e:
                print(f"Error creating embeddings for batch {i}: {e}")
                retry_count += 1
                sleep(5)

        if not done:
            print(f"Failed to create embeddings for batch {i} after {max_retries} retries. Skipping this batch.")
            continue

        embeds = [record.embedding for record in res.data]
        meta_batch = [{
            'file': x['file'],
            'text': x['text'],
            'title': x['title'],
            'headings': x['headings'],
            'images': x['images'],
            'folder': x['folder']
        } for x in meta_batch]

        # Append embeddings and metadata to DataFrame
        batch_data = []
        for idx, (emb, meta) in enumerate(zip(embeds, meta_batch)):
            data = {**meta, 'embedding': emb}
            batch_data.append(data)

        batch_df = pd.DataFrame(batch_data, columns=columns)
        df = pd.concat([df, batch_df], ignore_index=True)

    # Shape of the DataFrame
    print(f"The dataframe now has a shape of {df.shape}")

    return df
