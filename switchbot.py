#!/usr/bin/env python3
# coding=utf-8

import sys
import os
import json
from urllib.parse import urlencode
from urllib.request import urlopen, Request, URLError, HTTPError
from argparse import ArgumentParser

class SwitchBot:
    BASE_URL        = 'https://api.switch-bot.com'
    BASE_PATH       = os.path.dirname(os.path.abspath(__file__))
    TOKEN_FILE      = os.path.join(BASE_PATH, 'token.txt')
    DEVICES_FILE    = os.path.join(BASE_PATH, 'devices.json')

    def __init__(self):
        with open(SwitchBot.TOKEN_FILE, 'r') as f:
            self.token = f.read().strip()

    def get_headers(self):
        return { 'Authorization': self.token }

    def get_url(self, *pathes):
        url = SwitchBot.BASE_URL + '/v1.0'
        for path in pathes:
            url += '/' + path
        return url

    def do_get(self, url, data, headers={}):
        req = Request(url, data, headers)
        req.add_header('Authorization', self.token)
        res = urlopen(req)
        return res.read().decode()

    def get_devices(self):
        url = self.get_url('devices')
        body = self.do_get(url, None)
        dict = json.loads(body)
        return dict['body']['deviceList']
       
    def get_status(self, id):
        url = self.get_url('devices', id, 'status')
        body = self.do_get(url, None)
        dict = json.loads(body)
        return dict['body']

    def send_command(self, id, command, param, type):
        url = self.get_url('devices', id, command)
        data = { 'command': args.action, 'parameter': args.param, 'commandType': args.type }
        data = urlencode(data)
        data = data.encode('ascii')
        headers = {'Content-Type' : 'application/json'}
        body = self.do_get(url, data, headers)
        dict = json.loads(body)
        return dict

if __name__ == '__main__':
    argparser = ArgumentParser(description='SwitchBot device control.')
    argparser.add_argument('command', type=str, help='get_devices|get_status|post_action')
    argparser.add_argument('-d', '--dev_id',    type=str, dest='dev_id',  default='dev_id',  help='device id for reading status')
    argparser.add_argument('-a', '--action',    type=str, dest='action',  default='turnOn',  help='command to send device')
    argparser.add_argument('-p', '--parameter', type=str, dest='param',   default='default', help='parameter of command')
    argparser.add_argument('-t', '--type',      type=str, dest='type',    default='command', help='type of command')
    args = argparser.parse_args()

    sb = SwitchBot()
    if args.command.startswith('get_dev'):
        dict = sb.get_devices()
    elif args.command.startswith('get_sta'):
        dict = sb.get_status(args.dev_id)
    elif args.command.startswith('send_com'):
        dict = sb.send_command(args.dev_id, args.action, args.param, args.type)
    else:
        print("Command error: ", args.command)
        sys.exit(1)

    print(json.dumps(dict))
