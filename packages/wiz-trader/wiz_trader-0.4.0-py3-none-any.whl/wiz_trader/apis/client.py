import os
import json
import logging
from typing import Dict, List, Optional, Union, Any

import requests

# Setup module-level logger with a default handler if none exists.
logger = logging.getLogger(__name__)
if not logger.handlers:
  handler = logging.StreamHandler()
  formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
  handler.setFormatter(formatter)
  logger.addHandler(handler)

class WizzerClient:
  """
  A Python SDK for connecting to the Wizzer's REST API.

  Attributes:
    base_url (str): Base URL of the Wizzer's API server.
    token (str): JWT token for authentication.
    log_level (str): Logging level. Options: "error", "info", "debug".
    strategy_id (str): Default strategy ID to use if not provided in methods.
  """

  def __init__(
    self,
    base_url: Optional[str] = None,
    token: Optional[str] = None,
    strategy_id: Optional[str] = None,
    log_level: str = "error"  # default only errors
  ):
    # Configure logger based on log_level.
    valid_levels = {"error": logging.ERROR, "info": logging.INFO, "debug": logging.DEBUG}
    if log_level not in valid_levels:
      raise ValueError(f"log_level must be one of {list(valid_levels.keys())}")
    logger.setLevel(valid_levels[log_level])

    self.log_level = log_level
    # System env vars take precedence over .env
    self.base_url = base_url or os.environ.get("WZ__API_BASE_URL")
    self.token = token or os.environ.get("WZ__TOKEN")
    self.strategy_id = strategy_id or os.environ.get("WZ__STRATEGY_ID")
    
    if not self.token:
      raise ValueError("JWT token must be provided as an argument or in .env (WZ__TOKEN)")
    if not self.base_url:
      raise ValueError("Base URL must be provided as an argument or in .env (WZ__API_BASE_URL)")

    # Prepare the authorization header
    self.headers = {
      "Authorization": f"Bearer {self.token}",
      "Content-Type": "application/json"
    }

    logger.debug("Initialized WizzerClient with URL: %s", self.base_url)

  def _get_strategy(self, strategy: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """
    Get strategy information, either from the provided parameter or from the default.
    
    Args:
      strategy (Optional[Dict[str, str]]): Strategy object with id, identifier, and name.
    
    Returns:
      Dict[str, str]: A strategy object with at least the id field.
        
    Raises:
      ValueError: If no strategy is provided and no default is set.
    """
    if strategy and "id" in strategy:
      return strategy
    
    if not self.strategy_id:
      raise ValueError("Strategy ID must be provided either as a parameter or set in .env (WZ__STRATEGY_ID)")
    
    return {"id": self.strategy_id}

  # ===== DATA HUB METHODS =====

  def get_indices(self, trading_symbol: Optional[str] = None, exchange: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get list of indices available on the exchange.

    Args:
      trading_symbol (Optional[str]): Filter by specific index symbol.
      exchange (Optional[str]): Filter by specific exchange (NSE, BSE).

    Returns:
      List[Dict[str, Any]]: List of index information.
    """
    endpoint = "/datahub/indices"
    params = {}
    
    if trading_symbol:
      params["tradingSymbol"] = trading_symbol
    if exchange:
      params["exchange"] = exchange

    logger.debug("Fetching indices with params: %s", params)
    response = self._make_request("GET", endpoint, params=params)
    return response

  def get_index_components(self, trading_symbol: str, exchange: str) -> List[Dict[str, Any]]:
    """
    Get list of components (stocks) for a specific index.

    Args:
      trading_symbol (str): Index symbol (e.g., "NIFTY 50").
      exchange (str): Exchange name (NSE, BSE).

    Returns:
       List[Dict[str, Any]]: List of component stocks in the index.
    """
    endpoint = "/datahub/index/components"
    params = {
      "tradingSymbol": trading_symbol,
      "exchange": exchange
    }

    logger.debug("Fetching index components with params: %s", params)
    response = self._make_request("GET", endpoint, params=params)
    return response

  def get_historical_ohlcv(
    self, 
    instruments: List[str], 
    start_date: str, 
    end_date: str, 
    ohlcv: List[str],
    interval: str = "1d"
  ) -> List[Dict[str, Any]]:
    """
    Get historical OHLCV data for specified instruments.

    Args:
      instruments (List[str]): List of instrument identifiers (e.g., ["NSE:SBIN:3045"]).
      start_date (str): Start date in YYYY-MM-DD format.
      end_date (str): End date in YYYY-MM-DD format.
      ohlcv (List[str]): List of OHLCV fields to retrieve (open, high, low, close, volume).
      interval (str, optional): Data interval. Options: "1d" (daily, default), "1M" (monthly - last trading day of month).

    Returns:
      List[Dict[str, Any]]: Historical data for requested instruments.
    """
    endpoint = "/datahub/historical/ohlcv"
    data = {
      "instruments": instruments,
      "startDate": start_date,
      "endDate": end_date,
      "ohlcv": ohlcv,
      "interval": interval
    }

    logger.debug("Fetching historical OHLCV with data: %s", data)
    response = self._make_request("POST", endpoint, json=data)
    return response

  # ===== ORDER MANAGEMENT METHODS =====

  def place_order(
    self,
    exchange: str,
    trading_symbol: str,
    transaction_type: str,
    quantity: int,
    order_type: str = "MARKET",
    product: str = "CNC",
    price: float = 0,
    trigger_price: float = 0,
    disclosed_qty: int = 0,
    validity: str = "DAY",
    variety: str = "REGULAR",
    stoploss: float = 0,
    target: float = 0,
    segment: Optional[str] = None,
    exchange_token: Optional[int] = None,
    broker: str = "",
    strategy: Optional[Dict[str, str]] = None
  ) -> Dict[str, Any]:
    """
    Place a regular order.
    
    Args:
      exchange (str): Exchange code (e.g., "NSE", "BSE").
      trading_symbol (str): Symbol of the instrument.
      transaction_type (str): "BUY" or "SELL".
      quantity (int): Number of shares to trade.
      order_type (str, optional): Order type (e.g., "MARKET", "LIMIT"). Defaults to "MARKET".
      product (str, optional): Product code (e.g., "CNC" for delivery). Defaults to "CNC".
      price (float, optional): Price for limit orders. Defaults to 0.
      trigger_price (float, optional): Trigger price for stop orders. Defaults to 0.
      disclosed_qty (int, optional): Disclosed quantity. Defaults to 0.
      validity (str, optional): Order validity (e.g., "DAY", "IOC"). Defaults to "DAY".
      variety (str, optional): Order variety. Defaults to "REGULAR".
      stoploss (float, optional): Stop loss price. Defaults to 0.
      target (float, optional): Target price. Defaults to 0.
      segment (Optional[str], optional): Market segment. If None, determined from exchange.
      exchange_token (Optional[int], optional): Exchange token for the instrument.
      broker (str, optional): Broker code.
      strategy (Optional[Dict[str, str]], optional): Strategy information. If None, uses default.
        
    Returns:
      Dict[str, Any]: Order response containing orderId.
    """
    endpoint = "/orders"
    
    # Determine segment if not provided
    if not segment:
      segment = f"{exchange}CM"
    
    # Get strategy information
    strategy_info = self._get_strategy(strategy)
    
    data = {
      "exchange": exchange,
      "tradingSymbol": trading_symbol,
      "transactionType": transaction_type,
      "qty": quantity,
      "orderType": order_type,
      "product": product,
      "price": price,
      "triggerPrice": trigger_price,
      "disclosedQty": disclosed_qty,
      "validity": validity,
      "variety": variety,
      "stoploss": stoploss,
      "target": target,
      "segment": segment,
      "broker": broker,
      "strategy": strategy_info
    }
    
    # Add exchange token if provided
    if exchange_token:
      data["exchangeToken"] = exchange_token
        
    logger.debug("Placing order: %s", data)
    return self._make_request("POST", endpoint, json=data)
    
  def modify_order(
    self,
    order_id: str,
    **params
  ) -> Dict[str, Any]:
    """
    Modify an existing order.
    
    Args:
      order_id (str): Order ID to modify.
      **params: Parameters to update in the order.
        
    Returns:
      Dict[str, Any]: Order response containing orderId.
    """
    endpoint = f"/orders/{order_id}"
    
    logger.debug("Modifying order %s with params: %s", order_id, params)
    return self._make_request("PATCH", endpoint, json=params)
    
  def cancel_order(self, order_id: str) -> Dict[str, Any]:
    """
    Cancel an existing order.
    
    Args:
      order_id (str): Order ID to cancel.
        
    Returns:
      Dict[str, Any]: Response with the cancelled order ID.
    """
    endpoint = f"/orders/{order_id}"
    
    logger.debug("Cancelling order: %s", order_id)
    return self._make_request("DELETE", endpoint)
    
  def get_positions(self) -> List[Dict[str, Any]]:
    """
    Get current portfolio positions.
    
    Returns:
      List[Dict[str, Any]]: List of positions.
    """
    endpoint = "/portfolios/positions"
    
    logger.debug("Fetching positions")
    return self._make_request("GET", endpoint)
    
  def get_holdings(self, portfolios: Optional[str] = "default") -> List[Dict[str, Any]]:
    """
    Get current holdings.
    
    Args:
      portfolios (str, optional): Portfolio name. Defaults to "default".
        
    Returns:
      List[Dict[str, Any]]: List of holdings.
    """
    endpoint = "/portfolios/holdings"
    params = {"portfolios": portfolios}
    
    logger.debug("Fetching holdings for portfolio: %s", portfolios)
    return self._make_request("GET", endpoint, params=params)
    
  # ===== BASKET MANAGEMENT METHODS =====

  def create_basket(
    self,
    name: str,
    instruments: List[Dict[str, Any]],
    weightage_scheme: str = "equi_weighted",
    capital: Optional[Dict[str, float]] = None,
    instrument_types: Optional[List[str]] = None,
    trading_symbol: Optional[str] = None
  ) -> Dict[str, Any]:
    """
    Create a new basket.
    
    Args:
      name (str): Name of the basket.
      instruments (List[Dict[str, Any]]): List of instruments with weightage and shares.
      weightage_scheme (str, optional): Weightage scheme. Defaults to "equi_weighted".
      capital (Optional[Dict[str, float]], optional): Capital allocation. Defaults to {"minValue": 0, "actualValue": 0}.
      instrument_types (Optional[List[str]], optional): Types of instruments. Defaults to ["EQLC"].
        
    Returns:
      Dict[str, Any]: Basket information.
    """
    endpoint = "/baskets"
    
    # Set defaults
    if capital is None:
      capital = {"minValue": 0, "actualValue": 0}
        
    data = {
      "name": name,
      "weightageScheme": weightage_scheme,
      "instruments": instruments,
      "capital": capital,
      "instrumentTypes": instrument_types
    }
    
    logger.debug("Creating basket: %s", data)
    return self._make_request("POST", endpoint, json=data)
    
  def get_baskets(self) -> List[Dict[str, Any]]:
    """
    Get all baskets.
    
    Returns:
      List[Dict[str, Any]]: List of baskets.
    """
    endpoint = "/baskets"
    
    logger.debug("Fetching baskets")
    return self._make_request("GET", endpoint)
    
  def get_basket(self, basket_id: str) -> Dict[str, Any]:
    """
    Get a specific basket by ID.
    
    Args:
      basket_id (str): Basket ID.
        
    Returns:
      Dict[str, Any]: Basket information.
    """
    endpoint = f"/baskets/{basket_id}"
    
    logger.debug("Fetching basket: %s", basket_id)
    return self._make_request("GET", endpoint)
    
  def get_basket_instruments(self, basket_id: str) -> List[Dict[str, Any]]:
    """
    Get instruments in a basket.
    
    Args:
      basket_id (str): Basket ID.
        
    Returns:
      List[Dict[str, Any]]: List of instruments in the basket.
    """
    endpoint = f"/baskets/{basket_id}/instruments"
    
    logger.debug("Fetching instruments for basket: %s", basket_id)
    return self._make_request("GET", endpoint)
    
  def place_basket_order(
    self,
    trading_symbol: str,
    transaction_type: str,
    quantity: float,
    price: float = 0,
    order_type: str = "MARKET",
    product: str = "CNC",
    validity: str = "DAY",
    exchange_token: Optional[int] = None,
    trigger_price: float = 0,
    stoploss: float = 0,
    target: float = 0,
    broker: str = "wizzer",
    variety: str = "REGULAR",
    strategy: Optional[Dict[str, str]] = None,
    disclosed_qty: int = 0,
    sl_applied_level: Optional[str] = None
  ) -> Dict[str, Any]:
    """
    Place a basket order.
    
    Args:
      trading_symbol (str): Basket trading symbol (e.g., "/BASKET_NAME").
      transaction_type (str): "BUY" or "SELL".
      quantity (float): Quantity/units of the basket.
      price (float, optional): Price for limit orders. Defaults to 0.
      order_type (str, optional): Order type. Defaults to "MARKET".
      product (str, optional): Product code. Defaults to "CNC".
      validity (str, optional): Order validity. Defaults to "DAY".
      exchange_token (Optional[int], optional): Exchange token for the basket.
      trigger_price (float, optional): Trigger price. Defaults to 0.
      stoploss (float, optional): Stop loss price. Defaults to 0.
      target (float, optional): Target price. Defaults to 0.
      broker (str, optional): Broker code. Defaults to "wizzer".
      variety (str, optional): Order variety. Defaults to "REGULAR".
      strategy (Optional[Dict[str, str]], optional): Strategy information. If None, uses default.
      disclosed_qty (int, optional): Disclosed quantity. Defaults to 0.
      sl_applied_level (Optional[str], optional): Stop loss applied level (e.g., "basket").
        
    Returns:
      Dict[str, Any]: Order response containing orderId.
    """
    endpoint = "/orders/basket"
    
    # Get strategy information
    strategy_info = self._get_strategy(strategy)
    
    data = {
      "tradingSymbol": trading_symbol,
      "exchange": "WZR",
      "transactionType": transaction_type,
      "qty": quantity,
      "price": price,
      "orderType": order_type,
      "product": product,
      "validity": validity,
      "triggerPrice": trigger_price,
      "stoploss": stoploss,
      "target": target,
      "broker": broker,
      "variety": variety,
      "strategy": strategy_info,
      "segment": "WZREQ",
      "disclosedQty": disclosed_qty
    }
    
    # Add exchange token if provided
    if exchange_token:
      data["exchangeToken"] = exchange_token
        
    # Add stop loss level if provided
    if sl_applied_level:
      data["slAppliedLevel"] = sl_applied_level
        
    logger.debug("Placing basket order: %s", data)
    return self._make_request("POST", endpoint, json=data)
    
  def place_basket_exit_order(
    self,
    trading_symbol: str,
    exchange: str,
    transaction_type: str,
    quantity: float,
    exchange_token: int,
    **kwargs
  ) -> Dict[str, Any]:
    """
    Place a basket exit order.
    
    Args:
      trading_symbol (str): Basket trading symbol.
      exchange (str): Exchange code (usually "WZR" for baskets).
      transaction_type (str): "BUY" or "SELL" (usually "SELL" for exit).
      quantity (float): Quantity/units of the basket.
      exchange_token (int): Exchange token for the basket.
      **kwargs: Additional parameters for the order.
        
    Returns:
      Dict[str, Any]: Order response containing orderId.
    """
    endpoint = "/orders/basket/exit"
    
    # Build base data
    data = {
      "tradingSymbol": trading_symbol,
      "exchange": exchange,
      "transactionType": transaction_type,
      "qty": quantity,
      "exchangeToken": exchange_token,
      **kwargs
    }
    
    # Set strategy if not in kwargs
    if "strategy" not in kwargs:
      data["strategy"] = self._get_strategy(None)
        
    # Set defaults if not in kwargs
    defaults = {
      "orderType": "MARKET",
      "product": "CNC", 
      "validity": "DAY",
      "disclosedQty": 0,
      "price": 0,
      "variety": "REGULAR",
      "stoploss": 0,
      "broker": "wizzer",
      "triggerPrice": 0,
      "target": 0,
      "segment": "WZREQ"
    }
    
    for key, value in defaults.items():
      if key not in data:
        data[key] = value
    
    logger.debug("Placing basket exit order: %s", data)
    return self._make_request("POST", endpoint, json=data)
    
  def modify_basket_order(
    self,
    order_id: str,
    **params
  ) -> Dict[str, Any]:
    """
    Modify an existing basket order.
    
    Args:
      order_id (str): Order ID to modify.
      **params: Parameters to update in the order.
        
    Returns:
      Dict[str, Any]: Order response containing orderId.
    """
    endpoint = f"/orders/basket/{order_id}"
    
    logger.debug("Modifying basket order %s with params: %s", order_id, params)
    return self._make_request("PATCH", endpoint, json=params)
    
  def rebalance_basket(
    self,
    trading_symbol: str,
    instruments: List[str]
  ) -> Dict[str, Any]:
    """
    Rebalance a basket with new instruments.
    
    Args:
      trading_symbol (str): Basket trading symbol.
      instruments (List[str]): List of instrument identifiers for the new basket composition.
        
    Returns:
      Dict[str, Any]: Rebalance response.
    """
    endpoint = "/baskets/rebalance"
    
    data = {
      "tradingSymbol": trading_symbol,
      "instruments": instruments
    }
    
    logger.debug("Rebalancing basket %s with instruments: %s", trading_symbol, instruments)
    return self._make_request("POST", endpoint, json=data)

  def _make_request(
    self, 
    method: str, 
    endpoint: str, 
    params: Optional[Dict[str, str]] = None, 
    json: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None
  ) -> Any:
    """
    Make an HTTP request to the API.

    Args:
      method (str): HTTP method (GET, POST, etc.)
      endpoint (str): API endpoint path.
      params (Optional[Dict[str, str]]): Query parameters for GET requests.
      json (Optional[Dict[str, Any]]): JSON payload for POST requests.
      headers (Optional[Dict[str, str]]): Custom headers to override the defaults.

    Returns:
      Any: Parsed JSON response.

    Raises:
      requests.RequestException: If the request fails.
    """
    url = f"{self.base_url}{endpoint}"
    request_headers = headers if headers else self.headers
    
    try:
      logger.debug("%s request to %s", method, url)
      response = requests.request(
        method=method,
        url=url,
        headers=request_headers,
        params=params,
        json=json
      )
      response.raise_for_status()
      return response.json()
    except requests.RequestException as e:
      logger.error("API request failed: %s", e, exc_info=True)
      if hasattr(e.response, 'text'):
        logger.error("Response content: %s", e.response.text)
      raise