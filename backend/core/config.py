from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()

class Settings:
    ROOT = PROJECT_ROOT
    TOOLS_DIR = PROJECT_ROOT / "tools"
    FRONTEND_DIR = PROJECT_ROOT / "frontend"
    LOGO_PATH = PROJECT_ROOT / "logo.svg"
    
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 4500))
    
    ALLOWED_TOOLS = {"smoke-test.py", "load-test.py", "stability-test.py"}
    TOOL_TIMEOUT = 300          
    TOKEN_LIFETIME = 24 * 3600  

settings = Settings()