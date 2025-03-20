import msgspec
from typing import List
from nexustrader.schema import BaseMarket
from decimal import Decimal
from msgspec import Struct

from nexustrader.schema import Balance
from nexustrader.exchange.okx.constants import (
    OkxInstrumentType,
    OkxInstrumentFamily,
    OkxOrderType,
    OkxOrderSide,
    OkxPositionSide,
    OkxTdMode,
    OkxOrderStatus,
)


class OkxWsArgMsg(msgspec.Struct):
    channel: str | None = None
    instType: OkxInstrumentType | None = None
    instFamily: OkxInstrumentFamily | None = None
    instId: str | None = None
    uid: str | None = None


class OkxWsGeneralMsg(msgspec.Struct):
    event: str | None = None
    msg: str | None = None
    code: str | None = None
    connId: str | None = None
    channel: str | None = None
    arg: OkxWsArgMsg | None = None

    @property
    def is_event_msg(self) -> bool:
        return self.event is not None


class OkxWsBboTbtData(msgspec.Struct):
    ts: str
    seqId: int
    asks: list[list[str]]
    bids: list[list[str]]


class OkxWsBboTbtMsg(msgspec.Struct):
    """
    {
        "arg": {
            "channel": "bbo-tbt",
            "instId": "BCH-USDT-SWAP"
        },
        "data": [
            {
            "asks": [
                [
                "111.06","55154","0","2"
                ]
            ],
            "bids": [
                [
                "111.05","57745","0","2"
                ]
            ],
            "ts": "1670324386802",
            "seqId": 363996337
            }
        ]
    }
    """

    arg: OkxWsArgMsg
    data: list[OkxWsBboTbtData]


class OkxWsCandleMsg(msgspec.Struct):
    arg: OkxWsArgMsg
    data: list[list[str]]


class OkxWsTradeData(msgspec.Struct):
    instId: str
    tradeId: str
    px: str
    sz: str
    side: str
    ts: str
    count: str


class OkxWsTradeMsg(msgspec.Struct):
    arg: OkxWsArgMsg
    data: list[OkxWsTradeData]


class OkxWsOrderData(msgspec.Struct):
    instType: OkxInstrumentType
    instId: str
    tgtCcy: str
    ccy: str
    ordId: str
    clOrdId: str
    tag: str
    px: str
    pxUsd: str
    pxVol: str
    pxType: str
    sz: str
    notionalUsd: str
    ordType: OkxOrderType
    side: OkxOrderSide
    posSide: OkxPositionSide
    tdMode: OkxTdMode
    fillPx: str  # last fill price
    tradeId: str  # last trade id
    fillSz: str  # last filled quantity
    fillPnl: str  # last filled profit and loss
    fillTime: str  # last filled time
    fillFee: str  # last filled fee
    fillFeeCcy: str  # last filled fee currency
    fillPxVol: str  # last filled price volume
    fillPxUsd: str  # last filled price in USD
    fillMarkVol: str  # last filled mark volume
    fillFwdPx: str  # last filled forward price
    fillMarkPx: str  # last filled mark price
    execType: str  # last execution type
    accFillSz: str  # accumulated filled quantity
    fillNotionalUsd: str  # accumulated filled notional in USD
    avgPx: str  # average price
    state: OkxOrderStatus
    lever: str  # leverage
    attachAlgoClOrdId: str  # attached algo order id
    tpTriggerPx: str  # take profit trigger price
    tpTriggerPxType: str  # take profit trigger price type
    tpOrdPx: str  # take profit order price
    slTriggerPx: str  # stop loss trigger price
    slTriggerPxType: str  # stop loss trigger price type
    slOrdPx: str  # stop loss order price
    stpMode: str  # stop loss mode
    feeCcy: str  # fee currency
    fee: str  # fee
    rebateCcy: str  # rebate currency
    rebate: str  # rebate
    pnl: str
    source: str
    cancelSource: str
    amendSource: str
    category: str
    isTpLimit: bool
    uTime: int
    cTime: int
    reqId: str
    amendResult: str
    reduceOnly: bool
    quickMgnType: str
    algoClOrdId: str
    algoId: str
    lastPx: str  # last price
    code: str
    msg: str


class OkxWsOrderMsg(msgspec.Struct):
    arg: OkxWsArgMsg
    data: List[OkxWsOrderData]


################################################################################
# Place Order: POST /api/v5/trade/order
################################################################################


class OkxPlaceOrderData(msgspec.Struct):
    ordId: str
    clOrdId: str
    tag: str
    ts: str  # milliseconds when OKX finished order request processing
    sCode: str  # event code, "0" means success
    sMsg: str  # rejection or success message of event execution


