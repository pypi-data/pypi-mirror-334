import datetime , string , subprocess , psutil ,secrets , os ,ping3 , time , sys , argparse , ctypes , math , threading , random , jwt , socket


def getRandomKey(n=10,numbers=True) :
    if numbers :
        return ''.join(secrets.choice(string.digits)
            for i in range(n))
    else :
        return ''.join(secrets.choice(string.ascii_lowercase )
            for i in range(n))


def now() :
    return datetime.datetime.now()

def date_time_now() :
    return  str( now().replace(microsecond=0))


def timenow() : 
    return  str(now().strftime("%d/%m/%Y %H:%M:%S"))
    

def timenowForLabels() : 
    return now().strftime("%d-%m-%Y_%H-%M-%S")

def fixTupleForSql(list):
    if len(list) <= 1 :
        execlude = str(list).replace('[' , '(' ).replace(']' , ')')
    else :
        execlude = tuple(list)
        
    return execlude

def getDateTimeAfterFewSeconds(seconds=10):
    import datetime
    # Get the current time
    current_time = datetime.datetime.now()
    # Add the specified number of seconds
    new_time = current_time + datetime.timedelta(seconds=seconds)
    # Format the new time as a string
    return new_time.strftime('%Y-%m-%d %H:%M')


def isOsPortFree(port : str):
    for conn in psutil.net_connections():
        if str(conn.laddr.port) == port :
            return False
    return True

def getRandomKeysAndStr(n=5, upper=False):
    s = ''.join(random.choices(string.ascii_letters + string.digits, k=n))
    if upper :
        return s.upper()
    return s

def generateToken(iter=5,split=False) :
    if not split :
        return ''.join( [ getRandomKeysAndStr(n=5) for x in range( iter )] )
    return '-'.join( [ getRandomKeysAndStr(n=5) for x in range( iter )] )


def pingAddress( address ) : 
    try :
        trustedAddresses = ['127.0.0.1' , 'localhost']
        if address in trustedAddresses :
            return True
        response  = ping3.ping(f'{address}')
        if not response :
            return False
        else :
            return True
    except Exception : 
        return False

def getScriptDir(f= __file__):
    '''
    THis functions aims to return the script dir even if app is bundeled with py installer.
    '''
    if getattr(sys, 'frozen', False): 
        # The script is run from a bundled exe via PyInstaller
        path = sys._MEIPASS 
    else:
        # The script is run as a standard script
        path = os.path.dirname(os.path.abspath(f))
    return path

def getScriptDirInMachine(f= __file__):
    '''
    THis functions aims to return the script dir.
    '''
    return os.path.dirname(os.path.abspath(f))



def is_packed():
    # Check if the script is running from an executable produced by PyInstaller
    if getattr(sys, 'frozen', False):
        return True
    # Check if the 'bundle' directory exists
    elif hasattr(sys, '_MEIPASS') and os.path.exists(os.path.join(sys._MEIPASS, 'bundle')):
        return True
    else:
        return False

def get_executable_path(file=__file__) :
    if is_packed():
        return os.path.dirname(os.path.realpath(sys.argv[0]))
    return os.path.dirname(os.path.realpath(file))

def isArgsEmpty(args) :
    if True in args.__dict__.values() :
        return False
    else :
        return True
    
def convert_bytes_to_mb(bytes_size,rounded=True):
    """Convert bytes to megabytes (MB)."""
    if rounded :
        # print(f'''
        # {bytes_size} =>>> {round(float(bytes_size))}
        # ''')
        return round(float(bytes_size / (1024 * 1024)))
    return bytes_size / (1024 * 1024)

def convert_bytes_to_kb(bytes_size,rounded=True):
    """Convert bytes to kilobytes (KB)."""
    if rounded :
        return round(float(bytes_size / 1024))
    return bytes_size / 1024

def convert_mb_to_bytes(mb_size):
    return mb_size * 1024 * 1024

def getTimestamp(after_seconds=None, epoch=False) :
    '''
    get timestamp now or after few seconds.
    after_seconds is int.
    '''
    if not after_seconds :
        if epoch :
            return int(time.time()) * 1000
        return int(time.time())
    if epoch :
        return (int(time.time())  + int(after_seconds) ) * 1000  
    return int(time.time()) + int(after_seconds)

def kill_thread(thread):
    """
    thread: a threading.Thread object
    """
    thread_id = thread.ident
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
    if res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
        
def start_thread(target, args=(), kwargs=None, daemon=True):
    if kwargs is None:
        kwargs = {}
    th = threading.Thread(target=target, args=args, kwargs=kwargs)
    th.daemon = daemon
    th.start()
    return th
    
def pagination(data , iter=25 , base_url=None) :
    total_pages = math.ceil(len(data) / iter)
    paginated_data = {}
    token=generateToken()
    if not base_url :
        base_url=f'/pagination/{token}'
    for page_number in range(1, total_pages + 1):
        start_index = (page_number - 1) * iter
        end_index = min(start_index + iter, len(data))
        paginated_data[page_number] = {
            'url' : f"{base_url}/{page_number}" ,
            'data' : data[start_index:end_index] ,
            'page' : page_number
        }
    return base_url , paginated_data , len(paginated_data)

def lget(list , index , default=None) :
    '''
    this is same as what we have in dict.get , get the index of exists, else will return a default value.'''
    try :
        return list[index]
    except :
        return default

def mkdirs(path) :
    if not os.path.exists(path) :
        os.makedirs(path)

def releasify(release : float ) -> tuple :
    return (int(release), int(str(release).split(".")[1]))

def convertTimestampToDate(timestamp, return_date_time_object=False) :
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    if return_date_time_object :
        return dt_object
    return dt_object.strftime("%Y-%m-%d %H:%M:%S")

def generateJwtToken() :
    return jwt.encode({'timestamp' : getTimestamp() , 'r' : getRandomKey() }, getRandomKey(), algorithm="HS256")

def getMachineUuid() :
    if 'win' in sys.platform :
        cli = fr'reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v ProductID'
        return str(subprocess.getoutput(cli).splitlines()[2].split(' ')[-1].replace('\n',''))
    elif 'linux' in str(sys.platform) :
        return str(subprocess.getoutput('cat /sys/class/dmi/id/product_uuid').replace('\n' , ''))
    else :
        return ''

def getMachineAddresses() :
    ip_addresses = socket.gethostbyname_ex(socket.gethostname())[2]
    return ip_addresses

if __name__ == "__main__":
    pass
