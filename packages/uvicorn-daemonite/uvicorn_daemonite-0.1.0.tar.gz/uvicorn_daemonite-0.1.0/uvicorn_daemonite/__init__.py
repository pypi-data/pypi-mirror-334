import os
import signal
import sys
import argparse
import time
from multiprocessing import Process

import psutil
import uvicorn

__version__ = "0.1.0"
__author__  = "Juergen 'eTM' Mangler"
__credits__ = "Matz for creating something that doesnt suck as hard as this."

class Daemonite:
  def __init__(self,**arguments):
    self.config = arguments
    self.parser = argparse.ArgumentParser(
      prog = self.config['name'] + '.py',
      description = self.config['description'],
      exit_on_error=False)
    self.parser.add_argument('-v', '--verbose', action='store_true', help='show output and stay in foreground')
    self.parser.add_argument('COMMAND', help='stop, start, restart, info, help')
    self.parser.error = self.print_error

  def start(self):
    try:
      args = self.parser.parse_args()
    except Exception:
      self.parser.print_help()
      exit()

    if args.COMMAND == 'start' and args.verbose:
      self.start_server()
    elif args.COMMAND == 'start' and not args.verbose:
      self.run_server()
    elif args.COMMAND == 'restart' and not args.verbose:
      self.stop_server()
      self.run_server()
    elif args.COMMAND == 'restart' and args.verbose:
      self.stop_server()
      self.start_server()
    elif args.COMMAND == 'stop':
      self.stop_server()
    elif args.COMMAND == 'info':
      if os.path.exists(self.config['name'] + '.pid'):
        with open(self.config['name'] + ".pid","r") as f: pid =f.read()
        if psutil.pid_exists(int(pid)):
          print("It is probably startet as PID " + str(int(pid)) + ' (Port ' + str(self.config['port']) + ').')
        else:
          print("I think it is not started. If it were, it had Port " + str(self.config['port']) + '.')
          os.remove(self.config['name'] + '.pid')
      else:
        print("It is probably not started. If it were, it had Port " + str(self.config['port']) + '.')
    elif args.COMMAND == 'help':
      self.parser.print_help()
    else:
      self.parser.print_help()

  def fork_server(self):
    pid = os.fork()
    if pid != 0:
        return
    print('Starting as PID ' + str(os.getpid()) + ' (Port ' + str(self.config['port']) + ').')
    print(os.getpid(), file=open(self.config['name'] + '.pid', 'w'))
    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout = open('/dev/null', 'w')
    sys.stderr = open('/dev/null', 'w')
    self.start_server()

  def start_server(self):
    uvicorn.run(self.config['name'] + ":app", port=int(self.config['port']), log_level=self.config['log_level'])

  def run_server(self):
    proc = Process(target=self.fork_server, args=(), daemon=True)
    proc.start()
    proc.join()

  def running_server(self,pid):
    try:
      os.kill(pid, 0)
    except OSError:
      return False

    return True

  def print_error(self,msg):
    print("Error: " + msg + ".\n")
    self.parser.print_help()
    exit(-1)

  def stop_server(self):
    if os.path.exists(self.config['name'] + '.pid'):
      with open(self.config['name'] + ".pid","r") as f: pid =f.read()
      print('Killing PID ' + str(int(pid)) + '.')
      os.remove(self.config['name'] + '.pid')
      try:
        os.kill(int(pid),signal.SIGINT)
        while self.running_server(int(pid)):
          time.sleep(.25)
      except OSError:
        print('Nope, was not started.')
    else:
      print("Nothing to stop.")
