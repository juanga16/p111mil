import time

class WBAVariables(object):
    threshold = 3600
    def __init__(self, ctrl_be, threshold = 3600):
        self.ctrl_be = ctrl_be
        self.query = "show global variables"
        self.last_update_ts = 0
        self.variables = {}
        self.threshold = int(threshold)

    def update(self):
        if time.time() - self.last_update_ts > self.threshold:
            variables = {}

            if not self.ctrl_be.is_sql_connected():
                return

            result = self.ctrl_be.exec_query('SHOW GLOBAL VARIABLES')
            if result:
                while result.nextRow():
                    var_name  = result.stringByName('Variable_name')
                    var_value = result.stringByName('Value')
                    variables[var_name] = var_value
            self.last_update_ts = time.time()
            self.variables = variables

    def get_names(self):
        self.update()
        return self.variables.keys()

    def has_name(self, name):
        return name in self.variables

    def get_value(self, name):
        self.update()
        v = self.variables
        return v.get(name, "")
