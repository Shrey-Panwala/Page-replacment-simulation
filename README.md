# Page Replacement Simulator (LRU, MRU, FIFO, Optimal)

An interactive simulator for classic page replacement algorithms with animated, step-by-step visualization and a quick comparison view. Runs entirely in the browser (no backend needed) and optionally via Flask if you prefer.

## Features
- Animated memory visualization with hit/miss highlighting
- Algorithms: LRU, MRU, FIFO, Optimal
- Compare All: side-by-side total fault counts per algorithm
- Responsive layout with a visualization scale slider (no browser zoom required)
- Works offline by opening the static file directly

## Project Structure

```
Project/
  backend.py            # Optional Flask server to serve static files and API
  static/
    index.html          # Main UI (client-side algorithms + comparison)
  templates/
    index.html          # (unused) legacy template; static index is served instead
```

## Run Options

### Option A: Frontend-only (recommended)
Open the file `Project/static/index.html` directly in your browser. Everything runs client-side.

### Option B: Flask server (optional)
```powershell
cd "d:\4th Sem\OS\OS project LRU-MRU\OS project\Project"
& "D:/4th Sem/OS/OS project LRU-MRU/OS project/.venv/Scripts/python.exe" backend.py
```
Then visit http://127.0.0.1:5000

## Using the App
- Enter a comma-separated page sequence (e.g., `1,3,4,5,2,3,1,2,3,2,1,4,1`)
- Set `Frame Size`
- Choose `Algorithm` and click `Run Simulation`
- Use `Pause/Play` to control the animation
- Click `Compare All` to see fault totals across all algorithms
- Adjust `Visualization Scale` to fit without browser zoom

## API (when using Flask)
Endpoint: `POST /simulate`

Request JSON:
```json
{
  "sequence": [1,3,4,5,2,3,1,2,3,2,1,4,1],
  "frameSize": 4,
  "algorithm": "LRU" | "MRU" | "FIFO" | "Optimal"
}
```

Response JSON:
```json
{
  "result": [[1],[1,3],[1,3,4],...],
  "page_faults": [true,false,true,...]
}
```

## Development Notes
- Frontend implements all algorithms client-side for speed and offline use.
- The Flask backend remains for serving static files and an API if needed.

## License
This project is for educational purposes. Add a license if you plan to distribute.
