from types import ModuleType
import tornado.ioloop
import tornado.web
import json
import importlib
import importlib.util
import os
import threading
import traceback
from pydantic import ValidationError
from time import sleep

from models import ActionRequest

player: ModuleType = None

player_path = os.path.join(os.path.dirname(__file__), 'player.py')

def load_player():
    global player

    player_spec = importlib.util.spec_from_file_location('player', player_path)
    player = importlib.util.module_from_spec(player_spec)
    player_spec.loader.exec_module(player)

running = True

def monitor_changes():
    global player
    last_write_time = os.path.getmtime(player_path)

    while running:
        current_write_time = os.path.getmtime(player_path)
        if last_write_time != current_write_time:
            last_write_time = current_write_time
            print ('Change detected')
            load_player()
            print(player.get_player_info())

        sleep(1)

    print('Stopping')

class MainHandler(tornado.web.RequestHandler):

    def get_payload(self):
        
        payload_len = int(self.request.headers.get('content-length', 0))
        if payload_len == 0:
            return None
        return tornado.escape.json_decode(self.request.body)

    def post(self):
        try:
            payload = self.get_payload()
            actions = player.get_actions(ActionRequest.parse_obj(payload))
            response = json.dumps(list(map(lambda a : a.__dict__, actions)), sort_keys=True, indent=2).encode()
            self.set_status(200)
            self.set_header('Content-Type', 'application/json')
            self.write(response)

        except ValidationError as e:
            print(e)
            print(traceback.format_exc())
            self.set_status(400)
            self.write('Input validation Error')
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            self.set_status(500)
            self.write('An error occurred')


def make_app():
    return tornado.web.Application([
        (r"/.*", MainHandler),
    ])

def start_server(port):
    'Starts the server on specified port'
    print('Starting HTTP server at port %d' % port)
    app = make_app()
    app.listen(port)
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    port = 9080
    load_player()
    monitor = threading.Thread(target=monitor_changes)
    monitor.start()
    start_server(port)
    running = False
    monitor.join()