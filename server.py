from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os

HOST = "0.0.0.0"
PORT = 8080

MESSAGES_FILE = "messages.json"
USERS_FILE = "users.json"


def init_file(file_path):
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([], f)


init_file(MESSAGES_FILE)
init_file(USERS_FILE)


class ChatServer(BaseHTTPRequestHandler):

    def send_json(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())


    def do_GET(self):

        if self.path == "/":
            self.path = "/welcome.html"

        if self.path == "/messages":
            with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
                messages = json.load(f)
            return self.send_json(messages)

        try:
            path = self.path.lstrip("/")

            if path.endswith(".html"):
                file_type = "text/html"
            elif path.endswith(".css"):
                file_type = "text/css"
            elif path.endswith(".js"):
                file_type = "application/javascript"
            else:
                file_type = "text/plain"

            with open(path, "rb") as file:
                self.send_response(200)
                self.send_header("Content-type", file_type)
                self.end_headers()
                self.wfile.write(file.read())

        except:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")


    def do_POST(self):

        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
        except:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid JSON")
            return


        # ---------------- SEND MESSAGE ----------------
        if self.path == "/send":

            with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
                messages = json.load(f)

            if "username" in data and "message" in data:
                messages.append(data)

                with open(MESSAGES_FILE, "w", encoding="utf-8") as f:
                    json.dump(messages, f, ensure_ascii=False, indent=4)

                return self.send_response(200), self.end_headers()

            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid message format")
            return


        # ---------------- REGISTER ----------------
        elif self.path == "/register":

            with open(USERS_FILE, "r", encoding="utf-8") as f:
                users = json.load(f)

            for user in users:
                if user["username"] == data.get("username"):
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"User exists")
                    return

            users.append(data)

            with open(USERS_FILE, "w", encoding="utf-8") as f:
                json.dump(users, f, ensure_ascii=False, indent=4)

            self.send_response(200)
            self.end_headers()
            return


        # ---------------- LOGIN ----------------
        elif self.path == "/login":

            with open(USERS_FILE, "r", encoding="utf-8") as f:
                users = json.load(f)

            for user in users:
                if (
                    user["username"] == data.get("username")
                    and user["password"] == data.get("password")
                ):
                    self.send_response(200)
                    self.end_headers()
                    return

            self.send_response(401)
            self.end_headers()
            self.wfile.write(b"Wrong login")
            return


server = HTTPServer((HOST, PORT), ChatServer)

print(f"Server pornit pe http://localhost:{PORT}")
server.serve_forever()