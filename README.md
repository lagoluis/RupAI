# Hedra Avatar Pipeline

## Getting Started

1.  **Install Dependencies:**
    ```bash
    make install
    ```

2.  **Set up Environment:**
    Copy `.env.example` to `.env` and add your Hedra API key.

3.  **Run:**
    ```bash
    make run
    ```

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
