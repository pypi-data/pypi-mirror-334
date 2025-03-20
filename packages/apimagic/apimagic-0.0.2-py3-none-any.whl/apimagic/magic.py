
import os,io,sys,requests

#############################################################################
#############################################################################

admin_func = 'apimagic_admin_v02'
exec_func  = 'apimagic_exec_v04' 

suffix       = '.amazonaws.com/prod/invoke'
am_admin_url = 'https://9fwiqamsta.execute-api.us-east-1'+suffix
am_exec_url  = 'https://ivca9z4r7e.execute-api.us-east-1'+suffix 

#############################################################################
#############################################################################


def set_api_key(user_key):
    os.environ["AM_USER_KEY"] = user_key


#-----------------------------------------------------------
### ADMIN / MASTER FUNCTIONS
#-----------------------------------------------------------

def admin_request(key,request):
    main_body = {'api_key':key, 'request':request} 
    response = requests.post(am_admin_url, json=main_body) 
    J = response.json()  
    try:    return J['output']['response'] 
    except: return J


def mem_status(key=''):
    if key=='': key = os.getenv("AM_USER_KEY") 
    request = {'func_name':'memory'} 
    response = admin_request(key,request)
    return response 


def create_user(new_role='CREATOR',key=''):
    if key=='': key = os.getenv("AM_USER_KEY") 
    request = {
        'func_name':'create_user',
        'new_role' : new_role,
    }  
    response = admin_request(key,request)
    return response  


def get_info(key_or_id,key=''):
    if key=='': key = os.getenv("AM_USER_KEY") 
    request = {
        'func_name' :'get_info',
        'key_or_id' : key_or_id,
    }  
    response = admin_request(key,request)
    return response 


def deactivate_user(user_id,key=''):
    if key=='': key = os.getenv("AM_USER_KEY") 
    request = { 
        'func_name':'deactivate_user',
        'user_id'  : user_id,
    }  
    response = admin_request(key,request)
    return response  


def reactivate_user(user_id,key=''):
    if key=='': key = os.getenv("AM_USER_KEY") 
    request = { 
        'func_name':'reactivate_user',
        'user_id'  : user_id,
    }  
    response = admin_request(key,request)
    return response  


def issue_credits(user_id,credits=1000000,key=''):
    if key=='': key = os.getenv("AM_USER_KEY") 
    request = { 
        'func_name':'issue_credits',
        'user_id'  : user_id,
        'credits'  : credits,
    }  
    response = admin_request(key,request)
    return response  


def get_role(user_id,key=''):
    if key=='': key = os.getenv("AM_USER_KEY") 
    request = { 
        'func_name':'get_role',
        'user_id'  : user_id,
    }  
    response = admin_request(key,request) 
    return response  


def get_all_keys(user_id,key=''):
    if key=='': key = os.getenv("AM_USER_KEY") 
    request = { 
        'func_name':'get_all_keys',
        'user_id'  : user_id,
    }  
    response = admin_request(key,request) 
    return response  


#-----------------------------------------------------------
### CREATOR / USER FUNCTIONS
#-----------------------------------------------------------


def get_balance(user_id='',key=''):
    if key=='': key = os.getenv("AM_USER_KEY") 
    request = {'func_name':'get_balance'} 
    if user_id!='': request['user_id'] = user_id
    response = admin_request(key,request) 
    return response  


def list_apis(user_id='',key=''):
    if key=='': key = os.getenv("AM_USER_KEY") 
    request = {'func_name':'list_apis'} 
    if user_id!='': request['user_id'] = user_id 
    response = admin_request(key,request) 
    return response  


def deploy_api(code='',info={},key=''):
    if key=='': key = os.getenv("AM_USER_KEY") 
    request = {'func_name':'deploy_api'} 
    if len(code)>0: request['code'] = code
    if len(info)>0: request['info'] = info
    response = admin_request(key,request) 
    return response  

def update_api(api_id,code='',info={},key=''):
    if key=='': key = os.getenv("AM_USER_KEY") 
    request = {'func_name':'update_api','api_id':api_id} 
    if len(code)>0: request['code'] = code
    if len(info)>0: request['info'] = info
    response = admin_request(key,request) 
    return response  