class OkxPlaceOrderResponse(msgspec.Struct):
    code: str
    msg: str
    data: list[OkxPlaceOrderData]
    inTime: str  # milliseconds when request hit REST gateway
    outTime: str  # milliseconds when response leaves REST gateway


################################################################################
# Cancel order: POST /api/v5/trade/cancel-order
################################################################################


class OkxGeneralResponse(msgspec.Struct):
    code: str
    msg: str


class OkxErrorData(msgspec.Struct):
    sCode: str
    sMsg: str


class OkxErrorResponse(msgspec.Struct):
    code: str
    data: list[OkxErrorData]
    msg: str


class OkxCancelOrderData(msgspec.Struct):
    ordId: str
    clOrdId: str
    ts: str  # milliseconds when OKX finished order request processing
    sCode: str  # event code, "0" means success
    sMsg: str  # rejection or success message of event execution


class OkxCancelOrderResponse(msgspec.Struct):
    code: str
    msg: str
    data: list[OkxCancelOrderData]
    inTime: str  # milliseconds when request hit REST gateway
    outTime: str  # milliseconds when response leaves REST gateway


class OkxMarketInfo(msgspec.Struct):
    """
    {
        "alias": "",
        "auctionEndTime": "",
        "baseCcy": "BTC",
        "category": "1",
        "ctMult": "",
        "ctType": "",
        "ctVal": "",
        "ctValCcy": "",
        "expTime": "",
        "instFamily": "",
        "instId": "BTC-USDT",
        "instType": "SPOT",
        "lever": "10",
        "listTime": "1611907686000",
        "lotSz": "0.00000001",
        "maxIcebergSz": "9999999999.0000000000000000",
        "maxLmtAmt": "20000000",
        "maxLmtSz": "9999999999",
        "maxMktAmt": "1000000",
        "maxMktSz": "1000000",
        "maxStopSz": "1000000",
        "maxTriggerSz": "9999999999.0000000000000000",
        "maxTwapSz": "9999999999.0000000000000000",
        "minSz": "0.00001",
        "optType": "",
        "quoteCcy": "USDT",
        "ruleType": "normal",
        "settleCcy": "",
        "state": "live",
        "stk": "",
        "tickSz": "0.1",
        "uly": ""
    },

    {
        "alias": "this_week",
        "auctionEndTime": "",
        "baseCcy": "",
        "category": "1",
        "ctMult": "1",
        "ctType": "linear",
        "ctVal": "0.01",
        "ctValCcy": "BTC",
        "expTime": "1731657600000",
        "instFamily": "BTC-USDT",
        "instId": "BTC-USDT-241115",
        "instType": "FUTURES",
        "lever": "20",
        "listTime": "1730448600359",
        "lotSz": "0.1",
        "maxIcebergSz": "1000000.0000000000000000",
        "maxLmtAmt": "20000000",
        "maxLmtSz": "1000000",
        "maxMktAmt": "",
        "maxMktSz": "3000",
        "maxStopSz": "3000",
        "maxTriggerSz": "1000000.0000000000000000",
        "maxTwapSz": "1000000.0000000000000000",
        "minSz": "0.1",
        "optType": "",
        "quoteCcy": "",
        "ruleType": "normal",
        "settleCcy": "USDT",
        "state": "live",
        "stk": "",
        "tickSz": "0.1",
        "uly": "BTC-USDT"
    },

    {
        "alias": "",
        "auctionEndTime": "",
        "baseCcy": "",
        "category": "1",
        "ctMult": "1",
        "ctType": "linear",
        "ctVal": "0.01",
        "ctValCcy": "BTC",
        "expTime": "",
        "instFamily": "BTC-USDT",
        "instId": "BTC-USDT-SWAP",
        "instType": "SWAP",
        "lever": "100",
        "listTime": "1573557408000",
        "lotSz": "0.1",
        "maxIcebergSz": "100000000.0000000000000000",
        "maxLmtAmt": "20000000",
        "maxLmtSz": "100000000",
        "maxMktAmt": "",
        "maxMktSz": "12000",
        "maxStopSz": "12000",
        "maxTriggerSz": "100000000.0000000000000000",
        "maxTwapSz": "100000000.0000000000000000",
        "minSz": "0.1",
        "optType": "",
        "quoteCcy": "",
        "ruleType": "normal",
        "settleCcy": "USDT",
        "state": "live",
        "stk": "",
        "tickSz": "0.1",
        "uly": "BTC-USDT"
    },
    """

    alias: str | None = None  # Alias (this_week, next_week, etc)
    auctionEndTime: str | None = None  # Auction end time
    baseCcy: str | None = None  # Base currency
    category: str | None = None  # Category
    ctMult: str | None = None  # Contract multiplier
    ctType: str | None = None  # Contract type (linear/inverse)
    ctVal: str | None = None  # Contract value
    ctValCcy: str | None = None  # Contract value currency
    expTime: str | None = None  # Expiry time
    instFamily: str | None = None  # Instrument family
    instId: str | None = None  # Instrument ID
    instType: str | None = None  # Instrument type (SPOT/FUTURES/SWAP)
    lever: str | None = None  # Leverage
    listTime: str | None = None  # Listing time
    lotSz: str | None = None  # Lot size
    maxIcebergSz: str | None = None  # Maximum iceberg order size
    maxLmtAmt: str | None = None  # Maximum limit order amount
    maxLmtSz: str | None = None  # Maximum limit order size
    maxMktAmt: str | None = None  # Maximum market order amount
    maxMktSz: str | None = None  # Maximum market order size
    maxStopSz: str | None = None  # Maximum stop order size
    maxTriggerSz: str | None = None  # Maximum trigger order size
    maxTwapSz: str | None = None  # Maximum TWAP order size
    minSz: str | None = None  # Minimum order size
    optType: str | None = None  # Option type
    quoteCcy: str | None = None  # Quote currency
    ruleType: str | None = None  # Rule type
    settleCcy: str | None = None  # Settlement currency
    state: str | None = None  # Instrument state
    stk: str | None = None  # Strike price
    tickSz: str | None = None  # Tick size
    uly: str | None = None  # Underlying


