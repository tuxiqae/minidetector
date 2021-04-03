import datetime
import logging
import typing
from queue import Queue

from scapy.layers.inet import IP
from scapy.layers.l2 import Ether
from scapy.packet import Packet
from sqlalchemy.orm import Session

from lib.Entity import Entity
from lib.database import create_session, load_db_entries

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

    except Exception as e:
        logging.exception(e)
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

        except Exception as e:
            logging.exception(e)
            exit(1)

    session.close()
