import faiss
import pickle
import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
from sentence_transformers import SentenceTransformer
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)
INDEX_PATH = "diet_index.faiss"
DOCUMENTS_PATH = "documents.pkl"

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3,
    api_key=groq_api_key
)
index = faiss.read_index(INDEX_PATH)

prompt = ChatPromptTemplate.from_template(
"""
You are an AI Health Report Assistant.

You are NOT a doctor.

Your role is to explain blood report values and provide educational diet suggestions.

Use ONLY the retrieved nutrition context below.

Never diagnose diseases.

If the information is unavailable, reply:

"I couldn't find enough information in the provided nutrition documents."

Blood Report:

{report}

Retrieved Nutrition Context:

{context}

Question:

{question}

Answer:
"""

)

with open(DOCUMENTS_PATH, "rb") as f:
    documents = pickle.load(f)
def retrieve_context(query: str, k: int = 3):
    """
    Retrieves the top-k most relevant documents for a given query.
    """

    # Convert the query into an embedding
    query_embedding = model.encode([query])

    # Search the FAISS index
    distances, indices = index.search(query_embedding, k)

    # Retrieve the matching documents
    results = [documents[i] for i in indices[0]]

    return results
def get_context_string(query, k=3):
    docs = retrieve_context(query, k)
    return "\n\n---\n\n".join(docs)
parser = StrOutputParser()

def answer_question(question: str, report_text: str):
    retrieval_query = f"""
    Blood Report:
    {report_text}

    Question:
    {question}
    """

    retrieved_docs = retrieve_context(retrieval_query)

    context = "\n\n---\n\n".join(retrieved_docs)
    messages = prompt.format_messages(
    report=report_text,
    context=context,
    question=question
    )
    response = llm.invoke(messages)
    answer = parser.invoke(response)
    

    return {
        "answer": answer,
        "sources": retrieved_docs
    }

if __name__ == "__main__":
    report = """
    Hemoglobin: 10.5
    Vitamin D: 12
    Iron: Low
    """

    question = "explain my report"

    result = answer_question(question, report)

    print(result["answer"])
    print("\nSources:")
    for source in result["sources"]:
        print("-" * 40)
        print(source)

