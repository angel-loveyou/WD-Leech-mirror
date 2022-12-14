from threading import Thread
from time import time
from charset_normalizer import logging
from speedtest import Speedtest
from bot.helper.ext_utils.bot_utils import get_readable_time
from telegram.ext import CommandHandler
from bot.helper.telegram_helper.filters import CustomFilters
from bot import dispatcher, botStartTime
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import auto_delete_message, sendMessage, deleteMessage, sendPhoto, editMessage
from bot.helper.ext_utils.bot_utils import get_readable_file_size

def speedtest(update, context):
    speed = sendMessage("βοΈRunning Speed Test. Wait about some secs.", context.bot, update.message)
    test = Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()
    path = (result['share'])
    currentTime = get_readable_time(time() - botStartTime)
    string_speed = f'''
    π πππππππππ ππππ π
β <b>Upload β’</b> <code>{speed_convert(result['upload'], False)}</code>
β <b>Download β’</b>  <code>{speed_convert(result['download'], False)}</code>
β <b>Ping β’</b> <code>{result['ping']} ms</code>
β <b>Time β’</b> <code>{result['timestamp']}</code>
β <b>Data Sent β’</b> <code>{get_readable_file_size(int(result['bytes_sent']))}</code>
β <b>Data Received β’</b> <code>{get_readable_file_size(int(result['bytes_received']))}</code>

    π πππππππππ ππππππ π
β <b>Name β’</b> <code>{result['server']['name']}</code>
β <b>Country β’</b> <code>{result['server']['country']}, {result['server']['cc']}</code>
β <b>Sponsor β’</b> <code>{result['server']['sponsor']}</code>
β <b>Latency β’</b> <code>{result['server']['latency']}</code>
β <b>Latitude β’</b> <code>{result['server']['lat']}</code>
β <b>Longitude β’</b> <code>{result['server']['lon']}</code>

   π ππ πππππππ π
β <b>IP Address β’</b> <code>{result['client']['ip']}</code>
β <b>Latitude β’</b> <code>{result['client']['lat']}</code>
β <b>Longitude β’</b> <code>{result['client']['lon']}</code>
β <b>Country β’</b> <code>{result['client']['country']}</code>
β <b>ISP β’</b> <code>{result['client']['isp']}</code>
β <b>ISP Rating β’</b> <code>{result['client']['isprating']}</code>
'''
    try:
        pho = sendPhoto(text=string_speed, bot=context.bot, message=update.message, photo=path)
        deleteMessage(context.bot, speed)
        Thread(target=auto_delete_message, args=(context.bot, update.message, pho)).start()
    except Exception as g:
        logging.error(str(g))
        editMessage(string_speed, speed)
        Thread(target=auto_delete_message, args=(context.bot, update.message, speed)).start()

def speed_convert(size, byte=True):
    if not byte: size = size / 8
    power = 2 ** 10
    zero = 0
    units = {0: "B/s", 1: "KB/s", 2: "MB/s", 3: "GB/s", 4: "TB/s"}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"

speed_handler = CommandHandler(BotCommands.SpeedCommand, speedtest,
    CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)

dispatcher.add_handler(speed_handler)
