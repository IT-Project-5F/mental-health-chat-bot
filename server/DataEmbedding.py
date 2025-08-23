'''
This is the script to translate text data into embedding models and should only be used once 
'''


from langchain_openai import OpenAIEmbeddings
import tiktoken
import pandas as pd
from dotenv import load_dotenv


from dotenv import load_dotenv

load_dotenv() 

df = pd.read_csv('mental_health_services_nwmphn_dataset.csv')
df["index"] = range(1, len(df) + 1)

#Calculate the cost for the embedding for the entire content 

def num_token_from_string(string : str, encoding_name = "cl100k_base") -> int: 
 if not string : 
    return 0
 encoding_model = tiktoken.get_encoding(encoding_name) 
 num_tokens = len(encoding_model.encode(string)) 
 return num_tokens 

def get_essay_length(essay): 
  word_list = essay.split() 
  num_words = len(word_list) 
  return word_list 

def get_embedding_cost(num_tokens): 
   return num_tokens / 1000 * 0.0002

def get_total_embeddings_cost(): 
   total_tokens = 0
   for i in range(len(df.index)): 
       text = df.iloc[i].to_json() 
       token_len = num_token_from_string(text) 
       total_tokens += token_len
   total_cost = get_embedding_cost(total_tokens) 
   return total_cost

# Create a smaller chunk of contents 
def splitting_dataset(MAX_CHUNK_TOKENS = 512): 
  new_list = [] 
  for i in range(len(df.index)): 
    text = df.iloc[i].to_json() 
    token_len = num_token_from_string(text) 
    if token_len <= MAX_CHUNK_TOKENS : 
      new_list.append([
        df['index'][i], 
        token_len, 
        text 
      ]) 
    else : 
      # 1 token ~ 3 / 4 * (word) 
      # 512 tokens ~ 512 * 3 / 4 words 
      start = 0 
      ideal_token_size = MAX_CHUNK_TOKENS 
      ideal_word_size = int(ideal_token_size  // (4 / 3)) 
      end = ideal_word_size 
      words = text.split() 
      words = [x for x in words if x != ' '] 
      total_words = len(words) 
      chunks = total_words // ideal_word_size 
      if total_words % ideal_word_size > 0 : 
         chunks += 1 
      new_content = [] 
      for j in range(chunks): 
        if end > total_words : 
          end = total_words 
        new_content = words[start : end] 
        new_content_string = ' '.join(new_content)
        new_content_token_len = num_token_from_string(new_content_string)
        if new_content_token_len > 0: 
          new_list.append([df['index'][i], new_content_token_len, new_content_string])
        start += ideal_word_size
        end   += ideal_word_size   
  return new_list    



def get_embeddings_vector(text): 
  embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
  response = embedding_model.embed_query(text)
  return response

index_embedding_pairs = [] 
new_list = splitting_dataset() 
for i in range(len(new_list)): 
  text = new_list[i][2] 
  embedding = get_embeddings_vector(text)
  index_embedding_pairs.append([new_list[i][0], new_list[i][1], embedding])

if __name__ == "__main__" : 
 total_cost = get_total_embeddings_cost() 
 print("estimated price to embed the content = $" + str(total_cost))
 df_new = pd.DataFrame(index_embedding_pairs, columns = ['index', 'token_len', 'embeddings'])
 df_new.to_csv('mental_health_embedding.csv', index = False)
