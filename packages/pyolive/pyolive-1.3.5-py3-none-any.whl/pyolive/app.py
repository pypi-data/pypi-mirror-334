import os
import sys
import signal
import socket
import json
from .config import Config
from .adapter import Adapter
from .channel import Channel
from .worker import Worker
from .heartbeat import Heartbeat
from .log import AgentLog, AppLog
from .context import JobContext


def develop_mode(infile, params):
    log = AppLog("worker", devel=True).create_logger()
    ch = Channel(log, "dps.msm", "worker", devel=True)
    ctx = JobContext(devel=True)

    log.info("Developer mode started ...")
    ctx.set_fileset(infile, devel=True)
    ctx.set_param(params, devel=True)

    return log, ch, ctx


class Athena:
    def __init__(self, **kwargs):
        self.worker_name = 'ovd-worker'
        self.namespace = kwargs['namespace']
        self.alias = kwargs['alias']
        self.adapter = None
        self.channel = None
        self.tasks = []
        self.agent_logger = AgentLog(self.alias).create_logger()
        self.home = Config.ATHENA_HOME
        if self.home is None:
            print("Not found environment variable, ATHENA_HOME")
            sys.exit(0)

    def _get_pid_path(self):
        return os.path.join(self.home, 'var/pid')

    def _get_pid_filename(self):
        file = self.worker_name + '+' + self.namespace + '@' + socket.gethostname() + '.pid'
        path = self._get_pid_path()
        return os.path.join(path, file)

    def _create_pid_file(self):
        name = self._get_pid_filename()
        pid = os.getpid()
        with open(name, "w") as f:
            f.write(str(pid))

    def _remove_pid_file(self):
        name = self._get_pid_filename()
        if os.path.exists(name):
            os.remove(name)

    def _callback_signal(self, signum, frame):
        self.channel.stop()
        self.adapter.stop_consume()

    def _callback_subscribe(self, ch, method, properties, body):
        json_str = body.decode()
        self.agent_logger.info("BBB, %s", json_str)
        self.agent_logger.debug("received message, %s", json_str)
        message = json.loads(json_str)
        app_name = message['action-app']
        regkey = message['regkey']
        _s = regkey.split('@')[0] + '+' + app_name
        app_logger = AppLog(_s).create_logger()

        # worker를 thread로 실행함
        for task in self.tasks:
            if app_name == task['app']:
                ctx = JobContext(message)
                w = Worker(task['resource'], self.channel, self.agent_logger, app_logger, ctx)
                w.start()

    def run(self):
        self.agent_logger.info("------------------------------------------------")
        self.agent_logger.info("main, run %s", self.namespace)

        self.adapter = Adapter(self.agent_logger)
        if not self.adapter.open():
            return

        self._create_pid_file()
        # channel manager start
        self.channel = Channel(self.agent_logger, self.namespace, self.alias)
        self.channel.start()

        # heartbeat timer start
        heartbeat = Heartbeat(self.channel, self.namespace, self.worker_name)
        heartbeat.start()

        # signal 처리
        signal.signal(signal.SIGTERM, self._callback_signal)
        signal.signal(signal.SIGINT, self._callback_signal)

        # consume manager looping
        self.adapter.start_consume(self.namespace, self._callback_subscribe)

        # end job
        self.agent_logger.info("main, exit")
        print("main, exit")
        self.adapter.close()
        heartbeat.stop()
        self._remove_pid_file()
        sys.exit(0)

    def add_resource(self, resource, app_name):
        task = {}
        task['app'] = app_name
        task['resource'] = resource
        self.tasks.append(task)
