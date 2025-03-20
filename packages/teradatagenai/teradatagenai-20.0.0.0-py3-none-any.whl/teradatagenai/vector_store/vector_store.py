"""
Unpublished work.
Copyright (c) 2025 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: aanchal.kavedia@teradata.com
Secondary Owner: akhil.bisht@teradata.com

This file implements VectorStore class along with its method.
"""
import base64
import json, os, pandas as pd, time
from json.decoder import JSONDecodeError
from teradataml.common.constants import HTTPRequest
from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes
from teradataml.common.utils import UtilFuncs
from teradataml.context.context import _get_user
from teradataml import DataFrame
from teradataml.options.configure import configure
from teradataml.utils.validators import _Validators
from teradataml.scriptmgmt.UserEnv import _get_auth_token
from teradataml.utils.internal_buffer import _InternalBuffer
from teradatagenai.garbage_collector.garbage_collector import GarbageCollector

from teradatagenai.common.constants import Action as action_enum,\
    Permission as permission_enum, VectorStoreURLs, _Grant, _Revoke, Operation, UpdateStyle

# Getting VectorStoreURLs.
vector_store_urls = VectorStoreURLs()
class _ConnectionManager:
    """
    A class to update and get connection parameters for the vector
    store in Teradata Vantage.
    """
    @staticmethod
    def set_params(host, username, password, database):
        """
        DESCRIPTION:
            Sets the connection parameters for vector store in the internal buffer.

        PARAMETERS:
            host:
                Required Argument.
                Specifies the fully qualified domain name or IP address of the
                Teradata System to connect to.
                Types: str

            username:
                Required Argument.
                Specifies the username for connecting to/create a vector
                store in Teradata Vantage.
                Types: str

            password:
                Required Argument.
                Specifies the password required for the username.
                Types: str

            database:
                Required Argument.
                Specifies the initial database to use after logon,
                instead of the user's default database.
                Types: str

        RAISES:
            None

        RETURNS:
            None

        EXAMPLES:
            _ConnectionManager.set_params(host='<host>',
                                          username='<username'>,
                                          password='<password>',
                                          database='<database>')
        """
        vs_params = {"vs_host": host,
                     "vs_username": username,
                     "vs_password": password,
                     "vs_database": database}
        _InternalBuffer.add(vs_params=vs_params)

    @staticmethod
    def get_params():
        """
        DESCRIPTION:
            Get the connection parameters.

        RETURNS:
            dict: containing connection parameters.

        RAISES:
            RuntimeError: If connection parameters are not set.

        EXAMPLES:
            _ConnectionManager.get_params()

        """
        # Check if vs_params is set or not in the Internal buffer.
        _Validators._check_required_params(arg_value=_InternalBuffer.get("vs_params"),
                                           arg_name="Connection parameters",
                                           caller_func_name="get_params",
                                           target_func_name="VSManager._connect")
                                                                                  
        return _InternalBuffer.get("vs_params")

class VSManager:
    """
    Vector store manager allows user to:
        * Perform health check for the vector store service.
        * List all the vector stores.
        * List all the active sessions of the vector store service.
        * Disconnect from the database session.
    """
    @staticmethod
    def _connect(**kwargs):
        """
        DESCRIPTION:
            Establishes connection to Teradata Vantage.

        PARAMETERS:
             host:
                Optional Argument.
                Specifies the fully qualified domain name or IP address of the
                Teradata System to connect to.
                Types: str

            username:
                Optional Argument.
                Specifies the username for connecting to/create a vector
                store in Teradata Vantage.
                Types: str

            password:
                Optional Argument.
                Specifies the password required for the username.
                Types: str

            database:
                Optional Argument.
                Specifies the initial database to use after logon,
                instead of the user's default database.
                Types: str

        RETURNS:
            None

        RAISES:
            TeradataMlException

        EXAMPLES:
            from teradatagenai import VSManager
            # Example 1: Connect to the database using host, database,
            #            username and password.
            >>> VSManager._connect(host='<host>',
                                   username='<user>',
                                   password='<password>',
                                   database='<database>')
        """

        ## Initialize connection parameters.
        host = kwargs.get("host", None)
        user = kwargs.get("username", None)
        password = kwargs.get("password", None)
        database = kwargs.get("database", _get_user())
        # ssl_verify is always True for CCP enabled tenant.
        ssl_verify = True

        # get the auth_token
        headers = _get_auth_token()

        # Validations
        arg_info_matrix = []
        arg_info_matrix.append(["host", host, True, (str), True])
        arg_info_matrix.append(["username", user, True, (str), True])
        arg_info_matrix.append(["password", password, True, (str), True])
        arg_info_matrix.append(["database", database, True, (str), True])
        
        # Check if vector_store_base_url is set or not.
        _Validators._check_required_params(arg_value=configure._vector_store_base_url,
                                           arg_name="Auth token",
                                           caller_func_name="VectorStore()",
                                           target_func_name="set_auth_token")

        # Validate argument types.
        _Validators._validate_function_arguments(arg_info_matrix)

        # Form the header with username and password if it is not ccp enabled tenant.
        if not configure._ccp_enabled:
            # If the host and user are passed, we will set the new connection params.
            # For non CCP enabled tenants, we don't have SSL certificate,
            # hence should set it to False.                                               
            ssl_verify = False
            if user and password:
                _ConnectionManager.set_params(host, user, password, database)
            else:
                # We will get the connection params already stored.
                params = _ConnectionManager.get_params()
                host = params.get("vs_host")
                user = params.get("vs_username")
                password = params.get("vs_password")
                database = params.get("vs_database")

            credentials = f"{user}:{password}"
            # Encode the credentials string using Base64
            encoded_credentials = base64.b64encode(
                credentials.encode('utf-8')).decode('utf-8')
            # Form the Authorization header value
            headers = {"Authorization": f"Basic {encoded_credentials}"}

        # Triggering the 'connect' API
        data = {
            'database_name': database,
            'hostname': host
        }
        # Only add arguments which are not None as
        # service accepts only non None arguments.                                                                                                        
        data = {k: v for k, v in data.items() if v is not None}

        http_params = {
            "url": vector_store_urls.session_url,
            "method_type": HTTPRequest.POST,
            "headers": headers,
            "json": data,
            "verify": ssl_verify
        }

        response = UtilFuncs._http_request(**http_params)

        session_id = response.cookies.get("session_id")
        # Only add the session id if it is not None,
        # meaning when connect went through.
        if session_id:
            _InternalBuffer.add(vs_session_id=session_id)
            _InternalBuffer.add(vs_header=headers)

            GarbageCollector.add_session_id((session_id, headers))
        VectorStore._process_vs_response(api_name="connect", response=response)

    @staticmethod
    def _generate_session_id(**kwargs):
        """
        DESCRIPTION:
            Internal function to generate or get the session_id.

        PARAMETERS:
            None

        RETURNS:
            dict containing the headers and the session_id.

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> VSManager._generate_session_id()
        """
        # If the buffer is empty, meaning its the first call to
        # _connect, call _connect to generate the session id.
        if _InternalBuffer.get("vs_session_id") is None:
            VSManager._connect()

        return {"vs_session_id": _InternalBuffer.get("vs_session_id"),
                "vs_header": _InternalBuffer.get("vs_header")}

    @staticmethod
    def list():
        """
        DESCRIPTION:
            Lists all the vector stores.
            Notes:
                * Lists all vector stores if user has admin role permissions.
                * Lists vector stores permitted to the user.

        RETURNS:
            Pandas DataFrame containing the vector store details.

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> from teradatagenai import VSManager

            # List all the vector stores.
            >>> VSManager.list()
        """
        # Triggering the 'list_vector_stores' API
        list_vs_url = vector_store_urls.vectorstore_url
        session_header = VSManager._generate_session_id()
        response = UtilFuncs._http_request(list_vs_url, HTTPRequest.GET,
                                           cookies={'session_id': session_header["vs_session_id"]},
                                           headers=session_header["vs_header"]
                                           )
        # Process the response and return the dataframe.
        data = VectorStore._process_vs_response("list_vector_stores", response)
        return pd.DataFrame(data['vector_stores_list'])

    @staticmethod
    def health():
        """
        DESCRIPTION:
            Performs sanity check for the service.

        RETURNS:
            Pandas DataFrame containing details on the health of the service.

        RAISES:
            TeradataMlException

        EXAMPLES:
            # Example 1: Check the health of the service.
            >>> VSManager.health()
        """
        health_url = f'{vector_store_urls.base_url}health'
        session_header = VSManager._generate_session_id()
        response = UtilFuncs._http_request(health_url, HTTPRequest.GET,
                                           headers=session_header["vs_header"])
        return pd.DataFrame([VectorStore._process_vs_response("health", response)])

    @staticmethod
    def list_sessions():
        """
        DESCRIPTION:
            Lists all the active sessions of the vector store service.
            Notes:
                * Only admin users can use this method.
                * Refer to the 'Prerequisites' section under
                  'Vector Store Admin Workflow' in the
                  User guide for details.
        RETURNS:
            Pandas DataFrame containing the active sessions.

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> from teradatagenai import VSManager

            # List all the vector stores.
            >>> VSManager.list_sessions()
        """
        session_header = VSManager._generate_session_id()
        response = UtilFuncs._http_request(f"{vector_store_urls.session_url}s",
                                           HTTPRequest.GET,
                                           cookies={'session_id': session_header["vs_session_id"]},
                                           headers=session_header["vs_header"]
                                           )
        result = _ListSessions(VectorStore._process_vs_response("list_sessions", response))
        return result

    @staticmethod
    def list_patterns():
        """
        DESCRIPTION:
            Lists all the patterns in the vector store.
            Notes:
                * Only admin users can use this method.
                * Refer to the 'Prerequisites' section under
                  'Vector Store Admin Workflow' in the
                  User guide for details.

        RETURNS:
            Pandas DataFrame containing the patterns.

        RAISES:
            TeradataMlException

        EXAMPLES:
            from teradataml import VSManager

            # List all the patterns.
            VSManager.list_patterns()
        """
        session_header = VSManager._generate_session_id()
        response = UtilFuncs._http_request(vector_store_urls.patterns_url,
                                           HTTPRequest.GET,
                                           cookies={'session_id': session_header["vs_session_id"]},
                                           headers=session_header["vs_header"]
                                           )
        data = VectorStore._process_vs_response("list_patterns", response)
        return pd.DataFrame(data['pattern_list'])

    @staticmethod
    def disconnect(session_id=None):
        """
        DESCRIPTION:
            Databse session created for vector store operation is disconnected
            and corresponding underlying objects are deleted.
            Notes:
                * When 'session_id' argument is passed, only that session is
                  disconnected, else all session IDs created during the
                  current Python session are disconnected.
                * Only admin users can disconnect session
                  created by other users.
                * Refer to the 'Prerequisites' section under
                  'Vector Store Admin Workflow' in the
                  User guide for details.

        PARAMETERS:
            session_id:
                Optional Argument.
                Specifies the session ID to terminate.
                If not specified all the database sessions created
                in current Python session are terminated.
                Types: str

        RETURNS:
            None

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> from teradatagenai import VSManager
            # Example 1: Disconnect from the database.
            # Create an instance of the VectorStore class.
            >>> vs = VectorStore(name="vec1")

            # Create a vector store.
            >>> vs.create(object_names="amazon_reviews_25",
                          description="vector store testing",
                          database_name='oaf',
                          key_columns=['rev_id', 'aid'],
                          data_columns=['rev_text'],
                          vector_columns='VectorIndex',
                          embeddings_model="amazon.titan-embed-text-v1")

            # Disconnect from the database.
            >>> VSManager.disconnect()
        """
        if session_id:
            # Delete a user specified session.
            session_header = VSManager._generate_session_id()
            url = f"{vector_store_urls.session_url}s/{session_id}"
            delete_sessions = [(session_header["vs_session_id"], session_header["vs_header"])]
            update_internal_buffer = session_id == session_header["vs_session_id"]
            func_name = "terminate_session"
        else:
            # Delete all sessions.
            url = vector_store_urls.session_url
            delete_sessions = GarbageCollector.session_info
            update_internal_buffer = True if delete_sessions else False
            if not delete_sessions:
                print("No sessions to disconnect.")
            func_name = "disconnect"

        # Remove the sessions.
        for session_id, header in delete_sessions:
            try:
                response = UtilFuncs._http_request(url,
                                                   HTTPRequest.DELETE,
                                                   cookies={'session_id': session_id},
                                                   headers=header)
                VectorStore._process_vs_response(func_name, response)
                GarbageCollector.remove_session_id(session_id)
            except TeradataMlException as e:
                # Printing and not raising it so that the loop continues
                # and other sessions are disconnected.
                print(e)
        # Remove the session_id and header from the internal header.
        if update_internal_buffer:
            _InternalBuffer.remove_key("vs_session_id")
            _InternalBuffer.remove_key("vs_header")

