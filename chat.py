from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI
from langchain_community.vectorstores import Chroma
from typing import List, Dict
from langchain.prompts import PromptTemplate



def setup_consolidated_rag_chain(vectorstores: Dict[str, Chroma], openrouter_api_key: str, accessible_folders: List[str]):
    """
    Set up RAG chain that can query multiple department vectorstores and provide consolidated responses.
    """
    llm = ChatOpenAI(
        temperature=0.7,
        openai_api_key=openrouter_api_key,
        openai_api_base="https://openrouter.ai/api/v1",
        model_name="mistralai/mistral-small-3.2-24b-instruct:free"
    )
    
    # Custom prompt template for consolidated responses across departments
    custom_prompt = PromptTemplate(
        template="""
                    You are a helpful and friendly AI assistant for an organization. Use the following pieces of context from various departments to answer the user's question comprehensively.

                    Context from accessible departments:
                    {context}

                    Question: {question}

                    Instructions:
                    - Provide a single, well-structured answer that synthesizes information from all relevant sources
                    - If the question involves multiple topics, organize your response with clear sections or numbered points
                    - Use all relevant information from the context to provide the most complete answer possible
                    - If some information is not available in the context, clearly state what is missing
                    - Be specific and include relevant details, metrics, or examples from the context
                    - Maintain a professional and helpful tone

                    Answer:
                """,
        input_variables=["context", "question"]
    )
    
    return custom_prompt, llm


def handle_consolidated_query_with_content_filtering(vectorstores: Dict[str, Chroma], query: str, accessible_folders: List[str], openrouter_api_key: str) -> Dict:
    """
    Filter sources based on content similarity to the generated response.
    """
    all_docs = []
    doc_to_source = {}
    
    # Retrieve relevant documents from all accessible departments
    for dept in accessible_folders:
        if dept in vectorstores:
            vectorstore = vectorstores[dept]
            retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
            docs = retriever.get_relevant_documents(query)
            
            # Filter documents by department
            for doc in docs:
                if doc.metadata.get('department', '').lower() == dept.lower():
                    all_docs.append(doc)
                    source_file = doc.metadata.get('source_file', 'Unknown')
                    doc_to_source[doc.page_content] = source_file
    
    if not all_docs:
        return {"response": "No relevant information found in accessible documents.", "sources": []}
    
    # Set up LLM and prompt
    prompt_template, llm = setup_consolidated_rag_chain(vectorstores, openrouter_api_key, accessible_folders)
    
    # Prepare context from all relevant documents
    context = "\n\n".join([doc.page_content for doc in all_docs])
    
    # Generate consolidated response
    prompt = prompt_template.format(context=context, question=query)
    response = llm.invoke(prompt)
    response_text = response.content if hasattr(response, 'content') else str(response)
    
    # Find which documents were actually used by checking content similarity
    used_sources = set()
    
    # check if key phrases from documents appear in response
    for doc in all_docs:
        doc_content = doc.page_content.lower()
        response_lower = response_text.lower()
        
        # Extract key phrases (words longer than 4 characters)
        doc_words = [word for word in doc_content.split() if len(word) > 4]
        
        # Check if significant portion of document content is reflected in response
        matches = sum(1 for word in doc_words if word in response_lower)
        
        # If more than 20% of key words from document appear in response, consider it used
        if len(doc_words) > 0 and matches / len(doc_words) > 0.2:
            source_file = doc.metadata.get('source_file', 'Unknown')
            used_sources.add(source_file)
    
    # Fallback: if no sources identified through content matching, use top 2 most relevant
    if not used_sources:
        # Use similarity search to get top 2 most relevant documents
        for dept in accessible_folders:
            if dept in vectorstores:
                vectorstore = vectorstores[dept]
                docs_with_scores = vectorstore.similarity_search_with_score(query, k=1)
                for doc, score in docs_with_scores:
                    if doc.metadata.get('department', '').lower() == dept.lower() and score < 0.7:
                        source_file = doc.metadata.get('source_file', 'Unknown')
                        used_sources.add(source_file)
                        if len(used_sources) >= 2:  # Limit to top 2 sources
                            break
            if len(used_sources) >= 2:
                break
    
    return {
        "response": response_text,
        "sources": list(used_sources)
    }