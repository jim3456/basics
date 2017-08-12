'''
postgres_manger.py
========================
wraps psycopg2 for so that error handling is quicker
adds utility for quickly inserting or updating directly from data stuctures

postgres_manger - Module Contents
+++++++++++++++++++++++++++++++
'''

import logging, string
import psycopg2, psycopg2.extras
from logging_helpers import print_error, print_trace

log=logging.getLogger(__name__)


class DB_CONN(object):
    '''
    Manages Connections and Queries to and from the Database
    Assumes passwords are kept in the .pgpass configuration
    '''
    def __init__(self,host,port, user,dbname, timeout=10, charset='utf8', autocommit=False):        
        
        self.uncommitted=0
        self.autocommit=autocommit
        
        try:
            self.conn=psycopg2.connect(host=host, port=port,user=user,dbname=dbname)
        except:
            log.error(print_error())
            log.error(print_trace()) 
            self.conn=None
         
    def close(self):
        self.conn.close()
        return (self.conn.closed)
    
    def check(self):
        if self.conn is None:
            log.error('tried to query an invalid connection (connectino failed on intialization')
            return False
    
        return True
    
    def commit(self):
        self.conn.commit()
        self.uncommitted=0
        
    def rollback(self):
        self.conn.rollback()
        self.uncommitted=0
            
    def direct_query(self, direct_sql_string, params=None, commit=False):
        '''
        sends a SQL instruction to the database
        errors are automatically rolled back, handled, and logged
        params are sanitized
        
        if commit is true, the UPDATE, INSERT, or DELETE query will be immediately commited
        if commit is set to false, the user must take an extra step to commit the connection for UPDATE,  INSERT or DELETE queries
        
        '''
        if not self.check():
            return None
        
        cur=self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql=direct_sql_string
        
        try:
            if params is None:
                cur.execute(direct_sql_string)
            else:
                cur.execute(direct_sql_string, params)
            if commit:
                self.conn.commit()
                return(cur.fetchall())
            else:
                self.uncommitted+=1
                return(cur.rowcount)
            
        except:
            self.rollback()
            log.error('error with command {}'.format(sql))
            log.error('error with params {}'.format(params))
            log.error(print_error())
            log.error(print_trace())

print("test")