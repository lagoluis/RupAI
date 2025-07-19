# Hedra Avatar Pipeline

## Getting Started

### 1. Prerequisites

*   **Python 3.11**: Ensure you have Python 3.11 installed. You can download it from [python.org](https://www.python.org/downloads/) or use a tool like `pyenv`.
*   **uv**: A fast Python package installer and resolver. If you don't have `uv`, install it:
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
    Make sure `uv` is in your system's PATH.

### 2. Setup and Installation

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  **Create and activate a Python virtual environment**:
    ```bash
    python3.11 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    make install
    ```
    This command uses `uv` to install all required packages listed in `requirements.txt`.

4.  **Set up Environment Variables**:
    Copy the example environment file:
    ```bash
    cp .env.example .env
    ```
    Open the newly created `.env` file and replace `your_api_key_here` with your actual Hedra API key:
    ```
    HEDRA_API_KEY=your_actual_hedra_api_key
    ```
    If you plan to use the file watcher, also add the `FRIEND_IMG` variable to your `.env` file, pointing to the absolute path of your image file:
    ```
    FRIEND_IMG=/path/to/your/image.jpg
    ```

### 3. Running the Application

#### CLI Usage

You can run the main CLI application with:
```bash
source .venv/bin/activate # Activate your virtual environment if not already active
python -m hedra_avatar --wav /path/to/your/audio.wav --img /path/to/your/image.jpg --prompt "Your desired prompt"
```
Replace `/path/to/your/audio.wav` and `/path/to/your/image.jpg` with the actual paths to your audio and image files. The `--prompt` argument is optional.

#### File Watcher Usage

To automatically process new `.wav` files placed in the `incoming/` directory, run the watcher:
```bash
source .venv/bin/activate # Activate your virtual environment if not already active
python -m hedra_avatar.watch
```
Ensure that `FRIEND_IMG` is set in your `.env` file as described in step 2.


## File Watcher

To automatically process new `.wav` files, you can run the file watcher:

```bash
python -m hedra_avatar.watch
```

This will monitor the `incoming/` directory for new audio files and process them through the pipeline.

### Systemd Service (Linux)

To run the watcher as a background service on Linux, you can create a systemd user service.

1.  Create the service file:
    ```bash
    mkdir -p ~/.config/systemd/user
    nano ~/.config/systemd/user/hedra-avatar-watcher.service
    ```

2.  Add the following content, replacing `/path/to/your/project` with the absolute path to this project's directory:

    ```ini
    [Unit]
    Description=Hedra Avatar Watcher

    [Service]
    ExecStart=/path/to/your/project/.venv/bin/python -m hedra_avatar.watch
    WorkingDirectory=/path/to/your/project
    Restart=always

    [Install]
    WantedBy=default.target
    ```

3.  Enable and start the service:
    ```bash
    systemctl --user enable hedra-avatar-watcher.service
    systemctl --user start hedra-avatar-watcher.service
    ```
