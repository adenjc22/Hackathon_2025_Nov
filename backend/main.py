from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os
from app.database.init_database import init_db
from app.api.routes.health import router as health_router
from app.api.routes.uploads import router as uploads_router
from app.api.routes.users import router as users_router
from app.api.routes.auth import router as auth_router
from app.api.routes.media import router as media_router
from app.api.routes.people import router as people_router
from app.api.routes.search import router as search_router

app = FastAPI(
    title="Legacy Album API",
    version="0.1.0",
    description="Phase 1: FastAPI app structure with CORS and base routes."
)

@app.on_event("startup")
def ensure_schema() -> None:
    # Create tables if this is the first run; safe to call repeatedly.
    init_db()

# CORS configuration - supports both development and production
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
allowed_origins = [FRONTEND_URL]

# In development, also allow localhost variations
if "localhost" in FRONTEND_URL or "127.0.0.1" in FRONTEND_URL:
    allowed_origins.extend([
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def root() -> str:
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <title>Legacy Album | Auth</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f1f5f9;
                margin: 0;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            main {
                width: min(420px, calc(100vw - 2rem));
                background: #fff;
                border-radius: 14px;
                padding: 2rem;
                box-shadow: 0 20px 45px rgba(15, 23, 42, 0.15);
            }
            h1 {
            margin: 0 0 0.75rem;
                text-align: center;
                color: #0f172a;
            }
            nav {
                display: flex;
                gap: 0.75rem;
                justify-content: center;
                margin-bottom: 1.5rem;
            }
            nav button {
                border: none;
                border-radius: 999px;
                padding: 0.6rem 1.4rem;
                font-weight: 600;
                cursor: pointer;
                background: #e2e8f0;
                color: #0f172a;
                transition: background 0.2s ease;
            }
            nav button.active {
                background: #2563eb;
                color: #fff;
            }
            form {
                display: none;
                flex-direction: column;
                gap: 1rem;
                }
            form.active {
                display: flex;
            }
            label {
                font-weight: 600;
                color: #1e293b;
            }
            input {
                padding: 0.75rem 1rem;
                border-radius: 8px;
                border: 1px solid #cbd5f5;
                font-size: 1rem;
            }
            button[type="submit"] {
                border: none;
                border-radius: 8px;
                padding: 0.75rem 1rem;
                background: #2563eb;
                color: #fff;
                font-weight: 600;
                cursor: pointer;
                transition: background 0.2s ease;
            }
            button[type="submit"]:hover {
                background: #1d4ed8;
            }
            small {
            text-align: center;
                color: #64748b;
                display: block;
                margin-top: 1rem;
            }
        </style>
    </head>
    <body>
        <main>
        <h1>Legacy Album</h1>
            <nav>
                <button id="registerTab" class="active" type="button">Register</button>
                <button id="loginTab" type="button">Log in</button>
            </nav>

            <form id="registerForm" class="active" action="/api/auth/register" method="post">
                <div>
                <label for="reg-email">Email</label>
                    <input id="reg-email" name="email" type="email" required />
                </div>
                <div>
                <label for="reg-password">Password</label>
                    <input id="reg-password" name="password" type="password" minlength="6" required />
                </div>
                <button type="submit">Create account</button>
                <small>POSTS to <code>/api/auth/register</code></small>
            </form>

            <form id="loginForm" action="/api/auth/login" method="post">
                <div>
                    <label for="login-email">Email</label>
                    <input id="login-email" name="email" type="email" required />
                </div>
                <div>
                    <label for="login-password">Password</label>
                    <input id="login-password" name="password" type="password" required />
                </div>
                <button type="submit">Sign in</button>
                <small>POSTS to <code>/api/auth/login</code></small>
            </form>
            </main>

        <script>
            const registerTab = document.getElementById("registerTab");
            const loginTab = document.getElementById("loginTab");
            const registerForm = document.getElementById("registerForm");
            const loginForm = document.getElementById("loginForm");

            function activate(mode) {
                const isRegister = mode === "register";
                registerTab.classList.toggle("active", isRegister);
                loginTab.classList.toggle("active", !isRegister);
                registerForm.classList.toggle("active", isRegister);
                loginForm.classList.toggle("active", !isRegister);
            }

            registerTab.addEventListener("click", () => activate("register"));
            loginTab.addEventListener("click", () => activate("login"));
        </script>
    </body>
    </html>
    """

# Include sub-routers
app.include_router(health_router, prefix="/api/health", tags=["Health"])
app.include_router(uploads_router, prefix="/api/uploads", tags=["Uploads"])
app.include_router(users_router, prefix="/api/users", tags=["Users"])
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(media_router, prefix="/api/upload/media", tags=["Media"])
app.include_router(people_router, prefix="/api", tags=["People"])
app.include_router(search_router, prefix="/api/search", tags=["Search"])

# Mount static files for uploaded media
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")
