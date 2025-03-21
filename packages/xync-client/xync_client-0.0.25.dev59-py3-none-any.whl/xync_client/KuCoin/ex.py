from asyncio import run

from x_model import init_db
from xync_schema import models
from xync_schema import types

from xync_client.Abc.Base import MapOfIdsList
from xync_client.Abc.Ex import BaseExClient
from xync_client.loader import PG_DSN
from xync_client.KuCoin.etype import pm, ad
from xync_client.Abc.types import PmEx


class ExClient(BaseExClient):
    async def _pms(self, cur) -> list[pm.PmE]:
        params = {
            'legal': cur,
            'lang': 'ru_RU',
        }
        pms = await self._get("/_api/otc/legal/payTypes", params=params)
        return [pm.PmE(**_pm) for _pm in pms["data"]]

    async def curs(self) -> list[types.CurEx]:
        curs = (await self._get("/_api/otc/dictionary/getData", {"type": "LEGAL"}))["data"]
        return {
            cur["typeCode"]:types.CurEx(exid=cur["typeCode"], ticker=cur["typeCode"]) for cur in curs
        }

    async def pms(self, cur: models.Cur = None) -> dict[int | str, PmEx]:
        all_pms = {}
        for cur_obj in (await self.curs()).values():
            pms = await self._pms(cur_obj.ticker)
            for pm in pms:
                all_pms[pm.payTypeCode] = PmEx(exid=pm.payTypeCode, name=pm.payTypeName)
        return all_pms

    async def cur_pms_map(self) -> MapOfIdsList:
        return {cur.exid: [pm.payTypeCode for pm in await self._pms(cur.ticker)] for cur in (await self.curs()).values()}

    async def coins(self) -> list[types.CoinEx]:
        all_coins = {}
        for cur in (await self.curs()).keys():
            params = {
                'legal': cur,
                'lang': 'ru_RU',
            }
            coins = await self._get("/_api/otc/symbol/support", params=params)
            for coin in coins["data"]:
                all_coins[coin["currency"]] = types.CoinEx(exid=coin["currency"] ,ticker=coin["currency"], scale=coin["currencyPrecision"])
        return all_coins

    async def pairs(self) -> MapOfIdsList:
        coins = (await self.coins()).keys()
        curs = (await self.curs()).keys()
        s = {cur: {c for c in coins} for cur in curs}
        return s, s

    async def ads(
            self, coin_exid: str, cur_exid: str, is_sell: bool, pm_exids: list[str | int] = None, amount: int = None
    ) -> list[ad.Ad]:
        pass


async def main():
    _ = await init_db(PG_DSN, models, True)
    bg = await Ex.get(name="KuCoin")
    cl = ExClient(bg)
    # await cl.curs()
    # await cl.coins()
    await cl.pms()


if __name__ == "__main__":
    run(main())
