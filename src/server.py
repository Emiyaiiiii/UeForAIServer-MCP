import uvicorn
from starlette.applications import Starlette
from routes import routes
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import secrets

# Create Starlette application
app = Starlette(
    debug=True,
    routes=routes,
)

app.add_middleware(
    SessionMiddleware,
    secret_key=secrets.token_urlsafe(32),
    session_cookie="session_id"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def run():
    """Start the Starlette server"""
    import argparse

    parser = argparse.ArgumentParser(description='Run MCP SSE-based server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8020, help='Port to listen on')
    args = parser.parse_args()

    uvicorn.run(app, host=args.host, port=args.port)

if __name__ == "__main__":
    run()