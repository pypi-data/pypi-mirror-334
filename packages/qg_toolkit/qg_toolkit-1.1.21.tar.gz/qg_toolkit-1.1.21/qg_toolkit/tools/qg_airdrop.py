import random
from threading import Lock

from web3 import Web3
from qg_toolkit.tools.qg_log import logger
from qg_toolkit.tools.qg_eth import QGEth


class QGAirdropManager(QGEth):
    _lock = Lock()

    def __init__(self, index, sender_addr, private_key, mnemonic, chain, per_amount, remaining_amount,
                 check_receiver, min_balance, all_recipients):
        super().__init__(index=index, address=sender_addr, private_key=private_key, mnemonic=mnemonic)
        self.chain = chain
        self.per_amount = per_amount
        self.remaining_amount = remaining_amount
        self.check_receiver = check_receiver
        self.min_balance = min_balance
        self.all_recipients = all_recipients
        self.selected_recipients = []
        self.init_chains(chain)
        self._init_web3()
        self._allocate_recipients()

    @property
    def contract_addresses(self):
        return {
            "polygon": ["0xDCB4a16EB4F5F8214962357c96584F6955B9b525"],
            "opbnb": ["0x501Ab65Ec2E89aB6e9CBfE6eE3AED423995b1aef"],
            "goerli": ["0x9680D1e126bBeF521F97b6FFB2fe39Da5c88C290"],
            "sepolia": ["0xEf50B70800f0D5D89b7a0056A0746845C2Dbe7b7"],
            "linea": ["0x2Ce164CbdBFb8fA0BEbf1f2dCD2F364481Fa86d3"],
            "mantle": ["0x601074C151C229d04D339F807817e8cB87E6CF1e"],
            "berachain": ["0xaB06c32FCE992B423F17e57BCC78C1cA80dd7AaA"],
            "berachain2": ["0x2a61D1A184Bb3914A440468856c4085E416d3A19"],
            "blast": ["0x8B4a4AA2fD4bB59eBBEB987D229A3eb01f987E7b"],
            "zeta": ["0xBc4A4b3846C3F2F8085689F0A4A09D76627b6c2E"],
            "holesky": [
                "0x42d5f4D80dC931644627127385F51F07eb8a485D", "0x88B0D9b5046021313f96d4d83feF78b65bF92Ac9",
                "0x0760EB9694606121A8cfF688C4F70F92a0BA003c", "0xd6e6414e7a41816f212A308Ed1252CD473484596",
                "0xcF8DdFBC496Ca726f9bB3489f1Fcc992E137471f", "0x9324Ca1DBbE42E5176F33eAbe53a38599bA15a6B"
            ],
            "xter": ["0x7347Ae5a53F7b80A7eF6654E3b8eA0c0E396a4D3"],
            "bsc": ["0x8193f859bad92c89a3a8c89d3a96c4582a829f90"],
            "hemi": ["0x8B4a4AA2fD4bB59eBBEB987D229A3eb01f987E7b"],
            "base": ["0x3A9168c183Fc5522C85003974a131Dc67f6BA267"]
        }

    def _init_web3(self):
        self.w3 = getattr(self, f"{self.chain}_w3", None)
        self.balance = getattr(self, f"{self.chain}_balance", None)

    def _allocate_recipients(self):
        available_count = int((float(self.balance) - self.remaining_amount) / float(self.per_amount))
        if available_count < 0:
            available_count = 0

        with self._lock:
            if self.check_receiver:
                for recipient in self.all_recipients[:]:
                    if self.get_balance_from_web3(self.w3, recipient) < self.min_balance:
                        self.selected_recipients.append(recipient)
                        self.all_recipients.remove(recipient)
                    if len(self.selected_recipients) >= available_count:
                        break
            else:
                self.selected_recipients = self.all_recipients[:available_count]
                self.all_recipients = self.all_recipients[available_count:]

        logger.info(f'{self.address} 分配账号数量{len(self.selected_recipients)}:{self.selected_recipients}')

    def _generate_tx_data(self, method_id):
        if not self.selected_recipients:
            return None, None
        hex_amount = hex(Web3.to_wei(self.per_amount, "ether"))[2:].rjust(64, '0')
        recipient_count = len(self.selected_recipients)
        count_hex = hex(recipient_count)[2:].rjust(64, '0')
        param_index = 32 * (3 + recipient_count)
        param_index_hex = hex(param_index)[2:].rjust(64, '0')
        all_amounts = "".join([hex_amount] * recipient_count)
        all_addresses = "".join([addr[2:].rjust(64, '0') for addr in self.selected_recipients])
        total_amount = str(round(float(self.per_amount) * recipient_count, 5))

        tx_data = f"0x{method_id}" \
                  f"0000000000000000000000000000000000000000000000000000000000000040" \
                  f"{param_index_hex}" \
                  f"{count_hex}" \
                  f"{all_addresses}" \
                  f"{count_hex}" \
                  f"{all_amounts}"
        return tx_data, total_amount

    def _send_batch_tx(self, method_id, action_name):
        logger.info(f'【{self.address}】【{self.index}】接收地址数量：{len(self.selected_recipients)}')
        if not self.selected_recipients:
            return
        contract_addr = random.choice(self.contract_addresses.get(self.chain))
        if not contract_addr:
            return
        tx_data, total_amount = self._generate_tx_data(method_id)
        if not tx_data:
            return
        logger.info(f'【{self.address}】【{self.index}】批量空投-input_data：{tx_data}')
        self.sent_tx_with_assembled_by_type0(self.w3, contract_addr, total_amount, tx_data, action_name)

    def send_batch_by_lian(self):
        self._send_batch_tx("566316eb", "batch_send_eth_by_lian")

    def send_batch_by_chain(self):
        self._send_batch_tx("67243482", "batch_send_eth_by_chain")


# def qg_task(index, address, private_key, mnemonic):
#     # chain = "bsc"
#     # chain = "sepolia"
#     # chain = "hemi"
#     chain = "base"
#     per_amount = round(random.uniform(0.001, 0.00101), 5)
#     # 给自己留下金额
#     remaining_amount = 0.01
#     # 是否检查小号余额
#     check_receiver = True
#     # 检查小号余额是否大于0.001
#     min_balance = 0.001
#     airdrop = QGAirdropManager(index, address, private_key, mnemonic, chain, per_amount, remaining_amount,
#                                check_receiver, min_balance, all_recipients)
#     airdrop.send_batch_by_lian()

