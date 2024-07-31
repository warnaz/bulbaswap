import os
import json
from dotenv import load_dotenv


load_dotenv()
KEY = os.environ.get("KEY")


def get_abi(file_name):
    with open(f'{file_name}') as file:
        abi = json.load(file)
    return abi


QUOTER_V3_ADDRESS = "0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6" # Uniswap Quoter V3
QUOTER_V2_ADDRESS = "0x61fFE014bA17989E743c5F6cB21bF9697530B21e" # Uniswap Quoter V2

ROUTER_V3_ADDRESS = "0xE592427A0AEce92De3Edee1F18E0157C05861564" # Uniswap Router V3
ROUTER_V2_ADDRESS = "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45" # Uniswap Router V2

BULBASWAP_ROUTER_V3 = '0x07968156ADF895922406523887E5C157623c38Db' # Bulbaswap Router V3

ERC1967_ADDRESS = '0x9f6E8e1C33FC2AA6ff29B747922E3f8e32911B9D' # Bulbaswap ERC1967Proxy

QUOTER_V3_ABI = get_abi("abis/quoter_v1.json")
QUOTER_V2_ABI = get_abi("abis/quoter_v2.json")

ROUTER_V3_ABI = get_abi("abis/router_v1.json")
ROUTER_V2_ABI = get_abi("abis/router_v2.json")

ERC_PROXY_ABI = get_abi("abis/erc_proxy_abi.json")
BASE_ABI = get_abi("abis/base_abi.json")

GAS_MULTIPLIER = 1.5


TOKENS_PER_CHAIN = {
    "Morph": {
        'ETH'               : '0x0000000000000000000000000000000000000000',
        'WETH'              : '0x5300000000000000000000000000000000000011',
        'USDT'              : '0x9e12ad42c4e4d2acfbade01a96446e48e6764b98',
    },
    'Ethereum': {
        'ETH'               : '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
        'WETH'              : '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
        'USDC'              : '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
        'USDT'              : '0xdAC17F958D2ee523a2206206994597C13D831ec7',
    }
}

ERC20_ABI = [{'inputs': [{'internalType': 'string', 'name': '_name', 'type': 'string'}, {'internalType': 'string', 'name': '_symbol', 'type': 'string'}, {'internalType': 'uint256', 'name': '_initialSupply', 'type': 'uint256'}], 'stateMutability': 'nonpayable', 'type': 'constructor'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'owner', 'type': 'address'}, {'indexed': True, 'internalType': 'address', 'name': 'spender', 'type': 'address'}, {'indexed': False, 'internalType': 'uint256', 'name': 'value', 'type': 'uint256'}], 'name': 'Approval', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'from', 'type': 'address'}, {'indexed': True, 'internalType': 'address', 'name': 'to', 'type': 'address'}, {'indexed': False, 'internalType': 'uint256', 'name': 'value', 'type': 'uint256'}], 'name': 'Transfer', 'type': 'event'}, {'inputs': [{'internalType': 'address', 'name': 'owner', 'type': 'address'}, {'internalType': 'address', 'name': 'spender', 'type': 'address'}], 'name': 'allowance', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'spender', 'type': 'address'}, {'internalType': 'uint256', 'name': 'amount', 'type': 'uint256'}], 'name': 'approve', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'account', 'type': 'address'}], 'name': 'balanceOf', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'decimals', 'outputs': [{'internalType': 'uint8', 'name': '', 'type': 'uint8'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'spender', 'type': 'address'}, {'internalType': 'uint256', 'name': 'subtractedValue', 'type': 'uint256'}], 'name': 'decreaseAllowance', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'spender', 'type': 'address'}, {'internalType': 'uint256', 'name': 'addedValue', 'type': 'uint256'}], 'name': 'increaseAllowance', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'name', 'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'uint8', 'name': 'decimals_', 'type': 'uint8'}], 'name': 'setupDecimals', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'symbol', 'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'totalSupply', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'recipient', 'type': 'address'}, {'internalType': 'uint256', 'name': 'amount', 'type': 'uint256'}], 'name': 'transfer', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'sender', 'type': 'address'}, {'internalType': 'address', 'name': 'recipient', 'type': 'address'}, {'internalType': 'uint256', 'name': 'amount', 'type': 'uint256'}], 'name': 'transferFrom', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'nonpayable', 'type': 'function'}]

