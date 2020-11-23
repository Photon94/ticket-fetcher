from telethon import TelegramClient, events, sync
import re
import time
import os
import win32clipboard

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
api_id = os.getenv('TICKER_FETCHER_API_KEY')
api_hash = os.getenv('TICKER_FETCHER_API_HASH')

# no register sensitive
dialog_name = 'US Long'

exp = '[^🔒|❗️] (\w+) \((\d+.\d+) %\)'
msg_anc = '🕤 Последнее обновление'
max_msgs = 100

client = TelegramClient('session_name', api_id, api_hash)
client.start()


def main():
    dialogs = client.get_dialogs()
    dialog = ''
    for dialog in dialogs:
        if dialog.name.lower() == dialog_name.lower():
            break

    best_stock_id = ''
    while True:
        messages = client.get_messages(dialog, max_msgs)
        message = ''
        for message in messages:
            if msg_anc in message.message:
                break

        stocks_list = re.findall(exp, message.message)
        stocks_dict = {}
        for stock_tuple in stocks_list:
            stocks_dict[stock_tuple[0]] = float(stock_tuple[1].replace(',', '.'))

        try:
            best_stock = max(stocks_dict, key=stocks_dict.get)
        except ValueError:
            best_stock = ''

        if best_stock_id != best_stock and best_stock != '':
            best_stock_id = best_stock
            print(f'current best stock is: {best_stock_id}')
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(best_stock_id)
            win32clipboard.CloseClipboard()

        time.sleep(1)


if __name__ == '__main__':
    main()
