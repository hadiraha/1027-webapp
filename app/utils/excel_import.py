import pandas as pd
from sqlalchemy.orm import Session
from app.models import Company

def import_excel(file_path: str, db: Session):
    df = pd.read_excel(file_path)
    for _, row in df.iterrows():
        db.add(Company(
            name_fa=row.get("name_fa"),
            name_en=row.get("name_en"),
            website=row.get("website"),
            website_desc=row.get("website_desc"),
            magazine_desc=row.get("magazine_desc"),
            file_number=row.get("file_number"),
            sector=row.get("sector"),
            country=row.get("country"),
        ))
    db.commit()