import subprocess, time, urllib.request, socket
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _free_port():
    s = socket.socket(); s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]; s.close(); return port


def _serve():
    port = _free_port()
    p = subprocess.Popen(
        ["python3", "-m", "http.server", str(port)],
        cwd=str(ROOT), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.0)
    return p, port


def test_pages_serve_200():
    p, port = _serve()
    try:
        for path in ["/index.html", "/apply.html"]:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}{path}") as r:
                assert r.status == 200
                body = r.read().decode("utf-8")
                if path == "/index.html":
                    assert "$2,999" in body
                if path == "/apply.html":
                    assert 'id="applyForm"' in body
    finally:
        p.terminate()
