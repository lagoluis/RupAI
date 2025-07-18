
import os
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from hedra_avatar.core.assets import create_asset, upload_asset
from hedra_avatar.core.generation import start_generation
from hedra_avatar.core.poll import wait_and_download

console = Console()

class Watcher:
    def __init__(self, watch_dir: Path, img_path: Path, api_key: str):
        self.watch_dir = watch_dir
        self.img_path = img_path
        self.api_key = api_key
        self.observer = Observer()
        self.executor = ThreadPoolExecutor(max_workers=5)
        self.processed_files = set()

    def run(self):
        event_handler = self.Handler(self)
        self.observer.schedule(event_handler, self.watch_dir, recursive=True)
        self.observer.start()
        console.log(f"Watching directory: {self.watch_dir}")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

    class Handler(FileSystemEventHandler):
        def __init__(self, watcher: 'Watcher'):
            self.watcher = watcher

        def on_created(self, event):
            if not event.is_directory and event.src_path.endswith(".wav"):
                file_path = Path(event.src_path)
                if file_path in self.watcher.processed_files:
                    return  # Debounce
                self.watcher.processed_files.add(file_path)
                self.watcher.executor.submit(self.watcher.process_file, file_path)

    def process_file(self, wav_path: Path):
        try:
            console.log(f"Processing new file: {wav_path.name}")

            console.log("Creating audio asset...")
            audio_asset_id = create_asset(wav_path.name, "audio", self.api_key)
            upload_asset(audio_asset_id, wav_path, self.api_key)

            console.log("Creating image asset...")
            image_asset_id = create_asset(self.img_path.name, "image", self.api_key)
            upload_asset(image_asset_id, self.img_path, self.api_key)

            console.log("Starting generation...")
            prompt = f"A video of a person speaking."
            generation_id = start_generation(
                image_asset_id, audio_asset_id, prompt, self.api_key
            )

            console.log(f"Waiting for generation {generation_id} to complete...")
            output_path = wait_and_download(generation_id, Path("output"), self.api_key)

            console.log(f"[bold green]✅ Video downloaded to: {output_path}[/bold green]")

        except Exception as e:
            console.log(f"[bold red]❌ An error occurred: {e}[/bold red]")

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("HEDRA_API_KEY")
    friend_img = os.getenv("FRIEND_IMG")

    if not api_key or not friend_img:
        console.log("[bold red]Error: HEDRA_API_KEY and FRIEND_IMG must be set in .env[/bold red]")
        exit(1)

    watch_dir = Path("incoming")
    watch_dir.mkdir(exist_ok=True)

    watcher = Watcher(watch_dir, Path(friend_img), api_key)
    watcher.run()
