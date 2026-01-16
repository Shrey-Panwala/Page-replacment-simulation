from flask import Flask, request, jsonify, render_template

app = Flask(__name__, static_folder="static", static_url_path="/")

def simulate_lru(sequence, frame_size):
    frames = []
    output = []
    page_faults = []
    
    for page in sequence:
        fault = False
        if page not in frames:
            fault = True
            if len(frames) >= frame_size:
                frames.pop(0)  # Remove LRU page
            frames.append(page)
        else:
            frames.remove(page)
            frames.append(page)  # Move to most recent
        output.append(frames.copy())    
        page_faults.append(fault)
    
    return output, page_faults

def simulate_mru(sequence, frame_size):
    frames = []
    output = []
    page_faults = []
    most_recently_used = None
    
    for page in sequence:
        fault = False
        if page not in frames:
            fault = True
            # Evict the most recently used page among current frames
            if len(frames) >= frame_size and most_recently_used is not None and most_recently_used in frames:
                frames.remove(most_recently_used)
            frames.append(page)
        most_recently_used = page
        output.append(frames.copy())
        page_faults.append(fault)
    
    return output, page_faults

def simulate_fifo(sequence, frame_size):
    frames = []
    order = []  # queue of insertion order
    output = []
    page_faults = []

    for page in sequence:
        fault = False
        if page not in frames:
            fault = True
            if len(frames) >= frame_size:
                evict = order.pop(0)
                if evict in frames:
                    frames.remove(evict)
            frames.append(page)
            order.append(page)
        # on hit, FIFO does not change order
        output.append(frames.copy())
        page_faults.append(fault)
    return output, page_faults

def simulate_optimal(sequence, frame_size):
    frames = []
    output = []
    page_faults = []

    for i, page in enumerate(sequence):
        fault = False
        if page not in frames:
            fault = True
            if len(frames) < frame_size:
                frames.append(page)
            else:
                # Choose victim with farthest next use (or never used again)
                farthest_index = -1
                victim = None
                for f in frames:
                    try:
                        next_use = sequence[i+1:].index(f)
                        next_pos = i + 1 + next_use
                    except ValueError:
                        next_pos = float('inf')
                    if next_pos > farthest_index:
                        farthest_index = next_pos
                        victim = f
                if victim is not None:
                    frames.remove(victim)
                frames.append(page)
        output.append(frames.copy())
        page_faults.append(fault)
    return output, page_faults

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/simulate", methods=["POST"])
def simulate():
    data = request.get_json()
    sequence = data["sequence"]
    frame_size = data["frameSize"]
    algorithm = data["algorithm"]

    if algorithm == "LRU":
        result, page_faults = simulate_lru(sequence, frame_size)
    elif algorithm == "MRU":
        result, page_faults = simulate_mru(sequence, frame_size)
    elif algorithm == "FIFO":
        result, page_faults = simulate_fifo(sequence, frame_size)
    elif algorithm == "Optimal":
        result, page_faults = simulate_optimal(sequence, frame_size)
    else:
        return jsonify({"error": "Unknown algorithm"}), 400

    return jsonify({"result": result, "page_faults": page_faults})

if __name__ == "__main__":
    app.run(debug=True)
