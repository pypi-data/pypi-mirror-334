import argparse
import logging
from typing import Any

from ul_py_tool.commands.cmd import Cmd

from ul_db_utils.utils.waiting_for_mongo import waiting_for_mongo
from ul_db_utils.utils.waiting_for_postgres import waiting_for_postgres

logger = logging.getLogger(__name__)


class CmdWaiting(Cmd):
    uri: str
    max_times: int
    delay: int
    mongo_connect: bool

    @staticmethod
    def add_parser_args(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--db-uri', dest='uri', type=str, required=True)
        parser.add_argument('--retry-times', dest='max_times', type=int, default=100, required=False)
        parser.add_argument('--retry-delay-sec', dest='delay', type=int, default=1, required=False)
        parser.add_argument('--mongo-connect', dest='mongo_connect', type=bool, default=False, required=False)

    def run(self, *args: Any, **kwargs: Any) -> None:
        if self.mongo_connect:
            if not waiting_for_mongo(self.uri, retry_max_count=self.max_times, retry_delay_s=float(self.delay)):
                exit(2)
        else:
            if not waiting_for_postgres(self.uri, retry_max_count=self.max_times, retry_delay_s=float(self.delay)):
                exit(2)
        exit(0)
