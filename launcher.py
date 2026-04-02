"""
Estatística Policial - Launcher
Executável que configura e inicia o aplicativo automaticamente.
Funciona em Windows, Mac e Linux.
"""

import os
import sys
import subprocess
import threading
import webbrowser
import time
from pathlib import Path

ROOT_DIR = Path(__file__).parent.resolve()
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "frontend"
ENV_FILE = BACKEND_DIR / ".env"
VENV_DIR = BACKEND_DIR / ".venv"

IS_WINDOWS = sys.platform == "win32"
PYTHON = str(VENV_DIR / ("Scripts" if IS_WINDOWS else "bin") / "python")
PIP = str(VENV_DIR / ("Scripts" if IS_WINDOWS else "bin") / "pip")
UVICORN = str(VENV_DIR / ("Scripts" if IS_WINDOWS else "bin") / "uvicorn")


def get_api_key_from_env():
    """Lê a API key do arquivo .env se existir."""
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            if line.startswith("GEMINI_API_KEY="):
                key = line.split("=", 1)[1].strip()
                if key and key != "your_gemini_api_key_here":
                    return key
    return None


def save_api_key(key):
    """Salva a API key no arquivo .env."""
    ENV_FILE.write_text(
        f"GEMINI_API_KEY={key}\n"
        f"ALLOWED_ORIGINS=http://localhost:5173,http://localhost:8000\n"
        f"MAX_UPLOAD_SIZE_MB=50\n"
    )


def ask_api_key_gui():
    """Abre janela gráfica para pedir a API key."""
    try:
        import tkinter as tk
        from tkinter import messagebox
    except ImportError:
        return ask_api_key_terminal()

    result = {"key": None}

    root = tk.Tk()
    root.title("Estatística Policial - Configuração")
    root.geometry("520x320")
    root.resizable(False, False)
    root.configure(bg="#1e3a5f")

    try:
        root.iconname("Estatística Policial")
    except Exception:
        pass

    # Centralizar na tela
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - 260
    y = (root.winfo_screenheight() // 2) - 160
    root.geometry(f"+{x}+{y}")

    tk.Label(
        root, text="🛡️ Estatística Policial", font=("Arial", 18, "bold"),
        bg="#1e3a5f", fg="white"
    ).pack(pady=(20, 5))

    tk.Label(
        root, text="Dashboard de Produtividade com IA",
        font=("Arial", 10), bg="#1e3a5f", fg="#87CEEB"
    ).pack(pady=(0, 15))

    tk.Label(
        root, text="Para começar, insira sua API Key do Google Gemini:",
        font=("Arial", 10), bg="#1e3a5f", fg="white"
    ).pack(pady=(0, 5))

    tk.Label(
        root, text="(Obtenha grátis em: aistudio.google.com/apikey)",
        font=("Arial", 9), bg="#1e3a5f", fg="#87CEEB"
    ).pack(pady=(0, 10))

    entry = tk.Entry(root, width=50, font=("Arial", 11), show="*")
    entry.pack(pady=5, padx=30)
    entry.focus_set()

    def on_submit():
        key = entry.get().strip()
        if not key:
            messagebox.showwarning("Aviso", "Por favor, insira a API Key.")
            return
        result["key"] = key
        root.destroy()

    def on_enter(event):
        on_submit()

    entry.bind("<Return>", on_enter)

    btn = tk.Button(
        root, text="▶  Iniciar Aplicativo", font=("Arial", 12, "bold"),
        bg="#10B981", fg="white", activebackground="#059669",
        relief="flat", padx=20, pady=8, command=on_submit
    )
    btn.pack(pady=15)

    root.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))
    root.mainloop()

    return result["key"]


def ask_api_key_terminal():
    """Fallback: pede a API key pelo terminal."""
    print("\n" + "=" * 50)
    print("  Estatística Policial - Configuração")
    print("=" * 50)
    print("\nPara usar o app, você precisa de uma API Key do Google Gemini.")
    print("Obtenha grátis em: https://aistudio.google.com/apikey\n")
    key = input("Cole sua GEMINI_API_KEY: ").strip()
    return key if key else None