class OkxMarket(BaseMarket):
    """
     {
        "id": "BTC-USDT-SWAP",
        "lowercaseId": null,
        "symbol": "BTC/USDT:USDT",
        "base": "BTC",
        "quote": "USDT",
        "settle": "USDT",
        "baseId": "BTC",
        "quoteId": "USDT",
        "settleId": "USDT",
        "type": "swap",
        "spot": false,
        "margin": false,
        "swap": true,
        "future": false,
        "option": false,
        "index": null,
        "active": true,
        "contract": true,
        "linear": true,
        "inverse": false,
        "subType": "linear",
        "taker": 0.0005,
        "maker": 0.0002,
        "contractSize": 0.01,
        "expiry": null,
        "expiryDatetime": null,
        "strike": null,
        "optionType": null,
        "precision": {
            "amount": 0.1,
            "price": 0.1,
            "cost": null,
            "base": null,
            "quote": null
        },
        "limits": {
            "leverage": {
                "min": 1.0,
                "max": 100.0
            },
            "amount": {
                "min": 0.1,
                "max": null
            },
            "price": {
                "min": null,
                "max": null
            },
            "cost": {
                "min": null,
                "max": null
            }
        },
        "marginModes": {
            "cross": null,
            "isolated": null
        },
        "created": 1573557408000,
        "info": {
            "alias": "",
            "auctionEndTime": "",
            "baseCcy": "",
            "category": "1",
            "ctMult": "1",
            "ctType": "linear",
            "ctVal": "0.01",
            "ctValCcy": "BTC",
            "expTime": "",
            "instFamily": "BTC-USDT",
            "instId": "BTC-USDT-SWAP",
            "instType": "SWAP",
            "lever": "100",
            "listTime": "1573557408000",
            "lotSz": "0.1",
            "maxIcebergSz": "100000000.0000000000000000",
            "maxLmtAmt": "20000000",
            "maxLmtSz": "100000000",
            "maxMktAmt": "",
            "maxMktSz": "12000",
            "maxStopSz": "12000",
            "maxTriggerSz": "100000000.0000000000000000",
            "maxTwapSz": "100000000.0000000000000000",
            "minSz": "0.1",
            "optType": "",
            "quoteCcy": "",
            "ruleType": "normal",
            "settleCcy": "USDT",
            "state": "live",
            "stk": "",
            "tickSz": "0.1",
            "uly": "BTC-USDT"
        },
        "tierBased": null,
        "percentage": null
    },
    """

    info: OkxMarketInfo


class OkxPositionCloseOrderAlgo(Struct):
    algoId: str | None = None
    slTriggerPx: str | None = None
    slTriggerPxType: str | None = None
    tpTriggerPx: str | None = None
    tpTriggerPxType: str | None = None
    closeFraction: str | None = None


