from fastapi import UploadFile, File, Depends
import pandas as pd
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Company

@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # ---- Save uploaded file temporarily
    file_location = f"uploads/{file.filename}"
    with open(file_location, "wb+") as f:
        f.write(await file.read())

    # ---- Read Excel (xlsx)
    df = pd.read_excel(file_location)

    # Expected columns in Excel:
    # name_fa, name_en, website, website_desc, magazine_desc, file_number, sector, country

    for _, row in df.iterrows():
        company = Company(
            index= row.get("index"),
            name_fa=row.get("name_fa"),
            name_en=row.get("name_en"),
            website=row.get("website"),
            website_desc=row.get("website_desc"),
            magazine_desc=row.get("magazine_desc"),
            file_number=row.get("file_number"),
            sector=row.get("sector"),
            country=row.get("country")
        )
        db.add(company)

    db.commit()
    return {"status": "OK", "msg": "Excel imported successfully"}