#! /usr/bin/env python3
import threading
import logging
import typing
import datetime
from queue import Queue

from scapy.sendrecv import sniff
from scapy.layers.inet import IP
from scapy.layers.l2 import Ether
from scapy.packet import Packet

from lib.ascii_banner import print_ascii_banner
from lib.database import create_session, load_db_entries, Session, db_init
from lib.Entity import Entity
from argparser import argparse_init

packet_queue: Queue = Queue()


def on_packet(p: Packet) -> None:
    """
    Checks whether a packet `p` is valid, if so, insert into `packet_queue`
    :param p: Packet
    :return: None
    """
    if Ether not in p or IP not in p:
        return
    packet_queue.put(p)


def process_data() -> None:
    """
    Iterates over a list of packets and inserts them into the DB
    :return: None
    """
    packet_count = 0
    session: typing.Optional[Session] = None
    try:
        session = create_session()  # Creates a new DB session

    except BaseException as e:
        logging.critical(e)
        exit(1)

    ip_mac_set: typing.Set[typing.Tuple[str, str]] = load_db_entries(session)

    while packet := packet_queue.get():
        packet_count += 1

        if packet_count % 100 == 0 and (qs := packet_queue.qsize() or 0) != 0:
            logging.info(f'Queue size: {qs}')

        mac = packet[Ether].src
        ip = packet[IP].src
        entity = Entity(mac=mac, ip=ip)

        try:
            if (pair := (ip, mac)) not in ip_mac_set:
                logging.info(f'Added entity {entity}')
                ip_mac_set.add(pair)
                session.add(entity)
            else:
                logging.debug(f'Updated entity {entity}')
                session.query(Entity) \
                    .filter(Entity.mac == mac, Entity.ip == ip) \
                    .update({"timestamp": datetime.datetime.utcnow()})

            if packet_count % 10 == 0:
                session.commit()

        except BaseException as e:
            logging.critical(e)
            exit(1)

    session.close()


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
