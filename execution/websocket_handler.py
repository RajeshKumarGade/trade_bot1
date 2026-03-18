import threading

from kiteconnect import KiteTicker


class PriceTracker:
    def __init__(self, api_key, access_token, instrument_token, on_price, on_close=None):
        self._kws = KiteTicker(api_key, access_token)
        self._instrument_token = instrument_token
        self._on_price = on_price
        self._on_close = on_close
        self._closed = threading.Event()

    def _handle_ticks(self, ws, ticks):
        for tick in ticks:
            if tick.get("instrument_token") != self._instrument_token:
                continue
            self._on_price(ws, tick.get("last_price"))

    def _handle_connect(self, ws, _response):
        ws.subscribe([self._instrument_token])
        ws.set_mode(ws.MODE_LTP, [self._instrument_token])

    def _handle_close(self, ws, _code, _reason):
        self._closed.set()
        if self._on_close:
            self._on_close(ws)

    def connect(self):
        self._kws.on_ticks = self._handle_ticks
        self._kws.on_connect = self._handle_connect
        self._kws.on_close = self._handle_close
        self._kws.connect(threaded=True)

    def wait(self):
        self._closed.wait()
