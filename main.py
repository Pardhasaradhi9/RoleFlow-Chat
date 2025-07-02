import os
import logging
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from auth import verify_user, decode_jwt_token, create_jwt_token
from vector_store import VectorStoreManager
from chat import handle_consolidated_query_with_content_filtering
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI(title="RBAC RAG Chatbot API")

# Add CORS middleware to allow Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Streamlit default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize VectorStoreManager
vectorstore_manager = VectorStoreManager()

# Initialize security
security = HTTPBearer()

# Pydantic models for request/response
class LoginRequest(BaseModel):
    full_name: str
    department: str

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str
    sources: List[str]
    department: str

class ConsolidatedQueryResponse(BaseModel):
    response: str
    sources: List[str]

class LoginResponse(BaseModel):
    token: str
    user_data: Dict

# Dependency for JWT validation
async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        token = credentials.credentials
        return decode_jwt_token(token)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.get("/available-departments", response_model=List[str])
async def get_available_departments():
    """
    Get list of all available departments for the dropdown.
    """
    try:
        departments = [
            "Business",
            "Compliance",
            "Data",
            "Design",
            "Finance",
            "HR",
            "Marketing",
            "Operations",
            "Product",
            "Quality Assurance",
            "Risk",
            "Sales",
            "Technology"
        ]
        return departments
    except Exception as e:
        logger.error(f"Error fetching available departments: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch departments")

@app.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest):
    """
    Authenticate user and return JWT token with user data.
    """
    try:
        user_data = verify_user("data/hr/hr_data.csv", login_data.full_name, login_data.department)
        if not user_data:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_jwt_token(user_data)
        logger.info(f"User {user_data['full_name']} logged in successfully")
        return {"token": token, "user_data": user_data}
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@app.get("/departments", response_model=List[str])
async def get_departments(current_user: dict = Depends(get_current_user)):
    """
    Get list of accessible departments for the user.
    """
    try:
        return current_user["accessible_folders"]
    except Exception as e:
        logger.error(f"Error fetching departments: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch departments")

@app.post("/query", response_model=ConsolidatedQueryResponse)
async def query(query_data: QueryRequest, current_user: dict = Depends(get_current_user)):
    """
    Handle user query and return consolidated response from all accessible departments.
    """
    try:
        accessible_departments = current_user["accessible_folders"]
        
        # Get all vectorstores for accessible departments
        vectorstores = {}
        for dept in accessible_departments:
            vectorstore = vectorstore_manager.get_department_vectorstore(dept)
            if vectorstore:
                vectorstores[dept] = vectorstore
        
        if not vectorstores:
            logger.warning(f"No vectorstores found for departments: {accessible_departments}")
            raise HTTPException(status_code=404, detail="No accessible data found")

        result = handle_consolidated_query_with_content_filtering(
            vectorstores, 
            query_data.query, 
            accessible_departments, 
            os.getenv("OPENROUTER_API_KEY")
        )
        
        logger.info(f"Consolidated query processed for {current_user['full_name']}")
        
        return {
            "response": result["response"],
            "sources": result["sources"]
        }
        
    except Exception as e:
        logger.error(f"Query error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")
