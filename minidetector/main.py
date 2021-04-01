import threading
import logging

from scapy.sendrecv import sniff

from lib.ascii_banner import print_ascii_banner
from lib.database import db_init
from argparser import argparse_init
from minidetector.packet_processor import on_packet, process_data


def main() -> None:
    print_ascii_banner("MiniDetector")
    db_init(argparse_init().clean)

    logging.debug('Starting sniffing thread')
    sniffing_thread = threading.Thread(target=lambda: sniff(prn=on_packet), daemon=True)
    sniffing_thread.start()
    logging.debug('Starting to process packets')
    process_data()


if __name__ == '__main__':
    main()
