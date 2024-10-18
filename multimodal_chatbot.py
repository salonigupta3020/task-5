import os
import faiss
from sentence_transformers import SentenceTransformer

# Initialize Hugging Face Sentence Transformer
model = SentenceTransformer('all-MiniLM-L6-v2')

# Create or load FAISS vector store
def initialize_vector_db():
    index_path = "faiss_index"
    
    try:
        # Attempt to load the FAISS index
        index = faiss.read_index(f"{index_path}/index.faiss")
        print("Loaded existing FAISS index.")
    except Exception as e:
        print("FAISS index not found. Creating a new one...")
        texts = ["Hello world!", "How are you?", "This is a chatbot example."]
        
        # Generate embeddings for the texts
        embeddings = model.encode(texts, convert_to_tensor=False)
        
        # Create a FAISS index and add the embeddings
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
        
        # Save the FAISS index
        os.makedirs(index_path, exist_ok=True)
        faiss.write_index(index, f"{index_path}/index.faiss")
        print("New FAISS index created and saved locally.")
    
    return index

if __name__ == "__main__":
    try:
        vector_store = initialize_vector_db()
        print("FAISS vector store is ready.")
    except Exception as e:
        print(f"An error occurred: {e}")


