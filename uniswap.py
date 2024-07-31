import time
from loguru import logger
from web3 import Web3
from dex import DEX
from utils.config import (
    TOKENS_PER_CHAIN,
    QUOTER_V2_ABI, QUOTER_V2_ADDRESS,
    ROUTER_V3_ABI, ROUTER_V2_ADDRESS,
    BULBASWAP_ROUTER_V3, ERC1967_ADDRESS
)


class Uniswap(DEX):
    '''Класс для работы с Uniswap V3'''
    def __init__(
            self, 
            private_key: str,
            chain: str,
            amount: int | float,
            token_from: str,
            token_to: str
    ) -> None:
        super().__init__(network=chain, private_key=private_key)

        self.amount = amount
        self.token_from, self.token_to = token_from, token_to

        self._router_address = ROUTER_V2_ADDRESS
        self._quoter_address = QUOTER_V2_ADDRESS

        self.quoter = self.get_contract(self._quoter_address, QUOTER_V2_ABI)
        self.router = self.get_contract(self._router_address, ROUTER_V3_ABI)

    async def get_min_amount_out(self, path: bytes, amount_in_wei: int):
        SLIPPAGE = 1.5

        min_amount_out, _, _, _ = await self.quoter.functions.quoteExactInput(
            path,
            amount_in_wei
        ).call()

        return int(min_amount_out - (min_amount_out / 100 * SLIPPAGE))

    async def swap_exactInput(self):
        logger.success(f"Gas price: {await self.w3.eth.gas_price}")
        from_token_name, to_token_name, amount = self.token_from, self.token_to, self.amount

        from_token_address = TOKENS_PER_CHAIN[self.network.title()][from_token_name]
        to_token_address = TOKENS_PER_CHAIN[self.network.title()][to_token_name]

        balance = await self.get_balance(from_token_address)
        logger.success(f"Balance: {balance}")

        # decimal_token_from = await self.get_decimal(from_token_address)
        # decimal_token_to = await self.get_decimal(to_token_address)

        decimal_token_from = 18
        decimal_token_to = 18

        if self.token_from == "WETH":
            amount_in_wei = self.w3.to_wei(amount, 'ether')
        else:
            amount_in_wei = int(self.amount * 10 ** decimal_token_from)

        logger.info(f'Swap on Uniswap: {amount_in_wei} decimal: {decimal_token_from} wei in {from_token_name} -> {to_token_name}')

        path = self.get_path(from_token_address, to_token_address, from_token_name, to_token_name)

        # TODO сравнить, насколько min_amount_out отличается от self.price
        # min_amount_out = await self.get_min_amount_out(path, amount_in_wei)
        min_amount_out = self.amount * 10 ** decimal_token_to
        logger.info(f"We will receive of {to_token_name}: {min_amount_out / 10 ** decimal_token_to}")

        if from_token_name != self.token:
            await self.check_for_approved(
                from_token_address, self._router_address, amount_in_wei
            )

        logger.critical("Make a SWAP")
        tx_data = self.router.encodeABI(
            fn_name='exactInput',
            args=[(
                path,
                self.address if to_token_name != self.token else '0x0000000000000000000000000000000000000002',
                amount_in_wei,
                min_amount_out
            )]
        )

        full_data = [tx_data]

        if from_token_name == self.token or to_token_name == self.token:
            tx_additional_data = self.router.encodeABI(
                fn_name='unwrapWETH9' if from_token_name != self.token else 'refundETH',
                args=[
                    min_amount_out,
                    self.address
                ] if from_token_name != self.token else None
            )
            full_data.append(tx_additional_data)

        tx_params = await self.prepare_transaction(
            value=amount_in_wei if from_token_name == self.token else 0
        )

        transaction = await self.router.functions.multicall(
            full_data
        ).build_transaction(tx_params)

        return await self.send_transaction(transaction)

    async def swap_exactInputSingle(self, token_in: str, token_out: str, qty: float):
        balance = await self.get_balance(token_in)
        amount = int(qty*10**18)
        logger.info(f"Amount: {amount}")
        logger.info(f"Balance: {balance}")

        if token_in != self.token:
            await self.check_for_approved(
                token_in, self._router_address, amount
            )
        
        logger.critical("MAKE A SWAP")

        function = self.router.functions.exactInputSingle({
            "tokenIn": Web3.to_checksum_address(token_in),
            "tokenOut": Web3.to_checksum_address(token_out),
            "fee": 3000,
            "recipient": self.w3.to_checksum_address(self.address),
            "deadline": int(time.time()) + 10 * 60,
            "amountIn": amount,
            "amountOutMinimum": 0,
            "sqrtPriceLimitX96": 0,            
        })

        # last_block = await self.get_last_block()
        # logger.info(last_block)
        # base_fee = last_block.get('baseFeePerGas')
        # logger.success(base_fee)

        tx_params = { 
            "from": self.w3.to_checksum_address(self.address),
            "value": 0,
            "nonce": await self.w3.eth.get_transaction_count(self.address),
            "gasPrice": await self.w3.eth.gas_price,
            "gas": 100_000,
            "chainId": self.chain_id,
        }

        estimate_gas = await self.w3.eth.estimate_gas(tx_params)
        logger.info(f"estimate_gas: {estimate_gas}")
        # tx_params["gasPrice"] = int(estimate_gas * 1.3)

        transaction = await function.build_transaction(tx_params)

        # transaction['gas'] = 1000_000

        logger.info("Sign transaction")
        sign_tr = self.w3.eth.account.sign_transaction(transaction, self.private_key)

        logger.info("Send transaction")
        sent_tr = await self.w3.eth.send_raw_transaction(sign_tr.rawTransaction)

        logger.info("Wait for transaction receipt")
        trans = await self.w3.eth.wait_for_transaction_receipt(sent_tr)
        logger.info(f"Transaction hash: {trans}")

        return trans

