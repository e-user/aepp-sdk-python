from aeternity import EpochClient
from aeternity.aevm import pretty_bytecode


class ContractError(Exception):
    pass


class Contract:
    EVM = 'evm'
    RING = 'ring'

    def __init__(self, code, abi, client=None):
        if client is None:
            client = EpochClient()
        self.client = client
        self.code = code
        self.abi = abi

    def compile(self, options=''):
        """Compile a ring contract from source and return byte code"""
        data = self.client.local_http_post(
            'contract/compile',
            json={'code': self.code, 'options': options}
        )
        error = data.get('reason')
        if error:
            raise ContractError(error)
        return data['bytecode']

    def get_pretty_bytecode(self, options=''):
        bytecode = self.compile(options=options)
        return pretty_bytecode(bytecode)

    def call(self, function, arg):
        '''"Call a ring function with a given name and argument in the given
        bytecode off chain.'''

        compiled_code = self.compile()

        # see: /epoch/lib/aehttp-0.1.0/src/aehttp_dispatch_ext.erl
        data = self.client.local_http_post(
            'contract/call',
            json={
                # TODO: this looks the same as the encode-calldata call from the
                # TODO: outside, but actually *requires* compiled code as hex
                # TODO: string as argument
                'code': compiled_code,
                'function': function,
                'arg': arg,
                'abi': self.abi,
            }
        )
        # TODO: this just returns a 500 when we are out of gas. It would be nice to get something back
        error = data.get('reason')
        if error:
            raise ContractError(error)
        return data

    def encode_calldata(self, function, arg):
        data = self.client.local_http_post(
            'contract/encode-calldata',
            json={
                'abi': 'evm',
                'code': self.code,
                'function': function,
                'arg': arg,
            }
        )
        error = data.get('reason')
        if error:
            raise ContractError(error)
        return data['calldata']

