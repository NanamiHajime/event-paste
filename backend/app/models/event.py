from __future__ import annotations
from datetime import date, time
from typing import Annotated, Optional
from pydantic import BaseModel, Field, field_validator


class Event(BaseModel):
    """
    イベント情報
    """

    name: Optional[Annotated[str, Field(description="イベント名")]] = None
    start_date: Optional[Annotated[date, Field(description="YYYY/MM/DD 形式")]] = None
    start_at: Optional[Annotated[time, Field(description="HH:MM 形式")]] = None

    price: Optional[Annotated[int, Field(description="価格情報")]] = None
    with_1d: Optional[Annotated[bool, Field(description="1ドリンク込みかどうか")]] = False

    venue: Optional[Annotated[str, Field()]] = None
    address: Optional[Annotated[str, Field(description="会場の住所")]] = None
    hashtag: Optional[Annotated[str, Field(description="ハッシュタグ")]] = None
    description: Optional[Annotated[str, Field(description="イベントの説明")]] = None

    djs: Optional[Annotated[list[str], Field(description="DJの名前をカンマ区切りで入力")]] = None
    vjs: Optional[Annotated[list[str], Field(description="VJの名前をカンマ区切りで入力")]] = None

    host: Optional[Annotated[str, Field(description="主催のアカウント")]] = None

    @field_validator("start_date", "start_at", "price", mode="before")
    @classmethod
    def _empty_str_to_none(cls, value):
        if isinstance(value, str) and not value.strip():
            value = None

        return value

    @field_validator("hashtag")
    @classmethod
    def validate_hashtag(cls, value):
        if value is None:
            return value
        
        if "#" in value or "＃" in value:
            raise ValueError(
                "'#'や'＃'はハッシュタグの先頭に自動的に追加されます。"
            )
        return value

    @field_validator("name", "venue", "address", "hashtag", "description", "host")
    @classmethod
    def _disallow_newline(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        
        if "\n" in value or "\r" in value:
            raise ValueError("改行はできません")
        return value
    
    @field_validator("djs", "vjs")
    def _disallow_list_newline(cls, list_value: Optional[list[str]]) -> Optional[list[str]]:
        if list_value is None:
            return list_value
        
        if any("\n" in v or "\r" in v for v in list_value):
            raise ValueError("改行はできません")
        
        return list_value

    def _to_tweet_text(self) -> dict:
        return self.model_dump()
