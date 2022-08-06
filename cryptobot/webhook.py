import logging
from dataclasses import dataclass

import uvicorn
from colorama import Fore, Style
from fastapi import FastAPI, Request

logger = logging.getLogger(__name__)


@dataclass
class Listener:
    host: str
    callback: callable
    port: int = 2203
    url: str = "/webhook"
    log_level: str = "error"

    app = FastAPI()

    def __post_init__(self):
        @self.app.post(self.url)
        async def listen_webhook(request: Request):
            data = await request.json()

            self.callback(request.headers, data)

    def listen(self):
        url = f"https://{self.host}:{self.port}{self.url}"
        logger.info(f"Listening on {url}")

        print(
            Fore.BLUE
            + r"""
 $$$$$$\                                  $$\                     $$$$$$$\              $$\
$$  __$$\                                 $$ |                    $$  __$$\             $$ |
$$ /  \__| $$$$$$\  $$\   $$\  $$$$$$\  $$$$$$\    $$$$$$\        $$ |  $$ | $$$$$$\  $$$$$$\
$$ |      $$  __$$\ $$ |  $$ |$$  __$$\ \_$$  _|  $$  __$$\       $$$$$$$\ |$$  __$$\ \_$$  _|
$$ |      $$ |  \__|$$ |  $$ |$$ /  $$ |  $$ |    $$ /  $$ |      $$  __$$\ $$ /  $$ |  $$ |
$$ |  $$\ $$ |      $$ |  $$ |$$ |  $$ |  $$ |$$\ $$ |  $$ |      $$ |  $$ |$$ |  $$ |  $$ |$$\
\$$$$$$  |$$ |      \$$$$$$$ |$$$$$$$  |  \$$$$  |\$$$$$$  |      $$$$$$$  |\$$$$$$  |  \$$$$  |
 \______/ \__|       \____$$ |$$  ____/    \____/  \______/       \_______/  \______/    \____/
                    $$\   $$ |$$ |
                    \$$$$$$  |$$ |
                     \______/ \__|
"""
        )
        print(
            Style.RESET_ALL
            + f"""[Webhook Listener]

* Docs: https://help.crypt.bot/crypto-pay-api#Webhook
* Listening on {url} (Press CTRL+C to stop)
            """
        )
        uvicorn.run(self.app, host=self.host, port=self.port, log_level=self.log_level)
