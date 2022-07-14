import threading

from sqlalchemy import Column, String, UnicodeText, distinct, func

from . import BASE, SESSION


class GuardianBroadcast(BASE):
    __tablename__ = "guardianbroadcast"
    keywoard = Column(UnicodeText, primary_key=True)
    group_id = Column(String(14), primary_key=True, nullable=False)

    def __init__(self, keywoard, group_id):
        self.keywoard = keywoard
        self.group_id = str(group_id)

    def __repr__(self):
        return "<Guardian Broadcast channels '%s' for %s>" % (
            self.group_id,
            self.keywoard,
        )

    def __eq__(self, other):
        return bool(
            isinstance(other, GuardianBroadcast)
            and self.keywoard == other.keywoard
            and self.group_id == other.group_id
        )


GuardianBroadcast.__table__.create(checkfirst=True)

GUARDIANBROADCAST_INSERTION_LOCK = threading.RLock()


class BROADCAST_SQL:
    def __init__(self):
        self.BROADCAST_CHANNELS = {}


BROADCAST_SQL_ = BROADCAST_SQL()


def add_to_broadcastlist(keywoard, group_id):
    with GUARDIANBROADCAST_INSERTION_LOCK:
        broadcast_group = GuardianBroadcast(keywoard, str(group_id))

        SESSION.merge(broadcast_group)
        SESSION.commit()
        BROADCAST_SQL_.BROADCAST_CHANNELS.setdefault(keywoard, set()).add(str(group_id))


def rm_from_broadcastlist(keywoard, group_id):
    with GUARDIANBROADCAST_INSERTION_LOCK:
        broadcast_group = SESSION.query(GuardianBroadcast).get((keywoard, str(group_id)))
        if broadcast_group:
            if str(group_id) in BROADCAST_SQL_.BROADCAST_CHANNELS.get(keywoard, set()):
                BROADCAST_SQL_.BROADCAST_CHANNELS.get(keywoard, set()).remove(
                    str(group_id)
                )

            SESSION.delete(broadcast_group)
            SESSION.commit()
            return True

        SESSION.close()
        return False


def is_in_broadcastlist(keywoard, group_id):
    with GUARDIANBROADCAST_INSERTION_LOCK:
        broadcast_group = SESSION.query(GuardianBroadcast).get((keywoard, str(group_id)))
        return bool(broadcast_group)


def del_keyword_broadcastlist(keywoard):
    with GUARDIANBROADCAST_INSERTION_LOCK:
        broadcast_group = (
            SESSION.query(GuardianBroadcast.keywoard)
            .filter(GuardianBroadcast.keywoard == keywoard)
            .delete()
        )
        BROADCAST_SQL_.BROADCAST_CHANNELS.pop(keywoard)
        SESSION.commit()


def get_chat_broadcastlist(keywoard):
    return BROADCAST_SQL_.BROADCAST_CHANNELS.get(keywoard, set())


def get_broadcastlist_chats():
    try:
        chats = SESSION.query(GuardianBroadcast.keywoard).distinct().all()
        return [i[0] for i in chats]
    finally:
        SESSION.close()


def num_broadcastlist():
    try:
        return SESSION.query(GuardianBroadcast).count()
    finally:
        SESSION.close()


def num_broadcastlist_chat(keywoard):
    try:
        return (
            SESSION.query(GuardianBroadcast.keywoard)
            .filter(GuardianBroadcast.keywoard == keywoard)
            .count()
        )
    finally:
        SESSION.close()


def num_broadcastlist_chats():
    try:
        return SESSION.query(func.count(distinct(GuardianBroadcast.keywoard))).scalar()
    finally:
        SESSION.close()


def __load_chat_broadcastlists():
    try:
        chats = SESSION.query(GuardianBroadcast.keywoard).distinct().all()
        for (keywoard,) in chats:
            BROADCAST_SQL_.BROADCAST_CHANNELS[keywoard] = []

        all_groups = SESSION.query(GuardianBroadcast).all()
        for x in all_groups:
            BROADCAST_SQL_.BROADCAST_CHANNELS[x.keywoard] += [x.group_id]

        BROADCAST_SQL_.BROADCAST_CHANNELS = {
            x: set(y) for x, y in BROADCAST_SQL_.BROADCAST_CHANNELS.items()
        }

    finally:
        SESSION.close()


__load_chat_broadcastlists()
