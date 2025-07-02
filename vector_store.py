import os
import logging
from typing import List, Optional, Dict
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import MarkdownTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from document_loader import load_and_split_documents

# Configure logging
logger = logging.getLogger(__name__)

class VectorStoreManager:
    def __init__(self, data_root: str = "data", embeddings_model: str = "all-mpnet-base-v2", persist_dir: str = "./chroma_db"):
        """
        Initialize the vector store manager with ChromaDB.
        """
        self.data_root = data_root
        self.embeddings = HuggingFaceEmbeddings(model_name=embeddings_model)
        self.persist_dir = persist_dir
        self.vector_stores: Dict[str, Chroma] = {}
        
        # Ensure persist directory exists
        os.makedirs(persist_dir, exist_ok=True)

    def _get_department_files(self, department: str) -> List[str]:
        """Get all supported files for a department."""
        dept_path = os.path.join(self.data_root, department.lower())
        if not os.path.exists(dept_path):
            return []
        
        file_paths = []
        for root, _, files in os.walk(dept_path):
            for file in files:
                if file.endswith(('.pdf', '.md', '.txt', '.csv', '.markdown')):
                    file_paths.append(os.path.join(root, file))
        return file_paths

    def get_department_vectorstore(self, department: str) -> Optional[Chroma]:
        """Get or create vector store for a department."""
        department = department.lower()
        collection_name = f"dept_{department}"
        
        # Return cached vector store if available
        if department in self.vector_stores:
            return self.vector_stores[department]
        
        # Check if persisted vector store exists
        dept_persist_dir = os.path.join(self.persist_dir, department)
        if os.path.exists(dept_persist_dir) and os.listdir(dept_persist_dir):
            try:
                vectorstore = Chroma(
                    collection_name=collection_name,
                    embedding_function=self.embeddings,
                    persist_directory=dept_persist_dir
                )
                self.vector_stores[department] = vectorstore
                logger.info(f"Loaded existing vector store for {department}")
                return vectorstore
            except Exception as e:
                logger.warning(f"Error loading existing vector store for {department}: {e}")
        
        # Create new vector store
        file_paths = self._get_department_files(department)
        print(f"Files for {department}: {file_paths}")
        
        if not file_paths:
            logger.warning(f"No files found for department: {department}")
            return None

        try:
            docs = load_and_split_documents(file_paths)
            print(f"Loaded docs: {len(docs)}")
            
            # Filter documents for this department
            dept_docs = [doc for doc in docs if doc.metadata.get('department', '').lower() == department]
            print(f"Filtered docs: {len(dept_docs)}")
            
            if not dept_docs:
                logger.warning(f"No documents found for department: {department}")
                return None

            # Create vector store with persistence
            os.makedirs(dept_persist_dir, exist_ok=True)
            vectorstore = Chroma.from_documents(
                documents=dept_docs,
                embedding=self.embeddings,
                collection_name=collection_name,
                persist_directory=dept_persist_dir
            )
            
            self.vector_stores[department] = vectorstore
            logger.info(f"Created vector store for {department} with {len(dept_docs)} documents")
            return vectorstore
            
        except Exception as e:
            logger.error(f"Error creating vector store for {department}: {e}")
            return None

    def get_available_departments(self) -> List[str]:
        """Get list of departments with available documents."""
        if not os.path.exists(self.data_root):
            return []
        
        departments = []
        for item in os.listdir(self.data_root):
            if os.path.isdir(os.path.join(self.data_root, item)):
                if self._get_department_files(item):
                    departments.append(item.lower())
        return departments
    
    def refresh_department_vectorstore(self, department: str) -> Optional[Chroma]:
        """Refresh vector store for a department by recreating it."""
        department = department.lower()
        
        try:
            # Remove from cache
            if department in self.vector_stores:
                del self.vector_stores[department]
            
            # Remove persisted data
            dept_persist_dir = os.path.join(self.persist_dir, department)
            if os.path.exists(dept_persist_dir):
                import shutil
                shutil.rmtree(dept_persist_dir)
            
            # Recreate vector store
            return self.get_department_vectorstore(department)
            
        except Exception as e:
            logger.error(f"Error refreshing vector store for {department}: {e}")
            return None