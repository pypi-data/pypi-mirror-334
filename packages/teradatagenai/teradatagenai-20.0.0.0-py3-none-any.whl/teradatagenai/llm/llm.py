# ##################################################################
#
# Copyright 2024 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
#
# Primary Owner: Kesavaragavan B (kesavaragavan.b@teradata.com)
# Secondary Owner: Aanchal Kavedia (aanchal.kavedia@teradata.com)
#                  Snigdha Biswas (snigdha.biswas@teradata.com)
#
# Notes: 
#   * This code is only for internal use. 
#   * The code may perform modify, create, or delete operations 
#     in database based on given query. Hence, limit the permissions 
#     granted to the credentials.
# This file provides access to the LLM endpoints for inference.
# ##################################################################
# Import required packages.
import importlib
import json
import os
import shutil
import time
from abc import ABC, abstractmethod
from time import sleep
from typing import Optional

import boto3
import openai
import vertexai
from botocore.config import Config
from langchain_aws import BedrockLLM as Bedrock
from langchain_community.llms import AzureOpenAI, OpenAI
from teradataml import configure, create_env, get_env, list_user_envs
from teradataml.scriptmgmt.UserEnv import UserEnv
from teradataml.utils.validators import _Validators
from teradataml.hyperparameter_tuner.utils import _ProgressBar
from vertexai.generative_models import (GenerationConfig, GenerativeModel,
                                        HarmBlockThreshold, HarmCategory, Part)

def _get_bedrock_client(assumed_role: Optional[str] = None,
                        region: Optional[str] = None,
                        runtime: Optional[bool] = True,
                        cred: Optional[dict] = None):
    """
    DESCRIPTION:
        Internal function to get a client to perform operations with the Amazon Bedrock service.
            
    PARAMETERS:
        assumed_role:
            Optional Argument.
            Specifies the ARN of an AWS IAM role to assume for calling the Bedrock service.
            If not specified, the current active credentials will be used.
            Types: str

        region:
            Optional Argument.
            Specifies the name of the AWS Region in which the service should be called (e.g. "us-east-1").
            If not specified, AWS_REGION or AWS_DEFAULT_REGION environment variable will be used.
            Types: str
            
        runtime:
            Optional Argument.
            Specifies the choice of getting different client to perform operations with the Amazon Bedrock service.
            If not specified, the runtime client will be used.
            
        cred:
            Required Argument.
            Specifies the credentials to be used for the client.
            Types: dict

    RETURNS:
        None

    RAISES:
        None

    EXAMPLES:
        
        _get_bedrock_client(cred={"AWS_DEFAULT_REGION": api_region,
                            "AWS_ACCESS_KEY_ID": deployment_id,
                            "AWS_SECRET_ACCESS_KEY": api_key, 
                            "model_name": model_name,
                            "model_args": model_args})
    """
    # Set AWS credentials from the 'cred' dictionary as environment variables.
    os.environ["AWS_DEFAULT_REGION"] = cred["AWS_DEFAULT_REGION"]
    os.environ["AWS_ACCESS_KEY_ID"] = cred["AWS_ACCESS_KEY_ID"]
    os.environ["AWS_SECRET_ACCESS_KEY"] = cred["AWS_SECRET_ACCESS_KEY"]
    
    # Determine the target AWS region
    if region is None:
        target_region = os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION"))
    else:
        target_region = region
        
    # Prepare arguments for creating the boto3 session and client.
    session_kwargs = {"region_name": target_region}
    client_kwargs = {**session_kwargs}
    
    # If an AWS profile is specified, add it to the session arguments.
    profile_name = os.environ.get("AWS_PROFILE")
    if profile_name:
        session_kwargs["profile_name"] = profile_name

    retry_config = Config(
        region_name=target_region,
        retries={
            "max_attempts": 10,
            "mode": "standard",
        },
    )
    
    # Create a boto3 session.
    session = boto3.Session(**session_kwargs)
    
    # If an assumed role is specified, use it to get temporary credentials.
    if assumed_role:
        sts = session.client("sts")
        response = sts.assume_role(
            RoleArn=str(assumed_role),
            RoleSessionName="langchain-llm-1"
        )
        client_kwargs["aws_access_key_id"] = response["Credentials"]["AccessKeyId"]
        client_kwargs["aws_secret_access_key"] = response["Credentials"]["SecretAccessKey"]
        client_kwargs["aws_session_token"] = response["Credentials"]["SessionToken"]
        
    # Determine the service name for the client.
    if runtime:
        service_name='bedrock-runtime'
    else:
        service_name='bedrock'
        
    # Create a boto3 client for the Amazon Bedrock service.
    bedrock_client = session.client(
        service_name=service_name,
        config=retry_config,
        **client_kwargs
    )

    print("boto3 Bedrock client successfully created!")
    print(bedrock_client._endpoint)
    
    # Return the created client.
    return bedrock_client


def _set_openAI(api_key, api_type, api_base, api_version):
    """
    DESCRIPTION:
        Internal function to set environment variables for AzureAI.
            
    PARAMETERS:
        api_key:
            Required Argument.
            Specifies the AzureAI API key.
            Types: str

        api_type:
            Required Argument.
            Specifies the AzureAI API type.
            Types: str
            
        api_base:
            Required Argument.
            Specifies the AzureAI API base url.
            Types: str

        api_version:
            Required Argument.
            Specifies the AzureAI API version.
            Types: str

    RETURNS:
        None

    RAISES:
        None

    EXAMPLES:
        _set_openAI(api_type = "azure"
                    api_base = "https://***.openai.azure.com/"
                    api_version = "2021-12-35"
                    api_key = "999***")
    """
    # Set API type.
    os.environ["OPENAI_API_TYPE"] = api_type
    # Set API version like follow "2022-06-10".
    os.environ["OPENAI_API_VERSION"] = api_version
    # Set API Base URL as follow 
    # "https://****instance.openai.azure.com/".
    os.environ["OPENAI_API_BASE"] = api_base
    # Set API key.
    os.environ["OPENAI_API_KEY"] = api_key   

