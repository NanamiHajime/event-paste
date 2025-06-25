from __future__ import annotations
from datetime import date, time
from typing import Annotated, Optional
from pydantic import BaseModel, Field, field_validator


class Event(BaseModel):
    """
    イベント情報
    """

    name: Optional[Annotated[str, Field(description="イベント名")]] 
    start_date: Optional[Annotated[date, Field(description="YYYY/MM/DD 形式")]] 
    start_at: Annotated[time, Field(description="HH:MM 形式")] 

    price: Optional[Annotated[int, Field(description="価格情報")]] 
    with_1d: Optional[Annotated[bool, Field(description="1ドリンク込みかどうか")]] = False

    venue: Optional[Annotated[str, Field()]] 
    address: Optional[Annotated[str, Field(description="会場の住所")]] 
    hashtag: Optional[Annotated[str, Field(description="ハッシュタグ")]] 
    description: Optional[Annotated[str, Field(description="イベントの説明")]] 

    djs: Optional[Annotated[list[str], Field(description="DJの名前をカンマ区切りで入力")]] 
    vjs: Optional[Annotated[list[str], Field(description="VJの名前をカンマ区切りで入力")]] 

    host: Optional[Annotated[str, Field(description="主催のアカウント")]] 

    @field_validator("hashtag")
    @classmethod
    def validate_hashtag(cls, value):
        if "#" in value or "＃" in value:
            raise ValueError(
                "'#'や'＃'はハッシュタグの先頭に自動的に追加されます。"
            )
        return value

    @field_validator("name", "venue", "address", "hashtag", "description", "host")
    @classmethod
    def _disallow_newline(cls, value: str) -> str:
        if "\n" in value or "\r" in value:
            raise ValueError("改行はできません")
        return value
    
    @field_validator("djs", "vjs")
    def _disallow_list_newline(cls, value: list[str]) -> list[str]:
        for item in value:
            if "\n" in item or "\r" in item:
                raise ValueError("改行はできません")
        return value

    def _to_tweet_text(self) -> dict:
        return self.model_dump()
