# ##################################################################
#
# Copyright 2024 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
#
# Primary Owner: Kesavaragavan B (kesavaragavan.b@teradata.com)
# Secondary Owner: Prafulla V Tekawade (prafulla.tekawade@teradata.com)
#                  Aanchal Kavedia (aanchal.kavedia@teradata.com)
#
# Notes: 
#   * This code is only for internal use. 
#   * The code may perform modify, create, or delete operations 
#     in database based on given query. Hence, limit the permissions 
#     granted to the credentials.
#  This code is used for performing Text Analytics using LLM endpoints
#  also models from hugging face.
# ##################################################################

import os
import pandas as pd
from teradataml import copy_to_sql, DataFrame
from teradatagenai.llm.llm import TeradataAI
from teradataml.utils.dtypes import _Dtypes
from teradataml.utils.validators import _Validators
from teradatasqlalchemy import VARCHAR
from teradataml.common.utils import UtilFuncs

class _TextAnalyticsAICommon:
    """
    Class for holding common functions required for TextAnalytics.
    """
    def __init__(self, llm):
        """
        DESCRIPTION:
            Constructor for the _TextAnalyticsAICommon class.
            This class has common functions required for TextAnalytics 
            by the client side as well as BYO LLM.

        PARAMETERS:
            llm:
                Required Argument.
                Specifies the language model to be used.
                Types: TeradataAI instance

        RETURNS:
            None

        RAISES:
            None

        EXAMPLES:
            >>> _TextAnalyticsAICommon(llm=llm)

        """
        self.llm = llm
        self._table_name = None
        self.data = None
        self._base_dir = os.path.dirname(os.path.dirname(__file__))

    def _validate_arguments(self,
                            column,
                            data,
                            validate_matrix,
                            **kwargs):
        """
        DESCRIPTION:
            Internal method to validate the arguments passed to the text analytics
            functions.

        PARAMETERS:
            column:
                Required Argument.
                Specifies the column of the teradataml DataFrame
                containing the text content.
                Types: str

            data:
                Required Argument.
                Specifies the teradataml DataFrame containing the column to analyze.
                Types: teradataml DataFrame

            validate_matrix:
                Optional Argument.
                Specifies the matrix to be validated.
                Types: list

            kwargs:
                Optional Argument.
                Specifies the additional arguments passed to the function.
                Types: dict

        RETURNS:
            None

        RAISES:
            TeradataMlException, TypeError

        EXAMPLES:
            self._validate_arguments(column="text", data=data, validate_matrix=[])
        """
        # Validate missing required arguments.
        _Validators._validate_missing_required_arguments(validate_matrix)

        # Validate argument types
        _Validators._validate_function_arguments(validate_matrix)

        columns = UtilFuncs._as_list(column)
        for col in columns:
            if _Validators._check_isinstance(col, str):
                _Validators._validate_column_exists_in_dataframe([col], data._metaexpr)

    def _restore_table(self, result, persist=False):
        """
        DESCRIPTION:
            Internal function to restore a table in Vantage. It replaces any existing table
            with the same name. It generates unique table name with prefix 'TA_'. Then it
            uses the 'copy_to_sql' function to copy the data to the table in Vantage.
            If a table with the same name already exists, it is replaced.

        PARAMETERS:
            result:
                Required Argument.
                Specifies the data to be restored as a table in Vantage.
                Types: Pandas Dataframe, Teradataml DataFrame

            persist:
                Required Argument.
                Specifies whether to persist the output or not. When set to True, results are stored
                in permanent tables, otherwise in volatile tables.
                Default Value: False
                Types: bool

        RETURNS:
            None

        RAISES:
            None

        EXAMPLES:
            self._restore_table(output_df, persist=False)
        """
        # Generate a table name with a prefix of "ta_".
        # If persist is True, the table will not be garbage collected at the end of the session.
        self._table_name = UtilFuncs._generate_temp_table_name(prefix="ta_",
                                                               gc_on_quit=not persist)
        # Set index=True if result is pandas dataframe, else False.
        index = False
        if isinstance(result, pd.DataFrame):
            index = True

        # If a table with the same name already exists, it will be replaced.
        # If persist is True, the table will be permanent.
        copy_to_sql(df=result, table_name=self._table_name, if_exists='replace',
                    temporary=not persist, index=index)
        
    def _prepare_validate_matrix(self, **kwargs):
        """
        DESCRIPTION:
           Internal method to prepare the validation matrix.

        PARAMETERS:
           column:
               Required Argument.
               Specifies the column of the teradataml DataFrame
               containing the text content.
               Types: str

           data:
               Required Argument.
               Specifies the teradataml DataFrame containing the column to analyze.
               Types: teradataml DataFrame

        RETURNS:
           list

        RAISES:
           TeradataMlException, TypeError

        EXAMPLES:
           self._validate_arguments(column="text", data=data)
        """
        # Prepare a validation matrix.
        validate_matrix = []
        validate_matrix.append(["column", kwargs.get('column', None), False, (str, list), True])
        validate_matrix.append(["data", kwargs.get('data', None), False, (DataFrame)])
        validate_matrix.append(["persist", kwargs.get('persist', False), False, (bool)])
        return validate_matrix

