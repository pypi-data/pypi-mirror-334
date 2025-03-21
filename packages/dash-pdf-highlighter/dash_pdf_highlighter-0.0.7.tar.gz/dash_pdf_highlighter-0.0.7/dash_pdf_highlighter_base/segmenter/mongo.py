import os




class MongoDBConnection:
    def __init__(self):
        self._host = os.getenv('MONGO_HOST')
        self._db_name = os.getenv('MONGO_DB', 'pdf_highlighter')
        self.client = None
        self.db = None
        self._embedding_collection_name = "embedding_cache"
        self._segment_collection_name = "segment_cache"

        self.embeddings = None
        self.segments = None
        
        self._embedding_size = 1536
        self._embedding_name = "embedding"




    def create_vector_search_index(self, collection="segment_cache", extra_filters=["file_mode", "file_id"], name="vector_search"):

        # get the collection        
        collection = self.db[collection]

        
        # create indices for the extra filters if needed
        for el in extra_filters:
            collection.create_index([(el, "hashed")])
        
        vs_index = {
            "definition": {
                "fields": [
                    {
                        "numDimensions": self._embedding_size,
                        "path": self._embedding_name,
                        "similarity": "cosine",
                        "type": "vector"
                    },
                ],
            },
            "name": name,
            "type": "vectorSearch",
        }
        for el in extra_filters:
            vs_index["definition"]["fields"].append({
                "path": el,
                "type": "filter"
            })


        return collection.create_search_index(vs_index)

    def drop_search_index(self, collection="segment_cache", name="vector_search"):
        collection = self.db[collection]
        return collection.drop_search_index(name)
        

        
    def vector_search(self, embedding, collection=None, num_candidates=50, limit=10, extra_filters={}, name="vector_search", exact_match=False):

        if not collection:
            collection = self._segment_collection_name
       
        pipeline = [
            {
                "$vectorSearch": {
                    "exact": exact_match,
                    "index": name,
                    "path": self._embedding_name,
                    "queryVector": embedding,
                    "numCandidates": num_candidates,
                    "limit": limit,
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "content": 1,
                    "position": 1,
                    "file_id": 1,
                    "file_mode": 1,
                    "search_score": { "$meta": "vectorSearchScore" }
                }
            }
        ]

        # if there are extra_filters add them to the vector_search
        if extra_filters:
            pipeline[0]["$vectorSearch"]["filter"] = extra_filters


        collection = self.db[collection]

        res = collection.aggregate(pipeline)
        return res



    def __enter__(self):
        from pymongo import MongoClient
        self.client = MongoClient(self._host)
        self.db = self.client[self._db_name]

        self.embeddings = self.db[self._embedding_collection_name]
        self.segments = self.db[self._segment_collection_name]

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()

# Usage example:
# with MongoDBConnection() as mg:
#     collection = mg.db['your_collection_name']
#     # Perform database operations
