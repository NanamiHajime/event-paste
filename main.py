from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

import os
from backend.app.routers import event

# templatesディレクトリのパス
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "frontend", "templates")

app = FastAPI()

# Jinja2Templatesの初期化
templates = Jinja2Templates(directory=TEMPLATES_DIR)
# ファイルの場所にかかわらず一つのtemplates/を参照するように設定
app.state.templates = templates

app.include_router(event.router)


@app.get("/")
async def redirect_to_events():
    """イベント登録フォームへリダイレクト"""
    return RedirectResponse(url="/events")