class _SimilaritySearch:
    """
    Internal class to create a similarity search object which is needed
    to display the results in a tabular format and at the same time store
    the json object which is used in prepare response.
    """
    def __init__(self, response):
        self.similar_objects_count = response['similar_objects_count']
        self._json_obj = response['similar_objects_list']
        self.similar_objects = pd.DataFrame(self._json_obj)

    def __repr__(self):
        return f"similar_objects_count:{self.similar_objects_count}\nsimilar_objects:\n{self.similar_objects})"

class _ListSessions:
    """
    Internal class to create a _ListSessions object which is needed
    to display the results in a readable format.
    """
    def __init__(self, response):
        self.total_active_sessions = response['count']
        self.current_session_id = response['self_session_id']
        self.session_details = pd.DataFrame(response['session_details'])

    def __repr__(self):
        return f"total_active_sessions:{self.total_active_sessions}\n\ncurrent_session_id:\n{self.current_session_id}" \
               f"\n\nsession_details:\n{self.session_details}"

class VectorStore:
    def __init__(self,
                 name,
                 log=False,
                 **kwargs):
        """
        DESCRIPTION:
            VectorStore contains a vectorized version of data.
            The vectorization typically is a result of embeddings generated by
            an AI LLM.
            There are two types of vector stores based on the use cases:
                * Content-based vector store: A vector store built on the
                  contents of table/view/teradataml DataFrame.
                  The table can be formed from the contents of file / pdf.
                  Questions can be asked against the contents of the table and
                  top matches of relevant rows are returned based on search.
                  This can be followed by a textual response generated using
                  an LLM by manipulating the top matches.

                * Metadata-based vector store: A vector store built on the
                  metadata of a set of tables. Questions can be asked
                  against a table or set of tables and top table
                  matches are returned.
            Notes:
                * If the vector store mentioned in the name argument
                  already exists, it is initialized for use.
                * If not, user needs to call create() to create the same.

        PARAMETERS:
            name:
                Required Argument.
                Specifies the name of the vector store either to connect, if it
                already exists or to create a new vector store.
                Types: str

            log:
                Optional Argument.
                Specifies whether logging should be enabled for vector store
                methods.
                Default Value: False
                Types: bool

        RETURNS:
            None

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> vs = VectorStore(name="vs", log=True)
        """
        # Initialize variables.
        self.name = name
        self._log = log

        # Validating name and log.
        arg_info_matrix = []
        arg_info_matrix.append(["name", self.name, False, (str), True])
        arg_info_matrix.append(["log", self._log, True, (bool)])

        # As the rest call accepts 0, 1 converting it.
        self._log = 0 if not self._log else 1

        _Validators._validate_missing_required_arguments(arg_info_matrix)
        # Validate argument types.
        _Validators._validate_function_arguments(arg_info_matrix)
        
        # Check if vector_store_base_url is set or not.
        _Validators._check_required_params(arg_value=configure._vector_store_base_url,
                                           arg_name="Auth token",
                                           caller_func_name="VectorStore()",
                                           target_func_name="set_auth_token")

        # Call connect in case of CCP enabled tenant.
        # If non-ccp, connect should be explicitly called passing the required params.
        session_header = VSManager._generate_session_id()
        self.__session_id = session_header["vs_session_id"]
        self.__headers = session_header["vs_header"]

        # Create all the REST API urls.
        self.__url = f'{vector_store_urls.vectorstore_url}/{self.name}'
        self.__common_url = f'{self.__url}?log_level={self._log}'
        self.__list_user_permission_url = f'{vector_store_urls.base_url}permissions/{self.name}'
        self.__similarity_search_url = '{0}/similarity-search?question={1}&log_level={2}'

        self.__prepare_response_url = f'{self.__url}/prepare-response?log_level={self._log}'
        self.__ask_url = f'{self.__url}/ask?log_level={self._log}'
        self.__set_user_permissions_url = "{0}permissions/{1}?user_name={2}&action={3}&permission={4}&log_level={5}"
        self.__get_objects_url = f"{self.__url}?get_object_list=true"

        # Check if the vector store exists by calling the list API and validating for the name.
        try:
            vs_list = VSManager.list()
        except Exception as e:
            if 'No authorized vector stores found for the user' in str(e):
                vs_list = pd.DataFrame(columns=["vs_name", "description", "database_name"])
            else:
                raise e
            
        if any(vs_list['vs_name'].isin([self.name])):
            # If the vector store already exists, initialize the exisiting vector store.
            print(f"Vector store {self.name} is initialized for the session.")
        else:
            print(f"Vector Store {self.name} does not exist. Call create() to create the same.")

    # TODO: https://teradata-pe.atlassian.net/browse/ELE-7518
    def get_objects(self):
        """
        DESCRIPTION:
            Get the list of objects in the metadata-based vector store.

        PARAMETERS:
            None

        RETURNS:
            pandas DataFrame containing the list of objects.

        RAISES:
            TeradataMlException

        EXAMPLES:
            # Create an instance of the VectorStore class.
            >>> vs = VectorStore(name="vs")

            # Example: Get the list of objects that are used for creating the vector store.
            >>> vs.get_objects()
        """
        response = UtilFuncs._http_request(self.__get_objects_url, HTTPRequest.GET,
                                           headers=self.__headers,
                                           cookies={'session_id': self.__session_id})

        data = VectorStore._process_vs_response("get_objects", response)
        return pd.DataFrame(data['object_list'])

    def __set_vs_index_and_vs_parameters(self, create=True, **kwargs):
        """
        DESCRIPTION:
            Internal function to set the parameters for the vector store.
            Keeping it common, as it will be required by update and initialize
            methods.

        PARAMETERS:
            create:
                Optional Argument.
                Specifies whether call is from create or update function.
                Default Value: True
                Types: bool

            kwargs:
                Optional Argument.
                Specifies keyword arguments required for creating/updating vector store.
        RAISES:
            None

        EXAMPLES:
            >>> self.__set_vs_index_and_vs_parameters(key_columns="a",
                                                      create=False)
        """
        ## Initializing vs_index params
        self._database_name = kwargs.get('database_name', None)
        self._object_names = kwargs.get('object_names', None)
        self._key_columns = kwargs.get('key_columns', None)
        self._data_columns = kwargs.get('data_columns', None)
        self._vector_columns = kwargs.get('vector_columns', None)
        self._chunk_size = kwargs.get("chunk_size", None)
        self._optimized_chunking = kwargs.get('optimized_chunking', None)
        self._header_height = kwargs.get('header_height', None)
        self._footer_height = kwargs.get('footer_height', None)
        self._include_objects = kwargs.get('include_objects', None)
        self._exclude_objects = kwargs.get('exclude_objects', None)
        self._include_patterns = kwargs.get('include_patterns', None)
        self._exclude_patterns = kwargs.get('exclude_patterns', None)
        self._sample_size = kwargs.get('sample_size', None)
        self._alter_operation = kwargs.get('alter_operation', None)
        self._update_style = kwargs.get('update_style', None if self._alter_operation is None else UpdateStyle.MINOR)
        self._nv_ingestor = kwargs.get('nv_ingestor', False if create else None)
        self._display_metadata = kwargs.get('display_metadata', False if create else None)
        # TODO ELE-6025: Bug in Feb drop for these arguments, hence commented them.
        # self._acronym_objects = kwargs.get('acronym_objects', None)
        # self._acronym_objects_global = kwargs.get('acronym_objects_global', None)
        # self._acronym_files_global = kwargs.get('acronym_files_global', None)

        ## Initializing vs_parameters
        self._description = kwargs.get("description", None)
        self._embeddings_model = kwargs.get("embeddings_model", None)
        self._embeddings_dims = kwargs.get("embeddings_dims", None)
        self._initial_delay_ms = kwargs.get("initial_delay_ms", None)
        self._delay_max_retries = kwargs.get("delay_max_retries", None)
        self._delay_exp_base = kwargs.get("delay_exp_base", None)
        self._delay_jitter = kwargs.get("delay_jitter", None)
        self._metric = kwargs.get("metric", None)
        self._search_algorithm = kwargs.get("search_algorithm", None)
        self._top_k = kwargs.get("top_k", None)
        self._search_threshold = kwargs.get("search_threshold", None)
        self._initial_centroids_method = kwargs.get("initial_centroids_method", None)
        self._train_numcluster = kwargs.get("train_numcluster", None)
        self._max_iternum = kwargs.get("max_iternum", None)
        self._stop_threshold = kwargs.get("stop_threshold", None)
        self._seed = kwargs.get("seed", None)
        self._num_init = kwargs.get("num_init", None)
        self._search_numcluster = kwargs.get("search_numcluster", None)
        self._prompt = kwargs.get("prompt", None)
        self._document_files = kwargs.get("document_files", None)
        self._chat_completion_model = kwargs.get("chat_completion_model", None)
        self._p_value = kwargs.get("p_value", None)
        self._ef_search = kwargs.get("ef_search", None)
        self._num_layer = kwargs.get("num_layer", None)
        self._ef_construction = kwargs.get("ef_construction", None)
        self._num_connpernode = kwargs.get("num_connpernode", None)
        self._maxnum_connpernode = kwargs.get("maxnum_connpernode", None)
        self._apply_heuristics = kwargs.get("apply_heuristics", None)
        self._rerank_weight = kwargs.get("rerank_weight", None)
        self._relevance_top_k = kwargs.get("relevance_top_k", None)
        self._relevance_search_threshold = kwargs.get("relevance_search_threshold", None)
        self._ignore_embedding_errors = kwargs.get("ignore_embedding_errors", False)
        self._chat_completion_max_tokens = kwargs.get("chat_completion_max_tokens", None)
        # Validating vs_index
        arg_info_matrix = []
        arg_info_matrix.append(["database_name", self._database_name, True, (str), True])
        arg_info_matrix.append(["object_names", self._object_names, True if create else True, (str, DataFrame, list), True])
        arg_info_matrix.append(["key_columns", self._key_columns, True, (str, list), True])
        arg_info_matrix.append(["data_columns", self._data_columns, True, (str, list), True])
        arg_info_matrix.append(["vector_columns", self._vector_columns, True, (str), True])
        arg_info_matrix.append(["chunk_size", self._chunk_size, True, (int), True])
        arg_info_matrix.append(["optimized_chunking", self._optimized_chunking, True, (bool), True])
        arg_info_matrix.append(["header_height", self._header_height, True, (int), True])
        arg_info_matrix.append(["footer_height", self._footer_height, True, (int), True])
        # Explicitly checking alter_operation and update_style enum types, to display the correct error message.
        if self._alter_operation is not None:
            if not isinstance(self._alter_operation, Operation):
                raise TypeError(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE,
                                                     "alter_operation", "Operation Enum. Use 'Operation' enum."
                                                     " Check example"))
            else:
                # Convert the enum to value.
                self._alter_operation = self._alter_operation.value
        if self._update_style is not None:
            if not isinstance(self._update_style, UpdateStyle):
                raise TypeError(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE,
                                                    "update_style", "UpdateStyle Enum. Use "
                                                    "'UpdateStyle' enum."
                                                    " Check example"))
            else:
                # Convert the enum to value.
                self._update_style = self._update_style.value

        # TODO ELE-4937 check if this is str or DataFrame.
        arg_info_matrix.append(["include_objects", self._include_objects, True, (str, DataFrame, list), True])
        arg_info_matrix.append(["exclude_objects", self._exclude_objects, True, (str, DataFrame, list), True])
        arg_info_matrix.append(["include_patterns", self._include_patterns, True, (VSPattern, list), True])
        arg_info_matrix.append(["exclude_patterns", self._exclude_patterns, True, (VSPattern, list), True])
        arg_info_matrix.append(["sample_size", self._sample_size, True, (int), True])
        arg_info_matrix.append(["nv_ingestor", self._nv_ingestor, True, (bool), True])
        arg_info_matrix.append(["display_metadata", self._display_metadata, True, (bool), True])
        # TODO ELE-6025: Bug in Feb drop for these arguments, hence commented them.
        # arg_info_matrix.append(["acronym_objects", self._acronym_objects, True, (str, list), True])
        # arg_info_matrix.append(["acronym_objects_global", self._acronym_objects_global, True, (bool, list), True])
        # arg_info_matrix.append(["acronym_files_global", self._acronym_files_global, True, (bool, list), True])

        # Validating vs_parameters
        arg_info_matrix.append(["description", self._description, True, (str), True])
         # embeddings_model is required argument if create=True, else False.
        arg_info_matrix.append(["embeddings_model", self._embeddings_model, False if create else True, (str), True])
        arg_info_matrix.append(["embeddings_dims", self._embeddings_dims, True, (int), True])
        arg_info_matrix.append(["initial_delay_ms", self._initial_delay_ms, True, (int), True])
        arg_info_matrix.append(["delay_max_retries", self._delay_max_retries, True, (int), True])
        arg_info_matrix.append(["delay_exp_base", self._delay_exp_base, True, (int), True])
        arg_info_matrix.append(["delay_jitter", self._delay_jitter, True, (bool), True])
        arg_info_matrix.append(["metric", self._metric, True, (str), True])
        arg_info_matrix.append(["search_algorithm", self._search_algorithm, True, (str), True])
        arg_info_matrix.append(["top_k", self._top_k, True, (int), True])
        arg_info_matrix.append(["initial_centroids_method", self._initial_centroids_method, True, (str),
                                True])
        arg_info_matrix.append(["train_numcluster", self._train_numcluster, True, (int), True])
        arg_info_matrix.append(["max_iternum", self._max_iternum, True, (int), True])
        arg_info_matrix.append(["stop_threshold", self._stop_threshold, True, (float), True])
        arg_info_matrix.append(["seed", self._seed, True, (int), True])
        arg_info_matrix.append(["num_init", self._num_init, True, (int), True])
        arg_info_matrix.append(["search_threshold", self._search_threshold, True, (float), True])
        arg_info_matrix.append(["search_numcluster", self._search_numcluster, True, (int), True])
        arg_info_matrix.append(["prompt", self._prompt, True, (str), True])
        arg_info_matrix.append(["chat_completion_model", self._chat_completion_model, True, (str),
                                True])
        arg_info_matrix.append(["document_files", self._document_files, True, (str, list),
                                True])
        arg_info_matrix.append(["p_value", self._p_value, True, (int), True])
        arg_info_matrix.append(["ef_search", self._ef_search, True, (int), True])
        arg_info_matrix.append(["num_layer", self._num_layer, True, (int), True])
        arg_info_matrix.append(["ef_construction", self._ef_construction, True, (int), True])
        arg_info_matrix.append(["num_connpernode", self._num_connpernode, True, (int), True])
        arg_info_matrix.append(["maxnum_connpernode", self._maxnum_connpernode, True, (int), True])
        arg_info_matrix.append(["apply_heuristics", self._apply_heuristics, True, (bool), True])
        arg_info_matrix.append(["rerank_weight", self._rerank_weight, True, (float), True])
        arg_info_matrix.append(["relevance_top_k", self._relevance_top_k, True, (int), True])
        arg_info_matrix.append(["relevance_search_threshold", self._relevance_search_threshold, True, (float), True])
        arg_info_matrix.append(["ignore_embedding_errors", self._ignore_embedding_errors, True, (bool), True])
        arg_info_matrix.append(["chat_completion_max_tokens", self._chat_completion_max_tokens, True, (int), True])

        # Validate argument types.
        _Validators._validate_function_arguments(arg_info_matrix)

        # Forming document files structure as the API accepts:
        # Input document files structure is: [fully_qualified_file_name1,
        #                                     fully_qualified_file_name2]
        # document_files = [('document_files', ('file1.pdf',
        #                    open('/location/file1.pdf', 'rb'),
        #                    'application/pdf')),
        #                   ('document_files', ('file2.pdf',
        #                    open('/location/file2.pdf', 'rb'),
        #                    'application/pdf'))
        #                   ]
        if self._document_files:
            document_files = self._document_files
            self._document_files = []
            self._open_files = []

            for file in document_files:
                # Get the file name from fully qualified path
                file_name = os.path.basename(file)
                # Form the string 'application/pdf' based on the file extension.
                file_type = f"application/{os.path.splitext(file_name)[1]}".replace(".", "")
                file_handle = open(file, 'rb')
                self._document_files.append(('document_files', (file_name, file_handle, file_type)))
                # Register the file handle with the GarbageCollector.
                GarbageCollector.add_open_file(file_handle)

        # TODO ELE-6025: Bug in Feb drop for these arguments, hence commented them.
        # Will reuse again in April drop.
        # if self._acronym_objects:
        #     acronym_objects = self._acronym_objects
        #     self._acronym_objects = []

        #     for file in acronym_objects:
        #         # Get the file name from fully qualified path
        #         file_name = os.path.basename(file)
        #         # Form the string 'application/pdf' based on the file extension.
        #         file_type = f"application/{os.path.splitext(file_name)[1]}".replace(".", "")
        #         self._acronym_objects.append(('acronym_objects', (file_name,
        #                                                         open(file, 'rb'),
        #                                                         file_type)))

        # Extracting pattern names from include_patterns and exclude_patterns
        if self._include_patterns is not None:     
            include_patterns = []
            for pattern in UtilFuncs._as_list(self._include_patterns):
                include_patterns.append(pattern._pattern_name)
            self._include_patterns = include_patterns

        if self._exclude_patterns is not None:
            exclude_patterns = []
            for pattern in UtilFuncs._as_list(self._exclude_patterns):
                exclude_patterns.append(pattern._pattern_name)
            self._exclude_patterns = exclude_patterns

        vs_parameters = {"description": self._description,
                         "embeddings_model": self._embeddings_model,
                         "embeddings_dims": self._embeddings_dims,
                         "initial_delay_ms": self._initial_delay_ms,
                         "delay_max_retries": self._delay_max_retries,
                         "delay_exp_base": self._delay_exp_base,
                         "delay_jitter": self._delay_jitter,
                         "metric": self._metric,
                         "search_algorithm": self._search_algorithm,
                         "top_k": self._top_k,
                         "initial_centroids_method": self._initial_centroids_method,
                         "train_numcluster": self._train_numcluster,
                         "max_iternum": self._max_iternum,
                         "stop_threshold": self._stop_threshold,
                         "seed": self._seed,
                         "num_init": self._num_init,
                         "search_threshold": self._search_threshold,
                         "search_numcluster": self._search_numcluster,
                         "prompt": self._prompt,
                         "chat_completion_model": self._chat_completion_model,
                         "p_value": self._p_value,
                         "ef_search": self._ef_search,
                         "num_layer": self._num_layer,
                         "ef_construction": self._ef_construction,
                         "num_connPerNode": self._num_connpernode,
                         "maxNum_connPerNode": self._maxnum_connpernode,
                         "apply_heuristics": self._apply_heuristics,
                         "rerank_weight": self._rerank_weight,
                         "relevance_top_k": self._relevance_top_k,
                         "relevance_search_threshold": self._relevance_search_threshold,
                         "ignore_embedding_errors": self._ignore_embedding_errors,
                         "chat_completion_max_tokens": self._chat_completion_max_tokens}

        # Only add keys with non-None values
        self.__vs_parameters = {k: v for k, v in vs_parameters.items() if v is not None}
        if self._object_names is not None:
            self._object_names = UtilFuncs._as_list(self._object_names)
            self._object_names = list(map(lambda obj: obj._table_name.strip('"') 
                                          if _Validators._check_isinstance(obj, DataFrame) 
                                          else obj, self._object_names))
        vs_index = {
            'database_name': self._database_name,
            'object_names': self._object_names,
            'key_columns': self._key_columns,
            'data_columns': self._data_columns,
            'vector_column': self._vector_columns,
            'chunk_size': self._chunk_size,
            'optimized_chunking': self._optimized_chunking,
            'header_height': self._header_height,
            'footer_height': self._footer_height,
            'include_objects': self._include_objects,
            'exclude_objects': self._exclude_objects,
            'include_patterns': self._include_patterns,
            'exclude_patterns': self._exclude_patterns,
            'sample_size': self._sample_size,
            'alter_operation': self._alter_operation,
            'update_style': self._update_style,
            'nv_ingestor': self._nv_ingestor,
            'display_metadata': self._display_metadata
        }

        # TODO ELE-6025: Bug in Feb drop for these arguments, hence commented them.
        # 'acronym_objects': self._acronym_objects,
        # 'acronym_objects_global': self._acronym_objects_global,
        # 'acronym_files_global': self._acronym_files_global

        # Only add keys with non-None values
        self.__vs_index = {k: v for k, v in vs_index.items() if v is not None}

    def create(self, **kwargs):
        """
        DESCRIPTION:
            Creates a new vector store.
            Once vector store is created, it is initialized for use.
            If vector store already exists, error is raised.
            Notes:
                * Only admin users can use this method.
                * Refer to the 'Prerequisites' section under
                  'Vector Store Admin Workflow' in the
                  User guide for details.

        PARAMETERS:
            description:
                Optional Argument.
                Specifies the description of the vector store.
                Types: str

            database_name:
                Optional Argument.
                Specifies the database name of the table or view to be indexed
                for vector store.
                When "document_files" is passed, it refers to the database where
                the file content splits are stored.
                Note:
                    The vector store is also created in this database.
                Types: str

            object_names:
                Required for 'content-based vector store', Optional otherwise.
                Specifies the table name/teradataml DataFrame to be indexed for
                vector store.
                Notes:
                    * For content-based vector store:
                        * Only one table name/teradataml DataFrame can be specified.
                        * For data residing in multiple tables, view should be
                          created and view name/teradataml DataFrame over the view
                          should be specified here.
                    * For metadata-based vector store:
                        * Instead of "object_names", * Use"include_objects" or
                          "include_patterns" parameters instead of "object_names".
                Types: str or list of str or DataFrame

            key_columns:
                Optional Argument.
                Specifies the name(s) of the key column(s) to be used for indexing.
                Note:
                    * When "document_files" is used, this parameter is not needed.
                    * In case of multiple input files, a single key column
                      containing the file names should be generated.
                Types: str, list of str

            data_columns:
                Optional Argument.
                Specifies the name(s) of the data column(s) to be used
                for indexing.
                Types: str, list of str

            vector_columns:
                Optional Argument.
                Specifies the name(s) of the column(s) to be used for storing
                the embeddings.
                Default Value: vector_index
                Types: str, list of str

            chunk_size:
                Optional Argument.
                Specifies the size of each chunk when dividing document files
                into chunks.
                Default Value: 512
                Types: int

            optimized_chunking:
                Optional Argument.
                Specifies whether an optimized splitting mechanism supplied by
                Teradata should be used.
                The documents are parsed internally in an intelligent fashion
                based on file structure and chunks are dynamically created
                based on section layout.
                Notes:
                    * The "chunk_size" field is not applicable when
                      "optimized_chunking" is set to True.
                    *  Applicable only for "document_files".
                Default Value: True
                Types: bool

            header_height:
                Optional Argument.
                Specifies the height (in points) of the header section of a PDF
                document to be trimmed before processing the main content.
                This is useful for removing unwanted header information
                from each page of the PDF.
                Recommended value is 55.
                Default Value: 0
                Types: int

            footer_height:
                Optional Argument.
                Specifies the height (in points) of the footer section of a PDF
                document to be trimmed before processing the main content.
                This is useful for removing unwanted footer information from
                each page of the PDF.
                Recommended value is 55.
                Default Value: 0
                Types: int

            embeddings_model:
                Required Argument.
                Specifies the embeddings model to be used for generating the
                embeddings.
                Permitted Values:
                    * amazon.titan-embed-text-v1
                    * amazon.titan-embed-image-v1
                    * amazon.titan-embed-text-v2:0
                    * text-embedding-ada-002
                    * text-embedding-3-small
                    * text-embedding-3-large
                Types: str

            embeddings_dims:
                Optional Argument.
                Specifies the number of dimensions to be used for generating the embeddings.
                The value depends on the "embeddings_model".
                Permitted Values:
                    * amazon.titan-embed-text-v1: 1536 only
                    * amazon.titan-embed-image-v1: [256, 384, 1024]
                    * amazon.titan-embed-text-v2:0: [256, 512, 1024]
                    * text-embedding-ada-002: 1536 only
                    * text-embedding-3-small: 1 <= dims <= 1536
                    * text-embedding-3-large: 1 <= dims <= 3072
                Default Value:
                    * amazon.titan-embed-text-v1: 1536
                    * amazon.titan-embed-image-v1: 1024
                    * amazon.titan-embed-text-v2:0: 1024
                    * text-embedding-ada-002: 1536
                    * text-embedding-3-small: 1536
                    * text-embedding-3-large: 3072
                Types: int

            initial_delay_ms:
                Optional Argument.
                Specifies the millisecond delay after each input data
                row is sent for embeddings.
                Default Value: 5000
                Types: int

            delay_max_retries:
                Optional Argument.
                Specifies the maximum number of attempts after a failed
                input data row embedding request.
                Default Value: 12
                Types: int

            delay_exp_base:
                Optional Argument.
                Specifies the exponential base of delay time increase.
                Default Value: 1
                Types: int

            delay_jitter:
                Optional Argument.
                Specifies whether to use random sum term in exponent.
                Default Value: False
                Types: bool

            metric:
                Optional Argument.
                Specifies the metric to be used for calculating the distance
                between the vectors.
                Permitted Values:
                    * EUCLIDEAN
                    * COSINE
                    * MANHATTAN
                    * DOTPRODUCT
                    * MINKOWSKI
                Default Value: EUCLIDEAN
                Types: str

            search_algorithm:
                Optional Argument.
                Specifies the algorithm to be used for searching the
                tables and views relevant to the question.
                Permitted Values: VECTORDISTANCE, KMEANS, HNSW.
                Default Value: VECTORDISTANCE
                Types: str

            initial_centroids_method:
                Optional Argument.
                Specifies the algorithm to be used for initializing the
                centroids.
                Note:
                    Applicable when "search_algorithm" is 'KMEANS'.
                Permitted Values: RANDOM, KMEANS++
                Default Value: RANDOM
                Types: str

            train_numcluster:
                Optional Argument.
                Specifies the Number of clusters to be trained.
                Note:
                    Applicable when "search_algorithm" is 'KMEANS'.
                Types: int

            max_iternum:
                Optional Argument.
                Specifies the maximum number of iterations to be run during
                training.
                Note:
                    Applicable when "search_algorithm" is 'KMEANS'.
                Default Value: 10
                Types: int

            stop_threshold:
                Optional Argument.
                Specifies the threshold value at which training should be
                stopped.
                Note:
                    Applicable when "search_algorithm" is 'KMEANS'.
                Default Value: 0.0395
                Types: int

            seed:
                Optional Argument.
                Specifies the seed value to be used for random number
                generation.
                Note:
                    Applicable when "search_algorithm" is 'KMEANS'.
                Default Value: 0
                Types: int

            num_init:
                Optional Argument.
                Specifies the number of times the k-means algorithm should
                run with different initial centroid seeds.
                Default Value: 1
                Types: int

            top_k:
                Optional Argument.
                Specifies the number of top clusters to be considered while searching.
                Value should be between 1-100(both inclusive).
                Default Value: 10
                Types: int

            search_threshold:
                Optional Argument.
                Specifies the threshold value to consider for matching tables
                while searching.
                Types: float

            search_numcluster:
                Optional Argument.
                Specifies the number of clusters to be considered while
                searching.
                Note:
                    Applicable when "search_algorithm" is 'KMEANS'.
                Types: int

            prompt:
                Optional Argument.
                Specifies the prompt to be used by language model
                to generate responses using top matches.
                Types: str

            chat_completion_model:
                Optional Argument.
                Specifies the name of the chat completion model to be used for
                generating text responses.
                Permitted Values:
                    * anthropic.claude-3-haiku-20240307-v1:0
                    * anthropic.claude-3-opus-20240229-v1:0
                    * anthropic.claude-3-sonnet-20240229-v1:0
                    * anthropic.claude-3-5-sonnet-20240620-v1:0
                Default Value: anthropic.claude-3-haiku-20240307-v1:0
                Types: str

            document_files:
                Optional Argument.
                Specifies the input dataset in document files format.
                It can be used to specify input documents in file format.
                The files are processed internally, converted to chunks and stored
                into a database table.
                Alternatively, users can choose to chunk their files themselves,
                store them into a database table, create a table and specify
                the details of that using "database_name", "object_names",
                "data_columns" where the file content splits are stored.
                Notes:
                    * Only PDF format is currently supported.
                    * Multiple document files can be supplied.
                    * Fully qualified file name should be specified.
                Examples:
                    document_files=['file1.pdf','file2.pdf']
                Types: str, list

            p_value:
                Optional Argument.
                Specifies the p-value for computing the Minkowski distance.
                Applicable to "search_algorithm" VECTORDISTANCE.
                Default Value: 2
                Types: int

            ef_search:
                Optional Argument.
                Specifies the number of neighbors to be considered during search
                in HNSW graph.
                Note:
                    Applicable when "search_algorithm" is 'HNSW'.
                Default Value: 32
                Types: int

            num_layer:
                Optional Argument.
                Specifies the maximum number of layers for the HNSW graph.
                Note:
                    Applicable when "search_algorithm" is 'HNSW'.
                Types: int

            ef_construction:
                Optional Argument.
                Specifies the number of neighbors to be considered during
                construction of the HNSW graph.
                Applicable when "search_algorithm" is 'HNSW'.
                Default Value: 32
                Types: int

            num_connpernode:
                Optional Argument.
                Specifies the number of connections per node in the HNSW graph
                during construction.
                Note:
                    Applicable when "search_algorithm" is 'HNSW'.
                Default Value: 32
                Types: int

            maxnum_connpernode:
                Optional Argument.
                Specifies the maximum number of connections per node in the
                HNSW graph during construction.
                Note:
                    Applicable when "search_algorithm" is 'HNSW'.
                Default Value: 32
                Types: int

            apply_heuristics:
                Optional Argument.
                Specifies whether to apply heuristics optimizations during construction
                of the HNSW graph.
                Applicable when "search_algorithm" is 'HNSW'.
                Default Value: False
                Types: bool

            include_objects:
                Optional Argument.
                Specifies the list of tables and views included 
                in the metadata-based vector store.
                Types: str or list of str or DataFrame
            
            exclude_objects:
                Optional Argument.
                Specifies the list of tables and views excluded from 
                the metadata-based vector store.
                Types: str or list of str or DataFrame

            sample_size:
                Optional Argument.
                Specifies the number of rows to sample from tables and views 
                for the metadata-based vector store embeddings.
                Default Value: 20
                Types: int

            rerank_weight:
                Optional Argument.
                Specifies the weight to be used for reranking the search results.
                Applicable range is 0.0 to 1.0.
                Default Value: 0.2
                Types: float

            relevance_top_k:
                Optional Argument.
                Specifies the number of top similarity matches to be considered for reranking.
                Applicable range is 1 to 100.
                Default Value: 60
                Types: int

            relevance_search_threshold:
                Optional Argument.
                Specifies the threshold value to consider matching tables/views while reranking.
                A higher threshold value limits responses to the top matches only.
                Types: float

            include_patterns:
                Optional Argument.
                Specifies the list of patterns to be included in the metadata-based vector store.
                Types: VSPattern or list of VSPattern

            exclude_patterns:
                Optional Argument.
                Specifies the list of patterns to be excluded from the metadata-based vector store.
                Types: VSPattern or list of VSPattern

            nv_ingestor:
                Optional Argument.
                Specifies whether to use NVIDIA NV-Ingest for processing the document files.
                Default Value: False
                Types: bool

            display_metadata:
                Optional Argument.
                Specifies whether to display metadata describing objects extracted from the document files 
                when using NVIDIA NV-Ingest.
                Default Value: False
                Types: bool

            ignore_embedding_errors:
                Optional Argument.
                Specifies whether to ignore errors during embedding generation.
                Default Value: False
                Types: bool
            
            chat_completion_max_tokens:
                Optional Argument.
                Specifies the maximum number of tokens to be generated by the chat completion model.
                Default Value: 16384
                Types: int

        RETURNS:
            Pandas DataFrame containing status of create operation.

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> from teradatagenai import VectorStore

            # Create an instance of the VectorStore class.
            >>> vs = VectorStore(name="vec1")

            # Example 1: Create a content based vector store for the data
            #            in table 'amazon_reviews_25'.
            #            Use 'amazon.titan-embed-text-v1' embedding model for
            #            creating vector store.
            >>> vs.create(object_names="amazon_reviews_25",
                          description="vector store testing",
                          database_name='oaf',
                          key_columns=['rev_id', 'aid'],
                          data_columns=['rev_text'],
                          vector_columns='VectorIndex',
                          embeddings_model="amazon.titan-embed-text-v1")
            # Example 2: Create a content based vector store for the data
            #            in DataFrame 'df'.
            #            Use 'amazon.titan-embed-text-v1' embedding model for
            #            creating vector store.
            >>> from teradataml import DataFrame
            >>> df = DataFrame("amazon_reviews_25")
            >>> vs = VectorStore('vs_example_2') 
            >>> vs.create(object_names=df,
                          description="vector store testing",
                          database_name='oaf',
                          key_columns=['rev_id', 'aid'],
                          data_columns=['rev_text'],
                          vector_columns='VectorIndex',
                          embeddings_model="amazon.titan-embed-text-v1")
            # Example 3: Create a content based vector store for the data
            #            in 'SQL_Fundamentals.pdf' file.
            #            Use 'amazon.titan-embed-text-v1' embedding model
            #            for creating vector store.

            # Get the absolute path for 'SQL_Fundamentals.pdf' file.
            >>> import teradatagenai
            >>> files= [os.path.join(os.path.dirname(teradatagenai.__file__), "example-data",
                                 "SQL_Fundamentals.pdf")]
            >>> vs = VectorStore('vs_example_3')
            >>> vs.create(object_names="amazon_reviews_25",
                          description="vector store testing",
                          database_name='oaf',
                          key_columns=['rev_id', 'aid'],
                          data_columns=['rev_text'],
                          vector_columns='VectorIndex',
                          embeddings_model="amazon.titan-embed-text-v1"
                          document_files=files)
        """
        # Set the vs_index and vs_parameters
        self.__set_vs_index_and_vs_parameters(**kwargs)

        # Form the data to be passed to the API
        data = {}
        if self.__vs_parameters or self.__vs_index:
            data = {}
            if self.__vs_parameters:
                data['vs_parameters'] = json.dumps(self.__vs_parameters)
            if self.__vs_index:
                data['vs_index'] = json.dumps(self.__vs_index)
        # Form the http_params
        http_params = {
            "url": self.__common_url,
            "method_type": HTTPRequest.POST,
            "headers": self.__headers,
            "data": data,
            "files": self._document_files,
            "cookies": {'session_id': self.__session_id}
        }
        # Call the 'create' API
        response = UtilFuncs._http_request(**http_params)
        # Process the response
        self._process_vs_response("create", response) 

    def destroy(self):
        """
        DESCRIPTION:
            Destroys the vector store.
            Notes:
                * Only admin users can use this method.
                * Refer to the 'Prerequisites' section under
                  'Vector Store Admin Workflow' in the
                  User guide for details.

        PARAMETERS:
            None

        RETURNS:
            Pandas DataFrame containing status of destroy operation.

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> from teradatagenai import VectorStore

            # Create an instance of the VectorStore class.
            >>> vs = VectorStore(name="vec1")

            # Example 1: Create a content based vector store for the data
            #            in table 'amazon_reviews_25'.
            #            Use 'amazon.titan-embed-text-v1' embedding model for
            #            creating vector store.

            # Note this step is not needed if vector store already exists.
            >>> vs.create(object_names="amazon_reviews_25",
                          description="vector store testing",
                          database_name='oaf',
                          key_columns=['rev_id', 'aid'],
                          data_columns=['rev_text'],
                          vector_columns='VectorIndex',
                          embeddings_model="amazon.titan-embed-text-v1")

            # Destroy the Vector Store.
            >>> vs.destroy()
        """
        response = UtilFuncs._http_request(self.__common_url, HTTPRequest.DELETE,
                                           headers=self.__headers,
                                           cookies={'session_id': self.__session_id})
        self._process_vs_response("destroy", response)

    def update(self, **kwargs):
        """
        DESCRIPTION:
            Updates an existing vector store with the specified parameters.
            Notes:
                * Create a new vector store, if input contents are updated or
                  new data files become available.
                  Update is not supported in such scenario
                * Only admin users can use this method.
                * Refer to the 'Prerequisites' section under
                  'Vector Store Admin Workflow' in the
                  User guide for details.

        PARAMETERS:
            embeddings_model:
                Optional Argument.
                Specifies the embeddings model to be used for generating the
                embeddings.
                Permitted Values:
                    * amazon.titan-embed-text-v1
                    * amazon.titan-embed-image-v1
                    * amazon.titan-embed-text-v2:0
                    * text-embedding-ada-002
                    * text-embedding-3-small
                    * text-embedding-3-large
                Types: str

            embeddings_dims:
                Optional Argument.
                Specifies the number of dimensions to be used for generating the embeddings.
                The value depends on the "embeddings_model".
                Permitted Values:
                    * amazon.titan-embed-text-v1: 1536 only
                    * amazon.titan-embed-image-v1: [256, 384, 1024]
                    * amazon.titan-embed-text-v2:0: [256, 512, 1024]
                    * text-embedding-ada-002: 1536 only
                    * text-embedding-3-small: 1 <= dims <= 1536
                    * text-embedding-3-large: 1 <= dims <= 3072
                Types: int

            initial_delay_ms:
                Optional Argument.
                Specifies the millisecond delay after each input table
                row is sent for embeddings.
                Types: int

            delay_max_retries:
                Optional Argument.
                Specifies the maximum number of attempts after a failed
                input table row embedding request.
                Types: int

            delay_exp_base:
                Optional Argument.
                Specifies the exponential base of delay time increase.
                Types: int

            delay_jitter:
                Optional Argument.
                Specifies the random sum term in exponent.
                Types: bool

            metric:
                Optional Argument.
                Specifies the metric to be used for calculating the distance
                between the vectors.
                Permitted Values:
                    * EUCLIDEAN
                    * COSINE
                    * MANHATTAN
                    * DOTPRODUCT
                    * MINKOWSKI
                Types: str

            search_algorithm:
                Optional Argument.
                Specifies the algorithm to be used for searching the tables and
                views relevant to the question.
                Permitted Values: VECTORDISTANCE, KMEANS.
                Types: str

            initial_centroids_method:
                Optional Argument.
                Specifies the Algorithm to be used for initializing the
                centroids.
                Note:
                    Applicable when "search_algorithm" is 'KMEANS'.
                Allowed values are RANDOM and KMEANS++
                Permitted Values: RANDOM, KMEANS++
                Types: str

            train_numcluster:
                Optional Argument.
                Specifies the Number of clusters to be trained.
                Note:
                    Applicable when "search_algorithm" is 'KMEANS'.
                Types: int

            max_iternum:
                Optional Argument.
                Specifies the maximum number of iterations to be run during
                training.
                Note:
                    Applicable when "search_algorithm" is 'KMEANS'.
                Types: int

            stop_threshold:
                Optional Argument.
                Specifies the threshold value at which training should be
                stopped.
                Note:
                    Applicable when "search_algorithm" is 'KMEANS'.
                Types: int

            seed:
                Optional Argument.
                Specifies the seed value to be used for random number
                generation.
                Note:
                    Applicable when "search_algorithm" is 'KMEANS'.
                Types: int

            num_init:
                Optional Argument.
                Specifies the number of times the k-means algorithm will
                be run with different initial centroid seeds.
                Types: int

            top_k:
                Optional Argument.
                Specifies the number of top clusters to be considered while searching.
                Types: int

            search_threshold:
                Optional Argument.
                Specifies the threshold value to consider matching tables/views
                while searching.
                Types: float

            search_numcluster:
                Optional Argument.
                Specifies the number of clusters to be considered while
                searching.
                Notes:
                    Applicable when "search_algorithm" is 'KMEANS'.
                Types: int

            prompt:
                Optional Argument.
                Specifies the prompt to be used for generating answers.
                Types: str

            document_files:
                Optional Argument.
                Specifies the list of PDF files to be divided into chunks and
                used for document embedding.
                Types: tuple, list of tuple

            p_value:
                Optional Argument.
                Specifies the p-value for computing the Minkowski distance.
                Note:
                    Applicable to "search_algorithm" VECTORDISTANCE.
                Default Value: 2
                Types: int

            ef_search:
                Optional Argument.
                Specifies the number of neighbors to be considered during search
                in HNSW graph.
                Note:
                    Applicable when "search_algorithm" is 'HNSW'.
                Default Value: 32
                Types: int

            num_layer:
                Optional Argument.
                Specifies the maximum number of layers for the HNSW graph.
                Note:
                    Applicable when "search_algorithm" is 'HNSW'.
                Types: int

            ef_construction:
                Optional Argument.
                Specifies the number of neighbors to be considered during
                construction of the HNSW graph.
                Note:
                    Applicable when "search_algorithm" is 'HNSW'.
                Default Value: 32
                Types: int

            num_connpernode:
                Optional Argument.
                Specifies the number of connections per node in the HNSW graph
                during construction.
                Note:
                    Applicable when "search_algorithm" is 'HNSW'.
                Default Value: 32
                Types: int

            maxnum_connpernode:
                Optional Argument.
                Specifies the maximum number of connections per node in the
                HNSW graph during construction.
                Note:
                    Applicable when "search_algorithm" is 'HNSW'.
                Default Value: 32
                Types: int

            apply_heuristics:
                Optional Argument.
                Specifies whether to apply heuristics optimizations during construction
                of the HNSW graph.
                Note:
                    Applicable when "search_algorithm" is 'HNSW'.
                Default Value: False
                Types: bool
   
            include_objects:
                Optional Argument.
                Specifies the list of tables and views to be included in the
                metadata-based vector store.
                Types: str or list of str or DataFrame
            
            exclude_objects:
                Optional Argument.
                Specifies the list of tables and views to be excluded from the
                metadata-based vector store.
                Types: str or list of str or DataFrame

            sample_size:
                Optional Argument.
                Specifies the number of rows to sample from tables and views 
                for the metadata-based vector store embeddings.
                Default Value: 20
                Types: int

            rerank_weight:
                Optional Argument.
                Specifies the weight to be used for reranking the search results.
                Applicable range is 0.0 to 1.0.
                Default Value: 0.2
                Types: float

            relevance_top_k:
                Optional Argument.
                Specifies the number of top similarity matches to be considered for reranking.
                Applicable range is 1 to 100.
                Default Value: 60
                Types: int

            relevance_search_threshold:
                Optional Argument.
                Specifies the threshold value to consider matching tables/views while reranking.
                A higher threshold value limits responses to the top matches only.
                Types: float
            
            include_patterns:
                Optional Argument.
                Specifies the list of patterns to be included in the metadata-based vector store.
                Types: VSPattern or list of VSPattern

            exclude_patterns:
                Optional Argument.
                Specifies the list of patterns to be excluded from the metadata-based vector store.
                Types: VSPattern or list of VSPattern

            database_name:
                Optional Argument.
                Specifies the database name of the table or view to be indexed
                for vector store.
                When "document_files" is passed, it refers to the database where
                the file content splits are stored.
                Note:
                    The vector store is also created in this database.
                Types: str

            alter_operation:
                Optional Argument.
                Specifies the type of operation to be performed on the vector store.
                Permitted Values: ADD, DROP
                Types: str
            
            update_style:
                Optional Argument.
                Specifies the style to be used for "alter_operation" of the rows 
                from the vector store when "search_algorithm" is KMEANS/HNSW.
                Permitted Values: MINOR, MAJOR
                Default Value: MINOR
                Types: str     

            object_names:
                Optional Argument.
                Specifies the table name/teradataml DataFrame to be indexed for
                vector store. Applicable only for content-based vector store.
                Types: str, list of str, DataFrame

            ignore_embedding_errors:
                Optional Argument.
                Specifies whether to ignore errors during embedding generation.
                Types: bool
                Default Value: False

            chat_completion_max_tokens:
                Optional Argument.
                Specifies the maximum number of tokens to be generated by the chat completion model.
                Default Value: 16384
                Types: int


        RETURNS:
            Pandas DataFrame containing status of update operation.

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> from teradatagenai import VectorStore

            # Create an instance of the VectorStore class.
            >>> vs = VectorStore(name="vec1")

            # Create the Vector Store.
            # Note this step is not needed if vector store already exists.
            >>> vs.create(object_names="amazon_reviews_25",
                          description="vector store testing",
                          database_name='oaf',
                          key_columns=['rev_id', 'aid'],
                          data_columns=['rev_text'],
                          vector_columns='VectorIndex',
                          embeddings_model="amazon.titan-embed-text-v1"
                          )

            # Example 1: Update the search_algorithm, search_threshold and
            #            description of the Vector Store.
            >>> vs.update(search_algorithm='KMEANS',
                          search_threshold=0.6,
                          description='KMeans clustering method')
            
            # Example 2: Add the object_names of the content-based Vector Store using
            #            alter_operation and update_style.
            >>> from teradatagenai import Operation, UpdateStyle
            >>> vs = VectorStore(name="vs_update")
            >>> vs.create(embeddings_model= 'amazon.titan-embed-text-v1',
                          chat_completion_model= 'anthropic.claude-instant-v1',
                          search_algorithm= 'HNSW',
                          seed=10,
                          top_k=10,
                          ef_construction=32,
                          num_connpernode=32,
                          maxnum_connpernode=32,
                          metric='EUCLIDEAN',
                          apply_heuristics=False,
                          ef_search=32,
                          database_name= 'oaf',
                          object_names= 'amazon_reviews_25',
                          key_columns= ['rev_id', 'aid'],
                          data_columns= ['rev_text'],
                          vector_column= 'VectorIndex')

            >>> vs.update(object_names='amazon_reviews_10_alter',
                          alter_operation=Operation.ADD,
                          update_style=UpdateStyle.MINOR)

            # Example 3: Delete the object_names of the content-based Vector Store using
            #            alter_operation and update_style.
            >>> vs.update(object_names='amazon_reviews_25',
                          alter_operation=Operation.DELETE,
                          update_style=UpdateStyle.MAJOR)
        """
        self.__set_vs_index_and_vs_parameters(**kwargs, create=False)

        if self.__vs_parameters or self.__vs_index:
            data = {}
            if self.__vs_parameters:
                data['vs_parameters'] = json.dumps(self.__vs_parameters)
            if self.__vs_index:
                data['vs_index'] = json.dumps(self.__vs_index)

        response = UtilFuncs._http_request(self.__common_url,
                                           HTTPRequest.PATCH,
                                           data=data,
                                           files=self._document_files,
                                           headers=self.__headers,
                                           cookies={'session_id': self.__session_id})
        self._process_vs_response("update", response)

    def similarity_search(self, question):
        """
        DESCRIPTION:
            Performs similarity search in the Vector Store for the input question.
            The algorithm specified in "search_algorithm" is used to perform
            the search against the vector store.
            The result contains "top_k" rows along with similarity score
            found by the "search_algorithm".

        PARAMETERS:
            question:
                Required Argument.
                Specifies a string of text for which similarity search
                needs to be performed.
                Types: str

        RETURNS:
            list

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> from teradatagenai import VectorStore

            # Create an instance of the VectorStore class.
            >>> vs = VectorStore(name="vs")

            # Create a Vector Store.

            # Note this step is not needed if vector store already exists.
            >>> vs.create(object_names="amazon_reviews_25",
                          description="vector store testing",
                          database_name='oaf',
                          key_columns=['rev_id', 'aid'],
                          data_columns=['rev_text'],
                          vector_columns='VectorIndex',
                          embeddings_model="amazon.titan-embed-text-v1",
                          search_algorithm='VECTORDISTANCE',
                          top_k=10
                          )

            # Example: Perform similarity search in the Vector Store for
            #          the input question.
            >>> question = 'Are there any reviews about books?'
            >>> response = vs.similarity_search(question=question)

        """                               
        # TODO ELE-4940: Bug in Feb drop for these arguments, hence commented them.
        # Will reuse again in April drop.                         
        # # Batch similarity search
        # if input_table is not None or input_id_column is not None or input_query_column is not None:
        #     # Validating params
        #     arg_info_matrix = []
        #     arg_info_matrix.append(["input_table", input_table, False, (str), True])
        #     arg_info_matrix.append(["input_id_column", input_id_column, False, (str), True])
        #     arg_info_matrix.append(["input_query_column", input_query_column, False, (str), True])
        #     _Validators._validate_missing_required_arguments(arg_info_matrix)

        #     # Validate argument types.
        #     _Validators._validate_function_arguments(arg_info_matrix)

        #     # Batch similarity search
        #     batch_input_index = {
        #         "batch_input_table": input_table,
        #         "batch_input_id_column": input_id_column,
        #         "batch_input_query_column": input_query_column
        #     }
        #     # Batch similarity search URL
        #     similarity_batch_search_url = f'{vector_store_urls.vectorstore_url}/{self.name}/similarity-search-batch'
        #     print(similarity_batch_search_url)
        #     # Batch similarity search request
        #     response = UtilFuncs._http_request(similarity_batch_search_url, HTTPRequest.POST,
        #                                        headers=self.__headers,
        #                                        cookies={'session_id': self.__session_id},
        #                                        json=batch_input_index)
        #     # Process the response
        #     self._process_vs_response("similarity-search-batch", response)
        #     # Wait for similarity search to complete and make it a synchronous call.
        #     self.status_polling(return_status=False)
        #     # return
        #     # print('why no poll?')

        #     # Get the similarity search results.
        #     response = UtilFuncs._http_request(similarity_batch_search_url, HTTPRequest.GET,
        #                                        headers=self.__headers,
        #                                        cookies={'session_id': self.__session_id})

        #     return self._process_vs_response("similarity-search-batch", response)

        # Initializing params
        self._question = question

        # Validating params
        arg_info_matrix = []
        arg_info_matrix.append(["question", self._question, False, (str), True])
        _Validators._validate_missing_required_arguments(arg_info_matrix)

        # Validate argument types.
        _Validators._validate_function_arguments(arg_info_matrix)

        response = UtilFuncs._http_request(self.__similarity_search_url.format(self.__url,
                                                                               question,
                                                                               self._log),
                                           HTTPRequest.POST,
                                           headers=self.__headers,
                                           cookies={'session_id': self.__session_id})

        return _SimilaritySearch(self._process_vs_response(api_name="similarity-search",
                                                           response=response))

    def prepare_response(self,
                         question,
                         similarity_results,
                         prompt=None):
        """
        DESCRIPTION:
            Prepare a natural language response to the user using the input
            question and similarity_results provided by
            VectorStore.similarity_search() method.
            The response is generated by a language model configured
            in the environment using a pre-configured prompt.
            An optional parameter prompt can be used to specify a customized
            prompt that replaces the internal prompt.

        PARAMETERS:
            question:
                Required Argument.
                Specifies a string of text for which similarity search
                needs to be performed.
                Types: str

            similarity_results:
                Required Argument.
                Specifies the similarity results obtained by similarity_search().
                Types: str

            prompt:
                Optional Argument.
                Specifies a customized prompt that replaces the internal prompt.
                Types: str

        RETURNS:
            HTTP Response json.

        RAISES:
            TypeError, TeradataMlException

        EXAMPLES:
            # Create an instance of the VectorStore class.
            >>> vs = VectorStore(name="vs")

            # Creates a Vector Store.
            # Note this step is not needed if vector store already exists.
            >>> vs.create(object_names="amazon_reviews_25",
                          description="vector store testing",
                          database_name='oaf',
                          key_columns=['rev_id', 'aid'],
                          data_columns=['rev_text'],
                          vector_columns='VectorIndex',
                          embeddings_model="amazon.titan-embed-text-v1",
                          search_algorithm='VECTORDISTANCE',
                          top_k = 10
                          )

            # Perform similarity search in the Vector Store for
            # the input question.
            >>> question = 'Are there any reviews about books?'
            >>> response = vs.similarity_search(question=question)

            # Example 1: Prepare a natural language response to the user
            #            using the input question and similarity_results
            #            provided by similarity_search().

            question='Did any one feel the book is thin?'
            similar_objects_list = response['similar_objects_list']
            >>> vs.prepare_response(question=question,
                                    similarity_results=similar_objects_list)
        """ 

        # Initializing params
        self._question = question
        self._similarity_results = similarity_results
        self._prompt = prompt
        # TODO ELE-4940 Bug in Feb drop.                            
        # batch_mode = False

        # Validating params
        arg_info_matrix = []
        arg_info_matrix.append(["similarity_results", self._similarity_results, False, _SimilaritySearch, True])
        arg_info_matrix.append(["prompt", self._prompt, True, (str), True])

        # TODO ELE-4940 Bug in Feb drop for these arguments, hence commented them.
        # Will reuse again in April drop.
        # Batch mode params, if any
        # if input_table is not None or input_id_column is not None or input_query_column is not None:
        #     batch_mode = True
        #     arg_info_matrix.append(["input_table", input_table, False, (str), True])
        #     arg_info_matrix.append(["input_id_column", input_id_column, False, (str), True])
        #     arg_info_matrix.append(["input_query_column", input_query_column, False, (str), True])
        # else:
        # Non-batch mode params
        # Not required for batch mode

        arg_info_matrix.append(["question", self._question, False, (str), True])

        _Validators._validate_missing_required_arguments(arg_info_matrix)

        # Explicitly checking similarity search API, as correct message is not displayed.
        if not isinstance(similarity_results, _SimilaritySearch):
            raise TypeError(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE,
                                                 "similarity_results", "output of similarity_search()"))
        # Validate argument types.
        _Validators._validate_function_arguments(arg_info_matrix)

        # TODO ELE-4940
        # Bug in Feb drop for these arguments, hence commented them.
        # Will reuse again in April drop.
        # if batch_mode:
        #     # batch_input_index params
        #     batch_input_index = {
        #         "batch_input_table": input_table,
        #         "batch_input_id_column": input_id_column,
        #         "batch_input_query_column": input_query_column
        #     }
        #     # Data for batch mode
        #     data = {
        #         "batch_input_index": batch_input_index,
        #         "similar_objects": self._similarity_results._json_obj,
        #         "prompt": self._prompt,
        #     }
        #     # Prepare response in batch mode URL
        #     prepare_response_url = f'{vector_store_urls.vectorstore_url}/{self.name}/prepare-response-batch'
        #     # POST request for batch mode
        #     response = UtilFuncs._http_request(prepare_response_url, HTTPRequest.POST,
        #                                        headers=self.__headers,
        #                                        cookies={'session_id': self.__session_id},
        #                                        json=data)
        #     # Process the response
        #     self._process_vs_response(api_name="prepare_response", response=response)

        #     # Wait for prepare response to complete and make it a synchronous call.
        #     self.status_polling(return_status=False)

        #     # Get the prepare response results.
        #     response = UtilFuncs._http_request(prepare_response_url, HTTPRequest.GET,
        #                                        headers=self.__headers,
        #                                        cookies={'session_id': self.__session_id})
        #     return self._process_vs_response(api_name="prepare_response", response=response)

        # Data for non-batch mode

        data = {
            'question': self._question,
            'similar_objects': self._similarity_results._json_obj,
            'prompt': self._prompt,
        }

        # POST request for non-batch mode
        response = UtilFuncs._http_request(self.__prepare_response_url, HTTPRequest.POST,
                                           headers=self.__headers,
                                           cookies={'session_id': self.__session_id},
                                           json=data)
        # Process the response
        return self._process_vs_response(api_name="prepare_response", response=response)

    def ask(self, question, prompt=None):
        """
        DESCRIPTION:
            Performs similarity search in the vector store for
            the input question followed by preparing a natural
            language response to the user. This method combines
            the operation of similarity_search() and prepare_response()
            into one call for faster response time.

        PARAMETERS:
            question:
                Required Argument.
                Specifies a string of text for which similarity search
                needs to be performed.
                Types: str

            prompt:
                Optional Argument.
                Specifies a customized prompt that replaces the internal prompt.
                Types: str

        RETURNS:
            dict

        RAISES:
            TeradataMlException

        EXAMPLES:
            # Create an instance of the VectorStore class.
            >>> vs = VectorStore(name="vs")

            # Create a Vector Store.

            # Note this step is not needed if vector store already exists.
            >>> vs.create(object_names="amazon_reviews_25",
                          description="vector store testing",
                          database_name='oaf',
                          key_columns=['rev_id', 'aid'],
                          data_columns=['rev_text'],
                          vector_columns='VectorIndex',
                          embeddings_model="amazon.titan-embed-text-v1",
                          search_algorithm='VECTORDISTANCE',
                          top_k=10
                          )

            >>> custom_prompt = '''List good reviews about the books. Do not assume information.
                                Only provide information that is present in the data.
                                Format results like this:
                                Review ID:
                                Author ID:
                                Review:
                                '''
            # Example 1: Perform similarity search in the Vector Store for
            #            the input question followed by preparing a natural
            #            language response to the user.

            >>> question = 'Are there any reviews saying that the books are inspiring?'
            >>> response = vs.ask(question=question, prompt=custom_prompt)

        """
        # Initializing params
        self._question = question
        self._prompt = prompt
        # TODO ELE-4940 Bug in Feb drop.                         
        batch_mode = False

        # Validating params
        arg_info_matrix = []
        arg_info_matrix.append(["question", self._question, False, (str), True])
        arg_info_matrix.append(["prompt", self._prompt, True, (str), True])
        _Validators._validate_missing_required_arguments(arg_info_matrix)

        # Validate argument types.
        _Validators._validate_function_arguments(arg_info_matrix)


        # TODO ELE-4940
        # Bug in Feb drop for these arguments, hence commented them.
        # Will reuse again in April drop.                                                                   
        # if batch_mode:
        #     # batch_input_index params
        #     batch_input_index = {
        #         "batch_input_table": input_table,
        #         "batch_input_id_column": input_id_column,
        #         "batch_input_query_column": input_query_column
        #     }
        #     # Data for batch mode
        #     data = {
        #         "batch_input_index": batch_input_index,
        #         "prompt": self._prompt,
        #     }
        #     # Ask in batch mode URL
        #     ask_url = f'{vector_store_urls.vectorstore_url}/{self.name}/ask-batch'
        #     # POST request for batch mode
        #     response = UtilFuncs._http_request(ask_url, HTTPRequest.POST,
        #                                        headers=self.__headers,
        #                                        cookies={'session_id': self.__session_id},
        #                                        json=data)
        #     # Process the response
        #     self._process_vs_response(api_name="ask", response=response)

        #     # Wait for ask to complete and make it a synchronous call.
        #     self.status_polling(return_status=False)

        #     # Get the ask results.
        #     response = UtilFuncs._http_request(ask_url, HTTPRequest.GET,
        #                                        headers=self.__headers,
        #                                        cookies={'session_id': self.__session_id})
        #     return self._process_vs_response(api_name="ask", response=response)

        data = {
            'question': self._question,
            'prompt': self._prompt,
        }

        response = UtilFuncs._http_request(self.__ask_url, HTTPRequest.POST,
                                           headers=self.__headers,
                                           cookies={'session_id': self.__session_id},
                                           json=data)
        return self._process_vs_response(api_name="ask", response=response)

    @staticmethod
    def _process_vs_response(api_name, response, success_status_code=None):
        """
        DESCRIPTION:
            Process and validate the Vector Store service response.

        PARAMETERS:
            api_name:
                Required Argument.
                Specifies the name of the Vector Store method.
                Types: str

            response:
                Required Argument.
                Specifies the response recieved from Vector Store service.
                Types: requests.Response

            success_status_code:
                Optional Argument.
                Specifies the expected success status code for the corresponding
                Vector Store service.
                Default Value: None
                Types: int

        RETURNS:
            Response object.

        RAISES:
            TeradataMlException, JSONDecodeError.

        EXAMPLES:
                >>> _process_vs_response("create", resp)
        """
        try:
            data = response.json()
            # Success status code ranges between 200-300.
            if (success_status_code is None and 200 <= response.status_code < 300) or \
                    (success_status_code == response.status_code):
                if "message" in data:
                    if api_name not in ["similarity-search", "prepare_response", "ask"]:
                        print(data['message'])
                    return data['message']
                else:
                    return data
                return

            # teradataml API got an error response. Error response is expected as follows -
            # Success
            # Response:
            # {
            #     "message": "success string"
            # }
            # Failure
            # Response:
            # {
            #     "detail": "error message string"
            # }
            # Validation
            # Error:
            # {
            #     "detail": [
            #         {
            #             "loc": [
            #                 "string",
            #                 0
            #             ],
            #             "msg": "string",
            #             "type": "string"
            #         }
            #     ]
            # }
            # Extract the fields and raise error accordingly.
            if isinstance(data['detail'], str):
                error_description = data['detail']
            else:
                error_description = []
                for dict_ele in data['detail']:
                    error_msg = f"{dict_ele['msg']} for {dict_ele['loc'][1] if len(dict_ele['loc']) > 1 else dict_ele['loc'][0]}"
                    error_description.append(error_msg)
                error_description = ",".join(error_description)

            exception_message = "Request Failed - {}".format(error_description)

            error_msg = Messages.get_message(MessageCodes.FUNC_EXECUTION_FAILED,
                                             api_name,
                                             exception_message)
            raise TeradataMlException(error_msg, MessageCodes.FUNC_EXECUTION_FAILED)

        # teradatagenai API may not get a Json API response in some cases.
        # So, raise an error with the response received as it is.
        except JSONDecodeError:
            error_msg = Messages.get_message(MessageCodes.FUNC_EXECUTION_FAILED,
                                             api_name,
                                             response.text)
            raise TeradataMlException(error_msg, MessageCodes.FUNC_EXECUTION_FAILED)
        except Exception as e:
            raise

    def status(self):
        """
        DESCRIPTION:
            Checks the status of the below operations:
               * create
               * destroy
               * update

        PARAMETERS:
            None

        RETURNS:
            Pandas DataFrame containing the status of vector store operations.

        RAISES:
            None

        EXAMPLES:
           # Create an instance of the VectorStore class.
           >>> vs = VectorStore(name="vs")
           # Example 1: Check the status of create operation.

           # Create VectorStore.
           # Note this step is not needed if vector store already exists.
           >>> vs.create(object_names="amazon_reviews_25",
                         description="vector store testing",
                         database_name='oaf',
                         key_columns=['rev_id', 'aid'],
                         data_columns=['rev_text'],
                         vector_columns='VectorIndex',
                         embeddings_model="amazon.titan-embed-text-v1")

           # Check status.
           >>> vs.status()
        """

        response = UtilFuncs._http_request(self.__common_url, HTTPRequest.GET,
                                           headers=self.__headers,
                                           cookies={'session_id': self.__session_id})
        return pd.DataFrame([self._process_vs_response("status", response)])

    def list_user_permissions(self):
        """
        DESCRIPTION:
            Lists the users and their corresponding permissions
            on the vector store.
            Notes:
                * Only admin users can use this method.
                * Refer to the 'Prerequisites' section under
                  'Vector Store Admin Workflow' in the
                  User guide for details.

        PARAMETERS:
            None

        RETURNS:
            Pandas DataFrame containing the users and the
            corresponding permissions on the vector store.

        RAISES:
            TeradataMlException

        EXAMPLES:
            # Create an instance of an already existing vector store.
            >>> vs = VectorStore(name="vs")

            # Example: List the user permissions on the vector store.
            >>> vs.list_user_permissions()
        """

        # Get the user permissions on the vector store.
        response = UtilFuncs._http_request(self.__list_user_permission_url,
                                           HTTPRequest.GET,
                                           headers=self.__headers,
                                           cookies={'session_id': self.__session_id})
        # Process the response and return the user permissions.
        data = self._process_vs_response("list_user_permissions", response)
        return pd.DataFrame({"Users": data['authenticated_users'].keys(),
                            "Permissions": data['authenticated_users'].values()})
    
    @property
    def revoke(self):
        """
        DESCRIPTION:
            Revoke the permission of the user on the vector store.
            Notes:
                * Only admin users can use this method.
                * Refer to the 'Prerequisites' section under
                  'Vector Store Admin Workflow' in the
                  User guide for details.

        RETURNS:
            None

        RAISES:
            TeradataMlException

        EXAMPLES:
            # NOTE: It is assumed that vector store "vs" already exits.
            # Create an instance of the VectorStore class.
            >>> vs = VectorStore(name="vs")
            # Revoke 'write' permission of user 'alice' on the vector store 'vs'.
            >>> vs.revoke.write('alice')
            # Revoke 'read' permission of user 'alice' on the vector store 'vs'.
            >>> vs.revoke.read('alice')
        """
        return _Revoke(self)
    
    @property
    def grant(self):
        """
        DESCRIPTION:
            Grant the permission of the user on the vector store.
            Notes:
                * Only admin users can use this method.
                * Refer to the 'Prerequisites' section under
                  'Vector Store Admin Workflow' in the
                  User guide for details.

        RETURNS:
            None

        RAISES:
            TeradataMlException

        EXAMPLES:
            # NOTE: It is assumed that vector store "vs" already exits.
            # Create an instance of the VectorStore class.
            >>> vs = VectorStore(name="vs")
            # Grant 'write' permission to the user 'alice' on the vector store 'vs'.
            >>> vs.grant.write('alice')
            # Grant 'read' permission to the user 'alice' on the vector store 'vs'.
            >>> vs.grant.read('alice')
        """
        return _Grant(self)

