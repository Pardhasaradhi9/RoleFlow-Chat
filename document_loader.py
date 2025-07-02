import os
from typing import List
from langchain_community.document_loaders import (
    UnstructuredMarkdownLoader,
    CSVLoader,
    UnstructuredPDFLoader,
    TextLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def get_department_from_path(file_path):
    """
    Extracts the department name from the file path based on the folder
    immediately under 'data/'.
    """
    parts = file_path.split(os.sep)
    if "data" in parts:
        idx = parts.index("data")
        if idx + 1 < len(parts):
            return parts[idx + 1].lower()
    return "general"

def load_and_split_documents(file_paths: List[str], chunk_size: int = 1500, chunk_overlap: int = 150) -> List[Document]:
    """
    Load and process documents from various file types: PDF, Markdown, TXT, and CSV.
    Returns a list of Document objects with proper metadata.
    """
    all_docs = []
    
    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]  
    )
    
    for file_path in file_paths:
        print(f"Processing file: {file_path}")
        
        if not os.path.exists(file_path):
            print(f"Warning: File not found: {file_path}")
            continue
            
        ext = os.path.splitext(file_path)[1].lower()
        docs = []
        
        try:
            # Load documents based on file type
            if ext in ['.md', '.markdown']:
                loader = UnstructuredMarkdownLoader(file_path)
                docs = loader.load()
                print(f"  Loaded {len(docs)} markdown documents")
                
            elif ext == '.txt':
                loader = TextLoader(file_path, encoding='utf-8')
                docs = loader.load()
                print(f"  Loaded {len(docs)} text documents")
                
            elif ext == '.pdf':
                loader = UnstructuredPDFLoader(file_path)
                docs = loader.load()
                print(f"  Loaded {len(docs)} PDF documents")
                
            elif ext == '.csv':
                loader = CSVLoader(file_path=file_path)
                docs = loader.load()
                print(f"  Loaded {len(docs)} CSV documents")
                
            else:
                print(f"Warning: Unsupported file type '{ext}' for '{file_path}'")
                continue
                
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            continue
        
        if not docs:
            print(f"Warning: No content loaded from {file_path}")
            continue
        
        # Add metadata to all documents from this file
        department = get_department_from_path(file_path)
        for doc in docs:
            doc.metadata.update({
                'department': department,
                'source_file': os.path.basename(file_path),
                'full_path': file_path,
                'file_type': ext
            })
        
        # Split documents based on type
        if ext == '.csv':
            # CSV files are already row-based, don't split further
            all_docs.extend(docs)
            print(f"  Added {len(docs)} CSV rows without splitting")
        else:
            # Split text-based documents
            split_docs = text_splitter.split_documents(docs)
            all_docs.extend(split_docs)
            print(f"  Split into {len(split_docs)} chunks")
            
            # Debug: Show content preview for first chunk
            if split_docs:
                preview = split_docs[0].page_content[:200].replace('\n', ' ')
                print(f"  First chunk preview: {preview}...")
    
    print(f"\nTotal documents processed: {len(all_docs)}")
    return all_docs

def debug_document_content(docs: List[Document], search_terms: List[str] = None):
    """
    Debug function to analyze document content and search for specific terms.
    """
    if search_terms is None:
        search_terms = ['q1', '2024', 'benchmark', 'metric', 'performance']
    
    print(f"\nDEBUG: Analyzing {len(docs)} documents")
    print("=" * 50)
    
    for i, doc in enumerate(docs):
        content_lower = doc.page_content.lower()
        matches = [term for term in search_terms if term.lower() in content_lower]
        
        if matches:
            print(f"\nDocument {i+1}:")
            print(f"  Source: {doc.metadata.get('source_file', 'unknown')}")
            print(f"  Department: {doc.metadata.get('department', 'unknown')}")
            print(f"  Matching terms: {matches}")
            print(f"  Content length: {len(doc.page_content)}")
            print(f"  Content preview: {doc.page_content[:300]}...")
            print("-" * 30)

if __name__ == "__main__":
    files = [
        "data/engineering/engineering_master_doc.md",
        "data/finance/financial_summary.md", 
        "data/finance/quarterly_financial_report.md",
        "data/general/employee_handbook.md",
        "data/marketing/market_report_q4_2024.md",
        "data/marketing/marketing_report_2024.md",
        "data/marketing/marketing_report_q1_2024.md",
        "data/marketing/marketing_report_q2_2024.md",
        "data/marketing/marketing_report_q3_2024.md",
        "data/hr/hr_data.csv"
    ]
    
    all_docs = load_and_split_documents(files)
    print(f"Loaded {len(all_docs)} documents.")
    
    # Debug Q1 2024 marketing content specifically
    # marketing_docs = [doc for doc in all_docs if doc.metadata.get('department') == 'marketing']
    # debug_document_content(marketing_docs, ['q1', '2024', 'benchmark', 'metric', 'performance', 'kpi'])