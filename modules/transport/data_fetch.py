from pathlib import Path
import requests
import streamlit as st

# Point to a root-level 'data' directory
DATA_DIR = Path(__file__).parent.parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)
DATA_CSV = DATA_DIR / "green_tripdata_2020-01.csv.gz"

NYC_GREEN_JAN2020 = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-01.csv.gz"

@st.cache_resource
def ensure_transport_data():
    """Download the NYC taxi dataset if not cached locally."""
    if DATA_CSV.exists() and DATA_CSV.stat().st_size > 1000:
        return DATA_CSV
    
    print("Downloading NYC taxi dataset...")
    try:
        r = requests.get(NYC_GREEN_JAN2020, timeout=90)
        r.raise_for_status()
        DATA_CSV.write_bytes(r.content)
        print("NYC taxi dataset downloaded successfully.")
        return DATA_CSV
    except requests.RequestException as e:
        st.error(f"Failed to download taxi data: {e}")
        return None
