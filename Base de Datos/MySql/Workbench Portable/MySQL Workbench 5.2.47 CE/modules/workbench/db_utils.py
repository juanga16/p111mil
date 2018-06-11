from grt import modules
from grt import DBAccessDenied, DBLoginError

def escape_sql_string(s):
    return s.replace("\\", "\\\\").replace("'", "\\'")

def escape_sql_identifier(s):
    return s.replace("`", "``")


class MySQLError(Exception):
    def __init__(self, msg, code, location):
        Exception.__init__(self, msg + " (code %i)"%code)
        self.code = code
        self.location = location

class MySQLLoginError(MySQLError, DBLoginError):
    def __init__(self, msg, code, location):
        MySQLError.__init__(self, msg, code, location)
        DBLoginError.__init__(self, msg)


class QueryError(Exception):
  not_connected_errors = (2006, 2013, 2026, 2055, 2048)
  def __init__(self, msg, error, errortext = None):
    self.msg = msg
    self.error = error
    self.errortext = errortext

  def __str__(self):
    return self.msg + ".\nSQL Error: " + str(self.error)

  def is_connection_error(self):
    code = 0
    try:
      code = int(self.error)
    except ValueError:
      pass
    return code in self.not_connected_errors

  def is_error_recoverable(self):
    return self.error != 2006 # Probably add more errors here


class ConnectionTunnel:
    def __init__(self, info):
        self.tunnel = modules.DbMySQLQuery.openTunnel(info)
        if self.tunnel > 0:
            self.port = modules.DbMySQLQuery.getTunnelPort(self.tunnel)
        else:
            self.port = None
    
    def __del__(self):
        if self.tunnel > 0:
            modules.DbMySQLQuery.closeTunnel(self.tunnel)


class MySQLResult:
    def __init__(self, result):
        self.result = result


    def __del__(self):
        if self.result:
            modules.DbMySQLQuery.closeResult(self.result)

    def firstRow(self):
        return modules.DbMySQLQuery.resultFirstRow(self.result)

    def nextRow(self):
        return modules.DbMySQLQuery.resultNextRow(self.result)

    
    def stringByName(self, name):
        return modules.DbMySQLQuery.resultFieldStringValueByName(self.result, name)

    def unicodeByName(self, name):
        s = modules.DbMySQLQuery.resultFieldStringValueByName(self.result, name)
        if type(s) is str:
            return s.decode("utf-8")
        return s

    def intByName(self, name):
        return modules.DbMySQLQuery.resultFieldIntValueByName(self.result, name)

    
    def stringByIndex(self, i):
        return modules.DbMySQLQuery.resultFieldStringValue(self.result, i)

    def unicodeByIndex(self, i):
        s = modules.DbMySQLQuery.resultFieldStringValue(self.result, i)
        if type(s) is str:
            return s.decode("utf-8")
        return s


    def intByIndex(self, i):
        return modules.DbMySQLQuery.resultFieldIntValue(self.result, i)

    def numFields(self):
        return modules.DbMySQLQuery.resultNumFields(self.result)

    def numRows(self):
        return modules.DbMySQLQuery.resultNumRows(self.result)

    def fieldName(self, i):
        return modules.DbMySQLQuery.resultFieldName(self.result, i)

    def fieldType(self, i):
        return modules.DbMySQLQuery.resultFieldType(self.result, i)
        

class MySQLConnection:
    """
        Connection to a MySQL server, use as:
          info = grt.root.wb.rdbmsMgmt.storedConns[0]
          conn = MySQLConnection(info)
          conn.connect()
          result = conn.executeQuery("SHOW DATABASES")
          flag = result.firstRow()
          while flag:
              print result.stringByName("Database")
              flag = result.nextRow()
    """
    def __init__(self, info, status_cb = None, password = None):
        assert type(status_cb) is not unicode
        self.connect_info = info
        self.connection = 0
        self.server_down = 0
        self.status_cb = status_cb
        self.password = password


    def __del__(self):
        self.disconnect()

    def send_status(self, code, error = None):
        if self.status_cb:
            self.status_cb(code, error, self.connect_info)

    def connect(self):
        self.server_down = False
        if not self.connection:
            params = self.connect_info.parameterValues
            old_timeout_value = None
            if params.has_key('OPT_READ_TIMEOUT'):
                old_timeout_value = params['OPT_READ_TIMEOUT']
            params['OPT_READ_TIMEOUT'] = 5*60

            #self.thread = thread.get_ident()
            if self.password is not None:
                self.connection = modules.DbMySQLQuery.openConnectionP(self.connect_info, self.password)
            else:
                self.connection = modules.DbMySQLQuery.openConnection(self.connect_info)

            if old_timeout_value:
                params['OPT_READ_TIMEOUT'] = old_timeout_value
            else:
                del params['OPT_READ_TIMEOUT']
            if self.connection < 0:
                self.connection = 0
                code = modules.DbMySQLQuery.lastErrorCode()
                if code == 1045:
                    raise MySQLLoginError(modules.DbMySQLQuery.lastError(), modules.DbMySQLQuery.lastErrorCode(), "%s@%s" % (self.connect_info.parameterValues["userName"], self.connect_info.parameterValues["hostName"]))
                    
                if code in (2003,):
                    self.server_down = True
                raise MySQLError(modules.DbMySQLQuery.lastError(), modules.DbMySQLQuery.lastErrorCode(), "%s@%s" % (self.connect_info.parameterValues["userName"], self.connect_info.parameterValues["hostName"]))

            self.send_status(0, "Connection created")

    def ping(self):
        self.executeQuery("SELECT 1")
        return True

    
    def disconnect(self):
        if self.connection:
            modules.DbMySQLQuery.closeConnection(self.connection)
            self.connection = 0
            self.send_status(-1, "Connection closed by client")
    
    @property
    def is_connected(self):
        return self.connection > 0
    

    def execute(self, query):
        if self.connection:
            #assert self.thread == thread.get_ident()
            result = modules.DbMySQLQuery.execute(self.connection, query)
            if result < 0:
              code = modules.DbMySQLQuery.lastConnectionErrorCode(self.connection)
              error = modules.DbMySQLQuery.lastConnectionError(self.connection)
              self.send_status(code, error)
              raise QueryError("Error executing '%s'\n%s" %(query, error), code, error)

            self.send_status(0)
            return result != 0
        else:
            self.send_status(-1, "Connection to MySQL server is currently not established")
            raise QueryError("Connection to MySQL server is currently not established", -1)


    def executeQuery(self, query):
        if self.connection:
            #assert self.thread == thread.get_ident()
            result = modules.DbMySQLQuery.executeQuery(self.connection, query.encode("utf8") if type(query) is unicode else query)
            if result < 0:
                code = modules.DbMySQLQuery.lastConnectionErrorCode(self.connection)
                error = modules.DbMySQLQuery.lastConnectionError(self.connection)
                self.send_status(code, error)
                raise QueryError("Error executing '%s'\n%s"%(query, error), code, error)

            self.send_status(0)
            return MySQLResult(result)
        else:
            self.send_status(-1, "Connection to MySQL server is currently not established")
            raise QueryError("Connection to MySQL server is currently not established", -1)


    def updateCount(self):
        return modules.DbMySQLQuery.lastUpdateCount(self.connection)
    affectedRows = updateCount

