from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from typing import List
import asyncio
from greedles.parser.parser import InputHandler
from greedles.model.config.config import Config
from greedles.parser.parser import Parsers

app = FastAPI(title="Greedles PSO Parser API")


@app.post("/parse")
async def parse_files(files: List[UploadFile] = File(...)):
    try:
        # Initialize the input handler
        config = Config()
        Parsers.configure(config)
        handler = InputHandler(config)

        # Convert uploaded files to bytes
        file_bytes = []
        for file in files:
            contents = await file.read()
            file.filename = file.filename  # Preserve filename
            file_bytes.append(contents)

        # Process the files
        await handler.handle_files(file_bytes)

        # Return processed data
        return {
            "characters": handler.characters,
            "share_banks": handler.share_banks,
            "all_items": handler.all_items,
            "normals": handler.normals,
            "classics": handler.classics,
        }

    except Exception as e:
        return JSONResponse(
            status_code=500, content={"error": f"Failed to process files: {str(e)}"}
        )


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
