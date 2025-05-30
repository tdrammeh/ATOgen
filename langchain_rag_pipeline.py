
import json
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# Load enhancement data
with open('ATOgen_Control_Enhancements_Automation_Block.json', 'r') as f:
    controls = json.load(f)

# Create corpus text
corpus = []
for c in controls:
    text = f"Control ID: {c['control_id']}\n"
    text += f"Family: {c['control_family']}\n"
    text += f"Status: {c['status']}\n"
    text += f"Implementation: {c['implementation']['statement']}\n"
    corpus.append(text)

# Split text for embedding
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
documents = text_splitter.create_documents(corpus)

# Create embeddings and FAISS index
embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(documents, embeddings)

# Create retrieval QA chain
retriever = db.as_retriever()
llm = OpenAI(temperature=0)
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# Query example
query = "What controls cover incident response?"
result = qa_chain.run(query)
print("\n=== Answer ===")
print(result)
