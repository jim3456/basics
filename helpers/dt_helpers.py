'''
datetime_utilities.py
========================

Basic functions to make dealing with Dates and Times easier

datetime_utilities - Module Contents
+++++++++++++++++++++++++++++++
'''

import pytz

class tzAlias(object):
    '''
    Enum like objec to organize pytz time zones. They are called based on strings, so this will make it easiere in the IDE
    '''
    eastern=pytz.timezone('US/Eastern')
    central=pytz.timezone('US/Central')
    pacific=pytz.timezone('US/Pacific')
    london=pytz.timezone('Europe/London')
    paris=pytz.timezone('Europe/Paris')
    utc=pytz.UTC

def isAware(dtObject):
    '''
    determines if a datetime.datetime  or datetime.time object is aware or naive
    '''
    if hasattr(dtObject,'tzinfo') and not dtObject.tzinfo is None and not dtObject.tzinfo.utcoffset(dtObject) is None:
        return(True)
    
    return(False)

def modify_time_zone(dtObject,time_zone=pytz.UTC, old_time_zone=None):
    '''
    adjusts the time zone on a date time objects.
    accepts both aware and unaware objects
    For unaware objects it uses the time as 'tacks on' the time zone
    For aware objects it translates the time from the old to the new
    '''
    
    if time_zone is None:
        return dtObject
    
    if isAware(dtObject):
        output=time_zone.normalize(dtObject)
    else:
        if old_time_zone is None:
            output=time_zone.localize(dtObject)
        else:
            output=time_zone.normalize(old_time_zone.localize(dtObject))
        
    return(output)

