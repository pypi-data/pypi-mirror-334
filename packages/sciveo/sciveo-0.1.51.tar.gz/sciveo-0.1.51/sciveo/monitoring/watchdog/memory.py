#
# Pavlin Georgiev, Softel Labs
#
# This is a proprietary file and may not be copied,
# distributed, or modified without express permission
# from the owner. For licensing inquiries, please
# contact pavlin@softel.bg.
#
# 2025
#


import psutil
import subprocess
import time
import threading

from sciveo.tools.daemon import *
from sciveo.tools.logger import *
from sciveo.tools.simple_counter import RunCounter


class MemoryWatchDogDaemon(DaemonBase):
  def __init__(self, threshold_percent=90, period=5, command="echo '⚠️ Low Memory!'"):
    super().__init__(period=period)
    self.threshold_percent = threshold_percent
    self.command = command
    self.used_percent = 0
    self.printer = RunCounter(60, lambda: debug(f"Memory usage: {self.used_percent}%", f"threshold: {self.threshold_percent}%"))

  def loop(self):
    mem = psutil.virtual_memory()
    self.used_percent = mem.percent
    self.printer.run()
    if self.used_percent > self.threshold_percent:
      warning(f"⚠️ Memory usage {self.used_percent}% exceeded {self.threshold_percent}%, executing command: {self.command}")
      subprocess.run(self.command, shell=True)
