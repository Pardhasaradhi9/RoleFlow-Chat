import pandas as pd
from fastapi import HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import List, Optional
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY not set in .env file")
ALGORITHM = "HS256"
C_LEVEL_IDS = ['FINEMP1000', 'FINEMP1001']  # Example C-Level IDs

def verify_user(hr_df_path: str, full_name: str, department: str) -> Optional[dict]:
    """
    Verify user against HR database and return user info if valid.
    """
    try:
        hr_df = pd.read_csv(hr_df_path)
        n = full_name.strip().lower()
        d = department.strip().lower()
        match = hr_df[
            (hr_df['full_name'].str.strip().str.lower() == n) &
            (hr_df['department'].str.strip().str.lower() == d)
        ]
        if match.empty:
            return None
        user_data = match.iloc[0].to_dict()
        accessible_folders = get_accessible_folders(user_data)
        return {
            "employee_id": user_data["employee_id"],
            "full_name": user_data["full_name"],
            "department": user_data["department"],
            "role": user_data["role"],
            "attendance_pct": user_data["attendance_pct"],
            "leave_balance": user_data["leave_balance"],
            "accessible_folders": accessible_folders
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication error: {str(e)}")

def get_accessible_folders(user_data: dict) -> List[str]:
    """
    Determine accessible folders based on department and C-Level status.
    """
    department = user_data['department'].lower()
    employee_id = user_data['employee_id']
    if employee_id in C_LEVEL_IDS:
        return ['engineering', 'finance', 'hr', 'marketing', 'general']
    elif department == 'finance':
        return ['finance', 'general']
    elif department == 'marketing':
        return ['marketing', 'general']
    elif department == 'hr':
        return ['hr', 'general']
    elif department == 'technology':
        return ['engineering', 'general']
    else:
        return ['general']

def create_jwt_token(user_data: dict) -> str:
    """
    Create a JWT token with user info and accessible folders.
    """
    to_encode = user_data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt_token(token: str) -> dict:
    """
    Decode and modify JWT token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")