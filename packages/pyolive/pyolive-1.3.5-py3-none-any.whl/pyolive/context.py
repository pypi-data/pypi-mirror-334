import base64
import re
from dataclasses import dataclass

@dataclass
class JobContext:
    regkey:str
    topic:str
    action_id:int
    action_ns:str
    action_app:str
    action_params:str
    job_id:str
    job_hostname:str
    job_seq:int
    timestamp:int
    filenames:list
    msgbox:dict

    def __init__(self, message=None, devel=False):
        self.first_fileset = True
        if not devel:
            self.regkey = message['regkey']
            self.topic = message['topic']
            self.action_id = int(message['action-id'])
            self.action_ns = message['action-ns']
            self.action_app = message['action-app']
            self.action_params = message['action-params']
            self.job_id = message['job-id']
            self.job_hostname = message['job-hostname']
            self.job_seq = int(message['job-seq'])
            self.timestamp = int(message['timestamp'])
            self.filenames = message['filenames'][:]
            self.msgbox = message['msgbox']
        else:
            self.regkey = ''
            self.topic = ''
            self.action_id = 0
            self.action_ns = ''
            self.action_app = 'ovm_pytest'
            self.action_params = ''
            self.job_id = ''
            self.job_seq = 0
            self.timestamp = 0
            self.filenames = []
            self.msgbox = {}

    def get_param(self, key):
        pattern = re.compile(rf"{re.escape(key)}='(.*?)'")
        match = pattern.search(self.action_params)
        return match.group(1) if match else ''

    def get_fileset(self):
        return self.filenames

    def get_msgbox(self):
        if self.msgbox == {}:
            return ''
        if self.msgbox['type'] == 'binary':
            bstr = base64.b64decode(self.msgbox['data'])
            return bstr.decode('UTF-8')
        else:
            return self.msgbox['data']

    def set_param(self, string, devel=False):
        if not devel:
            pass
        else:
            self.action_params = string

    def set_fileset(self, filename, devel=False):
        if not devel:
            if self.first_fileset:
                self.filenames = []
                self.filenames.append(filename)
                self.first_fileset = False
            else:
                self.filenames.append(filename)
        else:
            self.filenames = filename.split(',')

    def reset_fileset(self, filenames):
        self.filenames = filenames[:]

    def set_msgbox(self, data):
        self.msgbox['type'] = 'ascii'
        self.msgbox['size'] = len(data)
        self.msgbox['data'] = data
