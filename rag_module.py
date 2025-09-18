from sentence_transformers import SentenceTransformer, util
import torch
from onto import OntologyParser

class RAG:
    def __init__(self, onto_file:str, model_similarity_name="all-mpnet-base-v2"):
        self.model_similarity = SentenceTransformer(model_similarity_name)
        self.ontology = OntologyParser(ontology_file=onto_file)
    
    def text_embedding(self, text):
        return self.model_similarity.encode(text, convert_to_tensor=True)

    def embedding_creator(self):
        info, text = self.ontology.instance_extractor()
        vector_db = [
        {"info": i, "text": t, "embedding": self.text_embedding(t)}
        for i, t in zip(info, text)
        ]
        return vector_db

class Retriever(RAG):
    def __init__(self, onto_file:str, model_similarity_name="all-mpnet-base-v2"):
        self.rag = RAG(onto_file, model_similarity_name)
        self.vec_db = self.rag.embedding_creator()
        
    def retrieve(self, query, top_k=4):
        query_embedding = self.rag.text_embedding(query)
        db_embedd = [embedd['embedding'] for embedd in self.vec_db]
        similarity_score = util.semantic_search(query_embedding, db_embedd, top_k=top_k)[0]
        return [
                (self.vec_db[score['corpus_id']]['info'],
                 self.vec_db[score['corpus_id']]['text'],
                 round(score['score'], 3)) 
                for score in similarity_score
               ]
        
    def update_ontology(self, new_onto_file: str):
        self.rag.ontology = OntologyParser(ontology_file=new_onto_file)
        self.vec_db = self.rag.embedding_creator()
        return self.vec_db