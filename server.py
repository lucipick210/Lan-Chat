from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os

HOST = "0.0.0.0"
PORT = 8080

MESSAGES_FILE = "messages.json"
USERS_FILE = "users.json"


def init_file(path, default):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default, f, ensure_ascii=False, indent=4)


init_file(MESSAGES_FILE, {
    "general": [],
    "gaming": [],
    "random": []
})

init_file(USERS_FILE, [])


class ChatServer(BaseHTTPRequestHandler):

    def send_json(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    # ---------------- GET ----------------
    def do_GET(self):

        if self.path == "/":
            self.path = "/index.html"

        if self.path == "/messages":
            with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
                messages = json.load(f)
            return self.send_json(messages)

        try:
            path = self.path.lstrip("/")

            if path == "":
                path = "index.html"

            if not os.path.exists(path):
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"404")
                return

            if path.endswith(".html"):
                ctype = "text/html"
            elif path.endswith(".css"):
                ctype = "text/css"
            elif path.endswith(".js"):
                ctype = "application/javascript"
            else:
                ctype = "text/plain"

            with open(path, "rb") as f:
                self.send_response(200)
                self.send_header("Content-type", ctype)
                self.end_headers()
                self.wfile.write(f.read())

        except Exception as e:
            print("GET ERROR:", e)
            self.send_response(500)
            self.end_headers()

    # ---------------- POST ----------------
    def do_POST(self):

        try:
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length)
            data = json.loads(raw.decode("utf-8"))
        except:
            self.send_response(400)
            self.end_headers()
            return

        # =========================
        # 🔥 SEND MESSAGE
        # =========================
        if self.path == "/send":

            room = data.get("room", "general")

            with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
                messages = json.load(f)

            if room not in messages:
                messages[room] = []

            messages[room].append(data)

            with open(MESSAGES_FILE, "w", encoding="utf-8") as f:
                json.dump(messages, f, ensure_ascii=False, indent=4)

            self.send_response(200)
            self.end_headers()
            return

        # =========================
        # 🔥 REGISTER
        # =========================
        elif self.path == "/register":

            username = data.get("username", "").strip()
            password = data.get("password", "").strip()

            with open(USERS_FILE, "r", encoding="utf-8") as f:
                users = json.load(f)

            for u in users:
                if u["username"].strip() == username:
                    self.send_response(400)
                    self.end_headers()
                    return

            users.append({
                "username": username,
                "password": password
            })

            with open(USERS_FILE, "w", encoding="utf-8") as f:
                json.dump(users, f, ensure_ascii=False, indent=4)

            self.send_response(200)
            self.end_headers()
            return

        # =========================
        # 🔥 LOGIN
        # =========================
        elif self.path == "/login":

            username = data.get("username", "").strip()
            password = data.get("password", "").strip()

            with open(USERS_FILE, "r", encoding="utf-8") as f:
                users = json.load(f)

            for u in users:
                if u["username"].strip() == username and u["password"].strip() == password:
                    self.send_response(200)
                    self.end_headers()
                    return

            self.send_response(401)
            self.end_headers()
            return

        # =========================
        # ❌ UNKNOWN ROUTE
        # =========================
        self.send_response(404)
        self.end_headers()

server = HTTPServer((HOST, PORT), ChatServer)
print(f"Server running on http://localhost:{PORT}")
server.serve_forever()