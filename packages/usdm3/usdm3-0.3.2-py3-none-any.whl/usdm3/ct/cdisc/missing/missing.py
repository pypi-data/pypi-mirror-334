import os
import yaml


class Missing:
    def __init__(self):
        f = open(os.path.join(os.path.dirname(__file__), "missing_ct.yaml"))
        self._missing_ct = yaml.load(f, Loader=yaml.FullLoader)

    def code_lists(self):
        for response in self._missing_ct:
            yield response