def show_loading_gui(stop_event):
    """Mostra janela de carregamento enquanto instala dependências."""
    try:
        import tkinter as tk
    except ImportError:
        return

    root = tk.Tk()
    root.title("Carregando...")
    root.geometry("400x150")
    root.resizable(False, False)
    root.configure(bg="#1e3a5f")

    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - 200
    y = (root.winfo_screenheight() // 2) - 75
    root.geometry(f"+{x}+{y}")

    tk.Label(
        root, text="🛡️ Estatística Policial", font=("Arial", 14, "bold"),
        bg="#1e3a5f", fg="white"
    ).pack(pady=(20, 10))

    label = tk.Label(
        root, text="Instalando dependências... Aguarde.",
        font=("Arial", 10), bg="#1e3a5f", fg="#87CEEB"
    )
    label.pack(pady=5)

    dots = [0]

    def animate():
        if stop_event.is_set():
            root.destroy()
            return
        dots[0] = (dots[0] % 3) + 1
        label.config(text=f"Instalando dependências{'.' * dots[0]}")
        root.after(500, animate)

    animate()
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    root.mainloop()


def setup_environment():
    """Configura venv e instala dependências."""
    # Criar venv se não existe
    if not VENV_DIR.exists():
        print("Criando ambiente Python...")
        subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True)

    # Instalar dependências do backend
    print("Instalando dependências do backend...")
    subprocess.run(
        [PIP, "install", "-q", "-r", str(BACKEND_DIR / "requirements.txt")],
        check=True, capture_output=True
    )

    # Build do frontend (se necessário)
    frontend_dist = FRONTEND_DIR / "dist"
    if not frontend_dist.exists():
        print("Compilando frontend...")
        npm_cmd = "npm.cmd" if IS_WINDOWS else "npm"
        subprocess.run([npm_cmd, "install"], cwd=str(FRONTEND_DIR), check=True, capture_output=True)
        subprocess.run([npm_cmd, "run", "build"], cwd=str(FRONTEND_DIR), check=True, capture_output=True)


def start_server():
    """Inicia o servidor FastAPI."""
    env = os.environ.copy()
    env["DOTENV_PATH"] = str(ENV_FILE)

    process = subprocess.Popen(
        [UVICORN, "main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=str(BACKEND_DIR),
        env=env,
    )
    return process


def wait_for_server(timeout=30):
    """Aguarda o servidor ficar pronto."""
    import urllib.request
    start = time.time()
    while time.time() - start < timeout:
        try:
            urllib.request.urlopen("http://127.0.0.1:8000/health", timeout=2)
            return True
        except Exception:
            time.sleep(0.5)
    return False


def main():
    print("\n🛡️  Estatística Policial - Iniciando...\n")

    # 1. Verificar/pedir API key
    api_key = get_api_key_from_env()
    if not api_key:
        api_key = ask_api_key_gui()
        if not api_key:
            print("API Key não fornecida. Encerrando.")
            sys.exit(1)
        save_api_key(api_key)
        print("✓ API Key salva.")

    # 2. Instalar dependências (com tela de loading)
    stop_event = threading.Event()
    loading_thread = threading.Thread(target=show_loading_gui, args=(stop_event,), daemon=True)

    try:
        loading_thread.start()
        setup_environment()
    finally:
        stop_event.set()

    print("✓ Dependências instaladas.")

    # 3. Iniciar servidor
    print("Iniciando servidor...")
    server = start_server()

    if wait_for_server():
        url = "http://127.0.0.1:8000"
        print(f"\n✓ Servidor rodando em {url}")
        print("  Abrindo navegador...\n")
        print("  Pressione Ctrl+C para encerrar.\n")
        webbrowser.open(url)
    else:
        print("Erro: servidor não iniciou. Verifique os logs.")
        server.terminate()
        sys.exit(1)

    # 4. Manter rodando até Ctrl+C
    try:
        server.wait()
    except KeyboardInterrupt:
        print("\nEncerrando servidor...")
        server.terminate()
        server.wait()
        print("Encerrado.")


if __name__ == "__main__":
    main()