def _set_vertex_env(vertexai_cred):
    """
    DESCRIPTION:
        Internal function to set environment variables for VertexAI credentials.

    PARAMETERS:
        vertexai_cred:
            Required Argument.
            Specifies the credentials file path for the Vertex client.
            Types: string
    """  
    # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable.
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']=vertexai_cred

class _TeradataAIStruct(ABC):
    """
    Abstract class for holding the structure as well as the
    common functions/methods.
    """
    def __init__(self, api_type, model_name):
        """
        DESCRIPTION:
            Constructor for the _TeradataAIStruct class.

        PARAMETERS:
            api_type:
               Required Argument.
               Specifies the LLM API type.
               Permitted Values: 'azure', 'aws', 'vertexai', 'hugging_face'
               Types: str

            model_name:
               Required Argument.
               Specifies the LLM model name.
               Types: str

        RETURNS:
            None

        RAISES:
            None
        """
        self.api_type = api_type
        self.model_name = model_name

    @abstractmethod
    def get_llm(self):
        """
        DESCRIPTION:
            Get the LLM inference endpoint.

        PARAMETERS:
            None

        RETURNS:
            LLM endpoint object, str

        RAISES:
            None
        """
        pass

class _TeradataAIClient(_TeradataAIStruct):
    """
    Class to hold the functions required to set up the enviornment
    and initialize the LLM endpoint.
    """
    def __init__(self, api_type, model_name, **kwargs):
        """
        DESCRIPTION:
            Function sets up the environment and initializes the LLM endpoint.

        PARAMETERS:
           api_key:
               Required if "api_type" is 'azure' or 'aws',
               optional otherwise.
               Specifies the LLM API key.
               Note:
                   Applicable only if "api_type" is either 'azure' or 'aws'.
               Types: str

           api_type:
               Required Argument.
               Specifies the LLM API type.
               Permitted Values: 'azure', 'aws', 'vertexai', 'hugging_face'
               Types: str

           deployment_id:
               Required if "api_type" is 'azure', 'aws' or 'vertexai'
               and "mode" is 'client', optional otherwise.
               Specifies the deployment ID of the LLM.
               This argument accepts:
                    * engine id for azure OpenAI,
                    * project name for VertexAI and
                    * access key ID for AWS bedrock.
               Note:
                   Applicable only if "api_type" is 'azure', 'aws',
                   or 'vertexai', and "mode" is 'client'.
               Types: str

           model_name:
               Required Argument.
               Specifies the LLM model name.
               Types: str

           api_base:
               Required if "api_type" is 'azure' and "mode" is 'client', optional
               otherwise.
               Specifies AzureAI LLM endpoint URL.
               Note:
                   Applicable only if "api_type" is either 'azure' or 'aws',
                   and "mode" is 'client'.
               Types: str

           api_version:
               Required if "api_type" is 'azure' and "mode" is 'client',
               optional otherwise.
               Specifies the LLM API version.
               Note:
                   Applicable only if "api_type" is either 'azure' or 'aws'
                   and "mode" is 'client'.
               Types: str

           api_region:
               Required if "api_type" is 'vertexai' or 'aws', optional otherwise.
               Specifies the AWS bedrock region.
               Note:
                   Applicable only if "api_type" is either 'vertexai' or 'aws'.
               Types: str

           model_args:
               Required if "api_type" is 'hugging_face', optional otherwise.
               Specifies the LLM arguments for generation.
               It can include the following keys:
                   - 'temperature': Adjusts prediction randomness by scaling logits before
                       softmax.
                   - 'top_k': Sets the limit for the highest probability vocabulary tokens
                       to keep for top-k-filtering.
                   - 'top_p': Sets the cumulative probability of the highest probability
                       vocabulary tokens to keep for nucleus sampling.
               Types: dict

           vertexai_cred:
               Required if "api_type" is 'vertexai', optional otherwise.
               Specifies the credentials file path of Vertex client.
               Note:
                   Applicable only if "api_type" is 'vertexai'.
               Types: string

           enable_safety:
               Optional Argument.
               Specifies whether to enable safety settings for the VertexAI inference.
               Note:
                   Applicable only if "api_type" is 'vertexai'.
               Types: bool
               Default: True

           resource:
               Optional Argument.
               Specifies the resource name for Azure AI embeddings.
               Note:
                   Applicable only if "api_type" is 'vertexai'.
               Types: str

           session_token:
               Optional Argument.
               Specifies the session token for AWS Bedrock embeddings.
               Note:
                   Applicable only if "api_type" is 'vertexai'.
               Types: str

           mode:
               Optional Argument.
               Specifies the mode of operation for the LLM.
               Note:
                   Applicable only if "api_type" is 'aws', 'azure', or 'vertexai'.
               Permitted Values: 'client', 'udf'
               Default Value: 'client'
               Types: str

        RETURNS:
           None

        RAISES:
           TeradataMlException, ValueError, TypeError

        EXAMPLES:

            # Import the required modules.
            >>> from teradatagenai import TeradataAI

            # Example 1: Create LLM endpoint for azure OpenAI.
            >>> obj = TeradataAI(api_type = "azure",
                                 api_base = "<https://****.openai.azure.com/>",
                                 api_version = "2000-11-35",
                                 api_key = <provide your llm API key>,
                                 deployment_id = <provide your azure OpenAI engine name>,
                                 model_name = "gpt-3.5-turbo")

            # Example 2: Create LLM endpoint for AWS bedrock.
            >>> obj = TeradataAI(api_type = "aws",
                                 api_key = <provide your llm secret API key>,
                                 deployment_id = <provide your AWS key ID>,
                                 api_region = "us-west-2",
                                 model_name = "anthropic.claude-v2",
                                 model_args = {"max_tokens_to_sample": 2048,
                                               "temperature": 0,
                                               "top_k": 250,
                                               "top_p": 1})

            # Example 3: Create LLM endpoint for VertexAI.
            >>> obj = TeradataAI(api_type = "vertexai",
                                 deployment_id = <provide your VertexAI project name>,
                                 model_name = "gemini-1.5-pro-001",
                                 api_region = "us-central1",
                                 enable_safety = True,
                                 vertexai_cred = "C:/Users/credential.cred",
                                 model_args = {"temperature": 1,
                                               "top_p": 0.95}
                                 )

            # Example 4: Access Azure OpenAI using 'resource' and 'deployment_id' parameters
            #            and set the mode to 'udf' for execution in Vantage.
            >>> obj = TeradataAI(api_type = "azure",
                                 api_key = "<Enter API Key>",
                                 deployment_id = <provide your Azure Deployment ID>,
                                 resource = <provide your Azure resource name>,
                                 model_name = "text-embedding-ada-002",
                                 mode = "udf")

            # Example 5: Access Azure OpenAI using 'api_base' parameter
            #            and set the mode to 'udf' for execution in Vantage.
            >>> obj = TeradataAI(api_type = "azure",
                                 api_key = "<Enter API Key>",
                                 api_base = "<Specify the UDF Endpoint URL>",
                                 model_name = "text-embedding-ada-002",
                                 mode = "udf")

            # Example 6: Access AWS Bedrock and set the mode to 'udf' for execution in Vantage.
            >>> obj = TeradataAI(api_type = "aws",
                                 api_key = "<Enter API Key>",
                                 deployment_id = "<Enter Deployment ID>",
                                 api_region = "us-west-2",
                                 model_name = "amazon.titan-embed-text-v1",
                                 mode = "udf")
        """
        deployment_id = kwargs.get('deployment_id', None)
        api_key = kwargs.get('api_key', None)
        api_base = kwargs.get('api_base', None)
        api_version = kwargs.get('api_version', None)
        api_region = kwargs.get('api_region', None)
        path_gc = kwargs.get('path_gc', None)
        vertexai_cred = kwargs.get('vertexai_cred', None)
        model_args = kwargs.get('model_args', None)

        super().__init__(api_type=api_type, model_name=model_name)

        # Check if the enable_safety is present in the kwargs.
        enable_safety = kwargs.get("enable_safety", True)

        resource = kwargs.get("resource", None)
        session_token = kwargs.get("session_token", '')
        mode = kwargs.get("mode", "client")

        azure = True if api_type == "azure" else False
        aws = True if api_type == "aws" else False
        vertex = True if api_type == "vertexai" else False
        udf = True if mode == "udf" else False
        client = True if mode == "client" else False

        arg_matrix = []
        permitted_values_mode = ["client", "udf"]
        arg_matrix.append(["deployment_id", deployment_id, not (client), (str), True])
        arg_matrix.append(["model_name", model_name, False, (str), True])
        arg_matrix.append(["api_key", api_key, not (azure or aws), (str), True])
        arg_matrix.append(["api_base", api_base, not (azure and client), (str), True])
        arg_matrix.append(["api_version", api_version, not (azure and client), (str), True])
        arg_matrix.append(["api_region", api_region, not (aws or vertex), (str), True])
        arg_matrix.append(["vertexai_cred", vertexai_cred, not vertex, (str), True])
        arg_matrix.append(["enable_safety", enable_safety, vertex, (bool), False])
        arg_matrix.append(["mode", mode, True, (str), False, permitted_values_mode])
        arg_matrix.append(["resource", resource, True, (str)])
        arg_matrix.append(["session_token", session_token, True, (str)])

        # Validate missing required arguments.
        _Validators._validate_missing_required_arguments(arg_matrix)
        # Validate file exists.
        if vertex:
            _Validators._validate_file_exists(vertexai_cred)

        # Validate argument types.
        _Validators._validate_function_arguments(arg_matrix)

        # Initialize the class variables.
        self.api_type = api_type

        if udf and aws:
            # Initialize AWS Bedrock embeddings specific attributes
            self.api_type = "aws-bedrock"
            self.__deployment_id = deployment_id
            self.model_name = model_name
            self.api_region = api_region
            self.api_key = api_key
            self.session_token = session_token

        elif udf and azure:
            # Initialize Azure AI embeddings specific attributes
            self.api_type = "az-ai-embedding"
            self.model_name = model_name
            self.resource = resource
            self.api_key = api_key
            self.__deployment_id = deployment_id
            self.api_base = api_base

        elif aws:
            # Create a dictionary to store AWS credentials and model details.
            cred = {
                "AWS_DEFAULT_REGION": api_region,  # AWS region where the service is hosted.
                "AWS_ACCESS_KEY_ID": deployment_id,  # AWS access key ID for authentication.
                "AWS_SECRET_ACCESS_KEY": api_key,  # AWS secret access key for authentication.
                "model_name": model_name,  # Name of the model to be used.
                "model_args": model_args  # Arguments to be passed to the model.
            }

            self.__setup_bedrock(cred)

        elif vertex:
            # Set all vertexai credentials.
            self.__deployment_id = deployment_id
            self.model_name = model_name
            self.__api_region = api_region
            self.model_args = model_args
            self.__generation_config = None

            self.__setup_vertexai(vertexai_cred, enable_safety)

        elif azure:
            # Set API Base URL as follow
            # "https://****instance.openai.azure.com/".
            self.api_base = api_base
            # Set API version like follow "2022-06-10".
            self.api_version = api_version
            # Set API key.
            self.api_key = api_key
            # Set LLM engine name.
            self.__deployment_id = deployment_id
            # Set model name.
            self.model_name = model_name

            # Update environment and openai variables.
            self.__set_llm_env()

            # Initialize AzureOpenAI LLM.
            if model_args is None:
                model_args = {}
            self._llm = AzureOpenAI(engine=self.__deployment_id, model_name=self.model_name, verbose=True, **model_args)

    def get_llm(self):
        """
        DESCRIPTION:
            Get LLM inference endpoint.

        PARAMETERS:
            None

        RETURNS:
            LLM endpoint object.

        RAISES:
            None

        EXAMPLES:
            obj.get_llm()
        """
        return self._llm

    def set_model_args(self, model_args):
        """
        DESCRIPTION:
            Update the model specific arguments.

        PARAMETERS:
            model_args:
                Required Argument.
                Specifies the model specific arguments.
                Types: dict

        RETURNS:
            None

        RAISES:
            TeradataMlException, TypeError

        EXAMPLES:
            obj.set_model_args(model_args)

        """
        arg_matrix = []
        arg_matrix.append(["model_args", model_args, False, (dict)])
        # Validate argument types.
        _Validators._validate_function_arguments(arg_matrix)

        self.model_args = model_args

        if self.api_type == "vertexai":
            self.__generation_config = GenerationConfig(
                temperature=self.model_args.get("temperature", None),
                top_p=self.model_args.get("top_p", None),
                top_k=self.model_args.get("top_k", None)
            )

    def __setup_vertexai(self, vertexai_cred, enable_safety=True):
        """
        DESCRIPTION:
            Internal function to setup vertex endpoind.

        PARAMETERS:
            vertexai_cred:
                Required Argument.
                Specifies the credentials file path of VertexAI client.
                Types: string

            enable_safety:
                Optional Argument.
                Specifies whether to enable safety settings for the VertexAI inference.
                Types: bool
                Default: True

        RETURNS:
            None

        RAISES:
            TeradataMlException, ValueError, TypeError

        EXAMPLES:
            self.__setup_vertexai(vertexai_cred, enable_safety)
        """
        # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable.
        _set_vertex_env(vertexai_cred=vertexai_cred)
        # Initialize VertexAI client.
        vertexai.init(project=self.__deployment_id, location=self.__api_region)

        # Set model parameters
        if self.model_args is not None:
            self.set_model_args(self.model_args)

        # Set safety settings
        self.__safety_settings = None if not enable_safety else {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        }

        # Initialize the LLM model.
        self._llm = GenerativeModel(self.model_name)

    def __set_llm_env(self):
        """
        DESCRIPTION:
            Internal function to set all LLM info in OS environment and
            openai variables.

        PARAMETERS:
            None

        RETURNS:
            None

        RAISES:
           None

        EXAMPLES:
            self.__set_llm_env()
        """
        # Set API type.
        openai.api_type = self.api_type
        # Set API Base URL as follow
        openai.api_base = self.api_base
        # Set API version.
        openai.api_version = self.api_version
        # Set API key.
        openai.api_key = self.api_key
        # Update OS environment variables.
        _set_openAI(api_type=self.api_type, api_base=self.api_base,
                    api_version=self.api_version, api_key=self.api_key)

    def __setup_bedrock(self, cred):
        """
        DESCRIPTION:
            Internal function to setup bedrock client using the provided credentials.

        PARAMETERS:
            cred:
                Required Argument.
                Specifies the credentials for the Bedrock client.
                Types: dict

        RETURNS:
            None

        RAISES:
            None

        EXAMPLES:
            self.__setup_bedrock(cred)
        """
        self._client = _get_bedrock_client(cred=cred)
        self._llm = Bedrock(model_id=cred["model_name"], client=self._client, model_kwargs=cred["model_args"])

    def answer(self, query):
        """
        DESCRIPTION:
            Get the answer to the query.

        PARAMETERS:
            query:
                Required Argument.
                Specifies the question which needs to be answered by LLM.
                Types: str

        RETURNS:
            str

        RAISES:
            TeradataMlException, TypeError

        EXAMPLES:
            obj.answer("Tell me a joke")
        """
        arg_matrix = []
        arg_matrix.append(["query", query, False, (str), True])
        # Validate argument types.
        _Validators._validate_function_arguments(arg_matrix)
        if self.api_type == "vertexai":
            response = self._llm.generate_content(query,
                                                  generation_config=self.__generation_config,
                                                  safety_settings=self.__safety_settings)
            return response.text
        return self._llm(query)

    def get_deployment_id(self):
        """
        DESCRIPTION:
            Get the deployment id of the LLM.

        PARAMETERS:
            None

        RETURNS:
            str

        RAISES:
            None

        EXAMPLES:
            obj.get_deployment_id()
        """
        return self.__deployment_id