class VSPattern:

    def __init__(self,
                 name, 
                 log=False):
        """
        DESCRIPTION:
            Initialize the VSPattern class for metadata-based vector store.

        PARAMETERS:
            name:
                Required Argument.
                Specifies the name of the pattern for vector store.
                Types: str

            log:
                Optional Argument.
                Specifies whether to enable logging.
                Default Value: False
                Types: bool

        RETURNS:
            None

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> from teradatagenai import VSPattern
            >>> pattern = VSPattern(pattern_name="metadata")
        """
        # Initialize variables.
        self._pattern_name = name
        self._enable_logging = log
        self._pattern_string = None

        # Validating name and enable_logging.
        arg_info_matrix = []
        arg_info_matrix.append(["name", self._pattern_name, False, (str), True])
        arg_info_matrix.append(["enable_logging", self._enable_logging, True, (bool)])

        # Validate argument types.
        _Validators._validate_function_arguments(arg_info_matrix)

        # As the rest call accepts 0, 1 converting it.
        self._enable_logging = 0 if not self._enable_logging else 1

        # Initialize URLs.
        self.__pattern_url = f'{vector_store_urls.patterns_url}/{self._pattern_name}'
        self.__common_pattern_url = f'{self.__pattern_url}?log_level={self._enable_logging}'

        # Call connect in case of CCP enabled tenant.
        # If non-ccp, connect should be explicitly called passing the required params.
        session_header = VSManager._generate_session_id()
        self.__session_id = session_header["vs_session_id"]
        self.__headers = session_header["vs_header"]
    
    @property
    def __create_pattern_url(self):
        """ Returns the URL for creating the pattern. """
        return f'{self.__pattern_url}?pattern_string={self._pattern_string}'

    def get(self):
        """
        DESCRIPTION:
            Gets the list of objects that matches the pattern name.
            Notes:
                * Only admin users can use this method.
                * Refer to the 'Prerequisites' section under
                  'Vector Store Admin Workflow' in the
                  User guide for details.

        PARAMETERS:
            None

        RETURNS:
            Pandas dataFrame containing the list of objects that matches the pattern name.

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> from teradatagenai import VSPattern
            >>> pattern = VSPattern(pattern_name="metadata")
            >>> pattern.create(pattern_string='SEMANTIC_DATA.CRICKET_%')
            >>> pattern.get()
        """
        response = UtilFuncs._http_request(self.__common_pattern_url, HTTPRequest.GET,
                                           headers=self.__headers,
                                           cookies={'session_id': self.__session_id})
        # Process the response
        data = VectorStore._process_vs_response("get_pattern", response)
        return pd.DataFrame({'Object list': data['object_list']})
        
    def create(self, pattern_string):
        """
        DESCRIPTION:
            Creates the pattern for metadata-based vector store.
            Notes:
                * Only admin users can use this method.
                * Refer to the 'Prerequisites' section under
                  'Vector Store Admin Workflow' in the
                  User guide for details.

        PARAMETERS:
            pattern_string:
                Required Argument.
                Specifies the pattern string to be used for creating the pattern.
                Types: str

        RETURNS:
            None

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> from teradatagenai import VSPattern
            >>> pattern = VSPattern(pattern_name="metadata")
            >>> pattern.create(pattern_string='SEMANTIC_DATA.CRICKET_%')
        """
        # Validating pattern_string.
        arg_info_matrix = []
        arg_info_matrix.append(["pattern_string", pattern_string, False, (str), True])

        # Validate argument types.
        _Validators._validate_function_arguments(arg_info_matrix)

        # Assign pattern_string.
        self._pattern_string = pattern_string

        response = UtilFuncs._http_request(self.__create_pattern_url, HTTPRequest.POST,
                                           headers=self.__headers,
                                           cookies={'session_id': self.__session_id})
        # Process the response
        VectorStore._process_vs_response("create_pattern", response)

    def delete(self):
        """
        DESCRIPTION:
            Deletes the pattern.
            Notes:
                * Only admin users can use this method.
                * Refer to the 'Prerequisites' section under
                  'Vector Store Admin Workflow' in the
                  User guide for details.

        PARAMETERS:
            None

        RETURNS:
            None

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> from teradatagenai import VSPattern
            >>> pattern = VSPattern(pattern_name="metadata")
            >>> pattern.delete()
        """
        response = UtilFuncs._http_request(self.__common_pattern_url, HTTPRequest.DELETE,
                                           headers=self.__headers,
                                           cookies={'session_id': self.__session_id})
        # Process the response
        VectorStore._process_vs_response("delete_pattern", response)