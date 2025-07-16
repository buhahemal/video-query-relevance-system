# Video Query Relevance System (Semantic Search with ChromaDB)

## Overview

This system indexes video transcripts using Whisper and Sentence Transformers, enabling fast semantic search for the most relevant video segment for a user query. It uses [ChromaDB](https://www.trychroma.com/) for persistent, efficient vector storage and search. The solution is fully containerized with Docker and Docker Compose for easy deployment.

## Tools & Libraries Used
- [OpenAI Whisper](https://github.com/openai/whisper) — Speech-to-text transcription
- [Sentence Transformers](https://www.sbert.net/) — Semantic embeddings
- [ChromaDB](https://www.trychroma.com/) — Vector database for storage and search
- [FastAPI](https://fastapi.tiangolo.com/) — API server
- [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/) — Containerization

## Usage

### 1. Add Your Videos
Place your `.mp4` files in the `app/data/` directory. For best results, use clear, speech-heavy videos (lectures, tutorials, interviews) with good audio quality.

### 2. Build and Run the API (Default)
This will build the image and start the FastAPI server on port 8000:
```bash
docker-compose up --build
```
The API will be available at [http://localhost:8000](http://localhost:8000).

### 3. Process Videos in the Running Container
If you want to process videos (transcribe, embed, and index) from within a running container:
1. **Start the container (as above):**
   ```bash
   docker-compose up --build
   ```
2. **Open a shell in the running container:**
   ```bash
   docker exec -it video-query /bin/bash
   ```
3. **Run the processing script:**
   ```bash
   python app/process_videos.py
   ```

### 4. (Alternative) Process Videos Directly (One-off)
You can also process videos without opening a shell:
```bash
docker-compose run --rm video-query process
```

### 5. Query the API
Send a POST request to `/search`:
```bash
curl -X POST "http://localhost:8000/search" -H "Content-Type: application/json" -d '{"query": "your question here", "top_k": 1}'
```
- The response will include the most relevant segment(s) with video filename, start/end time, transcript, and a direct video link (if you serve videos via HTTP).

### 6. Debug: View Embedding for Any Query
Send a POST request to `/embedding`:
```bash
curl -X POST "http://localhost:8000/embedding" -H "Content-Type: application/json" -d '{"query": "your text here"}'
```
This will return the embedding vector for your input string, useful for debugging and understanding the model’s output.

### 7. Inspect All Segment Embeddings
Send a GET request to `/segments`:
```bash
curl -X GET http://localhost:8000/segments | jq
```
This will return all stored segment embeddings and their metadata (video, timestamps, text, embedding vector).

## Best Practices for Video Input
- Use videos with clear, well-spoken audio and minimal background noise.
- Prefer speech-heavy content (lectures, interviews, tutorials).
- Avoid music videos, movies with lots of background noise, or mostly visual content.
- For best results, use videos in English or a language supported by Whisper.

## Requirements
- Docker
- Docker Compose
- Sufficient disk and CPU (or GPU for faster transcription)

## Project Structure
```
app/
  data/      # Place your .mp4 files here
  index/     # ChromaDB persistent storage will be here
  main.py    # FastAPI app
  model_utils.py
  process_videos.py
Dockerfile
entrypoint.sh
requirements.txt
docker-compose.yml
README.md
```

## API Endpoints
- `POST /search` — Semantic search for relevant video segments
- `POST /embedding` — Get embedding for any text
- `GET /segments` — Get all stored segment embeddings and metadata

## Notes
- The first run will take time to transcribe and index videos.
- You can adjust the model in `model_utils.py` for larger/faster models.
- For production, consider persistent storage and GPU acceleration. 