class _TeradataAIHuggingFace(_TeradataAIStruct):

    """
    Class to hold the functions required to setup the enviornment
    to use the hugging face models.
    """
    def __init__(self, model_name, **kwargs):
        """
        DESCRIPTION:
            Constructor to instantiate the class.
            Instantiation helps setup the environment,
            which includes downlaoding and installing the hugging face model.
            Prerequites for BYO LLM:
                * Bring Your Own LLM is a capability of Teradata’s Open Analytics Framework
                  which works on Vantage Cloud Lake on AWS only.
                * The combination of LLMs and GPU processing significantly boosts performance,
                  leading to a larger impact. To support these capabilities,
                  Teradata has added a new Analytic GPU cluster to the VantageCloud
                  Lake environment. Though BYO LLM work with Analytic clusters,
                  it is advisable to use with Analytic GPU clusters.
                Notes:
                    * When using any api_type as 'hugging_face', make sure to,
                        * establish connection with database using 'create_context()' function from teradataml.
                        * authenticate against the CCP using 'set_auth_token()' function from teradataml.
                    * Currently we can bring in hugging face models only upto 5 GB.

        PARAMETERS:
           api_type:
               Required Argument.
               Specifies the LLM API type.
               Permitted Values: 'azure', 'aws', 'vertexai', 'hugging_face'
               Types: str

           model_name:
               Required Argument.
               Specifies the LLM model name.
               Types: str

           model_args:
               Required Argument.
               Specifies the LLM arguments for generation.
               It can include the following keys:
                   - 'transformer_class': Sets the class specific to the model which allows
                                          easy loading of models.
                   - 'task': Specifies the task defining which pipeline will be returned.
                             This is used for doing tasks like sentiment-analysis,
                             summarization using the same model.
                             Note: Set the 'task' here if it is common to all TextAnalytics
                                   functions else we can set them at individual function calls.
                             More details can be found here:
                                https://huggingface.co/docs/transformers/en/main_classes/pipelines.
               Types: dict

           ues_args:
               Optional Argument.
               Specifies the parameters for the user environment service.
               It can include the following arguments:
                   - 'env_name': Specifies the remote user env. It can be the
                                 name of env or the UserEnv object.
               Types: dict

           asynchronous:
                Optional Argument.
                Specifies whether the model installation should be asynchronous.
                Default Value: False
                Types: bool

        RETURNS:
           None

        RAISES:
           TeradataMlException, ValueError, TypeError

        EXAMPLES:
            # Import the required modules.
            >>> from teradatagenai import TeradataAI

            # Example 1: Setup the environment to work with the
            #            'xlm-roberta-base-language-detection' hugging_face model.
            >>> model_name = 'papluca/xlm-roberta-base-language-detection'
            >>> model_args = {'transformer_class': 'AutoModelForSequenceClassification',
                              'task': 'text-classification'}
            >>> llm = TeradataAI(api_type = "hugging_face",
                                 model_name = model_name,
                                 model_args = model_args)

            # Example 2: Setup the environment 'demo' to work with the
            #            'xlm-roberta-base-language-detection' hugging_face model.
            >>> model_name = 'papluca/xlm-roberta-base-language-detection'
            >>> model_args = {'transformer_class': 'AutoModelForSequenceClassification',
                              'task' : 'text-classification'}
            >>> ues_args = {'env_name': 'demo'}
            >>> llm = TeradataAI(api_type = "hugging_face",
                                 model_name = model_name,
                                 model_args = model_args,
                                 ues_args = ues_args)
        """
        super().__init__(api_type="hugging_face", model_name=model_name)

        self._ues_args = kwargs.get("ues_args", {})
        self.model_args = kwargs.get('model_args', None)
        arg_matrix = []
        arg_matrix.append(["ues_args", self._ues_args, True, dict])
        arg_matrix.append(["model_args", self.model_args, False, dict])

        # Validate missing required arguments.
        _Validators._validate_missing_required_arguments(arg_matrix)
        # Validate argument types.
        _Validators._validate_function_arguments(arg_matrix)

        # Validate model_args and ues_args
        self.model_name = model_name
        self._transformer_class = self.model_args.get('transformer_class', None)
        self._task = self.model_args.get('task', None)
        env_name = self._ues_args.get("env_name", "td_gen_ai_env")
        self.__asynchronous = kwargs.get('asynchronous', None)
        arg_matrix = []
        arg_matrix.append(["transformer_class", self._transformer_class, False, str, True])
        arg_matrix.append(["task", self._task, True, (str), True])
        arg_matrix.append(["env_name", env_name, True, (str, UserEnv), True])
        arg_matrix.append(["asynchronous", self.__asynchronous, True, bool, True])

        # Validate missing required arguments.
        _Validators._validate_missing_required_arguments(arg_matrix)

        # Validate argument types.
        _Validators._validate_function_arguments(arg_matrix)

        # Set the example-data path which is base dir for all the example files.
        self.__base_dir = os.path.dirname(os.path.dirname(__file__))

        # Create/set a default env - td_gen_ai_env if env_name is not provided by the user.
        if isinstance(env_name, UserEnv):
            self._env = env_name
        else:
            # Get environments created by the current logged in user.
            user_envs_df = list_user_envs()
            is_none_user_env = user_envs_df is None
            env_not_exists = env_name not in user_envs_df.env_name.values if not is_none_user_env else True
            # If there are no envs or if the given env_name does not exist,
            # raise an error if it is anything other than default env.
            # If its default env, create it.
            if is_none_user_env or env_not_exists:
                if env_name == "td_gen_ai_env":
                    json_file = os.path.join(self.__base_dir, "example-data",
                                             "td_gen_ai_env_template.json")
                    create_env(template=json_file)
                # Raise an error if any other env_name is given which is not present.
                else:
                    raise Exception(
                        "User environment not present. Either use the default environment"
                        " or create the environment and pass the name.")
            # Get the env from env_name.
            self._env = get_env(env_name)
        print(f"Using env: '{env_name}'.")
        self._install_model(**kwargs)
        self._llm = model_name

    def _install_model(self, **kwargs):
        """
        DESCRIPTION:
            Install the model if not present in the user_env.

        PARAMETERS:
            asynchronous:
                Optional Argument.
                Specifies whether the model installation should be asynchronous.
                Default Value: False
                Types: bool

        RETURNS:
            None

        RAISES:
            None
        """
        if self._env.models is None or (not
        any(self._env.models['Model'].isin([self.model_name.split('/')[1]]))):
            model_path = "{}.zip".format(self.model_name.split('/')[1])
            try:
                globals()[self._transformer_class] = getattr(importlib.import_module("transformers"),
                                                             self._transformer_class)
                globals()["AutoTokenizer"] = getattr(importlib.import_module("transformers"), "AutoTokenizer")
                print("Model download started.")
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = eval("{}.from_pretrained('{}')".format(self._transformer_class, self.model_name))
                self.__save_zip()
                print("Model download completed.")

                claim_id = self._env.install_model(model_path=model_path, asynchronous=True)

                # If asynchronous is set to False, the cursor will not move ahead
                # and will keep checking till the model is installed.
                if not self.__asynchronous:
                    status = "STARTED"
                    print("Model installation started.")

                    pg = _ProgressBar(jobs=100, prefix="Installing", verbose=2)
                    while True:
                        if status.upper() in ['FILE INSTALLED', 'ERRORED']:
                            pg.completed_jobs = 99
                            pg.update(msg="Model Installation completed.")
                            break

                        response = self._env.status(claim_id).to_dict('records')
                        status = response[-1].get("Stage", "")
                        pg.update()
                        sleep(20)
            finally:
                os.remove(model_path)
                shutil.rmtree(f"{self.model_name.split('/')[1]}", ignore_errors=False)
        else:
            print("Model is already available in the user environment.")

    def __save_zip(self):
        """
        DESCRIPTION:
            Zip the downloaded model which is used for upload.

        PARAMETERS:
            None

        RETURNS:
            None

        RAISES:
            None
        """
        model_name = self.model_name.split('/')[1]
        self.tokenizer.save_pretrained("./{}".format(model_name))
        self.model.save_pretrained("./{}".format(model_name))
        shutil.make_archive(model_name, 'zip', model_name)

    def get_llm(self):
        """
        DESCRIPTION:
            Get the name of hugging face model.

        PARAMETERS:
            None

        RETURNS:
            str

        RAISES:
            None

        EXAMPLES:
            # Import the required modules.
            >>> from teradatagenai import TeradataAI

            # Example 1: Setup the environment to work with the
            #            'xlm-roberta-base-language-detection' hugging_face model.
            >>> model_name = 'papluca/xlm-roberta-base-language-detection'
            >>> model_args = {'transformer_class': 'AutoModelForSequenceClassification',
                              'task': 'text-classification'}
            >>> llm = TeradataAI(api_type = "hugging_face",
                                 model_name = model_name,
                                 model_args = model_args)
            # Get the LLM in use.
            >>> llm.get_llm()
        """
        return self.model_name

    def remove(self):
        """
        DESCRIPTION:
            Remove the installed hugging_face model.

        PARAMETERS:
            None

        RETURNS:
            None

        RAISES:
            None

        EXAMPLES:
            # Import the required modules.
            >>> from teradatagenai import TeradataAI

            # Example 1: Removing the installed model
            #            'xlm-roberta-base-language-detection'.

            # Setup the env and install the model.
            >>> model_name = 'papluca/xlm-roberta-base-language-detection'
            >>> model_args = {'transformer_class': 'AutoModelForSequenceClassification',
                              'task' : 'text-classification'}
            >>> llm = TeradataAI(api_type = "hugging_face",
                                 model_name = model_name,
                                 model_args = model_args)

            # Remove the model
            >>> llm.remove()
        """
        print(f"Uninstalling model from user environment: '{self.model_name.split('/')[1]}'.")
        self._env.uninstall_model(self.model_name.split('/')[1])
        print(f"Successfully uninstalled model: '{self.model_name.split('/')[1]}'.")

    def get_env(self):
        """
        DESCRIPTION:
            Get the user enviornment in use.

        PARAMETERS:
            None

        RETURNS:
            UserEnv object.

        RAISES:
            None

        EXAMPLES:
            # Example 1: Get the user enviornment in use while installing the
            #           'xlm-roberta-base-language-detection' hugging face model.
            >>> model_name = 'papluca/xlm-roberta-base-language-detection'
            >>> model_args = {'transformer_class': 'AutoModelForSequenceClassification',
                              'task' : 'text-classification'}
            >>> llm = TeradataAI(api_type = "hugging_face",
                                 model_name = model_name,
                                 model_args = model_args)
            >> llm.get_env()
        """
        return self._env

    def get_model_args(self):
        """
        DESCRIPTION:
            Get the model args which are being used.
            Specifically the 'transformer_class' and the 'pipeline'.

        PARAMETERS:
            None

        RETURNS:
            None

        RAISES:
            None

        EXAMPLES:
            # Example 1: Get the model args which are used while installing the
            #           'xlm-roberta-base-language-detection' hugging face model.
            >>> model_name = 'papluca/xlm-roberta-base-language-detection'
            >>> model_args = {'transformer_class': 'AutoModelForSequenceClassification',
                              'task' : 'text-classification'}
            >>> llm = TeradataAI(api_type = "hugging_face",
                                 model_name = model_name,
                                 model_args = model_args)
            >>> llm.get_model_args()
        """
        return self.model_args

    def task(self, **kwargs):
        """
        DESCRIPTION:
            This function can do any task which the llm supports.
            The advantage of this method is that it is not bounded
            to any operation and can be tweaked
            according to the requirements.
            Refer to the example for more details on how it can be used.

        PARAMETERS:
            column:
                Required Argument.
                Specifies the column(s) of the teradataml DataFrame
                which needs to be used for inferencing.
                Types: str or list of str

            data:
                Required Argument.
                Specifies the teradataml DataFrame containing the column(s)
                specified in "column" to analyze the content from.
                Types: teradataml DataFrame

            returns:
                Required Argument.
                Specifies the "returns" argument for the apply query.
                This is used mainly when the user writes his own script for
                inferencing. It contains a dict which specifies the
                column name as key and datatype as the value.
                For example:
                    The script returns two columns ‘text’ and ‘sentiment’
                    of VARCHAR datatype, then the "returns" argument
                    looks like this:
                    {"text": VARCHAR(10000), "sentiment": VARCHAR(10000)}
                Default Value: {"Text": VARCHAR(10000), "Sentiment": VARCHAR(10000)}
                Types: dict

            script:
                Required Argument.
                Specifies the user defined script for inferencing.
                This is used when the user wants to use the model to
                process the input and output in a user defined way.
                Refer to the sample script attached in the user guide for more
                details on custom script compilation.
                Types: str

            persist:
                Optional Argument.
                Specifies whether to persist the output or not.
                When set to True, results are stored in permanent tables,
                otherwise in volatile tables.
                Default Value: False
                Types: bool

            delimiter:
                Optional Argument.
                Specifies a delimiter to use when reading columns from a row and
                writing result columns. Delimiter must be a valid Unicode code point.
                Notes:
                    1) The "quotechar" cannot be the same as the Delimiter.
                    2) The value of delimiter cannot be an empty string,
                       newline and carriage return.
                Default value: comma (,)
                Types: str

            quotechar:
                Optional Argument.
                Specifies the character used to quote all input and
                output values for the script.
                Note:
                    * The "quotechar" cannot be the same as the "delimiter".
                Default value: double quote (")
                Types: str

            libs:
                Optional Argument.
                Specifies the add-on python library name(s)
                to be installed.
                Types: str OR list of str

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException, TypeError, ValueError

        EXAMPLES:
            # Import the modules and create a teradataml DataFrame.
            >>> import os
            >>> import teradatagenai
            >>> from teradatagenai import TeradataAI, TextAnalyticsAI, load_data
            >>> from teradataml import DataFrame
            >>> load_data('employee', 'employee_data')
            >>> data = DataFrame('employee_data')
            >>> df_articles = data.select(["employee_id", "employee_name", "articles"])
            >>> base_dir = os.path.dirname(teradatagenai.__file__)

            # Create LLM endpoint.
            >>> model_name = 'sentence-transformers/all-MiniLM-L6-v2'
            >>> model_args = {'transformer_class': 'AutoModelForTokenClassification',
                              'task': 'token-classification'}
            >>> llm = TeradataAI(api_type = "hugging_face",
                                 model_name = model_name,
                                 model_args = model_args)

            # Example 1: Generate the embeddings for employee reviews from the 'articles' column
            #            of a teradataml DataFrame using hugging face model 'all-MiniLM-L6-v2'.

            >>> embeddings_script = os.path.join(base_dir,
                                                 'example-data',
                                                 'embeddings.py')
            # Construct returns argument based on the user script.
            >>> returns = OrderedDict([('text', VARCHAR(512))])

            >>> _ = [returns.update({"v{}".format(i+1): VARCHAR(1000)}) for i in range(384)]
            >>> llm.task(column = "articles",
                         data = df_articles,
                         script = embeddings_script,
                         returns = returns,
                         libs = 'sentence_transformers',
                         delimiter = '#')

            # Example 2: Get the similarity score for 'employee_data' and 'articles' columns
            #            using the same hugging face model: 'all-MiniLM-L6-v2'.
            >>> sentence_similarity_script = os.path.join(base_dir, 'example-data',
                                                          'sentence_similarity.py')
            >>> llm.task(column = ["employee_data", "articles"],
                         data = data,
                         script = sentence_similarity_script,
                         libs = 'sentence_transformers',
                         returns = {"column1": VARCHAR(10000),
                                    "column2": VARCHAR(10000),
                                    "similarity_score": VARCHAR(10000)},
                         delimiter = "#")
        """
        from teradatagenai.text_analytics.TextAnalyticsAIHuggingFace\
            import _TextAnalyticsAIHuggingFace

        validate_matrix = []
        validate_matrix.append(["script", kwargs.get('script', None),
                                False, (str)])
        validate_matrix.append(["returns", kwargs.get('returns', None), False, (str)])
        # Validate missing required arguments.
        _Validators._validate_missing_required_arguments(validate_matrix)

        return _TextAnalyticsAIHuggingFace(self)._exec(**kwargs)