def get_api_info(api_id,key=''):
    if key=='': key = os.getenv("AM_USER_KEY") 
    request = {'func_name':'get_api_info','api_id':api_id}   
    response = admin_request(key,request) 
    return response  


def get_user_info(user_id='',key=''):
    if key=='': key = os.getenv("AM_USER_KEY") 
    request = {'func_name':'get_user_info'} 
    if user_id!='': request[user_id] = user_id
    response = admin_request(key,request) 
    return response  


def update_user_info(new_info,user_id='',key=''):
    if key=='': key = os.getenv("AM_USER_KEY") 
    request = {'func_name':'update_user_info','user_info':new_info}  
    if user_id!='': request['user_id'] = user_id
    response = admin_request(key,request) 
    return response  


def gen_key(role='',user_id='',key=''):
    if key=='': key = os.getenv("AM_USER_KEY") 
    request = {'func_name':'gen_key'}   
    if role != '':  request['role']    = role
    if user_id!='': request['user_id'] = user_id
    response = admin_request(key,request) 
    return response  


def del_key(key_to_delete,key=''):
    if key=='': key = os.getenv("AM_USER_KEY") 
    request = {'func_name':'del_key'}   
    request['key_to_delete'] = key_to_delete 
    response = admin_request(key,request) 
    return response  


#-----------------------------------------------------------
### EXECUTION / TESTING FUNCTIONS
#-----------------------------------------------------------


def test_run(code,fname,input_obj={},key='',full=False):
    if key=='': key = os.getenv("AM_USER_KEY") 
    main_body = { 
        'api_key' : key,  
        'code'    : code,
        'fname'   : fname,
        'input'   : input_obj, 
    } 
    res = requests.post(am_exec_url,json=main_body).json()
    if full: return res 
    try:     return res['output']['result'] 
    except:  return res 


def call_api(api_id,fname,input_obj={},key='',full=False):
    if key=='': key = os.getenv("AM_USER_KEY") 
    main_body = { 
        'api_key' : key,  
        'api_id'  : api_id,
        'fname'   : fname,
        'encoded' : 1, 
        'zipped'  : 0,
        'input'   : input_obj, 
    } 
    res = requests.post(am_exec_url,json=main_body).json()
    if full: return res 
    try:     return res['output']['result'] 
    except:  return res 


#############################################################################
#############################################################################

