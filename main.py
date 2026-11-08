from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database import get_connection, init_db

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html", {"error": None})

@app.post("/login", response_class=HTMLResponse)
def login(request: Request, nim: str = Form(...), password: str = Form(...)):
    conn = get_connection()
    cur = conn.cursor()
    query = f"SELECT * FROM mahasiswa WHERE nim = '{nim}' AND password = '{password}'"
    cur.execute(query)
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user:
        return templates.TemplateResponse(request, "dashboard.html", {"user": user})
    return templates.TemplateResponse(request, "login.html", {"error": "NIM atau password salah"})

@app.get("/search", response_class=HTMLResponse)
def search_page(request: Request):
    return templates.TemplateResponse(request, "search.html", {"results": None})

@app.post("/search", response_class=HTMLResponse)
def search(request: Request, keyword: str = Form(...)):
    conn = get_connection()
    cur = conn.cursor()
    query = f"SELECT nim, nama, jurusan FROM mahasiswa WHERE nama LIKE '%{keyword}%'"
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return templates.TemplateResponse(request, "search.html", {"results": results})

@app.get("/feedback", response_class=HTMLResponse)
def feedback_page(request: Request):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT nama, pesan FROM feedback ORDER BY id DESC")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return templates.TemplateResponse(request, "feedback.html", {"data": data})

@app.post("/feedback", response_class=HTMLResponse)
def feedback_submit(request: Request, nama: str = Form(...), pesan: str = Form(...)):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO feedback (nama, pesan) VALUES (%s, %s)", (nama, pesan))
    conn.commit()
    cur.close()
    conn.close()
    return RedirectResponse(url="/feedback", status_code=303)