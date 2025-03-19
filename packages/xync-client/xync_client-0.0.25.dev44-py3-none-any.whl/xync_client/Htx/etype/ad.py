from typing import Literal

from pydantic import BaseModel
from xync_schema.types import BaseAd


class TradeRule(BaseModel):
    title: str
    titleValue: str
    content: str
    inputType: int
    inputValue: str
    hint: str
    contentCode: str
    sort: int


class Req(BaseModel):
    tradeType: int
    coinId: int
    currency: int
    minTradeLimit: float
    maxTradeLimit: float
    tradeCount: float
    password: str
    securityToken: str | None = ""
    payTerm: int
    isFixed: Literal["off", "on"]
    premium: int
    fixedPrice: str | None = ""
    autoReplyContent: str | None = ""
    isAutoReply: Literal["off", "on"]
    tradeRule: str | None = ""
    takerAcceptOrder: int
    isPayCode: Literal["off", "on"]
    isVerifyCapital: bool
    receiveAccounts: int
    deviation: int
    isTakerLimit: Literal["off", "on"]
    blockType: int
    session: int
    chargeType: bool
    apiVersion: int
    channel: str
    tradeRulesV2: list[TradeRule]


class PayMethod(BaseModel):
    payMethodId: int
    name: str
    color: str
    isRecommend: bool | None = None


class PayName(BaseModel):
    bankType: int
    id: int


class Resp(BaseAd):
    blockType: int
    chargeType: bool
    coinId: int
    currency: int
    gmtSort: int
    id: int
    isCopyBlock: bool
    isFollowed: bool
    isOnline: bool
    isTrade: bool
    isVerifyCapital: bool
    labelName: str | None = None
    maxTradeLimit: str
    merchantLevel: int
    merchantTags: list[str] | None
    minTradeLimit: str
    orderCompleteRate: str
    payMethod: str
    payMethods: list[PayMethod]
    payName: str  # list[PayName]  # приходит массив объектов внутри строки
    payTerm: int
    price: str
    seaViewRoom: str | None = None
    takerAcceptAmount: str
    takerAcceptOrder: int
    takerLimit: int
    thumbUp: int
    totalTradeOrderCount: int
    tradeCount: str
    tradeMonthTimes: int
    tradeType: int
    uid: int
    userName: str
