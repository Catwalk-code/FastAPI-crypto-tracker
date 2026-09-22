import httpx
import asyncio

client = httpx.AsyncClient()

binance_semaphore = asyncio.Semaphore(5)

async def get_current_price(coin:str) -> float |  None:
    """Getting current price of coin using Binance API"""
    
    #Binance use symols like BTCUSDT, ETHUSDT
    symbol = f"{coin}USDT"
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"

    '''I found that creating a user using a fuction is a bad idea, the app 
    will work faster in case if user is created in the start of server. 
    This should be rewrite using lifespan'''
    async with binance_semaphore:
        try:
            response = await asyncio.wait_for(
                client.get(url),
                timeout=3.0
            )

            if response.status_code != 200:
                return None

            return float(response.json()["price"])
        except (asyncio.TimeoutError, httpx.RequestEror):
            return None