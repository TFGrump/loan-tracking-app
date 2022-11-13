import pyqrcode as qr
from argparse import ArgumentParser

def args_to_dict(args) -> str:
    return f'user: {args.user}, password: {args.password}'

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-u", "--user", type=str, required=True, help="The username for the sql connector")
    parser.add_argument("-p", "--password", type=str, required=True, help="The password for the sql connector")
    args = parser.parse_args()
    return args_to_dict(args)

qr_code = qr.create(parse_args())
qr_code.svg('qr_code.svg', scale=5)
