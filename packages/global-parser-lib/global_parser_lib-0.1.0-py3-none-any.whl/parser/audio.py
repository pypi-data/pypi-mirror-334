import asyncio
from whisper import load_model

async def parse_audio(file_path):
    try:
        model = load_model("base")
        text = await asyncio.to_thread(model.transcribe, file_path, fp16=False)
        return text.get("text")
    except asyncio.CancelledError:
        print("Task was cancelled. Cleaning up...")
        raise  # Re-raise to let FastAPI handle it
    except Exception as e:
        print(f"Error processing file: {e}")
        return None
