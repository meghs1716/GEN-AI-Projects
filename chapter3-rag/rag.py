import os
from google import genai
from dotenv import load_dotenv
import chromadb
load_dotenv()

gem_client=genai.Client(api_key=os.getenv('gemini_api_key'))
chroma_client=chromadb.Client()
#we store documents in collection
collection =  chroma_client.create_collection(name='test_db')
documents=[
    'the names of metropolitan cities in india are : mumbai,gurgaon,hyderabad, chennai, banglore.',
    'hyderabad has one of the largest economies in all of india',
    'there are 28 states and 9 union territories in india as of 2026'
]
for ind,doc in enumerate(documents):
    #use gemini to embedd
    response=gem_client.models.embed_content(
        model='gemini-embedding-001',
        contents=doc
    )
    embedding=response.embeddings[0].values
    #we store the embeddings using chromadb
    collection.add(
        documents=[doc], # index
        embeddings=[embedding],
        ids=[f'doc_{ind}']
    )
    
query='out of all metropolitan cities which city has one of the largest in india?'

query_res=gem_client.models.embed_content(
    model='gemini-embedding-001',
    contents=query   
)
query_embedding=query_res.embeddings[0].values
#we search the vector db for the most similar chunk
results=collection.query(
    query_embeddings=[query_embedding],
    n_results=1
)

retrieved_context = results["documents"][0][0]


prompt = f"""
Context: {retrieved_context}
Question: {query}
Answer:
"""

generation_response = gem_client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

print(generation_response.text)