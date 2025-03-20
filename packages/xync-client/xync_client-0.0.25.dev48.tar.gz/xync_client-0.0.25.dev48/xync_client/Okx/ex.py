from asyncio import run

from x_model import init_db
from xync_schema import models
from xync_schema import types

from xync_client.Abc.Base import MapOfIdsList
from xync_client.Abc.Ex import BaseExClient
from xync_client.loader import PG_DSN
from xync_client.Okx.pyd import PmE, Ads, Ad


class ExClient(BaseExClient):
    async def _pms(self, cur) -> list[PmE]:
        params = {
            "quoteCurrency": f"{cur}",
            "needField": "false",
        }
        pms = await self._get("/v3/c2c/configs/receipt/templates", params=params)
        return [PmE(**pm) for pm in pms["data"]]

    # 19: Список поддерживаемых валют тейкера
    async def curs(self) -> list[types.CurE]:  # {cur.exid: cur.ticker}
        curs = await self._get("/v3/users/common/list/currencies")
        return [types.CurE(exid=cur["currencyId"], ticker=cur["displayName"]) for cur in curs["data"]]

    # 20: Список платежных методов
    async def pms(self, cur: models.Cur = None) -> dict[int | str, types.Pm]:  # {pm.exid: pm}
        all_pms = {}
        for cur in await self.curs():
            pms = await self._pms(cur.ticker)
            for pm in pms:
                all_pms[pm.transferSpeed] = types.Pm(name=pm.paymentMethod)
        return all_pms

    # 21: Список платежных методов по каждой валюте
    async def cur_pms_map(self) -> MapOfIdsList:  # {cur.exid: [pm.exid]}
        return {cur.ticker: [pm.paymentMethod for pm in await self._pms(cur.ticker)] for cur in await self.curs()}

    # 22: Список торгуемых монет (с ограничениям по валютам, если есть)
    async def coins(self) -> list[types.CoinE]:  # {coin.exid: coin.ticker}
        ...

    # 23: Список пар валюта/монет
    async def pairs(self) -> MapOfIdsList:
        coins = await self.coins()
        curs = await self.curs()
        return {cur.ticker: set(c.ticker for c in coins) for cur in curs}

    # 24: Список объяв по (buy/sell, cur, coin, pm)
    async def ads(
        self, coin_exid: str, cur_exid: str, is_sell: bool, pm_exids: list[str | int] = None, amount: int = None
    ) -> list[Ads]:  # {ad.id: ad}
        params = {
            "side": "sell",
            "paymentMethod": "all",
            "userType": "all",
            "hideOverseasVerificationAds": "true" if is_sell else "false",
            "sortType": "price_asc",
            "limit": "100",
            "cryptoCurrency": f"{coin_exid}",
            "fiatCurrency": f"{cur_exid}",
            "currentPage": "1",
            "numberPerPage": "5",
        }
        ads = await self._get("/v3/c2c/tradingOrders/getMarketplaceAdsPrelogin", params=params)
        return [Ads(**ad) for ad in ads["data"]["sell"]]

    # 42: Чужая объява по id
    async def ad(self, ad_id: int) -> Ad:
        params = {
            "publicUserId": "f81434eb2a",
            "t": f"{ad_id}",
        }
        ad = await self._get("/v3/c2c/merchant/liteProfile", params=params)
        return Ad(**ad)


async def main():
    _ = await init_db(PG_DSN, models, True)
    bg = await models.Ex.get(name="Okx")
    cl = ExClient(bg)
    await cl.curs()
    # await cl.coins()
    # await cl.pms()
    await cl.close()


if __name__ == "__main__":
    run(main())
