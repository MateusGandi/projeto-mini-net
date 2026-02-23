"""
Script para rodar servidor e clientes com auto-reload
Pressione Ctrl+C para parar
"""
import subprocess
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

class CodeReloader(FileSystemEventHandler):
    def __init__(self, process_name):
        self.process_name = process_name
        self.process = None
        self.last_reload = 0
        
    def start_process(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
        print(f"\n{'='*50}")
        print(f"🔄 Iniciando {self.process_name}...")
        print(f"{'='*50}\n")
        self.process = subprocess.Popen([sys.executable, self.process_name])
        self.last_reload = time.time()
    
    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            # Evita múltiplos reloads em 2 segundos
            if time.time() - self.last_reload > 2:
                print(f"\n📝 Arquivo modificado: {event.src_path}")
                self.start_process()

def main():
    script = sys.argv[1] if len(sys.argv) > 1 else "servidor.py"
    
    reloader = CodeReloader(script)
    reloader.start_process()
    
    observer = Observer()
    observer.schedule(reloader, path='.', recursive=False)
    observer.start()
    
    try:
        print(f"\n👀 Monitorando alterações em arquivos .py...")
        print(f"Pressione Ctrl+C para parar\n")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        if reloader.process:
            reloader.process.terminate()
        print("\n\n✋ Parando...")
    
    observer.join()

if __name__ == "__main__":
    main()