SUPPORTED = [    
    'abc', 'aifc', 'argparse', 'array', 'ast', 'asyncio', 'atexit', 'audioop', 'awslambdaric', 'base64', 
    'bdb', 'binascii', 'bisect', 'bootstrap', 'boto3', 'botocore', 'bson', 'builtins', 'bz2', 'cProfile', 
    'calendar', 'certifi', 'cgi', 'cgitb', 'charset_normalizer', 'chunk', 'cmath', 'cmd', 'code', 'codecs', 
    'codeop', 'collections', 'colorsys', 'compileall', 'concurrent', 'configparser', 'contextlib', 
    'contextvars', 'copy', 'copyreg', 'crypt', 'csv', 'ctypes', 'curses', 'dataclasses', 'datetime', 
    'dateutil', 'dbm', 'decimal', 'difflib', 'dill', 'dis', 'doctest', 'email', 'encodings', 'ensurepip', 
    'enum', 'errno', 'faulthandler', 'fcntl', 'filecmp', 'fileinput', 'fnmatch', 'fractions', 'ftplib', 
    'functools', 'gc', 'genericpath', 'getopt', 'getpass', 'gettext', 'glob', 'graphlib', 'gridfs', 'grp', 
    'gzip', 'hashlib', 'heapq', 'hmac', 'html', 'http', 'idlelib', 'idna', 'imaplib', 'imghdr', 'importlib', 
    'inspect', 'io', 'ipaddress', 'itertools', 'jmespath', 'json', 'keyword', 'lib2to3', 'linecache', 'locale', 
    'logging', 'lzma', 'mailbox', 'mailcap', 'marshal', 'math', 'mimetypes', 'mmap', 'modulefinder', 
    'multiprocessing', 'netrc', 'nntplib', 'ntpath', 'nturl2path', 'numbers', 'numpy', 'opcode', 'operator', 
    'optparse', 'os', 'ossaudiodev', 'pandas', 'pathlib', 'pdb', 'pickle', 'pickletools', 'pip', 'pipes', 
    'pkgutil', 'platform', 'plistlib', 'poplib', 'posix', 'posixpath', 'pprint', 'profile', 'pstats', 
    'psycopg2', 'pty', 'pwd', 'py_compile', 'pyclbr', 'pydoc', 'pydoc_data', 'pyexpat', 'pymongo', 'pymysql', 
    'pytz', 'queue', 'quopri', 'random', 're', 'readline', 'redis', 'reprlib', 'requests', 'resource', 
    'rlcompleter', 'runpy', 'runtime_client', 's3transfer', 'sched', 'secrets', 'select', 'selectors', 
    'shelve', 'shlex', 'shutil', 'signal', 'simplejson', 'site', 'six', 'smtplib', 'snapshot_restore_py', 
    'sndhdr', 'socket', 'socketserver', 'spwd', 'sqlalchemy', 'sqlite3', 'sre_compile', 'sre_constants', 
    'sre_parse', 'ssl', 'stat', 'statistics', 'string', 'stringprep', 'struct', 'subprocess', 'sunau', 
    'symtable', 'sys', 'sysconfig', 'syslog', 'tabnanny', 'tarfile', 'telnetlib', 'tempfile', 'termios', 
    'test', 'textwrap', 'threading', 'time', 'timeit', 'token', 'tokenize', 'tomllib', 'trace', 'traceback', 
    'tracemalloc', 'tty', 'types', 'typing', 'typing_extensions', 'tzdata', 'unicodedata', 'unittest', 'urllib', 
    'urllib3', 'uu', 'uuid', 'venv', 'warnings', 'wave', 'weakref', 'webbrowser', 'wsgiref', 'xdrlib', 'xml', 
    'xmlrpc', 'xxlimited', 'xxlimited_35', 'xxsubtype', 'zipapp', 'zipfile', 'zipimport', 'zlib'
]


def supported():
    return SUPPORTED


#############################################################################
#############################################################################


