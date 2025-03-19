from asyncio import run

from msgspec import convert
from x_model import init_db
from xync_schema import models, types
from xync_schema.models import Ex, Cur
from xync_schema.enums import PmType

from xync_client.Abc.Base import MapOfIdsList
from xync_client.Abc.Ex import BaseExClient
from xync_client.Abc.types import PmEx
from xync_client.Htx.etype import pm, Country, ad
from xync_client.loader import PG_DSN


class ExClient(BaseExClient):
    def pm_type_map(self, typ: models.Pmex) -> str:
        pass

    async def pairs(self) -> tuple[MapOfIdsList, MapOfIdsList]:
        self.session.headers["client-type"] = "web"
        reb = (await self._get("/-/x/otc/v1/trade/fast/config/list?side=buy&tradeMode=c2c_simple"))["data"]
        res = (await self._get("/-/x/otc/v1/trade/fast/config/list?side=sell&tradeMode=c2c_simple"))["data"]
        coins = await self.coins()
        curs = await self.curs()
        b = {
            cur.exid: cns
            for tkr, cur in curs.items()
            if (
                cns := set(
                    coins[c["cryptoAsset"]["name"]].exid for c in reb if tkr in [q["name"] for q in c["quoteAsset"]]
                )
            )
        }
        s = {
            cur.exid: cns
            for tkr, cur in curs.items()
            if (
                cns := set(
                    coins[c["cryptoAsset"]["name"]].exid for c in res if tkr in [q["name"] for q in c["quoteAsset"]]
                )
            )
        }
        return b, s

    async def ads(
        self, coin_exid: int, cur_exid: int, is_sell: bool, pm_exids: list[str] = None, amount: int = None
    ) -> list[types.BaseAd]:
        params = {
            "coinId": coin_exid,
            "currency": cur_exid,
            "tradeType": "sell" if is_sell else "buy",
            "currPage": 1,
            "payMethod": ",".join(pm_exids) if pm_exids else 0,
            "acceptOrder": 0,
            "blockType": "general",
            "online": 1,
            "range": 0,
            "amount": amount or "",
            "onlyTradable": "false",
            "isFollowed": "false",
        }
        res = (await self._get("/-/x/otc/v1/data/trade-market", params))["data"]
        ads = [ad.Resp(**a) for a in res]
        return ads

    async def ad(self, ad_id: int) -> types.BaseAd:
        pass

    # 20: Get all pms
    async def pms(self, _cur: Cur = None) -> dict[int, PmEx]:
        dist = {
            0: PmType.card,
            1: PmType.bank,
            2: PmType.cash,
            3: PmType.emoney,
            4: PmType.emoney,
            5: PmType.IFSC,
        }

        pms: list[pm.Resp] = [convert(p, pm.Resp) for p in (await self._coin_curs_pms())["payMethod"]]

        pmsd = {
            p.payMethodId: PmEx(
                exid=p.payMethodId,
                name=p.name,
                typ=dist.get(p.template),
                logo=p.bankImage or p.bankImageWeb,
            )
            for p in pms
        }

        return pmsd

    # 21: Get all: currency,pay,allCountry,coin
    async def curs(self) -> dict[str, types.CurEx]:
        self.session.headers["client-type"] = "web"
        curs: list[dict] = (await self._coin_curs_pms())["currency"]
        cmap: dict[str, int] = {c["nameShort"]: c["currencyId"] for c in curs}
        res = (await self._get("/-/x/otc/v1/trade/fast/config/list?side=sell&tradeMode=c2c_simple"))["data"]
        cursd: dict[str, float] = {}
        for c in res:
            for q in c["quoteAsset"]:
                cursd[q["name"]] = max(cursd.get(q["name"], 0), float(q["minAmount"]))
        return {tkr: types.CurEx(exid=exid, ticker=tkr, minimum=cursd.get(tkr)) for tkr, exid in cmap.items()}

    # 22: Список платежных методов по каждой валюте
    async def cur_pms_map(self) -> dict[int, set[int]]:
        res = await self._coin_curs_pms()
        wrong_pms = {4, 34, 498, 548, 20009, 20010}  # , 212, 239, 363  # these ids not exist in pms
        return {c["currencyId"]: set(c["supportPayments"]) - wrong_pms for c in res["currency"] if c["supportPayments"]}

    # 23: Список торгуемых монет
    async def coins(self) -> dict[str, types.CoinEx]:
        self.session.headers["client-type"] = "web"
        coins: list[dict] = (await self._coin_curs_pms())["coin"]
        cmap: dict[str, int] = {c["coinCode"]: c["coinId"] for c in coins}
        res = (await self._get("/-/x/otc/v1/trade/fast/config/list?side=buy&tradeMode=c2c_simple"))["data"]
        coinsl: list[str] = [c["cryptoAsset"]["name"] for c in res]
        return {tkr: types.CoinEx(exid=cid, ticker=tkr, p2p=tkr in coinsl) for tkr, cid in cmap.items()}

    # 99: Страны
    async def countries(self) -> list[Country]:
        cmap = {
            "Kazakstan": "Kazakhstan",
        }
        res = await self._coin_curs_pms()
        cts = [
            Country(
                id=c["countryId"],
                code=c["code"],
                name=cmap.get(ct := name[:-1] if (name := c["name"].split(",")[0]).endswith(".") else name, ct),
                short=c["appShort"],
                cur_id=c["currencyId"],
            )
            for c in res["country"]
        ]
        return cts

    # Get all: currency,pay,allCountry,coin
    async def _coin_curs_pms(self) -> (dict, dict, dict, dict):
        res = (await self._get("/-/x/otc/v1/data/config-list?type=currency,pay,coin,allCountry"))["data"]
        res["currency"][0]["currencyId"] = 1
        [c.update({"currencyId": 1, "name": ""}) for c in res["country"] if c["currencyId"] == 172]
        return res


async def main():
    _ = await init_db(PG_DSN, models, True)
    ex = await Ex.get(name="Htx")
    cl = ExClient(ex)
    await cl.pms()
    await cl.pairs()
    await cl.set_pmcurexs()
    await cl.set_coinexs()
    await cl.close()


if __name__ == "__main__":
    run(main())
