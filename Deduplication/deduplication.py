import os
import pandas as pd
from datasketch import MinHash
from simhash import Simhash
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# from fuzzywuzzy import fuzz
from rapidfuzz import fuzz


# Creating a Pandas DataFrame our our entire Data.
path = '/hdfs2/dhruvpatel/RawDataset'
folders = os.listdir(path)

dataset = {'id': [],
      'title': [],
      'article': []}
i = 1
for folder_name in tqdm(folders, ncols = 100, desc = "importing corpus data"):
    folder = os.listdir(os.path.join(path,folder_name))
    for id,file_name in enumerate(folder):
      dataset['id'].append(i+1)
      i += 1
      dataset['title'].append(file_name)
      article = open(os.path.join(path,folder_name,file_name),"r",encoding = 'utf-8')
      dataset['article'].append(article.read())

dataset = pd.DataFrame(dataset)
print(f"total number of articles: {len(dataset)}")


### Using Minimun Hashing   
df = dataset
df['hash'] = "None"

### Creating token for Min Hash
for i,article in tqdm(enumerate(df['article']), ncols = 100, desc = "creating tokens for minhash"):
    m = MinHash()
    for token in article.split():
        m.update(token.encode('utf-8'))
    df.iloc[i,-1] = m

print("------------------ MIN HASH ------------------")

threshold = 0.8

index_list =[]

for i in tqdm(range(len(df)), ncols = 100, desc = "deduplicating using minhash"):
    hash_val = df.iloc[i,-1]

    for j in range(len(df)):
        if i != j:
            similarity = hash_val.jaccard(df.iloc[j,-1])
            if similarity > threshold:
                index_list.append(df.iloc[j,0])

print(f"Length before Deduplication: {len(df)}")
df = df[~df['id'].isin(index_list)]
print(f"Length after Deduplication: {len(df)}")

for i in tqdm(range(len(df)), ncols = 100, desc = "storing the deduplicated files"):
    file = open(f"/hdfs2/dhruvpatel/Dedup_data/Min_Hash/File{i+1}.txt","w",encoding="utf-8" )
    file.write(df.iloc[i,2])
    file.close()

### Using Similarity Hashing
df = dataset 
df['hash'] = None

# Calculating Sim Hah for 128 bits.
for i,article in tqdm(enumerate(df['article']), ncols = 100, desc = "calculating simhash for 128bits"):
    df.iloc[i,-1] = Simhash(article, f = 128)

# Calculating Hamming Distance for each value.
print("|------------------ SIM HASH ------------------|")

threshold = 80

index_list =[]

for i in tqdm(range(len(df)), ncols = 100, desc = "calculating hamming distance for each value"):
    hash_val = df.iloc[i,-1]

    for j in range(len(df)):
        if i != j:
            similarity = hash_val.distance(df.iloc[j,-1])
            if similarity > threshold:
                index_list.append(df.iloc[j,0])

print(f"Length before Deduplication: {len(df)}")
df = df[~df['id'].isin(index_list)]
print(f"Length after Deduplication: {len(df)}")

for i in tqdm(range(len(df)), ncols = 100, desc = "storing deduplicated files"):
    file = open(f"/hdfs2/dhruvpatel/Dedup_data/Sim_Hash/File{i+1}.txt","w",encoding="utf-8" )
    file.write(df.iloc[i,2])
    file.close()


### Using TF-IDF Cosine Similarity
print("|------------------ Tf-IDF ------------------|")
df = dataset
text = df['article']
vectorizer = TfidfVectorizer().fit_transform(text)
vectors = vectorizer.toarray()
print(f"size of Tf-Idf vector: {vectors.shape}")

index_list = []
threshold = 0.8
for i,vector1 in tqdm(enumerate(vectors), ncols = 100, desc = "calculating cosine-similarity"):
    for j,vector2 in enumerate(vectors):
        if i != j:
            similarity = cosine_similarity([vector1], [vector2])
            if similarity > threshold:
                index_list.append(j)

print(f"Length before Deduplication:{len(df)}")
df = df[~df['id'].isin(index_list)]
print(f"Length after Deduplication: {len(df)}")

for i in tqdm(range(len(df)), ncols = 100, desc = "storing deduplicated files"):
    file = open(f"/hdfs2/dhruvpatel/Dedup_data/Tf_idf/File{i+1}.txt","w",encoding="utf-8" )
    file.write(df.iloc[i,2])
    file.close()


### Using Fuzzy
print("|------------------  Fuzzy ------------------|")
df = dataset

text = df['article']
index_list =[]
threshold = 80

for doc1 in tqdm(range(len(text)), ncols = 100, desc = "calculating similarity between articles"):
    for doc2 in range(len(text)):
        if doc1 != doc2:
            similarity = fuzz.ratio(text[doc1],text[doc2])

            if similarity > threshold:
                index_list.append(doc2)

print(f"Length before Deduplication:{len(df)}")
df = df[~df['id'].isin(index_list)]
print(f"Length after Deduplication:{len(df)}")

for i in tqdm(range(len(df)), ncols = 100,desc = "storing deduplicated files"):
    file = open(f"/hdfs2/dhruvpatel/Dedup_data/Fuzzy/File{i+1}.txt","w",encoding="utf-8" )
    file.write(df.iloc[i,2])
    file.close()

print("THE END")