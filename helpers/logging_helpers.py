'''
helper functions 
    -to quickly instantiate normalized logging froma yaml config file
    -to preconfigure a timing profiler
    -preconfigure a memory profiler
    -to normalize logging for errors and traces
    -enable normalized logging for multiprocessed applications

'''


import sys, os, traceback, cProfile, io, pstats, psutil
import logging, logging.config
import yaml


def setup_logging(config_path=None,  default_level=logging.INFO):
    '''
    configures logging from a YAML formatted config file
    '''    
    if not config_path is None and os.path.exists(config_path):
        with open(config_path, 'rt') as f:
            config = yaml.load(f.read())
        logging.config.dictConfig(config)
        f.close()
    else:
        logging.basicConfig(level=default_level)

def print_error():
    '''
    returns the type and value of the exception currently being handled
    '''
    e = sys.exc_info()
    return "Error:" + str(e[0]) +'//' + str(e[1])

def print_trace(force_console=False):
    '''
    returns the traceback of the exception currently being handled
    '''
    e = sys.exc_info()
    
    if force_console:
        return "Trace:" + str(traceback.print_tb(e[2]))
    
    return "Trace:" + str(traceback.extract_tb(e[2]))

def profile_me(func, *args, **kwargs):  
    '''
    returns a printable summary of which functions were called while processing the main function
    includes number of calls, number of recursive calls, and aggregate stats regarding time spent on each 
    '''
    
    pr = cProfile.Profile()
    pr.enable()
    func(*args, **kwargs)
    pr.disable()
    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    return s.getvalue()

def memory_usage_psutil():
    '''
    returns a printable summary of system memory usage at the time the function is called
    utilizes the system performance monitoring, not specific to your application
    '''
    process = psutil.Process(os.getpid())
    mem = process.get_memory_info()[0] / float(2 ** 20)
    return mem

############## Multi Process Logging ######################################

class LockLevel(object):
    debug=10
    info=20
    warning=30
    error=40
    critical=50

class MPlog(object):
    '''
    Logging Interface for Multipurpose applications
    Mimics the Interface of the normal logger
    '''
    
    def __init__(self, queue, name):
        self.queue=queue
        self.name=name
        
    def debug(self, message, m_name=None):
        if m_name is None: m_name=self.name 
        self.queue.put((LockLevel.debug, message, m_name))
        
    def info(self, message, m_name=None):
        if m_name is None: m_name=self.name
        self.queue.put((LockLevel.info, message, m_name))
        
    def warning(self, message, m_name=None):
        if m_name is None: m_name=self.name
        self.queue.put((LockLevel.warning, message, m_name))
        
    def error(self, message, m_name=None):
        if m_name is None: m_name=self.name
        self.queue.put((LockLevel.error, message, m_name))
        
    def critical(self, message, m_name=None):
        if m_name is None: m_name=self.name
        self.queue.put((LockLevel.critical, message, m_name))
    
    def end(self):
        self.queue.put((None, None, self.name))
        
def listener_configurer(logging_config):
    setup_logging(logging_config)
    
def listener_process(queue, logging_config):
    '''
    function that aggregates log messages from different Python processes in a multi processed application and multiplexes them 
    '''
    listener_configurer(logging_config)
    log = logging.getLogger(__name__)
    while True:
        try:
            level, msg, name = queue.get()
            if level is None: # We send this as a sentinel to tell the listener to quit.
                log.info('ending logging thread')
                break
            logger = logging.getLogger(name)
            logger.log(level, msg)
        except Exception:
            log.info(print_error())
            log.info(print_trace(False))


if __name__ == '__main__':
    pass
