NETWORKS = {
    "MORPH": {
        'rpc': [
            'https://rpc-quicknode-holesky.morphl2.io',
            # 'https://rpc-holesky.morphl2.io'
        ],
        'chain_id': 2810,
        'eip1559_support': True,
        'token': 'ETH',
        'explorer': 'https://explorer-holesky.morphl2.io/',
    },

    "MAINNET": {
        "chain_id": 1,
        "token": "ETH",
        "explorer": "https://etherscan.io/",
        "rpc": [
                'https://rpc.ankr.com/eth',
                'https://ethereum.publicnode.com',
                'https://rpc.flashbots.net',
                'https://1rpc.io/eth',
                'https://eth.drpc.org'
            ]
    },

    "POLYGON": {
        "chain_id": 137,
        'token': 'MATIC',
        "explorer": 'https://polygonscan.com/',
        "rpc": ['https://polygon-rpc.com',],
    },

    "ARBITRUM": {
        "chain_id": 42161,
        "token": 'ETH',
        "explorer": 'https://arbiscan.io/',
        'rpc': ['https://rpc.ankr.com/arbitrum/',],
    },

    "LINEA": {
        'chain_id': 59144,
        'token': 'ETH',
        'explorer': 'https://lineascan.build/',
        "rpc": [
            'https://linea.drpc.org',
            'https://1rpc.io/linea',
            'https://rpc.linea.build'
        ],
    },

    "GOERLI": {
        'chain_id': 5,
        'token': 'ETH',
        'explorer': 'https://goerli.etherscan.io/',
        'rpc': [
            'https://endpoints.omniatech.io/v1/eth/goerli/public',
            'https://rpc.ankr.com/eth_goerli',
            'https://eth-goerli.public.blastapi.io',
            'https://goerli.blockpi.network/v1/rpc/public'
        ],
    },

    'AVALANCHE': {
        'chain_id': 43114,
        'token': 'AVAX',
        'explorer': 'https://snowtrace.io/',
        'rpc': [
            'https://avalanche.drpc.org'
        ],
    },

    "SEPOLIA": {
        "chain_id": 11155111,
        'token': 'ETH',
        'explorer': 'https://sepolia.etherscan.io/',
        'rpc': [
            "https://endpoints.omniatech.io/v1/eth/sepolia/public",
        ],
    }
}
