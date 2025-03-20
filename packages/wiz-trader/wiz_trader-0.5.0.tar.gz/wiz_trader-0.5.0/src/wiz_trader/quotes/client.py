import asyncio
import json
import os
import logging
import random
from typing import Callable, List, Optional

import websockets
from websockets.exceptions import ConnectionClosed
from websockets.protocol import State

# Setup module-level logger with a default handler if none exists.
logger = logging.getLogger(__name__)
if not logger.handlers:
  handler = logging.StreamHandler()
  formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
  handler.setFormatter(formatter)
  logger.addHandler(handler)


class QuotesClient:
  """
  A Python SDK for connecting to the Quotes Server via WebSocket.

  Attributes:
    base_url (str): WebSocket URL of the quotes server.
    token (str): JWT token for authentication.
    on_tick (Callable[[dict], None]): Callback to process received tick data.
    log_level (str): Logging level. Options: "error", "info", "debug".
  """

  def __init__(
    self, 
    base_url: Optional[str] = None, 
    token: Optional[str] = None,
    log_level: str = "error"  # default only errors
  ):
    # Configure logger based on log_level.
    valid_levels = {"error": logging.ERROR, "info": logging.INFO, "debug": logging.DEBUG}
    if log_level not in valid_levels:
      raise ValueError(f"log_level must be one of {list(valid_levels.keys())}")
    logger.setLevel(valid_levels[log_level])
    
    self.log_level = log_level
    # System env vars take precedence over .env
    self.base_url = base_url or os.environ.get("WZ__QUOTES_BASE_URL")
    self.token = token or os.environ.get("WZ__TOKEN")
    if not self.token:
      raise ValueError("JWT token must be provided as an argument or in .env (WZ__TOKEN)")
    if not self.base_url:
      raise ValueError("Base URL must be provided as an argument or in .env (WZ__QUOTES_BASE_URL)")

    # Construct the WebSocket URL.
    self.url = f"{self.base_url}?token={self.token}"
    self.ws: Optional[websockets.WebSocketClientProtocol] = None
    self.on_tick: Optional[Callable[[dict], None]] = None
    self.subscribed_instruments: set = set()

    # Backoff configuration for reconnection (in seconds)
    self._backoff_base = 1
    self._backoff_factor = 2
    self._backoff_max = 60

    logger.debug("Initialized QuotesClient with URL: %s", self.url)

  async def connect(self) -> None:
    """
    Continuously connect to the quotes server and process incoming messages.
    Implements an exponential backoff reconnection strategy.
    """
    backoff = self._backoff_base

    while True:
      try:
        logger.info("Connecting to %s ...", self.url)
        async with websockets.connect(self.url) as websocket:
          self.ws = websocket
          logger.info("Connected to the quotes server.")
          
          # On reconnection, re-subscribe if needed.
          if self.subscribed_instruments:
            subscribe_msg = {
              "action": "subscribe",
              "instruments": list(self.subscribed_instruments)
            }
            await self.ws.send(json.dumps(subscribe_msg))
            logger.info("Re-subscribed to instruments: %s", list(self.subscribed_instruments))

          # Reset backoff after a successful connection.
          backoff = self._backoff_base

          await self._handle_messages()
      except ConnectionClosed as e:
        logger.info("Disconnected from the quotes server: %s", e)
      except Exception as e:
        logger.error("Connection error: %s", e, exc_info=True)

      # Exponential backoff before reconnecting.
      sleep_time = min(backoff, self._backoff_max)
      logger.info("Reconnecting in %s seconds...", sleep_time)
      await asyncio.sleep(sleep_time)
      backoff *= self._backoff_factor
      # Add a bit of randomness to avoid thundering herd issues.
      backoff += random.uniform(0, 1)

  async def _handle_messages(self) -> None:
    """
    Handle incoming messages and dispatch them via the on_tick callback.
    """
    try:
      async for message in self.ws:  # type: ignore
        try:
          tick = json.loads(message)
          if self.on_tick:
            self.on_tick(tick)
          else:
            logger.debug("Received tick (no on_tick callback set): %s", tick)
        except json.JSONDecodeError:
          logger.debug("Received non-JSON message: %s", message)
    except ConnectionClosed as e:
      logger.info("Connection closed during message handling: %s", e)

  async def subscribe(self, instruments: List[str]) -> None:
    """
    Subscribe to a list of instruments and update the subscription list.

    Args:
      instruments (List[str]): List of instrument identifiers.
    """
    if self.ws and self.ws.state == State.OPEN:
      new_instruments = set(instruments) - self.subscribed_instruments
      if new_instruments:
        self.subscribed_instruments.update(new_instruments)
        message = {"action": "subscribe", "instruments": list(new_instruments)}
        await self.ws.send(json.dumps(message))
        logger.info("Sent subscription message for instruments: %s", list(new_instruments))
      else:
        logger.info("Instruments already subscribed: %s", instruments)
    else:
      logger.info("Cannot subscribe: WebSocket is not connected.")

  async def unsubscribe(self, instruments: List[str]) -> None:
    """
    Unsubscribe from a list of instruments and update the subscription list.

    Args:
      instruments (List[str]): List of instrument identifiers.
    """
    if self.ws and self.ws.state == State.OPEN:
      unsub_set = set(instruments)
      if unsub_set & self.subscribed_instruments:
        self.subscribed_instruments.difference_update(unsub_set)
        message = {"action": "unsubscribe", "instruments": list(unsub_set)}
        await self.ws.send(json.dumps(message))
        logger.info("Sent unsubscription message for instruments: %s", list(unsub_set))
      else:
        logger.info("No matching instruments found in current subscription.")
    else:
      logger.info("Cannot unsubscribe: WebSocket is not connected.")

  async def close(self) -> None:
    """
    Close the WebSocket connection.
    """
    if self.ws:
      await self.ws.close()
      logger.info("WebSocket connection closed.")
