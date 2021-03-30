#! /usr/bin/env python3
import argparse
import threading
import logging
import typing

from scapy.sendrecv import sniff
from scapy.layers.inet import IP
from scapy.layers.l2 import Ether
from scapy.packet import Packet
from typing import Set

from .database import create_tables, Entity, create_session, drop_tables, load_db_entries
from queue import Queue

packet_queue: Queue = Queue()


def on_packet(p: Packet) -> None:
    if Ether not in p or IP not in p:
        return
    packet_queue.put(p)


def process_data() -> None:
    ip_mac_set: typing.Set[typing.Tuple[str, str]] = load_db_entries()

    packet_count = 0
    session = create_session()  # Creates a new DB session
    while packet := packet_queue.get():
        packet_count += 1
        if packet_count % 100 == 0 and (qs := packet_queue.qsize() or 0) != 0:
            logging.info(f'Queue size: {qs}')
        mac = packet[Ether].src
        ip = packet[IP].src

        if (pair := (ip, mac)) not in ip_mac_set:
            ip_mac_set.add(pair)

            entity = Entity(mac=mac, ip=ip)
            session.add(entity)
            session.commit()

            logging.info(f'Added entity {entity}')
    session.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description='minidetector is an example tool '
                    'for detecting network identities and inserting them into a PostgreSQL database')
    parser.add_argument("--clean", const=True, default=False, nargs='?', help="prune the existing data before starting")
    parser.add_argument("--debug", const=True, default=False, nargs='?', help="enable debug logging")
    args = parser.parse_args()
    logging.root.setLevel(logging.DEBUG if args.debug else logging.INFO)
    if args.clean:
        logging.debug('Dropping all tables')
        drop_tables()
    logging.debug('Creating all tables')
    create_tables()
    logging.debug('Starting sniffing thread')
    sniffing_thread = threading.Thread(target=lambda: sniff(prn=on_packet), daemon=True)
    sniffing_thread.start()
    logging.debug('Starting to process packets')
    process_data()


if __name__ == '__main__':
    main()
