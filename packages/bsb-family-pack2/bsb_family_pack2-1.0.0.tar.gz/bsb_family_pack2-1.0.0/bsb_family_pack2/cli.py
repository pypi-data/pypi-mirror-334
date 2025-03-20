# bsb_family_pack2/cli.py
import argparse
from .core import connect_family, disconnect_family
from .auto_monitor import start_monitoring

def main():
    parser = argparse.ArgumentParser(
        description="BSB Family Pack 2 - Family Connection and Monitoring Tool"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-connect", action="store_true", help="Connect to the Telegram family bot")
    group.add_argument("-disconnect", action="store_true", help="Disconnect from the Telegram family bot")
    group.add_argument("-monitor", action="store_true", help="Start automatic monitoring of new events")
    
    parser.add_argument("-t", "--token", type=str, help="Telegram Bot Token (required for connect)")
    parser.add_argument("-c", "--chat_id", type=str, help="Telegram Chat ID (required for connect)")
    
    args = parser.parse_args()
    
    if args.connect:
        if not args.token or not args.chat_id:
            print("For connecting, please provide both --token and --chat_id.")
        else:
            connect_family(args.token, args.chat_id)
    elif args.disconnect:
        disconnect_family()
    elif args.monitor:
        start_monitoring()

if __name__ == "__main__":
    main()