class TextAnalyticsAI:
    """
    Class for performing text analytics using the given LLM inference endpoint.
    """
    def __init__(self, llm):
        """
        DESCRIPTION:
            Create an instance of TextAnalyticsAI to perform various text
            analytics tasks using the given LLM inference endpoint
            with the following methods:
                * analyze_sentiment
                * classify
                * detect_language
                * extract_key_phrases
                * mask_pii
                * recognize_entities
                * recognize_linked_entities
                * recognize_pii_entities
                * summarize
                * translate
                * embeddings

        PARAMETERS:
            llm:
                Required Argument.
                Specifies the language model to be used.
                Types: TeradataAI

        RETURNS:
            None

        RAISES:
            TypeError

        EXAMPLES:
            # Import the modules.
            >>> from teradatagenai import TeradataAI
            # Example 1: Create LLM endpoint and TextAnalyticsAI object
            #            using api_type = 'azure'.
            >>> llm_azure = TeradataAI(api_type = "azure",
                                       api_base = ""********"",
                                       api_version = "2000-11-35",
                                       api_key = "********",
                                       engine = "********",
                                       model_name = "gpt-3.5-turbo")
            >>> TA_obj = TextAnalyticsAI(llm=llm_azure)

            # Example 2: Create LLM endpoint and TextAnalyticsAI object
            #            using api_type = 'hugging_face'.
            >>> model_name = 'bhadresh-savani/distilbert-base-uncased-emotion'
            >>> model_args = {'transformer_class': 'AutoModelForSequenceClassification',
                              'task' : 'text-classification'}
            >>> llm = TeradataAI(api_type = "hugging_face",
                                 model_name = model_name,
                                 model_args = model_args)

            # Create a TextAnalyticsAI object.
            >>> obj = TextAnalyticsAI(llm=llm)
        """

        # Validate the 'llm' argument.
        _Validators._validate_function_arguments([["llm", llm, False,
                                                   (TeradataAI)]])

        from teradatagenai.text_analytics.TextAnalyticsAIHuggingFace\
            import _TextAnalyticsAIHuggingFace
        from teradatagenai.text_analytics.TextAnalyticsAIClient \
            import _TextAnalyticsAIClient

        mapping_dict = {'azure': _TextAnalyticsAIClient,
                        'aws': _TextAnalyticsAIClient,
                        'vertexai': _TextAnalyticsAIClient,
                        'hugging_face': _TextAnalyticsAIHuggingFace}

        # Wrapping the instance of '_TextAnalyticsAIClient' and
        # '_TextAnalyticsAIHuggingFace' into TextAnalyticsAI instance.
        self._wrapped_instance = mapping_dict[llm.api_type](llm)

    def __getattr__(self, name):
        """
        DESCRIPTION:
            Delegate attribute access to the wrapped instance.

        PARAMETERS:
            name:
                Required Argument.
                Specifies the parameter name to be retrieved.
                Types: str

        RETURNS:
            str

        RAISES:
            None
        """
        return getattr(self._wrapped_instance, name)