WELCOME = """

WELCOME

Welcome, friends, to API Magic - your new favorite tool!
API Magic is the fastest way to deploy serverless APIs to the Cloud.
Here we will show you the basics of how API Magic works.

---

HOW TO SIGN-UP

To sign-up for your FREE API key and your FREE credits, connect with 
the creator, James Rolfsen on LinkedIn and request access. Depending 
on the volume of interest, there may be a waitlist applied to ensure
safe and scaleable distribution of this tool. 

Connect with James here:
https://www.linkedin.com/in/jamesrolfsen/

---

DISCLAIMER

This product and this Python Library are currently in a Prototype
phase of development. This means that the current configuration and 
settings of the underlying system and this library are under active 
development and may be changed. We expect that when we announce a 
public beta, the core configurations will be stable and fixed.
This product is owned by Think.dev LLC, a consulting company.

---

(1) SHORT EXAMPLE: The 3-Line API Deployment

You can deploy your first API in 3 lines of code:
```
from apimagic import *
code = "def times2(n): return n*2" 
api_info = deploy_api(code,key=YOUR_API_KEY) 
```

In this example, we are defining a new API that contains just one
simple function, "times2()". After defining your API, you can call 
your new API with 3 lines of code from any other Python environment.

```
from apimagic import *
api_id,fname,input_obj = api_info['api_id'], 'times2', 3
output = call_api(api_id,fname,input_obj,key=YOUR_API_KEY) 
```

In this example, we are calling the "times2()" function with 
the input value of 3, resulting in an output of 6.

The purpose of this demo is to show how simple API creation can be. 
As a philosopy, we believe that "simple things SHOULD be simple" and 
that "difficult things should be possible", all in one framework.

---

(2) LONG EXAMPLE: 

We will create an API that aggregates data about a given US ZipCode, by 
calling 4 seperate APIs and then organizing that data in a single response.
In this example, the "get_zip_info()" function will be the one we call.

We deploy the API as such: 

```
### Here we are importing the API Magic library: 
from apimagic import *

### Here we define the code of our API:
code = '''

# Notice we are importing the required modules here:
import requests,json

def zipcode_location(zipcode):
    r = requests.get("http://api.zippopotam.us/us/"+str(zipcode)) 
    loc1 = r.json()["places"][0] 
    loc2 = dict() 
    loc2['place'] = loc1['place name'] 
    loc2['state'] = loc1['state']
    loc2['lat'] = float(loc1['latitude']) 
    loc2['lon'] = float(loc1['longitude']) 
    return loc2

def location_elevation(loc):
    loc_str = str(loc['lat'])+','+str(loc['lon']) 
    params = {"locations": loc_str} 
    r = requests.get("https://api.open-elevation.com/api/v1/lookup", params=params)
    results = dict() 
    results['elevation_meters'] = int(float(r.json()['results'][0]['elevation'])) 
    results['elevation_feet']   = int(results['elevation_meters']*3.28084) 
    return results 
    
def location_weather(loc):
    loc_str = str(loc['lat'])+','+str(loc['lon'])  
    r = requests.get("https://wttr.in/"+loc_str+"?format=%C+%t") 
    return str(r.text).replace('\u00b0C',' C.').replace('\u00b0F',' F.') 

def location_sunlight(loc):
    lat, lon = loc['lat'], loc['lon'] 
    params = {"lat": lat, "lng": lon, "formatted": 1}
    r = requests.get("https://api.sunrise-sunset.org/json", params=params) 
    sun1 = r.json()['results'] 
    sun2 = {'time_zone':'GMT'}  
    for var in ['sunrise','sunset','solar_noon','day_length']:
        sun2[var] = sun1[var]+' GMT' 
    return sun2 

def get_zip_info(zipcode):
    zip_info = {'target_zipcode':str(zipcode)}  
    try:
        loc = zipcode_location(zipcode)
        zip_info['location'] = loc
    except:
        zip_info['location'] = 'Zipcode not found.'
    try: 
        elevation = location_elevation(loc) 
        zip_info['elevation'] = elevation
    except:
        zip_info['elevation'] = "Elevation data not found."
    try: 
        weather = location_weather(loc) 
        zip_info['weather'] = weather
    except:
        zip_info['weather'] = "Weather data not found." 
    try: 
        sunlight = location_sunlight(loc) 
        zip_info['sunlight'] = sunlight
    except:
        zip_info['sunlight'] = "Sunlight data not found." 
    return zip_info 

### EXAMPLE LOCAL USAGE: 
#res = get_zip_info(78712) 
#print(json.dumps(res, indent=4)) 
'''

# Now deploy the code as an endpoint: 
api_info = deploy_api(code,key=YOUR_API_KEY) 
```

Fantastic!! Now we can call this API as such:

```
from apimagic import *
api_id,fname,input_obj = api_info['api_id'], 'get_zip_info', 78749
output = call_api(api_id,fname,input_obj,key=YOUR_API_KEY) 
print(json.dumps(output, indent=4)) 
```

The code above will render a response similar to: 
```
{
    "target_zipcode": "78749",
    "location": {
        "place": "Austin",
        "state": "Texas",
        "lat": 30.2166,
        "lon": -97.8508
    },
    "elevation": {
        "elevation_meters": 234,
        "elevation_feet": 767
    },
    "weather": "Sunny +74 F.",
    "sunlight": {
        "time_zone": "GMT",
        "sunrise": "12:38:05 PM GMT",
        "sunset": "12:41:39 AM GMT",
        "solar_noon": "6:39:52 PM GMT",
        "day_length": "12:03:34 GMT"
    }
}
```

---

(3) Supported Libraries

We currently support more than 200 library modules!! 
To review a list of supported python libraries that 
may be used in an API Magic API, please run this:

```
from apimagic import *
supported()
```

This returns a list of strings as such:

```
['abc', 'aifc', 'argparse', '...','zipfile', 'zipimport', 'zlib']
```

---

CONCLUSION

We are excited to see what you build with API Magic! 
To submit feedback or to flag bugs, 
please email:  info@think.dev

Happy Building!!

"""


def welcome(): 
    print(WELCOME) 


#############################################################################
#############################################################################


