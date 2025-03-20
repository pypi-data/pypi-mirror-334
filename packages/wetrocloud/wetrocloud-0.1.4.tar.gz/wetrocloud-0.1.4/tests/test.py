from wetrocloud import WetroRAG

if __name__ == "__main__":
    pass
    rag_client = WetroRAG(api_key="c80d5cb1f295297ef77eb82f42aafe09b71625e1",base_url="http://127.0.0.1:8000/")
    rag_client.collection.get_or_create_collection_id("sdk_unique_id_5")
    query_response = rag_client.collection.query("What are the key points of the article?")
    print(query_response)