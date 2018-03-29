# Keypirinha launcher (keypirinha.com)

import socket

import keypirinha as kp
import keypirinha_net as kpnet
import keypirinha_util as kpu


class MyIP(kp.Plugin):
    """
    Get your public and local IP directly from Keypirinha.
    """

    ITEM_CAT = kp.ItemCategory.USER_BASE + 1
    KEYWORD = 'ip'

    def __init__(self):
        super().__init__()
        self._urlopener = kpnet.build_urllib_opener()

    def on_suggest(self, user_input, items_chain):
        if user_input.lower() == self.KEYWORD:
            public_ip = self._get_public_ip()
            local_ip = self._get_local_ip()

            self.set_catalog(
                [
                    self.create_item(
                        category=kp.ItemCategory.KEYWORD,
                        label='Your public IP',
                        short_desc=public_ip,
                        target='public_ip',
                        args_hint=kp.ItemArgsHint.FORBIDDEN,
                        hit_hint=kp.ItemHitHint.NOARGS
                    ),
                    self.create_item(
                        category=kp.ItemCategory.KEYWORD,
                        label='Your local IP',
                        short_desc=local_ip,
                        target='local_ip',
                        args_hint=kp.ItemArgsHint.FORBIDDEN,
                        hit_hint=kp.ItemHitHint.NOARGS
                    )
                ]
            )

    def on_execute(self, item, action):
        kpu.set_clipboard(item.short_desc())

    def on_events(self, flags):
        if flags & kp.Events.NETOPTIONS:
            self._urlopener = kpnet.build_urllib_opener()

    def _get_public_ip(self):
        try:
            with self._urlopener.open('http://icanhazip.com') as res:
                return res.read().decode('utf-8')
        except Exception as ex:
            self.err(ex)
            return 'Could not establish your public ip'

    def _get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        except Exception as ex:
            self.err(ex)
            return 'Could not establish your local ip'
