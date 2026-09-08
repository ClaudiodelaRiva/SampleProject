from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "CompanyDB.db"
SCHEMA_PATH = BASE_DIR / "resources" / "schema.sql"
DATA_PATH = BASE_DIR / "resources" / "data.sql"