class OkxPosition(Struct, kw_only=True):
    adl: str
    availPos: str
    avgPx: str
    baseBal: str | None = None
    baseBorrowed: str | None = None
    baseInterest: str | None = None
    bePx: str
    bizRefId: str | None = None
    bizRefType: str | None = None
    cTime: str
    ccy: str
    clSpotInUseAmt: str | None = None
    closeOrderAlgo: List[OkxPositionCloseOrderAlgo] = []
    deltaBS: str | None = None
    deltaPA: str | None = None
    fee: str
    fundingFee: str
    gammaBS: str | None = None
    gammaPA: str | None = None
    idxPx: str
    imr: str | None = None
    instId: str
    instType: str
    interest: str | None = None
    last: str
    lever: str
    liab: str | None = None
    liabCcy: str | None = None
    liqPenalty: str
    liqPx: str
    margin: str
    markPx: str
    maxSpotInUseAmt: str | None = None
    mgnMode: str
    mgnRatio: str
    mmr: str
    notionalUsd: str
    optVal: str | None = None
    pTime: str
    pendingCloseOrdLiabVal: str | None = None
    pnl: str
    pos: str
    posCcy: str | None = None
    posId: str
    posSide: OkxPositionSide
    quoteBal: str | None = None
    quoteBorrowed: str | None = None
    quoteInterest: str | None = None
    realizedPnl: str
    spotInUseAmt: str | None = None
    spotInUseCcy: str | None = None
    thetaBS: str | None = None
    thetaPA: str | None = None
    tradeId: str
    uTime: str
    upl: str
    uplLastPx: str
    uplRatio: str
    uplRatioLastPx: str
    usdPx: str
    vegaBS: str | None = None
    vegaPA: str | None = None


class OkxAccountDetail(Struct, kw_only=True):
    accAvgPx: str | None = None
    availBal: str
    availEq: str
    borrowFroz: str | None = None
    cashBal: str
    ccy: str
    clSpotInUseAmt: str | None = None
    coinUsdPrice: str
    crossLiab: str | None = None
    disEq: str
    eq: str
    eqUsd: str
    fixedBal: str
    frozenBal: str
    imr: str
    interest: str | None = None
    isoEq: str
    isoLiab: str | None = None
    isoUpl: str
    liab: str | None = None
    maxLoan: str | None = None
    maxSpotInUseAmt: str | None = None
    mgnRatio: str | None = None
    mmr: str
    notionalLever: str
    openAvgPx: str | None = None
    ordFrozen: str
    rewardBal: str
    smtSyncEq: str
    spotBal: str | None = None
    spotCopyTradingEq: str
    spotInUseAmt: str | None = None
    spotIsoBal: str
    spotUpl: str | None = None
    spotUplRatio: str | None = None
    stgyEq: str
    totalPnl: str | None = None
    totalPnlRatio: str | None = None
    twap: str
    uTime: str
    upl: str
    uplLiab: str | None = None

    def parse_to_balance(self) -> Balance:
        """Convert OKX account detail to standard Balance object"""
        return Balance(
            asset=self.ccy,
            free=Decimal(self.availBal),
            locked=Decimal(self.frozenBal),
        )


class OkxAccount(Struct):
    adjEq: str | None = None
    borrowFroz: str | None = None
    details: List[OkxAccountDetail] | None = None
    imr: str | None = None
    isoEq: str | None = None
    mgnRatio: str | None = None
    mmr: str | None = None
    notionalUsd: str | None = None
    ordFroz: str | None = None
    totalEq: str | None = None
    uTime: str | None = None
    upl: str | None = None

    def parse_to_balance(self) -> list[Balance]:
        return [detail.parse_to_balance() for detail in self.details]


class OkxWsPositionMsg(Struct):
    arg: dict
    data: List[OkxPosition]


class OkxWsAccountMsg(Struct):
    arg: dict
    data: List[OkxAccount]

################################################################################
# GET /api/v5/account/balance
################################################################################

