# ##################################################################
#
# Copyright 2024 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
#
# Primary Owner: Kesavaragavan B (kesavaragavan.b@teradata.com)
# Secondary Owner: Prafulla V Tekawade (prafulla.tekawade@teradata.com)
#
# Notes:
#   * This code is only for internal use.
#   * The code is used for performing text analytics on the client side
#     using LLM from azure, aws, vertexai.
# ##################################################################

import json
import os
import re
import sys
import warnings
import wikipedia
from teradatagenai.common import InferenceWarning
from teradatagenai.text_analytics.TextAnalyticsAI import _TextAnalyticsAICommon
from teradataml import DataFrame
from teradataml.dataframe.sql_interfaces import ColumnExpression
from teradataml.utils.validators import _Validators
from teradatasqlalchemy import VARCHAR

class _TextAnalyticsAIClient(_TextAnalyticsAICommon):
    """
    Class holds functions for performing text analytics on client machine.
    """
    def __init__(self, llm):
        """
        DESCRIPTION:
            Constructor for _TextAnalyticsAIClient class.

        PARAMETERS:
           llm:
               Required Argument.
               Specifies the language model to be used.
               Types: TeradataAI instance
        """
        super().__init__(llm)

        # Load JSON data.
        file_path = os.path.join(self._base_dir, 'prompt', 'prompt.json')
        with open(file_path) as f:
            self.__data = json.load(f)

    def __extract_column_to_documents(self, column, data=None):
        """
        DESCRIPTION:
            Internal method that extracts a specified column from a DataFrame and stores
            it in the '__documents' variable. If the column is specified as a string, it
            is extracted from the provided DataFrame. If the column is not a string, it
            is assumed to be a ColumnExpression and is used directly. The method then
            calls '_extract_table_to_pandas' to convert the column to a pandas DataFrame.
            If the '__documents' variable ends up as a string, it is converted to a list.

        PARAMETERS:
            column:
                Required Argument.
                Specifies the column to extract from the teradataml DataFrame.
                Types: str

            data:
                Required Argument.
                Specifies the teradataml DataFrame to extract the column.
                Types: teradataml DataFrame

        RETURNS:
            None

        RAISES:
            TeradataMlException, TypeError

        EXAMPLES:
            self.__extract_column_to_documents(column="text", data=data)
            self.__extract_column_to_documents(column=data.text)
        """
        # Extract the specified column and convert it to a pandas DataFrame.
        self._extract_table_to_pandas(column, data)
        # Check if the column is a string.
        if _Validators._check_isinstance(column, str):
            # If the column is a string, select the column from the DataFrame.
            documents = self.__pdf[column]
        else:
            # If the column is not a string, it will be a column expression.
            # In this case, select the column from the DataFrame using the name attribute of the column expression.
            documents = self.__pdf[column.name]
        # If the documents variable is a string, convert it to a list.
        if _Validators._check_isinstance(documents, str):
            documents = [documents]
        return documents

    def __issue_inference_warning(self, message=None):
        """
        DESCRIPTION:
            Issue an inference warning with a custom message at a specific index.

        PARAMETERS:
            message:
                Optional Argument.
                Specifies the message to display in the warning.
                Types: str

        RETURNS:
            None

        RAISES:
            None

        EXAMPLES:
            self.__issue_inference_warning(message="This is a custom warning message.")
        """
        if message is None:
            message = "Processing the request returned None for one or more rows."
        # Save the original showwarning function
        # This is done to ensure that after our custom warning handling is done,
        # we can restore the original functionality
        original_showwarning = warnings.showwarning

        # Replace showwarning with our custom function
        # This allows us to control how warnings are displayed during the execution
        # of our specific code
        warnings.showwarning = InferenceWarning.custom_showwarning
        # Use a context manager to temporarily modify the behavior of warnings
        with warnings.catch_warnings():
            # Set the warning filter to 'always' within this context,
            # so all warnings will be displayed
            warnings.simplefilter('always')
            # Issue a warning with a custom message
            warnings.warn(InferenceWarning(f"{message}"))
            # After all items have been processed, restore the original warning behavior
        warnings.showwarning = original_showwarning

    def _extract_table_to_pandas(self, column, data=None):
        """
        DESCRIPTION:
            Method extracts a table from a given DataFrame column and converts it into
            a pandas DataFrame.

        PARAMETERS:
            column:
                Required Argument.
                Specifies the column of the teradataml DataFrame containing the text content
                Types: str

            data:
                Required Argument.
                Specifies the teradataml DataFrame containing the column to analyze.
                Types: teradataml DataFrame

        RETURNS:
            None

        RAISES:
            TeradataMlException

        EXAMPLES:
            self._extract_table_to_pandas(data['column_name'])
        """
        if _Validators._check_isinstance(column, ColumnExpression):
            data = DataFrame(column.table.name)
            # Validate the column type.
            _Validators._validate_column_type(data, column.name, column.name, [VARCHAR])
        else:
            _Validators._validate_column_type(data, column, column, [VARCHAR])
        self._table_name = data._table_name
        self.__pdf = data.to_pandas()

    def _wiki_crawl(self, search_term, num_sentences=4, num_search_results=5):
        """
        DESCRIPTION:
            This private method is used to search Wikipedia for a given term and
            count its frequency in the summaries of the top search results.

        PARAMETERS:
            search_term:
                Required Argument.
                Specifies the term to search for on Wikipedia.
                Types: str

            num_sentences:
                Optional Argument.
                Specifies the number of sentences to include from each Wikipedia summary.
                Default Value: 4
                Types: int

            num_search_results:
                Optional Argument.
                Specifies the number of search results to consider.
                Default Value: 5
                Types: int

        RETURNS:
            dict

        RAISES:
            None

        EXAMPLES:
            self._wiki_crawl(search_term="Python", num_sentences=3, num_search_results=10)
        """
        results = wikipedia.search(search_term, results=num_search_results)

        wfreq = {}
        wfreq[search_term] = 0

        for res in results:
            try:
                # Finding result for the search.
                result = wikipedia.summary(res, sentences=num_sentences)

                text = result.lower()
                words = []
                words = text.split()
                wfreq[search_term] += text.count(search_term.lower())
            except:
                pass
        return wfreq

    def analyze_sentiment(self, column, data=None, **kwargs):
        """
        DESCRIPTION:
            Analyze the sentiment of the text in the specified column of a DataFrame.
            Sentiment Analysis is a sub-field of Natural Language Processing (NLP) that
            tries to identify and extract opinions within a given text. The goal of
            sentiment analysis is to determine the attitude of a speaker or a writer with
            respect to some topic or the overall contextual polarity of a document.
            Based on the text analysis, the sentiment can be positive, negative, or
            neutral. If any error or exception occurs during the sentiment analysis, the
            result is set to None.

        PARAMETERS:
            column:
                Required Argument.
                Specifies the column of the teradataml DataFrame containing the text content
                to analyze the sentiment.
                Types: str

            data:
                Required Argument.
                Specifies the teradataml DataFrame containing the column specified
                in "column" to analyze the content from.
                Types: teradataml DataFrame

            persist:
                Optional Argument.
                Specifies whether to persist the output or not. When set to True, results are stored
                in permanent tables, otherwise in volatile tables.
                Default Value: False
                Types: bool

            show_warning:
                Optional Argument.
                Specifies whether to display warnings during execution. If set to True,
                Runtime Inference warnings are shown. Otherwise, InferenceWarnings
                are suppressed. In either case, a row with 'NaN' values is added.
                Default Value: True
                Types: bool

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException, TypeError, ValueError


        EXAMPLES:
            # Import the modules and create a teradataml DataFrame.
            >>> from teradataml import DataFrame
            >>> from teradatagenai import TeradataAI, TextAnalyticsAI, load_data
            >>> load_data('employee', 'employee_data')
            >>> data = DataFrame('employee_data')
            >>> df_reviews = data.select(["employee_id", "employee_name", "reviews"])

            # Example 1: Analyze sentiment of food reviews in the 'reviews' column of a
            #            teradataml DataFrame using Azure OpenAI. Reviews are passed as a
            #            column name along with the teradataml DataFrame.
            # Create LLM endpoint.
            >>> llm_azure = TeradataAI(api_type = "azure",
                  api_base = "********",
                  api_version = "*********",
                  api_key = "********",
                  engine_id = "*********",
                  model_name = "gpt-3.5-turbo")
            # Create a TextAnalyticsAI object.
            >>> obj = TextAnalyticsAI(llm=llm_azure)
            >>> obj.analyze_sentiment(column="reviews", data=df_reviews, persist=True)

            # Example 2: Analyze sentiment of food reviews in the 'reviews' column of a
            #            teradataml DataFrame using AWS Bedrock. Reviews are passed as a
            #            column name along with the teradataml DataFrame.
            # Create LLM endpoint.
            >>> llm_aws = TeradataAI(api_type = "aws",
                  api_key = "********",
                  engine_id = "********",
                  api_region = "us-west-2",
                  model_name = "anthropic.claude-v2",
                  model_args = {"max_tokens_to_sample": 2048,
                                "temperature": 0,
                                "top_k": 250,
                                "top_p": 1})
            # Create a TextAnalyticsAI object.
            >>> obj = TextAnalyticsAI(llm=llm_aws)
            >>> obj.analyze_sentiment(column="reviews", data=df_reviews, persist=True)

            # Example 3: Analyze sentiment of food reviews in the 'reviews' column of a
            #            teradataml DataFrame using Google VertexAI. Reviews are passed as a
            #            column name along with the teradataml DataFrame.
            # Create LLM endpoint.
            >>> llm_vertex = TeradataAI(api_type="vertexai",
                                        deployment_id=<provide your VertexAI project name>,
                                        model_name="gemini-1.5-flash-001",
                                        api_region="us-central1",
                                        enable_safety=False,
                                        vertexai_cred="C:/Users/credential.cred",
                                        model_args={"temperature": 1,
                                                    "top_p": 0.95}
                                        )
            # Create a TextAnalyticsAI object.
            >>> obj = TextAnalyticsAI(llm=llm_vertex)
            >>> obj.analyze_sentiment(column="reviews", data=df_reviews)
        """
        # Check if the show_warning is present in the kwargs.
        show_warning = kwargs.get("show_warning", True)
        persist = kwargs.get("persist", False)
        # Create basic validation matrix
        # Validations
        validate_matrix = self._prepare_validate_matrix(column=column, data=data,
                                                        **kwargs)
        validate_matrix.append(["show_warning", show_warning, False, (bool)])
        self._validate_arguments(column=column, data=data, validate_matrix=validate_matrix)

        # Initialize a list to store the sentiment analysis results.
        result = []
        documents = self.__extract_column_to_documents(column, data)
        warning = False
        # For each document, analyze the sentiment and store the result in the list.
        for doc in documents:
            try:
                if len(doc) < 1:
                    result.append(None)
                    falg = True
                    continue

                # The 'answer' method of the 'llm' object is called with a formatted
                # string that includes the current sentence.
                answer = self.llm.answer(
                    self.__data["prompts"]["analyze_sentiment"].format(sent=doc))
                # Check if the answer is 'nan' or an empty string.
                if 'nan' in answer.lower() or answer.strip() == '':
                    answer = None
                    warning = True
                result.append(answer)
            except Exception as e:
                # If an error occurs during the sentiment analysis (for example, if
                # the 'answer' method call fails), None is appended to the list.
                if show_warning:
                    self.__issue_inference_warning(str(e))
                result.append(None)
                continue
        # Issue a warning if the `warning` variable is set to True.
        if warning:
            self.__issue_inference_warning()

        # Add the sentiment analysis results to the DataFrame.
        self.__pdf["Sentiment"] = result

        # Restore the table and return the DataFrame.
        self._restore_table(result=self.__pdf, persist=persist)
        return DataFrame(self._table_name)

    def detect_language(self, column, data=None, language=None, **kwargs):
        """
        DESCRIPTION:
            Detect the language of the text data in a specified DataFrame column. It
            processes each text entry in the specified column and assigns a language
            label to it. The languages supported align with those supported by the
            respective large language models (LLMs) in use. In case of any error or
            exception during the language detection process, the result is set to None.

        PARAMETERS:
            column:
                Required Argument.
                Specifies the column of the teradataml DataFrame containing the text
                content to detect the language.
                Types: str

            data:
                Required Argument.
                Specifies the teradataml DataFrame containing the column specified
                in "column" to analyze the content from.
                Types: teradataml DataFrame

            language:
                Optional Argument.
                Specifies the languages for detection. If no specific language is
                provided, the function will attempt to automatically detect the
                language of the text to the best of its ability. It can also detect
                languages that are not specified in the parameter.
                Types: list,str

            persist:
                Optional Argument.
                Specifies whether to persist the output or not. When set to True, results are stored
                in permanent tables, otherwise in volatile tables.
                Default Value: False
                Types: bool

            show_warning:
                Optional Argument.
                Specifies whether to display warnings during execution. If set to True,
                Runtime Inference warnings are shown. Otherwise, InferenceWarnings
                are suppressed. In either case, a row with 'NaN' values is added.
                Default Value: True
                Types: bool

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException, TypeError, ValueError

        EXAMPLES:
            # Import the modules and create a teradataml DataFrame.
            >>> from teradataml import DataFrame
            >>> from teradatagenai import TeradataAI, TextAnalyticsAI, load_data
            >>> load_data('employee', 'employee_data')
            >>> data = DataFrame('employee_data')
            >>> df_quotes = data.select(["employee_id", "employee_name", "quotes"])

            # Example 1: Detect the language of text in the 'quotes' column of a teradataml DataFrame
            #            using Azure OpenAI. The text for language detection is passed as a column
            #            name along with the teradataml DataFrame.
            # Create LLM endpoint.
            >>> llm_azure = TeradataAI(api_type = "azure",
                         api_base = ""********"",
                         api_version = "2000-11-35",
                         api_key = ""********"",
                         engine_id = ""********"",
                         model_name = "gpt-3.5-turbo")
            # Create a TextAnalyticsAI object.
            >>> obj = TextAnalyticsAI(llm=llm_azure)
            >>> obj.detect_language(column="quotes", data=df_quotes)

            # Example 2: Detect the language of text in the 'quotes' column of a teradataml DataFrame
            #            using AWS BedRock. The text for language detection is passed as a column
            #            name along with the teradataml DataFrame. A list of languages to consider
            #            during detection is passed in the 'language' argument.
            # AWS BedRock credentials.
            >>> llm_aws = TeradataAI(api_type = "aws",
                                    api_key = "*********************",
                                    engine_id = "**********",
                                    api_region = "us-west-2",
                                    model_name = "anthropic.claude-v2",
                                    model_args = {"max_tokens_to_sample": 2048,
                                                    "temperature": 0,
                                                    "top_k": 250,
                                                    "top_p": 1})

            # Create a TextAnalyticsAI object.
            >>> obj = TextAnalyticsAI(llm=llm_aws)
            # Detecting the language of the 'quotes' column in the 'df_quotes' teradataml DataFrame.
            >>> obj.detect_language(column="quotes", data=df_quotes, langauge=["Chinese_Simplified","French"], persist=True)

            # Example 3: Detect the language of text in the 'quotes' column of a teradataml DataFrame
            #            using Google VertexAI. The text for language detection is passed as a column
            #            name along with the teradataml DataFrame. A specific language is passed in the
            #            'language' argument.
            # Create LLM endpoint.
            >>> llm_vertex = TeradataAI(api_type="vertexai",
                                        deployment_id=<provide your VertexAI project name>,
                                        model_name="gemini-1.5-flash-001",
                                        api_region="us-central1",
                                        enable_safety=False,
                                        vertexai_cred="C:/Users/credential.cred",
                                        model_args={"temperature": 1,
                                                    "top_p": 0.95}
                                        )
            # Create a TextAnalyticsAI object.
            >>> obj = TextAnalyticsAI(llm=llm_vertex)
            # Detecting the language of the 'quotes' column in the 'df_quotes' teradataml DataFrame.
            >>> obj.detect_language(column="quotes", data=df_quotes, language="French")
        """

        # Check if the show_warning is present in the kwargs.
        show_warning = kwargs.get("show_warning", True)
        persist = kwargs.get("persist", False)

        if _Validators._check_isinstance(language, str):
            language = [language]

        # Create basic validation matrix
        validate_matrix = self._prepare_validate_matrix(column=column, data=data,
                                                        **kwargs)
        validate_matrix.append(["show_warning", show_warning, False, (bool)])
        validate_matrix.append(["language", language, True, (str, list)])
        self._validate_arguments(column=column, data=data, validate_matrix=validate_matrix)

        # Initialize a list to store the language detection results.
        result = []
        documents = self.__extract_column_to_documents(column, data)
        warning = False
        # For each document, analyze the sentiment and store the result in the list.
        for doc in documents:
            try:
                if len(doc) < 1:
                    result.append(None)
                    warning = True
                    continue
                # The 'answer' method of the 'llm' object is called with a formatted string that includes the current sentence.
                answer = self.llm.answer(self.__data["prompts"]["detect_language"].format(language=language, sent=doc))
                if 'nan' in answer.lower() or answer.strip() == '':
                    answer = None
                    warning = True
                result.append(answer)
            except Exception as e:
                # If an error occurs during the language detection (for example, if the 'answer' method call fails),
                # None is appended to the result list as a placeholder.
                if show_warning:
                    self.__issue_inference_warning(str(e))
                result.append(None)
                continue

                # Issue a warning if the `warning` variable is set to True.
        if warning:
            self.__issue_inference_warning()
        # Add the language detection results to the DataFrame.
        self.__pdf["Language"] = result

        # Restore the table and return the DataFrame.
        self._restore_table(result=self.__pdf, persist=persist)
        return DataFrame(self._table_name)

    def classify(self, column, data, labels=None, multi_label=False, **kwargs):
        """
        DESCRIPTION:
            Text classification is a LLM powered approach that classifies unstructured
            text using a set of predetermined labels. Almost any kind of text can be
            classified with the classify() function. classify() function supports both
            multi-class and multi-label classification. In case of any error or
            exception during the classification process, the result is set to None.

        PARAMETERS:
            column:
                Required Argument.
                Specifies the column of the teradataml DataFrame containing the text
                content to classify.
                Types: str

            data:
                Required Argument.
                Specifies the teradataml DataFrame containing the column specified
                in "column" to classify the content.
                Types: teradataml DataFrame

            labels:
                Required Argument.
                Specifies the set of labels used to categorize the text.
                It takes either a list of labels or a list of multiple labels for
                classification.
                Types: str or List of str

            multi_label:
                Optional Argument.
                Specifies whether the classification is multi-label or not.
                When set to True, the multi-label classification is performed on the text.
                Otherwise, multi-class classification is performed.
                Note:
                    * In multi-label classification, different labels may be selected from
                      various groups of labels when a list of grouped labels is passed.
                Default Value: False
                Types: bool

            persist:
                Optional Argument.
                Specifies whether to persist the output or not. When set to True, results are stored
                in permanent tables, otherwise in volatile tables.
                Default Value: False
                Types: bool

            show_warning:
                Optional Argument.
                Specifies whether to display warnings during execution. If set to True,
                Runtime Inference warnings are shown. Otherwise, InferenceWarnings
                are suppressed. In either case, a row with 'NaN' values is added.
                Default Value: True
                Types: bool

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException, TypeError, ValueError

        EXAMPLES:
            # Import the modules and create a teradataml DataFrame.
            >>> from teradataml import DataFrame
            >>> from teradatagenai import TeradataAI, TextAnalyticsAI, load_data
            >>> load_data('employee', 'employee_data')
            >>> data = DataFrame('employee_data')
            >>> df_reviews = data.select(["employee_id", "employee_name", "reviews"])
            >>> df_classify_articles = data.select(["employee_id", "articles"])

            # Example 1: Classify the text in the 'articles' column of a teradataml DataFrame
            #            using Azure OpenAI. The text for classification is passed as a column
            #            name along with the teradataml DataFrame. In addition, List of labels
            #            are passed for classification.
            # Create LLM endpoint.
            >>> llm_azure = TeradataAI(api_type = "azure",
                         api_base = "********",
                         api_version = "2000-11-35",
                         api_key = "********",
                         engine_id = "********",
                         model_name = "gpt-3.5-turbo")
            # Create a TextAnalyticsAI object.
            >>> obj = TextAnalyticsAI(llm=llm_azure)
            # Classification is performed on the 'articles' column in
            # the 'df_classify_articles' teradataml DataFrame.
            >>> obj.classify("articles", df_classify_articles, labels=["Medical",
                                                                       "historical-news",
                                                                       "Environment",
                                                                       "technology",
                                                                       "Games"])

            # Example 2: Perform multi-label classification for the text in the 'articles' column
            #            of a teradataml DataFrame using AWS BedRock. The text for classification
            #            is passed as a column name along with the teradataml DataFrame. A list of
            #            labels is passed in the 'labels' argument.
            # AWS BedRock credentials.
            >>> llm_aws = TeradataAI(api_type = "aws",
                                    api_key = "*********************",
                                    engine_id = "**********",
                                    api_region = "us-west-2",
                                    model_name = "anthropic.claude-v2",
                                    model_args = {"max_tokens_to_sample": 2048,
                                                    "temperature": 0,
                                                    "top_k": 250,
                                                    "top_p": 1})

            # Create a TextAnalyticsAI object.
            >>> obj = TextAnalyticsAI(llm=llm_aws)
            # Multi-Label classification is performed on the 'articles' column in
            # the 'df_classify_articles' teradataml DataFrame.
            >>> obj.classify("articles",
                             df_classify_articles,
                             labels=["Medical",
                                     "historical-news",
                                     "Environment",
                                     "technology",
                                     "Games"],
                             multi_label=True,
                             persist=True)

            # Example 3: Classify the text in the 'articles' column of a teradataml DataFrame
            #            using Google VertexAI. The text for classification is passed as a column
            #            name along with the teradataml DataFrame. A list of labels is passed
            #            in the 'labels' argument.
            # Create LLM endpoint.
            >>> llm_vertex = TeradataAI(api_type="vertexai",
                                        deployment_id=<provide your VertexAI project name>,
                                        model_name="gemini-1.5-flash-001",
                                        api_region="us-central1",
                                        enable_safety=False,
                                        vertexai_cred="C:/Users/credential.cred",
                                        model_args={"temperature": 1,
                                                    "top_p": 0.95}
                                        )
            # Create a TextAnalyticsAI object.
            >>> obj = TextAnalyticsAI(llm=llm_vertex)
            # Grouped label classification is performed on the 'articles' column in the
            # 'df_classify_articles' teradataml DataFrame.
            >>> obj.classify("articles",
                             df_classify_articles,
                             labels=[["Medical", "Hospitality", "Healthcare"],
                                     ["historical-news", "Games"],
                                     ["Environment", "Technology"],
                                     ["Games"]])

            # Example 4: Perform multi-label classification in the 'articles' column of a
            #            teradataml DataFrame. A list of multiple labels are passed along
            #            with 'multi_label' argument is set to True.
            # Create LLM endpoint.
            >>> llm_vertex = TeradataAI(api_type="vertexai",
                                        deployment_id=<provide your VertexAI project name>,
                                        model_name="gemini-1.5-flash-001",
                                        api_region="us-central1",
                                        enable_safety=False,
                                        vertexai_cred="C:/Users/credential.cred",
                                        model_args={"temperature": 1,
                                                    "top_p": 0.95}
                                        )
        """

        # Check if the show_warning is present in the kwargs.
        show_warning = kwargs.get("show_warning", True)
        persist = kwargs.get("persist", False)

        # Validations
        # Create basic validation matrix
        validate_matrix = self._prepare_validate_matrix(column=column, data=data,
                                                        **kwargs)
        validate_matrix.append(["show_warning", show_warning, False, (bool)])
        validate_matrix.append(["labels", labels, False, (list), True])
        validate_matrix.append(["multi_label", multi_label, True, (bool)])
        self._validate_arguments(column=column, data=data, validate_matrix=validate_matrix)


        if len(labels) < 2:
            raise ValueError("The 'labels' argument must contain at least one label.")
        if any(len(label) == 0 for label in labels):
            raise ValueError("The 'labels' argument must contain list of non-empty label.")

        # Check if labels contains both string and list.
        # When both list and string present convert all string to list of string.
        if len(set(type(label) for label in labels)) > 1:
            labels = [[label] if isinstance(label, str) else label for label in labels]

        # Initialize a list to store the classification results.
        result = []
        documents = self.__extract_column_to_documents(column, data)
        warning = False

        # Check if the classification is multi-label or multi-class and choose right prompt.
        if multi_label:
            prompt = self.__data["prompts"]["classify_multi_class"]
        else:
            prompt = self.__data["prompts"]["classify"] if isinstance(labels[0], str) \
                else self.__data["prompts"]["classify_grouped_class"]

        # For each document, classify and store the result in the list.
        for doc in documents:
            try:
                if len(doc) < 1:
                    result.append(None)
                    warning = True
                    continue
                # The 'answer' method of the 'llm' object is called with a formatted
                # string that includes the current sentence.
                answer = self.llm.answer(prompt.format(labels=str(labels).upper(), sent=doc))
                if 'nan' in answer.lower() or answer.strip() == '':
                    answer = None
                    warning = True
                result.append(answer)
            except Exception as e:
                # If an error occurs during the classification(for example, if the
                # 'answer' method call fails),
                # None is appended to the result list as a placeholder.
                if show_warning:
                    self.__issue_inference_warning(str(e))
                result.append(None)
                continue

        print(result)
        # Issue a warning if the `warning` variable is set to True.
        if warning:
            self.__issue_inference_warning()
        # Add the classification results to the DataFrame.
        self.__pdf["Labels"] = result

        # Restore the table and return the DataFrame.
        self._restore_table(result=self.__pdf, persist=persist)
        return DataFrame(self._table_name)

    def extract_key_phrases(self, column, data=None, **kwargs):
        """
        DESCRIPTION:
            Extract key phrases from the text in the specified column of a DataFrame.
            These key phrases, often referred to as "keywords",are words or phrases
            that best describe the subject or themes underlying the text data. It
            analyzes the text and recognizes words or phrases that appear significantly
            often and carry substantial meaning. These could include names, locations,
            technical terms, or any other significant nouns or phrases.
            If any error or exception occurs during the key phrase extraction process,
            the result is set to None.

        PARAMETERS:
            column:
                Required Argument.
                Specifies the column of the teradataml DataFrame containing the text content
                to extract key phrases.
                Types: str

            data:
                Required Argument.
                Specifies the teradataml DataFrame containing the column specified
                in "column" to analyze the content from.
                Types: teradataml DataFrame

            persist:
                Optional Argument.
                Specifies whether to persist the output or not. When set to True, results are stored
                in permanent tables, otherwise in volatile tables.
                Default Value: False
                Types: bool

            show_warning:
                Optional Argument.
                Specifies whether to display warnings during execution. If set to True,
                Runtime Inference warnings are shown. Otherwise, InferenceWarnings
                are suppressed. In either case, a row with 'NaN' values is added.
                Default Value: True
                Types: bool

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException, TypeError, ValueError

        EXAMPLES:
            # Import the modules and create a teradataml DataFrame.
            >>> from teradataml import DataFrame
            >>> from teradatagenai import TeradataAI, TextAnalyticsAI, load_data
            >>> load_data('employee', 'employee_data')
            >>> data = DataFrame('employee_data')
            >>> df_articles = data.select(["employee_id", "employee_name", "articles"])

            # Example 1: Extract key phrases from articles in the 'articles' column
            #            of a teradataml DataFrame using Azure OpenAI. Articles are
            #            passed as a column name along with the teradataml DataFrame.
            # Create LLM endpoint.
            >>> llm_azure = TeradataAI( api_type = "azure",
                                        api_base = "******************",
                                        api_version = "2023-05-15",
                                        api_key = "**************",
                                        engine_id="******",
                                        model_name="gpt-3.5-turbo")
            # Create a TextAnalyticsAI object.
            >>> obj = TextAnalyticsAI(llm=llm_azure)
            >>> obj.extract_key_phrases(column="articles", data=df_articles, persist=True)

            # Example 2: Extract key phrases from articles in the 'articles' column
            #             of a teradataml DataFrame using AWS BedRock. Articles are
            #            passed as a column name along with the teradataml DataFrame.
            # Create LLM endpoint.
            >>> llm_aws = TeradataAI(api_type = "aws",
                  api_key = "********",
                  engine_id = "********",
                  api_region = "us-west-2",
                  model_name = "anthropic.claude-v2",
                  model_args = {"max_tokens_to_sample": 2048,
                                "temperature": 0,
                                "top_k": 250,
                                "top_p": 1})
            # Create a TextAnalyticsAI object.
            >>> obj = TextAnalyticsAI(llm=llm_aws)
            >>> obj.extract_key_phrases(column="articles", data=df_articles)

            # Example 3: Extract key phrases from articles in the 'articles' column
            #            of a teradataml DataFrame using Google VertexAI. Articles are passed
            #            as a column name along with the teradataml DataFrame.
            # Create LLM endpoint.
            >>> llm_vertex = TeradataAI(api_type="vertexai",
                                        deployment_id=<provide your VertexAI project name>,
                                        model_name="gemini-1.5-flash-001",
                                        api_region="us-central1",
                                        enable_safety=False,
                                        vertexai_cred="C:/Users/credential.cred",
                                        model_args={"temperature": 1,
                                                    "top_p": 0.95}
                                        )
            # Create a TextAnalyticsAI object.
            >>> obj = TextAnalyticsAI(llm=llm_vertex)
            >>> obj.extract_key_phrases(column="articles", data=df_articles)
        """
        # Check if the show_warning is present in the kwargs.
        show_warning = kwargs.get("show_warning", True)
        persist = kwargs.get("persist", False)

        # Validations
        # Create basic validation matrix
        validate_matrix = self._prepare_validate_matrix(column=column, data=data,
                                                        **kwargs)
        validate_matrix.append(["show_warning", show_warning, False, (bool)])
        self._validate_arguments(column=column, data=data, validate_matrix=validate_matrix)

        # Initialize a list to store the key phrase extraction results.
        result = []
        documents = self.__extract_column_to_documents(column, data)
        warning = False
        # For each document, extract key phrases and store the results in the list.
        for doc in documents:
            try:
                if len(doc) < 1:
                    result.append(None)
                    warning = True
                    continue
                # The 'answer' method of the 'llm' object is called with a formatted
                # string that includes the current sentence.
                answer = self.llm.answer(
                    self.__data["prompts"]["extract_key_phrases"].format(sent=doc))
                if 'nan' in answer.lower() or answer.strip() == '':
                    answer = None
                    warning = True
                result.append(answer)
            except Exception as e:
                # If an error occurs during the extraction of key phrases (for example,
                # if the 'answer' method call fails), None is appended to the list.
                if show_warning:
                    self.__issue_inference_warning(str(e))
                result.append(None)
                continue

        # Issue a warning if the `warning` variable is set to True.
        if warning:
            self.__issue_inference_warning()
        # Add the key phrase extraction results to the DataFrame.
        self.__pdf["Key_Phrases"] = result

        # Restore the table and return the DataFrame.
        self._restore_table(result=self.__pdf, persist=persist)
        return DataFrame(self._table_name)

    def mask_pii(self, column, data=None, **kwargs):
        """
        DESCRIPTION:
            Recognize and mask Personally Identifiable Information (PII) entities within
            a specified column of a DataFrame. PII encompasses any data that could
            potentially identify a specific individual. Direct identifiers are explicit
            pieces of information that can uniquely identify an individual. These include
            sensitive data such as names, email addresses and phone numbers. Indirect
            identifiers, on the other hand, are pieces of information that may not
            identify an individual on their own but can do so when combined with other
            data. Examples include dates or unique device identifiers. The function is
            capable of recognizing a diverse set of PII entities including 'Name',
            'address', 'contact numbers', 'date/time' and 'serial numbers'. The output
            has two columns 'PII_Entities' which contains the name, start position and
            the length of the identified entity and 'Masked_Phrase' where PII entities
            are masked with astrick(*) sign and returned. In case of any error or
            exception during the PII entity recognition process, the result is set to
            None.
            Note:
                This function handles sensitive information and is compatible with Google
                Vertex AI exclusively when the `enable_safety` parameter is set to False.

        PARAMETERS:
            column:
                Required Argument.
                Specifies the column of the teradataml DataFrame containing the text
                content to recognize and mask pii entities.
                Types: str

            data:
                Required Argument.
                Specifies the teradataml DataFrame containing the column specified
                in "column" to analyze the content from.
                Types: teradataml DataFrame

            persist:
                Optional Argument.
                Specifies whether to persist the output or not. When set to True, results are stored
                in permanent tables, otherwise in volatile tables.
                Default Value: False
                Types: bool

            show_warning:
                Optional Argument.
                Specifies whether to display warnings during execution. If set to True,
                Runtime Inference warnings are shown. Otherwise, InferenceWarnings
                are suppressed. In either case, a row with 'NaN' values is added.
                Default Value: True
                Types: bool

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException, TypeError, ValueError

        EXAMPLES:
            # Import the modules and create a teradataml DataFrame.
            >>> from teradataml import DataFrame
            >>> from teradatagenai import TeradataAI, TextAnalyticsAI, load_data
            >>> load_data('employee', 'employee_data')
            >>> data = DataFrame('employee_data')
            >>> df_employeeData = data.select(["employee_id", "employee_name", "employee_data"])

            # Example 1: Recognize and mask PII entities in the 'employee_data' column of a
            #            teradataml DataFrame using Azure OpenAI. The text containing potential
            #            PII like names, addresses, credit card numbers, etc., is passed as a
            #            olumn name along with the teradataml DataFrame.
            # Create LLM endpoint.
            >>> llm_azure = TeradataAI( api_type = "azure",
                                        api_base = "**********************",
                                        api_version = "2023-05-15",
                                        api_key = "*******************",
                                        engine_id="******",
                                        model_name="gpt-3.5-turbo")

            # Create a TextAnalyticsAI object.
            >>> obj = TextAnalyticsAI(llm=llm_azure)
            >>> obj.masking_pii(column="employee_data", data=df_employeeData)

            # Example 2: Recognize and mask PII entities in the 'employee_data' column of a
            #            teradataml DataFrame using AWS BedRock. The text containing potential
            #            PII like names, addresses, credit card numbers, etc., is passed as a
            #            column name along with the teradataml DataFrame.
            # AWS BedRock credentials.
            >>> llm_aws = TeradataAI(api_type = "aws",
                                    api_key = "*********************",
                                    engine_id = "*************",
                                    api_region = "us-west-2",
                                    model_name = "anthropic.claude-v2",
                                    model_args = {"max_tokens_to_sample": 2048,
                                                    "temperature": 0,
                                                    "top_k": 250,
                                                    "top_p": 1})
            # Create a TextAnalyticsAI object.
            >>> obj = TextAnalyticsAI(llm=llm_aws)
            >>> obj.mask_pii_(column="employee_data", data=df_employeeData, persist=True)

            # Example 3: Recognize and mask PII entities in the 'employee_data' column of a
            #            teradataml DataFrame using Google VertexAI. The text containing potential
            #            PII like names, addresses, credit card numbers, etc., is passed as a
            #            column name along with the teradataml DataFrame.
            # Create LLM endpoint.
            >>> llm_vertex = TeradataAI(api_type="vertexai",
                                        deployment_id=<provide your VertexAI project name>,
                                        model_name="gemini-1.5-flash-001",
                                        api_region="us-central1",
                                        enable_safety=False,
                                        vertexai_cred="C:/Users/credential.cred",
                                        model_args={"temperature": 1,
                                                    "top_p": 0.95}
                                        )
            # Create a TextAnalyticsAI object.
            >>> obj = TextAnalyticsAI(llm=llm_vertex)
            >>> obj.mask_pii(column="employee_data", data=df_employeeData)
        """
        # Check if the show_warning is present in the kwargs.
        show_warning = kwargs.get("show_warning", True)
        persist = kwargs.get("persist", False)

        # Validations
        # Create basic validation matrix
        validate_matrix = self._prepare_validate_matrix(column=column, data=data,
                                                        **kwargs)
        validate_matrix.append(["show_warning", show_warning, False, (bool)])
        self._validate_arguments(column=column, data=data, validate_matrix=validate_matrix)

        documents = self.__extract_column_to_documents(column, data)
        # Call recognize_pii_entities to get the recognized PII entities.
        self.recognize_pii_entities(column=column, data=data, persist=persist, show_warning=show_warning)

        # Initialize lists to store the masked sentences.
        masked_sentence = []

        # For each sentence, mask the recognized PII entities.
        for sentence, entities in zip(documents, self.__pii_entities):
            if entities is None:
                masked_sentence.append(sentence)
                continue
            temp_sent = sentence
            for entity in entities.split(","):
                if any(["start_position" in entity, "length" in entity.lower(),
                        "start" in entity.lower(), "position" in entity.lower()]):
                    pass
                else:
                    parts = entity.split("=")
                    if len(parts) != 2:
                        continue
                    _entity, _temp_info = entity.split("=")
                    _info = _temp_info.replace('"', "").strip("'")
                    if _info in temp_sent:
                        temp_sent = temp_sent.replace(_info, "*" * len(_info))
            masked_sentence.append(temp_sent)

        # Add the masked sentences to the DataFrame.
        self.__pdf["Masked_Phrase"] = masked_sentence

        # Restore the table and return the DataFrame.
        self._restore_table(result=self.__pdf, persist=persist)
        return DataFrame(self._table_name)

    def recognize_entities(self, column, data=None, **kwargs):
        """
        DESCRIPTION:
            Identify and extract various types of entities from the text data in the
            specified column of a DataFrame. By identifying these entities, we can gain
            a more nuanced understanding of the text's context and semantic structure.
            It provides an efficient way to extract this valuable information, enabling
            users to quickly analyze and interpret large volumes of text. The function
            is capable of recognizing a diverse set of entities including 'people',
            'places', 'products', 'organizations', 'date/time', 'quantities',
            'percentages', 'currencies', and 'names'. In case of any error or exception
            during the entity recognition process, the result is set to None.

        PARAMETERS:
            column:
                Required Argument.
                Specifies the column of the teradataml DataFrame containing the text content
                to recognize entities.
                Types: str

            data:
                Required Argument.
                Specifies the teradataml DataFrame containing the column specified
                in "column" to analyze the content from.
                Types: teradataml DataFrame

            persist:
                Optional Argument.
                Specifies whether to persist the output or not. When set to True, results are stored
                in permanent tables, otherwise in volatile tables.
                Default Value: False
                Types: bool

            show_warning:
                Optional Argument.
                Specifies whether to display warnings during execution. If set to True,
                warnings will be shown, allowing observation of errors. If False, warnings
                will be suppressed. In either case, a row with 'NaN' values is added.
                Default Value: True
                Types: bool

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException, TypeError, ValueError

        EXAMPLES:
            # Import the modules and create a teradataml DataFrame.
            >>> from teradataml import DataFrame
            >>> from teradatagenai import TeradataAI, TextAnalyticsAI, load_data
            >>> load_data('employee', 'employee_data')
            >>> data = DataFrame('employee_data')
            >>> df_articles = data.select(["employee_id", "employee_name", "articles"])

            # Example 1: Recognize entities from articles in the 'articles' column
            #            of a teradataml DataFrame using Azure OpenAI. Articles are
            #            passed as column name along with the teradataml DataFrame.
            # Create LLM endpoint.
            >>> llm_azure = TeradataAI( api_type = "azure",
                                        api_base = "**************",
                                        api_version = "2023-05-15",
                                        api_key = "**************",
                                        engine_id="******",
                                        model_name="gpt-3.5-turbo")

            # Create a TextAnalyticsAI object.
            >>> obj = TextAnalyticsAI(llm=llm_azure)
            >>> obj.recognize_entities(column="articles", data=df_artciles)

            # Example 2: Recognize entities from articles in the 'articles' column
            #            of a teradataml DataFrame using AWS BedRock. Articles are
            #            passed as column name along with the teradataml DataFrame.
            # AWS BedRock credentials.
            >>>llm_aws = TeradataAI(api_type = "aws",
                  api_key = "******************",
                  engine_id = "**********",
                  api_region = "us-west-2",
                  model_name = "anthropic.claude-v2",
                  model_args = {"max_tokens_to_sample": 2048,
                                "temperature": 0,
                                "top_k": 250,
                                "top_p": 1})
            # Create a TextAnalyticsAI object.
            >>> obj = TextAnalyticsAI(llm=llm_aws)
            # Recognizing entities in the 'artciles' column in the 'df_articles' teradataml DataFrame.
            >>> obj.recognize_entities(column="articles", data=df_articles)

            # Example 3: Recognize entities from articles in the 'articles' column
            #            of a teradataml DataFrame using Google VertexAI. Articles are
            #            passed as a column name along with the teradataml DataFrame.
            # Create LLM endpoint.
            >>> llm_vertex = TeradataAI(api_type="vertexai",
                                        deployment_id=<provide your VertexAI project name>,
                                        model_name="gemini-1.5-flash-001",
                                        api_region="us-central1",
                                        enable_safety=False,
                                        vertexai_cred="C:/Users/credential.cred",
                                        model_args={"temperature": 1,
                                                    "top_p": 0.95}
                                        )
            # Create a TextAnalyticsAI object.
            >>> obj = TextAnalyticsAI(llm=llm_vertex)
            # Recognizing entities in the 'articles' column in the 'df_articles' teradataml DataFrame.
            >>> obj.recognize_entities(column="articles", data=df_articles)
        """

        # Check if the show_warning is present in the kwargs.
        show_warning = kwargs.get("show_warning", True)
        persist = kwargs.get("persist", False)

        # Validations
        # Create basic validation matrix
        validate_matrix = self._prepare_validate_matrix(column=column, data=data,
                                                        **kwargs)
        validate_matrix.append(["show_warning", show_warning, False, (bool)])
        self._validate_arguments(column=column, data=data, validate_matrix=validate_matrix)

        # Initialize a list to store the entity recognition results.
        result = []
        documents = self.__extract_column_to_documents(column, data)
        warning = False
        # For each review, recognize entities and store the results in the list.
        for sent in documents:
            try:
                if len(sent) < 1:
                    result.append(None)
                    warning = True
                    continue
                # The 'answer' method of the 'llm' object is called with a formatted
                # string that includes the current sentence.
                answer = self.llm.answer(
                    self.__data["prompts"]["recognize_entities"].format(sent=sent))
                if 'nan' in answer.lower() or answer.strip() == '':
                    answer = None
                    warning = True
                result.append(answer)
            except Exception as e:
                # If an error occurs during entity recognition (for example, if the
                # 'answer' method call fails), None is appended to the list.
                if show_warning:
                    self.__issue_inference_warning(str(e))
                result.append(None)
                continue

        # Issue a warning if the `warning` variable is set to True.
        if warning:
            self.__issue_inference_warning()
        for index, res in enumerate(result):
            # Checking if 'STRUCTURED_DATA:' is present in the result or exception
            # has occurred.
            if _Validators._check_isinstance(res, str) and "STRUCTURED_DATA:" in res:
                result[index] = res.replace("STRUCTURED_DATA:", "")

        # Add the entity recognition results to the DataFrame.
        self.__pdf["Labeled_Entities"] = result

        # Restore the table and return the DataFrame.
        self._restore_table(result=self.__pdf, persist=persist)
        return DataFrame(self._table_name)

    def recognize_linked_entities(self, column, data=None, **kwargs):
        """
        DESCRIPTION:
            Identify a collection of entities found in the specified column of a DataFrame.
            It analyzes the text and recognizes words or phrases that appear significantly
            often and carry substantial meaning. These could include names, locations,
            technical terms, or any other significant nouns or phrases.
            It allows user to identify the key words from input text and validate identified
            entities using relevant wikipedia articles based on frequency of the word.
            The output has two columns 'Key_Phrases' which contains the identified key phrases
            and 'Linked_Entities' which contains the linked entities with the frequency of the word.
            In case of any error or exception during the entity recognition process, the result
            is set to None.

        PARAMETERS:
            column:
                Required Argument.
                Specifies the column of the teradataml DataFrame containing the text content
                to recognize the linked entities.
                Types: str

            data:
                Required Argument.
                Specifies the teradataml DataFrame containing the column specified
                in "column" to analyze the content from.
                Types: teradataml DataFrame

            persist:
                Optional Argument.
                Specifies whether to persist the output or not. When set to True, results are stored
                in permanent tables, otherwise in volatile tables.
                Default Value: False
                Types: bool

            show_warning:
                Optional Argument.
                Specifies whether to display warnings during execution. If set to True,
                Runtime Inference warnings are shown. Otherwise, InferenceWarnings
                are suppressed. In either case, a row with 'NaN' values is added.
                Default Value: True
                Types: bool

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException, TypeError, ValueError

        EXAMPLES:
            # Import the modules and create a teradataml DataFrame.
            >>> from teradataml import DataFrame
            >>> from teradatagenai import TeradataAI, TextAnalyticsAI, load_data
            >>> load_data('employee', 'employee_data')
            >>> data = DataFrame('employee_data')
            >>> df_articles = data.select(["employee_id", "employee_name", "articles"])

            # Example 1: Recognize linked entities from articles in the 'articles' column
            #            of a teradataml DataFrame using Azure OpenAI. Articles are
            #            passed as a column name along with the teradataml DataFrame.
            # Create LLM endpoint.
            >>> llm_azure = TeradataAI(api_type = "azure",
                         api_base = ""********"",
                         api_version = "2000-11-35",
                         api_key = ""********"",
                         engine = ""********"",
                         model_name = "gpt-3.5-turbo")
            # Create a TextAnalyticsAI object.
            >>> obj = TextAnalyticsAI(llm=llm_azure)
            # Recognizing linked entities in the 'articles' column in the 'df_articles' teradataml DataFrame.
            >>> obj.recognize_linked_entities(column="articles", data=df_articles, persist=True)

            # Example 2: Recognize linked entities from articles in the 'articles' column
            #            of a teradataml DataFrame using AWS BedRock. Articles are passed
            #            as a column name along with the teradataml DataFrame.
            # AWS BedRock credentials.
            >>> llm_aws = TeradataAI(api_type = "aws",
                                    api_key = "*************",
                                    engine_id = "**********",
                                    api_region = "us-west-2",
                                    model_name = "anthropic.claude-v2",
                                    model_args = {"max_tokens_to_sample": 2048,
                                                    "temperature": 0,
                                                    "top_k": 250,
                                                    "top_p": 1})

            # Create a TextAnalyticsAI object.
            >>> obj = TextAnalyticsAI(llm=llm_aws)
            >>> obj.recognize_linked_entities(column="articles", data=df_articles)

            # Example 3: Recognize linked entities from articles in the 'articles' column
            #            of a teradataml DataFrame using Google VertexAI. Articles are passed
            #            as a column name along with the teradataml DataFrame.
            # Create LLM endpoint.
            >>> llm_vertex = TeradataAI(api_type="vertexai",
                                        deployment_id=<provide your VertexAI project name>,
                                        model_name="gemini-1.5-flash-001",
                                        api_region="us-central1",
                                        enable_safety=False,
                                        vertexai_cred="C:/Users/credential.cred",
                                        model_args={"temperature": 1,
                                                    "top_p": 0.95}
                                        )
            # Create a TextAnalyticsAI object.
            >>> obj = TextAnalyticsAI(llm=llm_vertex)
            # Recognizing linked entities in the 'articles' column in the 'df_articles' teradataml DataFrame.
            >>> obj.recognize_linked_entities(column="articles", data=df_articles)
        """
        # Check if the show_warning is present in the kwargs.
        show_warning = kwargs.get("show_warning", True)
        persist = kwargs.get("persist", False)

        # Validations
        # Create basic validation matrix
        validate_matrix = self._prepare_validate_matrix(column=column, data=data,
                                                        **kwargs)
        validate_matrix.append(["show_warning", show_warning, False, (bool)])
        self._validate_arguments(column=column, data=data, validate_matrix=validate_matrix)

        # Extract key phrases from the specified column of the DataFrame.
        self.extract_key_phrases(column=column, data=data, persist=persist, show_warning=show_warning)
        results = self.__pdf["Key_Phrases"].to_list()
        warning = False

        # Initialize a list to store the frequency of each word.
        freq = []
        for words in results:
            try:
                if words is None:
                    freq.append("None")
                    warning = True
                else:
                    temp = []
                    for word in words.split(", "):
                        # Use the _wiki_crawl method to get the frequency of the word.
                        wfreq = self._wiki_crawl(word)
                        temp.append("({word},{freq})".format(word=word, freq=wfreq[word]))
                    freq.append(str(temp))
            except Exception as e:
                if show_warning:
                    self.__issue_inference_warning(str(e))
                freq.append("None")
                continue
        # Issue a warning if the `warning` variable is set to True.
        if warning:
            self.__issue_inference_warning()
        # Add the frequencies to the DataFrame.
        self.__pdf["Linked_Entities"] = freq

        # Restore the table and return the DataFrame.
        self._restore_table(result=self.__pdf, persist=persist)
        return DataFrame(self._table_name)

    def recognize_pii_entities(self, column, data=None, **kwargs):
        """
        DESCRIPTION:
            Recognize Personally Identifiable Information (PII) entities within a
            specified column of a DataFrame. PII encompasses any data that could
            potentially identify a specific individual. Direct identifiers are explicit
            pieces of information that can uniquely identify an individual. These
            include sensitive data such as names, email addresses and phone numbers.
            Indirect identifiers, on the other hand, are pieces of information that may
            not identify an individual on their own but can do so when combined with
            other data. Examples include dates or unique device identifiers.
            The function is capable of recognizing a diverse set of PII entities
            including 'Name', 'address', 'contact numbers', 'date/time' and 'serial
            numbers'. The output has a column 'PII_Entities' which contains the name,
            start position and the length of the identified entity.
            In case of any error or exception during the PII entity recognition process,
            the result is set to None.
            Note:
                This function handles sensitive information and is compatible with Google
                Vertex AI exclusively when the `enable_safety` parameter is set to False.

        PARAMETERS:
            column:
                Required Argument.
                Specifies the column of the teradataml DataFrame containing the text
                content to recognize pii entities.
                Types: str

            data:
                Required Argument.
                Specifies the teradataml DataFrame containing the column specified
                in "column" to analyze the content from.
                Types: teradataml DataFrame

            persist:
                Optional Argument.
                Specifies whether to persist the output or not. When set to True, results are stored
                in permanent tables, otherwise in volatile tables.
                Default Value: False
                Types: bool

            show_warning:
                Optional Argument.
                Specifies whether to display warnings during execution. If set to True,
                Runtime Inference warnings are shown. Otherwise, InferenceWarnings
                are suppressed. In either case, a row with 'NaN' values is added.
                Default Value: True
                Types: bool

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException, TypeError, ValueError

        EXAMPLES:
            # Import the modules and create a teradataml DataFrame.
            >>> from teradataml import DataFrame
            >>> from teradatagenai import TeradataAI, TextAnalyticsAI, load_data
            >>> load_data('employee', 'employee_data')
            >>> data = DataFrame('employee_data')
            >>> df_employeeData = data.select(["employee_id", "employee_name", "employee_data"])

            # Example 1: Recognize PII entities in the 'employee_data' column of a teradataml
            #            DataFrame using Azure OpenAI. The text containing potential
            #            PII like names, addresses, credit card numbers, etc., is passed
            #            as a column name along with the teradataml DataFrame.
            # Create LLM endpoint.
            >>> llm_azure = TeradataAI( api_type = "azure",
                                        api_base = "**********************",
                                        api_version = "2023-05-15",
                                        api_key = "*******************",
                                        engine_id="******",
                                        model_name="gpt-3.5-turbo")

            # Create a TextAnalyticsAI object.
            >>> obj = TextAnalyticsAI(llm=llm_azure)
            # Recognizing PII entities in the 'employee_data' column in the 'df_employeeData' teradataml DataFrame.
            >>> obj.recognize_pii_entities(column="employee_data", data=df_employeeData, persist=True)

            # Example 2: Recognize PII entities in the 'employee_data' column of a teradataml
            #            DataFrame using AWS BedRock. The text containing potential PII
            #            like names, addresses, credit card numbers, etc., is passed as a
            #            column name along with the teradataml DataFrame.
            # AWS BedRock credentials.
            >>> llm_aws = TeradataAI(api_type = "aws",
                                    api_key = "*********************",
                                    engine_id = "*************",
                                    api_region = "us-west-2",
                                    model_name = "anthropic.claude-v2",
                                    model_args = {"max_tokens_to_sample": 2048,
                                                    "temperature": 0,
                                                    "top_k": 250,
                                                    "top_p": 1})

            # Create a TextAnalyticsAI object.
            >>> obj = TextAnalyticsAI(llm=llm_aws)
            # Recognizing PII entities in the 'employee_data' column in the 'df_employeeData' teradataml DataFrame.
            >>> obj.recognize_pii_entities(column="employee_data", data=df_employeeData, persist=True)

            # Example 3: Recognize PII entities in the 'employee_data' column of a teradataml
            #            DataFrame using Google VertexAI. The text containing potential PII
            #            like names, addresses, credit card numbers, etc., is passed as a
            #            column name along with the teradataml DataFrame.
            # Create LLM endpoint.
            >>> llm_vertex = TeradataAI(api_type="vertexai",
                                        deployment_id=<provide your VertexAI project name>,
                                        model_name="gemini-1.5-flash-001",
                                        api_region="us-central1",
                                        enable_safety=False,
                                        vertexai_cred="C:/Users/credential.cred",
                                        model_args={"temperature": 1,
                                                    "top_p": 0.95}
                                        )
            # Create a TextAnalyticsAI object.
            >>> obj = TextAnalyticsAI(llm=llm_vertex)
            # Recognizing PII entities in the 'employee_data' column in the 'df_employeeData' teradataml DataFrame.
            >>> obj.recognize_pii_entities(column="employee_data", data=df_employeeData)
        """
        # Check if the show_warning is present in the kwargs.
        show_warning = kwargs.get("show_warning", True)
        persist = kwargs.get("persist", False)

        # Validations
        # Create basic validation matrix
        validate_matrix = self._prepare_validate_matrix(column=column, data=data,
                                                        **kwargs)
        validate_matrix.append(["show_warning", show_warning, False, (bool)])
        self._validate_arguments(column=column, data=data, validate_matrix=validate_matrix)

        # Initialize lists to store the PII recognition results and the masked sentences.
        result = []
        documents = self.__extract_column_to_documents(column, data)
        warning = False
        # For each sentence, recognize PII entities and store the results in the list.
        for sentence in documents:
            try:
                if len(sentence) < 1:
                    result.append(None)
                    warning = True
                    continue
                # The 'answer' method of the 'llm' object is called with a formatted
                # string that includes the current sentence.
                temp = self.llm.answer(
                    self.__data["prompts"]["recognize_pii_entities"].format(
                        sentence=sentence))
                if 'nan' in temp.lower() or temp.strip() == '':
                    temp = None
                    warning = True
                else:
                    temp = temp.replace("STRUCTURED_DATA:", "")
                result.append(temp)
            except Exception as e:
                # If an error occurs during PII recognition (for example, if the
                # 'answer' method call fails), None is appended to the result list.
                if show_warning:
                    # Use a context manager to temporarily modify the behavior of warnings
                    with warnings.catch_warnings():
                        self.__issue_inference_warning(str(e))
                result.append(None)
                continue

        # Issue a warning if the `warning` variable is set to True.
        if warning:
            self.__issue_inference_warning()
        for index, res in enumerate(result):
            if isinstance(res, str):
                # Remove triple backticks
                res = re.sub(r"```", "", res)
                # Remove anything preceding and including "STRUCTURED_DATA:"
                res = re.sub(r".*STRUCTURED_DATA:", "", res, flags=re.IGNORECASE).strip()
                result[index] = res

        # Add the PII recognition results and the masked sentences to the DataFrame.
        self.__pdf["PII_Entities"] = result
        self.__pii_entities = result

        # Restore the table and return the DataFrame.
        self._restore_table(result=self.__pdf, persist=persist)
        return DataFrame(self._table_name)

    def summarize(self, column, data=None, level=1, **kwargs):
        """
        DESCRIPTION:
            Summarize the text in the specified column of a DataFrame. It generates an
            abstractive summary for the input using different levels. Abstractive
            summarization is a process in which the function not only extracts key
            information from the text but also paraphrases and presents it in a condensed
            form, much like a human summarizer would. The conciseness of the summary can
            be adjusted using different levels. Higher levels yield more concise
            summaries. For instance, if the 'level' parameter is set to 2, the function
            first generates a summary of the original text, and then it further
            summarizes that summary. This recursive process allows for a highly condensed
            representation of the original text, making it easier to grasp the main
            points without having to read through the entire text. The output contains
            the summarized text and count of the characters in the summarized text. In
            case of any error or exception during the summarization process, the result
            is set to None.

        PARAMETERS:
            column:
                Required Argument.
                Specifies the column of the teradataml DataFrame containing the text
                content to summarize.
                Types: str

            data:
                Required Argument.
                Specifies the teradataml DataFrame containing the column specified
                in "column" to analyze the content from.
                Types: teradataml DataFrame

            level:
                Optional Argument.
                Specifies the level of summarization. Higher levels yield more concise
                summaries.
                Default Value: 1
                Types: int

            persist:
                Optional Argument.
                Specifies whether to persist the output or not. When set to True, results are stored
                in permanent tables, otherwise in volatile tables.
                Default Value: False
                Types: bool

            show_warning:
                Optional Argument.
                Specifies whether to display warnings during execution. If set to True,
                Runtime Inference warnings are shown. Otherwise, InferenceWarnings
                are suppressed. In either case, a row with 'NaN' values is added.
                Default Value: True
                Types: bool

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException, TypeError, ValueError

        Example:
            # Import the modules and create a teradataml DataFrame.
            >>> from teradataml import DataFrame
            >>> from teradatagenai import TeradataAI, TextAnalyticsAI, load_data
            >>> load_data('employee', 'employee_data')
            >>> data = DataFrame('employee_data')
            >>> df_articles = data.select(["employee_id", "employee_name", "articles"])

            # Example 1: Summarize articles in the 'articles' column of a teradataml DataFrame
            #            using Azure OpenAI. Articles are passed as a column name along with
            #            the teradataml DataFrame.
            >>> llm_azure = TeradataAI(api_type = "azure",
                                       api_base = "********",
                                       api_version = "2000-11-35",
                                       api_key = "********",
                                       engine_id = "********",
                                       model_name = "gpt-3.5-turbo")
            >>> obj_azure = TextAnalyticsAI(llm=llm_azure)
            >>> summary_azure = obj_azure.summarize(column="articles", data=df_articles)

            # Example 2: Summarize articles in the 'articles' column of a teradataml DataFrame
            #            using AWS BedRock with a summarization level set to 2. Articles are
            #            passed as a column name along with the teradataml DataFrame.
            >>> llm_aws = TeradataAI(api_type = "aws",
                                     api_key = "**********",
                                     engine_id = "**********",
                                     api_region = "us-west-2",
                                     model_name = "anthropic.claude-v2",
                                     model_args = {"max_tokens_to_sample": 2048,
                                                   "temperature": 0,
                                                   "top_k": 250,
                                                   "top_p": 1})
            >>> obj_aws = TextAnalyticsAI(llm=llm_aws)
            >>> summary_aws = obj_aws.summarize(column="articles", data=df_articles, level=2)

            # Example 3: Summarize articles in the 'articles' column of a teradataml DataFrame
            #            using Google VertexAI. Articles are passed as a column name along with
            #            the teradataml DataFrame.
            >>> llm_vertex = TeradataAI(api_type="vertexai",
                                        deployment_id=<provide your VertexAI project name>,
                                        model_name="gemini-1.5-flash-001",
                                        api_region="us-central1",
                                        enable_safety=False,
                                        vertexai_cred="C:/Users/credential.cred",
                                        model_args={"temperature": 1,
                                                    "top_p": 0.95}
                                        )
            >>> obj_vertex = TextAnalyticsAI(llm=llm_vertex)
            >>> summary_vertex = obj_vertex.summarize(column="articles", data=df_articles)
        """

        # Check if the show_warning is present in the kwargs.
        show_warning = kwargs.get("show_warning", True)
        persist = kwargs.get("persist", False)

        # Validations
        # Create basic validation matrix
        validate_matrix = self._prepare_validate_matrix(column=column, data=data,
                                                        **kwargs)
        validate_matrix.append(["show_warning", show_warning, False, (bool)])
        validate_matrix.append(["level", level, True, (int)])
        self._validate_arguments(column=column, data=data, validate_matrix=validate_matrix)

        # Initialize lists to store the summarization results and their lengths.
        result = []
        length = []

        documents = self.__extract_column_to_documents(column, data)
        warning = False
        # For each document, generate a summary and store it in the result list.
        for sent in documents:
            try:
                if len(sent) < 1:
                    result.append(None)
                    warning = True
                    continue
                ans = sent
                for i in range(level):
                    ans = self.llm.answer(
                        self.__data["prompts"]["summarize"].format(sent=ans))
                    if ans == None:
                        ans = None
                        l = None
                        warning = True
                    else:
                        l = len(ans)

                result.append(ans)
                length.append(l)
            except Exception as e:
                # If an error occurs during the summarization (for example, if the
                # 'answer' method call fails), None is appended to the result list.
                if show_warning:
                    self.__issue_inference_warning(str(e))
                result.append(None)
                length.append(None)
                continue

        # Issue a warning if the `warning` variable is set to True.
        if warning:
            self.__issue_inference_warning()
        # Add the summarization results and their lengths to the DataFrame.
        self.__pdf["Summary"] = result
        self.__pdf["Count"] = length

        # Restore the table and return the DataFrame.
        self._restore_table(result=self.__pdf, persist=persist)
        return DataFrame(self._table_name)

    def translate(self, column, data=None, target_lang="English", **kwargs):
        """
        DESCRIPTION:
            Translate the input language to target language from the specified column of
            a DataFrame. The function is capable of translating the text content to the
            targeted language. The output has one additional column 'Translation' which
            contains the translated text content. The languages supported align with
            those supported by the respective large language models (LLMs) in use. By
            default the target language is set to 'English'. In case of any error or
            exception during the translation process, the result is set to None.

        PARAMETERS:
            column:
                Required Argument.
                Specifies the column of the teradataml DataFrame containing the text content
                to translate.
                Types: str

            data:
                Required Argument.
                Specifies the teradataml DataFrame containing the column specified
                in "column" to analyze the content from.
                Types: teradataml DataFrame

            target_lang:
                Optional Argument.
                Specifies the target language to translate the text content to.
                Default Value: "English".
                Types: str

            persist:
                Optional Argument.
                Specifies whether to persist the output or not. When set to True, results are stored
                in permanent tables, otherwise in volatile tables.
                Default Value: False
                Types: bool

            show_warning:
                Optional Argument.
                Specifies whether to display warnings during execution. If set to True,
                Runtime Inference warnings are shown. Otherwise, InferenceWarnings
                are suppressed. In either case, a row with 'NaN' values is added.
                Default Value: True
                Types: bool

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException, TypeError, ValueError

        EXAMPLES:
            # Import the modules and create a teradataml DataFrame.
            >>> from teradataml import DataFrame
            >>> from teradatagenai import TeradataAI, TextAnalyticsAI, load_data
            >>> load_data('employee', 'employee_data')
            >>> data = DataFrame('employee_data')
            >>> df_quotes = data.select(["employee_id", "employee_name", "quotes"])

            # Example 1: Translate the quotes from the 'quotes' column of a teradataml DataFrame
            #            into English using Azure OpenAI. The text for translation is passed as
            #            a column name along with the teradataml DataFrame. As no target language is
            #            specified, the default translation language is set to English.
            # Create LLM endpoint.
            >>> llm_azure = TeradataAI(api_type = "azure",
                         api_base = "********",
                         api_version = "2000-11-35",
                         api_key = ""********"",
                         engine_id = ""********"",
                         model_name = "gpt-3.5-turbo")

            # Create a TextAnalyticsAI object.
            >>> obj = TextAnalyticsAI(llm=llm_azure)
            >>> obj.translate(column="quotes", data=df_quotes)

            Example 2: Translate the quotes from the 'quotes' column of a teradataml DataFrame
            #          into German using AWS BedRock. The text for translation is passed as a
            #          column name along with the teradataml DataFrame. The target language
            #          for translation is set as German.
            # Import the modules.
            # AWS BedRock credentials.
            >>> llm_aws = TeradataAI(api_type = "aws",
                                    api_key = "*******************",
                                    engine_id = "*************",
                                    api_region = "us-west-2",
                                    model_name = "anthropic.claude-v2",
                                    model_args = {"max_tokens_to_sample": 2048,
                                                    "temperature": 0,
                                                    "top_k": 250,
                                                    "top_p": 1})

            # Create a TextAnalyticsAI object.
            >>> obj = TextAnalyticsAI(llm=llm_aws)
            >>> obj.translate(column="quotes", data=df_quotes, target_lang="German", persist=True)

            # Example 3: Translate the quotes from the 'quotes' column of a teradataml DataFrame
            #            into French using Google VertexAI. The text for translation is passed as a
            #            column name along with the teradataml DataFrame. The target language for
            #            translation is set as French.
            # Create LLM endpoint.
            >>> llm_vertex = TeradataAI(api_type="vertexai",
                                        deployment_id=<provide your VertexAI project name>,
                                        model_name="gemini-1.5-flash-001",
                                        api_region="us-central1",
                                        enable_safety=False,
                                        vertexai_cred="C:/Users/credential.cred",
                                        model_args={"temperature": 1,
                                                    "top_p": 0.95}
                                        )
            # Create a TextAnalyticsAI object.
            >>> obj = TextAnalyticsAI(llm=llm_vertex)
            >>> obj.translate(column="quotes", data=df_quotes, target_lang="French")
        """
        # Check if the show_warning is present in the kwargs.
        show_warning = kwargs.get("show_warning", True)
        persist = kwargs.get("persist", False)

        # Validations
        # Create basic validation matrix
        validate_matrix = self._prepare_validate_matrix(column=column, data=data,
                                                        **kwargs)
        validate_matrix.append(["show_warning", show_warning, False, (bool)])
        validate_matrix.append(["target_lang", target_lang, True, (str)])
        self._validate_arguments(column=column, data=data, validate_matrix=validate_matrix)

        target = target_lang.split()

        # Initialize a list to store the translation results.
        result = []
        documents = self.__extract_column_to_documents(column, data)
        warning = False
        # For each document, generate a translation and store it in the result list.
        for sent in documents:
            try:
                if len(sent) < 1:
                    result.append(None)
                    warning = True
                    continue

                answer = self.llm.answer(
                    self.__data["prompts"]["translate"].format(target=target, sent=sent))
                if 'nan' in answer.lower() or answer.strip() == '':
                    answer = None
                    warning = True
                result.append(answer)
            except Exception as e:
                # If an error occurs during the translation (for example, if the
                # 'answer' method call fails), None is appended to the result list.
                if show_warning:
                    self.__issue_inference_warning(str(e))
                result.append(None)
                continue
        # Issue a warning if the `warning` variable is set to True.
        if warning:
            self.__issue_inference_warning()
        # Add the translation results to the DataFrame.
        self.__pdf["Translation"] = result

        # Restore the table and return the DataFrame.
        self._restore_table(result=self.__pdf, persist=persist)
        return DataFrame(self._table_name)

    def embeddings(self, column, data=None, persist=False, **kwargs):
        """
        DESCRIPTION:
            Retrieve embeddings using API_Request in-database function for a specified
            table and column. This function returns a teradataml DataFrame with an 'embeddings'
            column containing text embeddings in varbyte format.
            Notes:
                * API_Request UDF must be preset on the Vantage. Check API_Request
                  documentation for installation details.
                * For Azure OpenAI, both Vantage Enterprise and VantageCloud Lake are supported.
                  However, for AWS Bedrock, only VantageCloud Lake is supported due to limitations
                  and considerations related to the curl library.
                * UDF is compatible with Azure OpenAI and Amazon Bedrock only.

        PARAMETERS:
            column:
                Required Argument.
                Specifies the column of the teradataml DataFrame containing the text content
                to translate.
                Types: str

            data:
                Required Argument.
                Specifies the teradataml DataFrame containing the column specified
                in "column" to analyze the content from.
                Types: teradataml DataFrame

            persist:
                Optional Argument.
                Specifies whether to persist the output or not. When set to True, results are stored
                in permanent tables, otherwise in volatile tables.
                Default Value: False
                Types: bool

            num_embeddings:
                Optional Argument.
                Specifies the number of embeddings to fetch.
                Default Value: 1536
                Types: int

            initial_delay_ms:
                Optional Argument.
                Specifies the millisecond delay after each input
                table row is sent for embeddings.
                Default Value: 0
                Types: int

            delay_max_retries:
                Optional Argument.
                Specifies maximum number of attempts after a failed
                input table row embedding request.
                Default Value: 0
                Types: int

            delay_exp_base:
                Optional Argument.
                Specifies the exponential base of delay time increase.
                Default Value: 1
                Types: int

            delay_jitter:
                Optional Argument.
                Specifies the random sum term in exponent.
                Default Value: 0
                Types: int

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException, TypeError, ValueError

        EXAMPLES:
            # Import the modules and create a teradataml DataFrame.
            >>> from teradataml import DataFrame
            >>> from teradatagenai import TeradataAI, TextAnalyticsAI, load_data
            >>> load_data('employee', 'employee_data')
            >>> data = DataFrame('employee_data')
            >>> df_reviews = data.select(["employee_id", "employee_name", "reviews"])

            # Example 1: Generate the embeddings for employee reviews from the 'reviews' column
            #            of a teradataml DataFrame using Azure OpenAI. The text for generatiung the
            #            embeddings is passed as a column name along with the teradataml DataFrame.
            #            As no optional arguments are specified, the default values will be considered.
            >>> az_ai_embedding = TeradataAI(api_type = "azure",
                                            api_key = "<Enter api_key>",
                                            deployment_id = "<Enter Deployment ID>",
                                            resource = "<Enter Resource Name>",
                                            model_name = "text-embedding-ada-002",
                                            mode = "udf")
            >>> obj = TextAnalyticsAI(llm=az_ai_embedding)
            >>> obj.embeddings(column="reviews", data=df_reviews)

            # Example 2: Generate the embeddings for employee reviews from the 'reviews' column
            #            of a teradataml DataFrame using AWS BedRock. The text for generatiung the
            #            embeddings is passed as a column name along with the teradataml DataFrame.
            #            The optional arguments are specified to customize the embeddings generation.
            >>> aws_bedrock_embedding = TeradataAI(api_type = "aws",
                                        deployment_id = "<Enter Deployment>",
                                        api_key = "<Enter API Key>",
                                        api_region = "us-west-2",
                                        model_name = "amazon.titan-embed-text-v1",
                                        mode = "udf")
            >>> obj = TextAnalyticsAI(llm=aws_bedrock_embedding)
            >>> obj.embeddings(column="reviews", data=df_reviews, num_embeddings=1536,
                               initial_delay_ms=0, delay_max_retries=0, delay_exp_base=1,
                               delay_jitter=1)
        """

        # Check kwargs for optional arguments.
        show_warning = kwargs.get("show_warning", True)

        num_embeddings = kwargs.get("num_embeddings", 1536)
        initial_delay_ms = kwargs.get("initial_delay_ms", 0)
        delay_max_retries = kwargs.get("delay_max_retries", 0)
        delay_exp_base = kwargs.get("delay_exp_base", 1)
        delay_jitter = kwargs.get("delay_jitter", 0)

        az_ai_embedding = True if self.llm.api_type == "az-ai-embedding" else False
        aws_bedrock_embedding = True if self.llm.api_type == "aws-bedrock" else False

        # Validations
        # Create basic validation matrix
        validate_matrix = self._prepare_validate_matrix(column=column, data=data,
                                                        **kwargs)
        validate_matrix.append(["show_warning", show_warning, False, (bool)])

        validate_matrix.append([
            "num_embeddings", num_embeddings,
            not (az_ai_embedding or aws_bedrock_embedding),
            (int), False
        ])
        validate_matrix.append([
            "initial_delay_ms", initial_delay_ms,
            not (az_ai_embedding or aws_bedrock_embedding),
            (int), False
        ])
        validate_matrix.append([
            "delay_max_retries", delay_max_retries,
            not (az_ai_embedding or aws_bedrock_embedding),
            (int), False
        ])
        validate_matrix.append([
            "delay_exp_base", delay_exp_base,
            not (az_ai_embedding or aws_bedrock_embedding),
            (int), False
        ])
        validate_matrix.append([
            "delay_jitter", delay_jitter,
            not (az_ai_embedding or aws_bedrock_embedding),
            (int), False
        ])

        self._validate_arguments(column=column, data=data, validate_matrix=validate_matrix)

        authorization = ''
        endpoint = ''
        api_type = ''
        # Construct the authorization part based on API type.
        if aws_bedrock_embedding:
            api_type = 'aws-bedrock'
            authorization = (
                f'{{"Access_ID": "{self.llm.get_deployment_id()}", "Region": "{self.llm.api_region}", '
                f'"Access_Key": "{self.llm.api_key}", "Session_Token": "{self.llm.session_token}"}}'
            )
        elif az_ai_embedding:
            api_type = 'az-ai-embedding'
            if hasattr(self.llm, 'api_base') and self.llm.api_base:
                # For Azure OpenAI using Azure endpoint.
                authorization = f'{{"Key": "{self.llm.api_key}"}}'
                endpoint = f" ENDPOINT('{self.llm.api_base}')"
            else:
                # For Azure OpenAI using Azure resource name and deployment.
                authorization = (
                    f'{{"Key": "{self.llm.api_key}", "Resource": "{self.llm.resource}", '
                    f'"Deployment": "{self.llm.get_deployment_id()}"}}'
                )

        # To retrieve query used to generate the input DataFrame if it's not materialized.
        input_query = data.show_query(True)

        self.udf_query = (
            f"SELECT * FROM tapidb.API_Request( ON ({input_query}) "
            f"USING AUTHORIZATION('{authorization}'){endpoint} DATA_COLUMNS('{column}') "
            f"NUM_EMBEDDINGS('{num_embeddings}') MODEL_NAME('{self.llm.model_name}') "
            f"API_TYPE('{api_type}') INITIAL_DELAY_MS('{initial_delay_ms}') "
            f"DELAY_MAX_RETRIES('{delay_max_retries}') DELAY_EXP_BASE('{delay_exp_base}') "
            f"DELAY_JITTER('{delay_jitter}')) as \"DT\""
        )

        # Execute the UDF query and fetch the results into a teradataml DataFramee.
        output_df = DataFrame.from_query(query=self.udf_query)

        # Restore the table and return the DataFrame.
        self._restore_table(result=output_df, persist=persist)
        return DataFrame(self._table_name)