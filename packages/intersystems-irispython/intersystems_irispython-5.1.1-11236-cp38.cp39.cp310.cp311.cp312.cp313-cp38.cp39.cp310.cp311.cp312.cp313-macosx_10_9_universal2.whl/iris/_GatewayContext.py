import threading
import iris

class _GatewayContext(object):

    __thread_local_connection = {}

    @classmethod
    def _clear_thread(cls):
        thread_id = threading.get_ident()
        cls.__thread_local_connection.pop(thread_id, None)

    @classmethod
    def _set_connection(cls, connection):
        thread_id = threading.get_ident()
        cls.__thread_local_connection[thread_id] = connection

    @classmethod
    def _get_connection(cls):
        thread_id = threading.get_ident()
        return cls.__thread_local_connection.get(thread_id)

    @classmethod
    def getConnection(cls):
        connection = cls._get_connection()
        if connection != None:
            connection._check_xdbc_initialization()
        return connection

    @classmethod
    def getIRIS(cls):
        return iris.IRIS(cls._get_connection())

    @classmethod
    def findClass(cls, class_name):
        return iris._Callback._Callback._execute("find-class", class_name)