class OkxBalanceDetail(msgspec.Struct):
    availBal: str  # Available balance
    availEq: str  # Available equity
    borrowFroz: str  # Potential borrowing IMR in USD
    cashBal: str  # Cash balance
    ccy: str  # Currency
    crossLiab: str  # Cross liabilities
    disEq: str  # Discount equity in USD
    eq: str  # Equity
    eqUsd: str  # Equity in USD
    smtSyncEq: str  # Smart sync equity
    spotCopyTradingEq: str  # Spot smart sync equity
    fixedBal: str  # Frozen balance for Dip/Peak Sniper
    frozenBal: str  # Frozen balance
    imr: str  # Cross initial margin requirement
    interest: str  # Accrued interest
    isoEq: str  # Isolated margin equity
    isoLiab: str  # Isolated liabilities
    isoUpl: str  # Isolated unrealized PnL
    liab: str  # Liabilities
    maxLoan: str  # Max loan
    mgnRatio: str  # Cross margin ratio
    mmr: str  # Cross maintenance margin requirement
    notionalLever: str  # Leverage
    ordFrozen: str  # Margin frozen for open orders
    rewardBal: str  # Trial fund balance
    spotInUseAmt: str  # Spot in use amount
    clSpotInUseAmt: str  # User-defined spot risk offset amount
    maxSpotInUse: str  # Max possible spot risk offset amount
    spotIsoBal: str  # Spot isolated balance
    stgyEq: str  # Strategy equity
    twap: str  # Risk indicator of auto liability repayment
    uTime: str  # Update time
    upl: str  # Unrealized PnL
    uplLiab: str  # Liabilities due to unrealized loss
    spotBal: str  # Spot balance
    openAvgPx: str  # Spot average cost price
    accAvgPx: str  # Spot accumulated cost price
    spotUpl: str  # Spot unrealized PnL
    spotUplRatio: str  # Spot unrealized PnL ratio
    totalPnl: str  # Spot accumulated PnL
    totalPnlRatio: str  # Spot accumulated PnL ratio
    
    def parse_to_balance(self) -> Balance:
        return Balance(
            asset=self.ccy,
            free=Decimal(self.availBal),
            locked=Decimal(self.frozenBal),
        )

class OkxBalanceData(msgspec.Struct):
    adjEq: str  # Adjusted/Effective equity in USD
    borrowFroz: str  # Potential borrowing IMR of account in USD
    details: list[OkxBalanceDetail]  # Detailed asset information
    imr: str  # Initial margin requirement in USD
    isoEq: str  # Isolated margin equity in USD
    mgnRatio: str  # Margin ratio in USD
    mmr: str  # Maintenance margin requirement in USD
    notionalUsd: str  # Notional value of positions in USD
    ordFroz: str  # Cross margin frozen for pending orders
    totalEq: str  # Total equity in USD
    uTime: int  # Update time
    upl: str  # Unrealized PnL in USD
    
    def parse_to_balances(self) -> list[Balance]:
        return [detail.parse_to_balance() for detail in self.details]

class OkxBalanceResponse(msgspec.Struct):
    code: str  # Response code
    data: list[OkxBalanceData]  # Balance data
    msg: str  # Response message

################################################################################
# GET /api/v5/account/positions
################################################################################


class OkxPositionResponseData(msgspec.Struct):
    adl: str
    availPos: str
    avgPx: str
    bePx: str
    bizRefId: str
    bizRefType: str
    cTime: str
    ccy: str
    clSpotInUseAmt: str
    closeOrderAlgo: List[OkxPositionCloseOrderAlgo]
    deltaBS: str
    deltaPA: str
    fee: str
    fundingFee: str
    gammaBS: str
    gammaPA: str
    idxPx: str
    imr: str
    instId: str
    instType: str
    interest: str
    last: str
    lever: str
    liab: str
    liabCcy: str
    liqPenalty: str
    liqPx: str
    margin: str
    markPx: str
    maxSpotInUseAmt: str
    mgnMode: str
    mgnRatio: str
    mmr: str
    notionalUsd: str
    optVal: str
    pendingCloseOrdLiabVal: str
    pnl: str
    pos: str
    posCcy: str
    posId: str
    posSide: OkxPositionSide
    realizedPnl: str
    spotInUseAmt: str
    spotInUseCcy: str
    thetaBS: str
    thetaPA: str
    tradeId: str
    uTime: int
    upl: str
    uplLastPx: str
    uplRatio: str
    uplRatioLastPx: str
    usdPx: str
    vegaBS: str
    vegaPA: str


class OkxPositionResponse(msgspec.Struct):
    code: str
    data: List[OkxPositionResponseData]
    msg: str

class OkxCandlesticksResponse(msgspec.Struct):
    code: str
    data: list['OkxCandlesticksResponseData']
    msg: str

class OkxCandlesticksResponseData(msgspec.Struct, array_like=True):
    """
    [
        "1597026383085",
        "3.721",
        "3.743",
        "3.677",
        "3.708",
        "8422410",
        "22698348.04828491",
        "12698348.04828491",
        "1"
    ],
    """
    ts: int
    o: str
    h: str
    l: str
    c: str
    vol: str
    volCcy: str
    volCcyQuote: str
    confirm: int
    
    
    
    