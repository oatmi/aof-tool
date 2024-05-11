from rdbtools.parser import RdbCallback
from rdbtools import encodehelpers


class AOFCallback(RdbCallback):
    """
    A Callback to handle events as the Redis AOF file is parsed.
    This callback process specific type of commands.
    """

    def __init__(self):
        super(AOFCallback, self).__init__(encodehelpers.STRING_ESCAPE_UTF8)

    def start_rdb(self):
        """
        Called once we know we are dealing with a valid redis dump file
        """
        pass

    def start_database(self, db_number):
        """
        Called to indicate database the start of database `db_number`.
        Once a database starts, another database cannot start unless the first
        one completes and then `end_database` method is called. Typically,
        callbacks store the current database number in a class variable
        """
        pass

    def set(self, key, value, expiry, info):
        """
        Callback to handle a key with a string value and an optional expiry
        `key` is the redis key
        `value` is a string or a number
        `expiry` is a datetime object. None and can be None
        `info` is a dictionary containing additional information about object.
        """
        pass

    def end_database(self, db_number):
        """
        Called when the current database ends
        After `end_database`, one of the methods are called:
        1) `start_database` with a new database number
            OR
        2) `end_rdb` to indicate we have reached the end of the file
        """
        pass

    def end_rdb(self):
        """Called to indicate we have completed parsing of the dump file"""
        pass
