#!/usr/bin/env python3
# coding=utf-8

import sys
import os
import time
import json
import uuid
import base64
import hashlib
import hmac
import requests
from argparse import ArgumentParser

class SwitchBot:
    BASE_URL        = 'https://api.switch-bot.com'
    BASE_PATH       = os.path.dirname(os.path.abspath(__file__))
    TOKEN_FILE      = os.path.join(BASE_PATH, 'token.txt')
    SECRET_FILE     = os.path.join(BASE_PATH, 'secret.txt')
    DEVICES_FILE    = os.path.join(BASE_PATH, 'devices.json')

    def __init__(self):
        with open(SwitchBot.TOKEN_FILE, 'r') as f:
            self.token = f.read().strip()
        with open(SwitchBot.SECRET_FILE, 'r') as f:
            self.secret = f.read().strip()

    def get_headers(self):
        sign, t, nonce = self.sign(self.token, self.secret)

        headers = {}
        headers['Authorization'] = self.token
        headers['charset'] = 'utf8'
        headers['t'] = str(t)
        headers['sign'] = str(sign, 'utf-8')
        headers['nonce'] = nonce
        return headers

    def sign(self, token, secret):
        key = bytes(secret, "utf-8")
        t = int(round(time.time() * 1000))
        nonce = str(uuid.uuid4())
        string_to_sign = "{}{}{}".format(token, t, nonce)
        msg = bytes(string_to_sign, "utf-8")
        sign = base64.b64encode( hmac.new(key, msg=msg, digestmod=hashlib.sha256).digest() )
        return sign, t, nonce
	
    def get_url(self, *pathes):
        url = SwitchBot.BASE_URL + '/v1.1'
        for path in pathes:
            url += '/' + path
        return url

    def do_get(self, url):
        headers = self.get_headers()
        response = requests.get(url=url, headers=headers)
        return response.text
    
    def do_post(self, url, data):
        headers = self.get_headers()
        headers['Content-Type'] = 'application/json'
        response = requests.post(url=url, data=data, headers=headers)
        return response.text
    
    def get_devices(self):
        url = self.get_url('devices')
        body = self.do_get(url)
        dict = json.loads(body)
        return dict['body']['deviceList']
      
    def get_infrared_devices(self):
        url = self.get_url('devices')
        body = self.do_get(url)
        dict = json.loads(body)
        return dict['body']['infraredRemoteList']
 
    def get_status(self, id):
        url = self.get_url('devices', id, 'status')
        body = self.do_get(url)
        dict = json.loads(body)
        return dict['body']

    def send_command(self, id, command, param, type):
        url = self.get_url('devices', id, 'commands')
        data = { 'command': command, 'parameter': param, 'commandType': type }
        data = json.dumps(data)
        data = data.encode('ascii')
        body = self.do_post(url, data)
        dict = json.loads(body)
        return dict

if __name__ == '__main__':
    argparser = ArgumentParser(description='SwitchBot device control.')
    argparser.add_argument('command', type=str, help='get_devices|get_infrared_devices|get_status|send_command')
    argparser.add_argument('-d', '--dev_id',    type=str, dest='dev_id',  default='dev_id',  help='device id for reading status')
    argparser.add_argument('-a', '--action',    type=str, dest='action',  default='turnOn',  help='command to send device')
    argparser.add_argument('-p', '--parameter', type=str, dest='param',   default='default', help='parameter of command')
    argparser.add_argument('-t', '--type',      type=str, dest='type',    default='command', help='type of command')
    args = argparser.parse_args()

    sb = SwitchBot()
    if args.command.startswith('get_dev'):
        dict = sb.get_devices()
    elif args.command.startswith('get_infra'):
        dict = sb.get_infrared_devices()
    elif args.command.startswith('get_sta'):
        dict = sb.get_status(args.dev_id)
    elif args.command.startswith('send_com'):
        dict = sb.send_command(args.dev_id, args.action, args.param, args.type)
    else:
        print("Command error: ", args.command)
        sys.exit(1)

    print(json.dumps(dict))
