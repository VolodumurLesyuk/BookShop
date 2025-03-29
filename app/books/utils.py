import json, csv
from fastapi import UploadFile, HTTPException

async def parse_books_file(file: UploadFile):
    content = await file.read()
    try:
        if file.filename.endswith(".json"):
            return json.loads(content)
        elif file.filename.endswith(".csv"):
            content = content.decode()
            reader = csv.DictReader(content.splitlines())
            return [row for row in reader]
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"File parsing error: {str(e)}")
