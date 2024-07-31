import asyncio
from uniswap import Uniswap
from utils.config import TOKENS_PER_CHAIN, KEY
from utils.networks import NETWORKS


if __name__ == "__main__":
    data = {
        "private_key": KEY,
        "chain": "Morph",
        "price": 3200,
        "amount": 0.01
    }
    token_from, token_to = "WETH", "USDT"
    private_key, chain, price, amount = data.values()
    morph_rpc = NETWORKS["MORPH"]["rpc"][0]

    from_token_address = TOKENS_PER_CHAIN['Morph'][token_from]
    to_token_address = TOKENS_PER_CHAIN['Morph'][token_to]

    uni = Uniswap(private_key, chain, amount, token_from, token_to)
    asyncio.run(uni.swap_exactInputSingle(from_token_address, to_token_address, amount))