class TeradataAI:
    """
    Class sets up the environment and initializes the LLM endpoint depending
    on the API type.
    It also wraps the instance of '_TeradataAIClient' and '_TeradataAIHuggingFace'
    into TeradataAI instance.
    """
    def __init__(self, api_type, model_name, **kwargs):
        """
        DESCRIPTION:
            Instantiates the TeradataAI class to set up the
            environment and initializes the LLM endpoint.
            Prerequites for BYO LLM:
                * Bring Your Own LLM is a capability of Teradata’s Open
                  Analytics Framework which works on Vantage Cloud Lake.
                  Look at the respective user guide for more details.
                * The combination of LLMs and GPU processing significantly
                  boosts performance, leading to a larger impact.
                  To support these capabilities, Teradata has added a new
                  Analytic GPU cluster to the VantageCloud
                  Lake environment. Though BYO LLM work with Analytic clusters,
                  it is advisable to use with Analytic GPU clusters.
               Notes:
                    * When using any api_type as 'hugging_face', make sure to,
                        * establish connection with database using 'create_context()'
                          function from teradataml.
                        * authenticate against the CCP using 'set_auth_token()'
                          function from teradataml.
                    * Currently we can bring in hugging face models only upto 5 GB.
        PARAMETERS:
           api_key:
               Required if "api_type" is 'azure' or 'aws',
               optional otherwise.
               Specifies the LLM API key.
               Note:
                   Applicable only if "api_type" is either 'azure' or 'aws'.
               Types: str

           api_type:
               Required Argument.
               Specifies the LLM API type.
               Permitted Values: 'azure', 'aws', 'vertexai', 'hugging_face'
               Types: str

           deployment_id:
               Required if "api_type" is 'azure', 'aws' or 'vertexai'
               and "mode" is 'client', optional otherwise.
               Specifies the deployment ID of the LLM.
               This argument accepts:
                    * engine id for azure OpenAI,
                    * project name for VertexAI and
                    * access key ID for AWS bedrock.
               Note:
                   Applicable only if "api_type" is 'azure', 'aws',
                   or 'vertexai', and "mode" is 'client'.
               Types: str

           model_name:
               Required Argument.
               Specifies the LLM model name.
               Types: str

           api_base:
               Required if "api_type" is 'azure' and "mode" is 'client', optional
               otherwise.
               Specifies AzureAI LLM endpoint URL.
               Note:
                   Applicable only if "api_type" is either 'azure' or 'aws',
                   and "mode" is 'client'.
               Types: str

           api_version:
               Required if "api_type" is 'azure' and "mode" is 'client',
               optional otherwise.
               Specifies the LLM API version.
               Note:
                   Applicable only if "api_type" is either 'azure' or 'aws',
                   and "mode" is 'client'.
               Types: str

           api_region:
               Required if "api_type" is 'vertexai' or 'aws', optional otherwise.
               Specifies the AWS bedrock region.
               Note:
                   Applicable only if "api_type" is either 'vertexai' or 'aws'.
               Types: str

           model_args:
               Required if "api_type" is 'hugging_face', optional otherwise.
               Specifies the LLM arguments for generation.
               It can include the following keys:
                   - 'temperature': Adjusts prediction randomness by scaling logits before
                       softmax.
                   - 'top_k': Sets the limit for the highest probability vocabulary tokens
                       to keep for top-k-filtering.
                   - 'top_p': Sets the cumulative probability of the highest probability
                       vocabulary tokens to keep for nucleus sampling.
                   - 'transformer_class': Sets the class specific to the model which allows
                                          easy loading of models.
                                          Note:
                                            Only applicable if "api_type" is 'hugging_face'.
                   - 'task': Sets the task defining which pipeline will be returned.
                             Note:
                                Only applicable if "api_type" is 'hugging_face'.
               Types: dict

           vertexai_cred:
               Required if "api_type" is 'vertexai', optional otherwise.
               Specifies the credentials file path of Vertex client.
               Note:
                   Applicable only if "api_type" is 'vertexai'.
               Types: string

           enable_safety:
               Optional Argument.
               Specifies whether to enable safety settings for the VertexAI inference.
               Note:
                   Applicable only if "api_type" is 'vertexai'.
               Default Value: True
               Types: bool

           resource:
               Optional Argument.
               Specifies the resource name for Azure AI embeddings.
               Note:
                   Applicable only if "api_type" is 'azure'.
               Types: str

           session_token:
               Optional Argument.
               Specifies the session token for AWS Bedrock embeddings.
               Note:
                    Applicable only if "api_type" is 'aws'.
               Types: str

           mode:
               Optional Argument.
               Specifies the mode of operation for the LLM.
               Note:
                   Applicable only if "api_type" is 'aws', 'azure', or 'vertexai'.
               Permitted Values: 'client', 'udf'
               Default Value: 'client'
               Types: str

           ues_args:
               Optional Argument.
               Specifies the parameters for the user environment service.
               It can include the following arguments:
                   - 'env_name': Specifies the remote user env. It can be the
                                 name of env or the UserEnv object.
                                 Note:
                                     If not specified, the model is installed in
                                     the default env which is 'td_gen_ai_env'.
               Note:
                   Applicable only if "api_type" is 'hugging_face'.
               Types: dict

           asynchronous:
                Optional Argument.
                Specifies whether the model installation should be
                asynchronous or not.
                Note:
                    Applicable only if "api_type" is 'hugging_face'.
                Default Value: False
                Types: bool

        RETURNS:
           None

        RAISES:
           TeradataMlException, ValueError, TypeError

        EXAMPLES:

        # Import the required modules.
        >>> from teradatagenai import TeradataAI

        # Example 1: Create LLM endpoint for azure OpenAI.
        >>> obj = TeradataAI(api_type = "azure",
                             api_base = "<https://****.openai.azure.com/>",
                             api_version = "2000-11-35",
                             api_key = <provide your llm API key>,
                             deployment_id = <provide your azure OpenAI engine name>,
                             model_name = "gpt-3.5-turbo")

        # Example 2: Create LLM endpoint for AWS bedrock.
        >>> obj = TeradataAI(api_type = "aws",
                             api_key = <provide your llm secret API key>,
                             deployment_id = <provide your AWS key ID>,
                             api_region = "us-west-2",
                             model_name = "anthropic.claude-v2",
                             model_args = {"max_tokens_to_sample": 2048,
                                           "temperature": 0,
                                           "top_k": 250,
                                           "top_p": 1})

        # Example 3: Create LLM endpoint for VertexAI.
        >>> obj = TeradataAI(api_type = "vertexai",
                             deployment_id = <provide your VertexAI project name>,
                             model_name = "gemini-1.5-pro-001",
                             api_region = "us-central1",
                             enable_safety = True,
                             vertexai_cred = "C:/Users/credential.cred",
                             model_args = {"temperature": 1,
                                           "top_p": 0.95}
                             )

        # Example 4: Access Azure OpenAI using 'resource' and 'deployment_id' parameters
        #            and set the mode to 'udf' for execution in Vantage.
        >>> obj = TeradataAI(api_type = "azure",
                             api_key = "<Enter API Key>",
                             deployment_id = <provide your Azure Deployment ID>,
                             resource = <provide your Azure resource name>,
                             model_name = "text-embedding-ada-002",
                             mode = "udf")

        # Example 5: Access Azure OpenAI using 'api_base' parameter
        #            and set the mode to 'udf' for execution in Vantage.
        >>> obj = TeradataAI(api_type = "azure",
                             api_key = "<Enter API Key>",
                             api_base = "<Specify the UDF Endpoint URL>",
                             model_name = "text-embedding-ada-002",
                             mode = "udf")

        # Example 6: Access AWS Bedrock and set the mode to 'udf' for execution in Vantage.
        >>> obj = TeradataAI(api_type = "aws",
                             api_key = "<Enter API Key>",
                             deployment_id = "<Enter Deployment ID>",
                             api_region = "us-west-2",
                             model_name = "amazon.titan-embed-text-v1",
                             mode = "udf")

        # Example 7: Setup the environment to work with the
        #            'xlm-roberta-base-language-detection' hugging_face model.
        >>> model_name = 'papluca/xlm-roberta-base-language-detection'
        >>> model_args = {'transformer_class': 'AutoModelForSequenceClassification',
                          'task' : 'text-classification'}
        >>> llm = TeradataAI(api_type = "hugging_face",
                             model_name = model_name,
                             model_args = model_args)

        # Example 8: Setup the environment 'demo' to work with the
        #            'xlm-roberta-base-language-detection' hugging_face model.
        >>> model_name = 'papluca/xlm-roberta-base-language-detection'
        >>> model_args = {'transformer_class': 'AutoModelForSequenceClassification',
                          'task' : 'text-classification'}
        >>> ues_args = {'env_name': 'demo'}
        >>> llm = TeradataAI(api_type = "hugging_face",
                             model_name = model_name,
                             model_args = model_args,
                             ues_args = ues_args)
        """

        arg_matrix = []
        model_args = kwargs.get('model_args', None)

        # Define permitted values for api_type
        permitted_values_api = ["azure", "aws", "vertexai", "hugging_face"]
        arg_matrix.append(["api_type", api_type, False, str, False, permitted_values_api])
        arg_matrix.append(["model_name", model_name, False, (str), True])
        arg_matrix.append(["model_args", model_args, True, (dict)])
        # Validate missing required arguments.
        _Validators._validate_missing_required_arguments(arg_matrix)
        # Validate argument types.
        _Validators._validate_function_arguments(arg_matrix)

        api_type = api_type.lower()

        mapping_dict = {'azure': _TeradataAIClient,
                        'aws': _TeradataAIClient,
                        'vertexai': _TeradataAIClient,
                        'hugging_face': _TeradataAIHuggingFace}
        self._wrapped_instance = mapping_dict[api_type](api_type=api_type,
                                                        model_name=model_name,
                                                        **kwargs)

    def __getattr__(self, name):
        """
        DESCRIPTION:
            Delegate attribute access to the wrapped instance

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