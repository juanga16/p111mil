# Copyright (c) 2012, Oracle and/or its affiliates. All rights reserved.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; version 2 of the
# License.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301  USA

from MySQLGetRequestResult import MySQLGetRequestResult
from HTMLGetData import HTMLGetData
from HTMLParser import HTMLParseError
from wb import DefineModule
import urllib, urllib2, cookielib
import grt, shutil, zipfile, os, mimetypes
from grt import log_info, log_error, log_warning, log_debug

ModuleInfo = DefineModule(name= "WbBugReport", author= "Oracle", version="1.0")

@ModuleInfo.export(grt.STRING, grt.STRING, grt.STRING, grt.DICT)
def submitBug(user, password, data):
    #Initializes the return value as no error
    ret_val = ''

    try:
        # Creates the object to open and manage the cookies
        cookieJar = cookielib.CookieJar()
        urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))

        # Attempts to login
        ret_val = login(urlOpener, user, password)
        
        if ret_val == '':
            log_file = ''
            if 'log_file' in data.keys():
                log_file = data['log_file']
                del data['log_file']

            # Submits the bug, returning any error message to the caller
            ret_val = submit_bug(urlOpener, data, log_file)

            

            # Finally logs out
            logout(urlOpener)

    except Exception, e:
        ret_val = 'error|Unknown failure submitting bug report, please proceed through http://bugs.mysql.com/report.php'
        log_error("WB Bug Report", 'An error occurred while submitting the request, %s : %s\n' % (e.__class__.__name__, str(e)))
    
    return ret_val


def submit_bug(opener, data, log_file):

    # The default error in case of unknown failure
    ret_val = 'error|Unknown error while submitting the bug, please proceed through http://bugs.mysql.com/report.php'

    try:
        # Encodes the received information for the bug submition
        params = urllib.urlencode(data)

        # Submits the bug
        response = opener.open('http://bugs.mysql.com/report.php', params)


        # Reads the server response
        data = response.read()

        parser = MySQLGetRequestResult()
        parser.feed(data)

        # If we have a result...
        if parser.result_type != '':
            # Starts creating the result of the bug submition
            ret_val = parser.result_type + '|'

            # Creates the bug submition result
            new_line = "\n"
            result_data = new_line.join(parser.result)

            # When a log file is to be appended, tries uploading it
            # On error, add an entry into the bug submition result data
            if parser.result_type == 'success' and log_file != '':
                file_attach_error = attach_file(opener, parser.result[1][1:], log_file)
                
                if file_attach_error != '':
                    ret_val = ret_val + 'no_log_submitted: ' + file_attach_error + new_line

            ret_val = ret_val + result_data
            
    except urllib2.URLError, e:
        # The default error in case of unknown failure
        ret_val = 'error|An error occurred while submitting the report, please proceed through http://bugs.mysql.com/report.php'
        log_error("WB Bug Report", 'An error occurred while submitting the request: %s\n' % str(e))
        
    return ret_val
	
def login(opener, user, password):

    ret_val = 'error|Unknown error accessing the bug system'

    try:
        # Encodes the needed information for the login
        params = urllib.urlencode({'email': user,
                                   'password': password,
                                   'dest': ''})

        # Performs the actual login
        response = opener.open('https://dev.mysql.com/login/', params)

        # Reads the server response
        data = response.read()

        # Creates the parser to confirm successful login
        parser = HTMLGetData()
        parser.quit_on_done = True
        parser.add_path_node("html")
        parser.add_path_node("body")
        parser.add_path_conditioned_node("div",[('id','container')])
        parser.add_path_conditioned_node("div",[('class','page_container')])
        parser.add_path_conditioned_node("div",[('id','page')])
        parser.add_path_conditioned_node("h1",[('class','page_header'),('id','mainContent')])

        # Performs the parsing
        parser.feed(data)

        # Initializing error, to be cleaned in case of success
        # A simple error is returned on any login attemp failure, just as the web page does
        ret_val = 'error|Error accessing the bug system, please verify your email and password'
        # Sets the return value
        if len(parser.result) == 1:
            if parser.result[0] == 'Login Successful':
                ret_val = ''

    except urllib2.URLError, e:
        ret_val = 'error|Error accessing the bug system, check your network settings'
        log_error('WB Bug Report', 'Error accessing the bug system: %s\n' % str(e))

    return ret_val

