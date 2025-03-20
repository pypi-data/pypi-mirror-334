# -*- coding: utf-8 -*-
"""
Unpublished work.
Copyright (c) 2025 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: aanchal.kavedia@teradata.com
Secondary Owner: PankajVinod.Purandare@teradata.com

teradatagenai.garbage_collector.garbage_collector
----------
A class for garbage collection.
Cleaning up session id for Vector Stores.
"""

class GarbageCollector:
    session_info = []
    open_files = []

    @staticmethod
    def add_session_id(session_info):
        """
        DESCRIPTION:
            Adds a session information tuple to the session_info list.

        PARAMETERS:
            session_info:
                Required Argument.
                A tuple containing session_id and header information.
                Types: tuple

        RETURNS:
            None

        RAISES:
            None

        EXAMPLES:
            GarbageCollector.add_session_id(('session1', 'header1'))
        """
        GarbageCollector.session_info.append(session_info)

    @staticmethod
    def remove_session_id(session_id):
        """
        DESCRIPTION:
            Removes a session information tuple from the session_info list based on the session_id.

        PARAMETERS:
            session_info:
                Required Argument.
                Specifies a tuple containing session_id.
                Types: str

        RETURNS:
            None

        RAISES:
            None

        EXAMPLES:
            GarbageCollector.remove_session_id('session1')
        """
        GarbageCollector.session_info[:] = [x for x in GarbageCollector.session_info if x[0] != session_id]

    @staticmethod
    def add_open_file(file_handle):
        """
        DESCRIPTION:
            Adds a file handle to the open_files list.

        PARAMETERS:
            file_handle:
                Required Argument.
                Specifies the file_handle.
                Types: file object

        RETURNS:
            None

        RAISES:
            None

        EXAMPLES:
            file = open('example.txt', 'r')
            GarbageCollector.add_open_file(file)
        """
        GarbageCollector.open_files.append(file_handle)

    @staticmethod
    def cleanup_temp_variables():
        """
        DESCRIPTION:
            Performs garbage collection to clean up temporary variables.

        PARAMETERS:
            None

        RETURNS:
            None

        RAISES:
            None

        EXAMPLES:
            GarbageCollector.cleanup_temp_variables()
        """
        import gc
        gc.collect()

    @staticmethod
    def cleanup_sessions():
        """
        DESCRIPTION:
            Disconnects all sessions stored in the session_info list.

        PARAMETERS:
            None

        RETURNS:
            None

        RAISES:
            None

        EXAMPLES:
            GarbageCollector.cleanup_sessions()
        """
        from teradatagenai.vector_store.vector_store import VSManager
        if GarbageCollector.session_info:
            VSManager.disconnect()


    @staticmethod
    def cleanup_files():
        """
        DESCRIPTION:
            Closes all open file handles and clears the open_files list.

        PARAMETERS:
            None

        RETURNS:
            None

        RAISES:
            None

        EXAMPLES:
            GarbageCollector.cleanup_files()
        """
        for file_handle in GarbageCollector.open_files:
            try:
                file_handle.close()
            except Exception as e:
                print(f"Failed to close file handle: {e}")
        GarbageCollector.open_files = []

# Register the cleanup methods to be called at exit
import atexit
atexit.register(GarbageCollector.cleanup_sessions)
atexit.register(GarbageCollector.cleanup_files)
