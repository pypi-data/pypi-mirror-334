from __future__ import annotations

from typing import Any, List

from pydantic import BaseModel, Field

from ..setting import Domains


class Multiple(BaseModel):
    min_price: float | None = None
    max_price: float | None = None
    model_id: str | None = None
    title: str | None = None
    current_price: float | None = None


class Store(BaseModel):
    # image: str
    # link: str
    name: str | None = None
    discount_info: str | None = None
    # rate_desc: str | None = None
    # is_cashback: bool


class Shop(BaseModel):
    name: str | None = None
    username: str | None = None
    uid: str | None = None
    location: str | None = None
    # seller_credit: int | None = None


class ListItem(BaseModel):
    nindex: str | None = None
    oid: str | None = None
    # subscribe_id: Any
    history_id: str | None = None
    item_id: str | None = None
    # is_ad: bool
    # is_group: bool
    # is_offline: bool
    # is_notfound: bool
    # is_expired: bool
    # is_adult: bool
    # is_multiple_product: bool
    # is_subscribe: bool
    title: str | None = None

    # purl: str | None = None
    affurl: str | None = None
    url: str | None = None

    image: str | None = None
    # gallery_count: int
    # origin_image: str
    cata: List | None = None
    symbol: str | None = None
    currency: str | None = None
    multiple: Multiple | None = None
    price: float | None = None
    price_range_min: Any | None = None
    price_range_max: Any | None = None
    count_result_store: Any | None = None
    count_result_product: Any | None = None
    store: Store | None = None
    has_shop: bool | None = None
    shop: Shop | None = None
    price_diff_real: float | None = None
    product_nindex_price: List | None = None
    # subscribe_tags: List
    # subscribe_time: Any


class BiggoCItem(BaseModel):
    key: str | None = None
    value: str | None = None
    time: int | None = None


class ProductSearchAPIRet(BaseModel):
    # result: bool
    # total: int
    # total_page: int
    # pure_total: int
    # ec_count: int
    # mall_count: int
    # bid_count: int
    # size: int
    # took: int
    # is_shop: bool
    # is_suggest_query: bool
    # is_ypa: bool
    # is_adsense: bool
    # q_suggest: str
    # arr_suggest: List[str]
    # offline_count: int
    # spam_count: int
    # promo: List
    # filter: Dict[str, Any]
    # top_ad_count: int
    # group: Any
    # recommend_group: List
    list: List[ListItem] = Field(default_factory=list)
    # biggo_c: List[BiggoCItem]
    low_price: float | None = None
    high_price: float | None = None

    def generate_r_link(self, domain: Domains):
        for product in self.list:
            product.url = f"https://{domain.value}{product.affurl}"
            product.affurl = None