def logout(opener):
    opener.open('https://dev.mysql.com/logout/')

# This function will copy the WB log file to the local directory and then
# will create a wb_log.zip containing it. The copy is needed to prevent the
# zip file to contain the whole path to the file included
def attach_file(opener, bug_number, file):

    # default error response
    ret_val = 'Unknown error attaching log file to bug report'
    
    # The file names to be used
    local_file_name = "wb.log"
    zip_file_name = 'wb_log.zip'

    # Copies the file to the local folder
    normalized_path = file.replace("\\","/")

    try:
        shutil.copyfile(normalized_path, local_file_name)

        # Creates the zip file
        zip_file = zipfile.ZipFile(zip_file_name,'w')
        zip_file.write(local_file_name, os.path.basename(local_file_name), zipfile.ZIP_DEFLATED)
        zip_file.close()

        # Reads the file as binary data
        zip_data = open(zip_file_name,'rb').read()


        # Creates the list of fields to be encoded
        fields = [  ('MAX_FILE_SIZE','512000'),
                    ('file_desc', 'Workbench Log File'),
                    ('file_private' , '1'),
                    ('file_add' , 'Add file')]

        # Creates the file to be encoded
        files = [('file',zip_file_name, zip_data)]

        # Encodes the request data
        content_type, body = encode_multipart_formdata(fields, files)


        # Creates a custom request for the file submition
        request = urllib2.Request('http://bugs.mysql.com/bug.php?id=' + bug_number + '&files=2')
        request.add_unredirected_header('Content-Type', content_type)
        request.add_unredirected_header('Content-Length', str(len(body)))

        # Performs the request
        response = opener.open(request, body)

        data = response.read();

        parser = MySQLGetRequestResult()
        parser.feed(data)

        if parser.result_type == 'success':
            ret_val = ''
        else:
            ret_val = 'Error attaching the log file to the bug report'

    except urllib2.URLError, e:
        ret_val = 'Error attaching the log file to the bug report'
        log_error('WB Bug Report', 'Error attaching the log file: %s \n' % str(e))
        
    except IOError, e:
        ret_val = 'Error getting the log file'
        log_error('WB Bug Report', 'Error getting the log file: %s\n' % str(e))
        

    return ret_val

def encode_multipart_formdata(fields, files):
    LIMIT = '----------wb_file_limit'
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        L.append('--' + LIMIT)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for (key, filename, value) in files:
        L.append('--' + LIMIT)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: %s' % get_content_type(filename))
        L.append('')
        L.append(value)
    L.append('--' + LIMIT + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % LIMIT
    return content_type, body
#   return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

@ModuleInfo.export(grt.STRING)
def test_connection():

    #Initializes the return value as no error
    ret_val = 'error|Unable to connecto through the Bug System, please proceed through http://bugs.mysql.com/report.php'

    try:
        # Creates the object to open and manage the cookies
        cookieJar = cookielib.CookieJar()
        urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))

        # Attempts to login
        response = urlOpener.open('http://bugs.mysql.com/index.php')

        # Reads the server response
        data = response.read()

        # Creates the parser to confirm successful login
        parser = HTMLGetData()
        parser.quit_on_done = True
        parser.add_path_node("html")
        parser.add_path_node("body")
        parser.add_path_conditioned_node("div",[('id','nav')])
        parser.add_path_node("ul")
        parser.add_path_conditioned_node("li",[('id','current')])
        
        parser.feed(data)

        if len(parser.result)==1:
            if parser.result[0] == 'Bugs Home':
                ret_val = 'success|'

    except BaseException, e:
        log_error("WB Bug Report", 'An error occurred while testing conectivity, %s: %s\n' % (e.__class__.__name__, str(e)))
        
    return ret_val
