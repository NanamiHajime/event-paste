from typing import Optional
from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from urllib.parse import quote_plus

from backend.app.models.event import Event
from backend.app.services.tweet_formatter import _format_to_tweet

def get_event(
    name: Optional[str] = Form(None),
    price: Optional[str] = Form(None),
    venue: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    hashtag: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    djs: Optional[list[str]] = Form(None),
    vjs: Optional[list[str]] = Form(None),
    host: Optional[str] = Form(None),
    start_date: Optional[str] = Form(None),
    start_at: Optional[str] = Form(None),
    with_1d: Optional[bool] = Form(None),
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
    formatted_tweet = _format_to_tweet(event)
    url = f"https://twitter.com/intent/tweet?text={quote_plus(formatted_tweet)}"

    return RedirectResponse(url)