import asyncio
import random
from asyncio import sleep
from eth_typing import HexStr
from hexbytes import HexBytes
from loguru import logger
from web3 import AsyncHTTPProvider, AsyncWeb3
from web3.exceptions import TransactionNotFound, TimeExhausted
from web3.middleware import geth_poa

from utils.config import ERC20_ABI, GAS_MULTIPLIER, TOKENS_PER_CHAIN
from utils.networks import NETWORKS


class DEX:
    '''Главный класс дексов'''
    def __init__(self, network: str, private_key: str, proxy: None | str = None) -> None:
        self.network = network

        self.chain_id = NETWORKS[network.upper()]["chain_id"]
        self.explorer = NETWORKS[network.upper()]["explorer"]
        self.token = NETWORKS[network.upper()]["token"]
        self.rpc = random.choice(NETWORKS[network.upper()]["rpc"])

        self.request_kwargs = {"proxy": f"http://{proxy}"} if proxy else {}
        self.w3 = AsyncWeb3(AsyncHTTPProvider(self.rpc, request_kwargs=self.request_kwargs))

        self.private_key = private_key
        self.address = AsyncWeb3.to_checksum_address(self.w3.eth.account.from_key(private_key).address)

    @staticmethod
    def get_path(from_token_address: str, to_token_address: str, *args):
        from_token_bytes = HexBytes(from_token_address).rjust(20, b'\0')
        to_token_bytes = HexBytes(to_token_address).rjust(20, b'\0')
        fee_bytes = (500).to_bytes(3, 'big')

        return from_token_bytes + fee_bytes + to_token_bytes

    def _get_path(self, from_token_address: str, to_token_address: str, from_token_name: str, to_token_name: str):

        pool_fee_info = {
            'Base': {
                "USDC.e/ETH": 500,
                "ETH/USDC.e": 500,
            },
            'Polygon':{
                'USDT/MATIC': 500,
                'MATIC/USDT': 500,
                'USDC.e/MATIC': 500,
                'MATIC/USDC.e': 500,
                'USDC/MATIC': 500,
                'MATIC/USDC': 500,
                'MATIC/WETH': 500,
                'WETH/MATIC': 500,
                'WETH/USDT': 500,
            }
        }[self.network.title()]

        if 'USDT' not in [from_token_name, to_token_name] or self.network.title() == 'Polygon':
            from_token_bytes = HexBytes(from_token_address).rjust(20, b'\0')
            to_token_bytes = HexBytes(to_token_address).rjust(20, b'\0')
            fee_bytes = (500).to_bytes(3, 'big')
            return from_token_bytes + fee_bytes + to_token_bytes
        else:
            from_token_bytes = HexBytes(from_token_address).rjust(20, b'\0')
            index_1 = f'{from_token_name}/USDC'
            fee_bytes_1 = pool_fee_info[index_1].to_bytes(3, 'big')
            middle_token_bytes = HexBytes(TOKENS_PER_CHAIN[self.network]['USDC']).rjust(20, b'\0')
            index_2 = f'USDC/{to_token_name}'
            fee_bytes_2 = pool_fee_info[index_2].to_bytes(3, 'big')
            to_token_bytes = HexBytes(to_token_address).rjust(20, b'\0')
            return from_token_bytes + fee_bytes_1 + middle_token_bytes + fee_bytes_2 + to_token_bytes

    @staticmethod
    def get_normalize_error(error: Exception) -> Exception | str:
        try:
            if isinstance(error.args[0], dict):
                error = error.args[0].get('message', error)
            return error
        except:
            return error

    def get_contract(self, contract_address: str, abi: dict = ERC20_ABI):
        return self.w3.eth.contract(
            address=AsyncWeb3.to_checksum_address(contract_address),
            abi=abi
        )

    async def get_decimal(self, token_address: str):
        contract_address = self.get_contract(contract_address=token_address)

        return await contract_address.functions.decimals().call()
    
    async def get_last_block(self) -> dict:
            self.w3.middleware_onion.inject(geth_poa.async_geth_poa_middleware, layer=0)
            last_block = await self.w3.eth.get_block('latest')
            self.w3.middleware_onion.remove(geth_poa.async_geth_poa_middleware)
            return last_block
    
    async def prepare_transaction(self, value: int = 0) -> dict:
        try:
            tx_params = {
                'chainId': self.chain_id,
                'from': self.w3.to_checksum_address(self.address),
                'nonce': await self.w3.eth.get_transaction_count(self.address),
                'value': value,
                'gasPrice': await self.w3.eth.gas_price
            }

            logger.info(f"Transaction: {tx_params}")
            return tx_params

        except Exception as error:
            raise error

    async def get_allowance(self, token_address: str, spender_address: str) -> int:
        contract = self.get_contract(token_address)

        return await contract.functions.allowance(
            self.address,
            spender_address
        ).call()
    
    async def get_balance(self, token_address: str) -> int:
        contract = self.get_contract(token_address)

        return await contract.functions.balanceOf(self.address).call()

    async def check_for_approved(self, token_address: str, spender_address: str, amount_in_wei: int) -> bool:
        try:
            contract = self.get_contract(token_address)

            balance_in_wei = await contract.functions.balanceOf(self.address).call()
            symbol = await contract.functions.symbol().call()

            logger.info(f'Check for approval {self.address}')

            if balance_in_wei <= 0:
                logger.info(f'Zero {symbol} balance: {self.address}')
                raise Exception(f'Zero {symbol} balance')

            approved_amount_in_wei = await self.get_allowance(
                token_address=token_address,
                spender_address=spender_address
            )
            logger.success(f"Allowance {approved_amount_in_wei}")

            if amount_in_wei <= approved_amount_in_wei:
                logger.info(f'Already approved: {self.address}')
                return False

            logger.warning("Make approve")
            result = await self.make_approve(token_address, spender_address, amount_in_wei)

            await sleep(random.randint(5, 9))
            return False
        except Exception as error:
            raise Exception(error)

    async def make_approve(self, token_address: str, spender_address: str, amount_in_wei: int) -> bool:
        transaction = await self.get_contract(token_address).functions.approve(
            spender_address,
            amount=amount_in_wei
        ).build_transaction(await self.prepare_transaction())

        return await self.send_transaction(transaction)

    async def send_transaction(
            self, transaction, need_hash: bool = False, poll_latency: int = 10,
            timeout: int = 360
    ) -> bool | HexStr:
        try:
            transaction['gas'] = int((await self.w3.eth.estimate_gas(transaction)) * GAS_MULTIPLIER)
        except Exception as error:
            raise Exception(f'{self.get_normalize_error(error)}')

        try:
            singed_tx = self.w3.eth.account.sign_transaction(transaction, self.private_key)
            logger.info("Signed transaction")
            tx_hash = self.w3.to_hex(await self.w3.eth.send_raw_transaction(singed_tx.rawTransaction))
        except Exception as error:
            if self.get_normalize_error(error) == 'already known':
                logger.warning(f'RPC got error, but tx was send. User: {self.address}')
                return True
            else:
                raise Exception(f'{self.get_normalize_error(error)}')

        total_time = 0
        timeout = timeout if self.network != 'POLYGON' else 1200

        while True:
            try:
                logger.info("Get transaction receipt")
                receipts = await self.w3.eth.get_transaction_receipt(tx_hash)
                status = receipts.get("status")
                if status == 1:
                    message = f'Transaction was successful: {self.explorer}tx/{tx_hash}'
                    logger.success(f"User: {self.address}. {message}")

                    return tx_hash
                elif status is None:
                    logger.warning(f'User: {self.address}. Transaction is still pending: {self.explorer}tx/{tx_hash}')
                    await asyncio.sleep(poll_latency)
                else:
                    logger.error(f'User: {self.address}. Transaction failed: {self.explorer}tx/{tx_hash}')
                    return False
            except TransactionNotFound:
                if total_time > timeout:
                    raise TimeExhausted(
                        f"Transaction is not in the chain after {timeout} seconds. User: {self.address}")
                total_time += poll_latency
                await asyncio.sleep(poll_latency)

            except Exception as error:
                logger.warning(f'RPC got autims response. Error: {error}. User: {self.address}')
                total_time += poll_latency
                await asyncio.sleep(poll_latency)
