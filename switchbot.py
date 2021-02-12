#!/usr/bin/env python3
# coding=utf-8

import sys
import os
import json
from urllib.parse import urlencode
from urllib.request import urlopen, Request, URLError, HTTPError
from argparse import ArgumentParser

BASE_URL        = "https://api.switch-bot.com"
BASE_PATH       = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE      = os.path.join(BASE_PATH, 'token.txt')
DEVICES_FILE    = os.path.join(BASE_PATH, 'devices.json')

usage = 'Usage: python {} command [--dev_id dev_id]'.format(__file__)
commands = '|'.join(['get_devices', 'get_status', 'post_action'])
argparser = ArgumentParser(usage=usage)
argparser.add_argument('command', type=str, help=commands)
argparser.add_argument('-d', '--dev_id',    type=str, dest='dev_id',  default='dev_id',  help='device id for reading status')
argparser.add_argument('-a', '--action',    type=str, dest='action',  default='turnOn',  help='command to send device')
argparser.add_argument('-p', '--parameter', type=str, dest='param',   default='default', help='parameter of command')
argparser.add_argument('-t', '--type',      type=str, dest='type',    default='command', help='type of command')
args = argparser.parse_args()

def get_token():
    with open(TOKEN_FILE, 'r') as f:
        token = f.read().strip()
        # print(token)
        return token

token = get_token()

url = BASE_URL + '/v1.0'
headers = { 'Authorization': token } 
data = None
if args.command.startswith('get_dev'):
    url += '/devices'
elif args.command.startswith('get_sta'):
    url += '/devices/' + args.dev_id + '/status'
elif args.command.startswith('send_com'):
    url += '/devices/' + args.dev_id + '/commands/' + args.action
    data = { 'command': args.action, 'parameter': args.param, 'commandType': args.type }
    data = urlencode(data)
    data = data.encode('ascii')
    headers['Content-Type'] = 'application/json'
else:
    print("Command error: ", args.command)
    sys.exit(1)
# print(url)

req = Request(url, data, headers)
req.add_header('Authorization', token)
try:
    res = urlopen(req)
except HTTPError as e:
    print('Error code: ', e.getcode())
    sys.exit(1)
except URLError as e:
    print('Reason: ', e.reason)
    sys.exit(1)

body = res.read().decode()
print(body)
