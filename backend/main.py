from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from app.database.init_database import init_db
from app.api.routes.health import router as health_router
from app.api.routes.uploads import router as uploads_router
from app.api.routes.users import router as users_router
from app.api.routes.auth import router as auth_router



app = FastAPI(
    title="Legacy Album API",
    version="0.1.0",
    description="Phase 1: FastAPI app structure with CORS and base routes."
)

#@app.on_event("startup")
#def ensure_schema() -> None:
#    # Create tables if this is the first run; safe to call repeatedly.
#    init_db()

# # Allow requests from React
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app.get("/", response_class=HTMLResponse)
def root() -> str:
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <title>Legacy Album | Register</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f8fafc;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            main {
                padding: 2rem;
                border-radius: 12px;
                background: #ffffff;
                box-shadow: 0 15px 35px rgba(15, 23, 42, 0.1);
                width: min(400px, calc(100vw - 2rem));
            }
            h1 {
                margin-top: 0;
                color: #0f172a;
                text-align: center;
            }
            form {
                display: flex;
                flex-direction: column;
                gap: 1rem;
                margin-top: 1.5rem;
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
            button {
                padding: 0.75rem 1rem;
                border-radius: 8px;
                border: none;
                background: #2563eb;
                color: #ffffff;
                font-weight: 600;
                cursor: pointer;
                transition: background 0.2s ease;
            }
            button:hover {
                background: #1d4ed8;
            }
            small {
                display: block;
                text-align: center;
                color: #64748b;
                margin-top: 1rem;
            }
        </style>
    </head>
    <body>
        <main>
            <h1>Register</h1>
            <form action="/api/register/" method="post">
                <div>
                    <label for="email">Email</label>
                    <input id="email" name="email" type="email" required />
                </div>
                <div>
                    <label for="password">Password</label>
                    <input id="password" name="password" type="password" minlength="6" required />
                </div>
                <button type="submit">Create account</button>
            </form>
            <small>POSTs to <code>/api/register/</code> and echoes the JSON response.</small>
        </main>
    </body>
    </html>
    """



# Include sub-routers
app.include_router(health_router, prefix="/api/health", tags=["Health"])
app.include_router(uploads_router, prefix="/api/uploads", tags=["Uploads"])
app.include_router(users_router, prefix="/api/users", tags=["Users"])
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
