import json
from typing import Annotated
from datetime import date, time
from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from urllib.parse import quote_plus

from backend.app.models.event import Event
from backend.app.services.tweet_formatter import _format_to_tweet

# FastAPIのForm依存をAnnotatedで定義
def get_event(
    name: Annotated[str, Form(...)],
    start_date: Annotated[date, Form(...)],
    start_at: Annotated[time, Form(...)],
    price: Annotated[str, Form(...)],
    venue: Annotated[str, Form(...)],
    address: Annotated[str, Form(...)],
    hashtag: Annotated[str, Form(...)],
    description: Annotated[str, Form(...)],
    djs: Annotated[list[str], Form(...)],
    vjs: Annotated[list[str], Form(...)],
    host: Annotated[str, Form(...)],
    with_1d: Annotated[bool, Form()] = False,
) -> Event:
    """FormからEventオブジェクトへ変換"""
    return Event(
        name=name,
        start_date=start_date,
        start_at=start_at,
        price=price,
        with_1d=with_1d,
        venue=venue,
        address=address,
        hashtag=hashtag,
        djs=djs,
        vjs=vjs,
        description=description,
        host=host,
    )


router = APIRouter(prefix="/events", tags=["events"])


@router.get("/", response_class=HTMLResponse)
async def show_register_form(request: Request):
    """イベント登録フォーム"""
    return request.app.state.templates.TemplateResponse(
        "index.html", {"request": request}
    )


@router.post("/", response_class=HTMLResponse)
async def register_event(request: Request, event: Event = Depends(get_event)):
    # ツイートのテキストを投稿する分ごとに分割
    formatted_tweet = _format_to_tweet(event)
    url = f"https://twitter.com/intent/tweet?text={quote_plus(formatted_tweet)}"

    return RedirectResponse(url)