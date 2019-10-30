import boto3
import os
import json


class UpdateSpamScoreStub(object):
    """
    Helper class that can be used to invoke the `UpdateSpamScore` Lambda from
    other Lambdas.  It is a small wrapper around the main AWS SDK Lambda invoke
    mechanisms.  It handles accepting the normal arguments, verifying the
    result, and parsing the response.

    NOTE: This relies on a `LAMBDA_UPDATE_SPAM_SCORE` environment variable
    containing the ARN of the `UpdateSpamScore` Lambda to use.
    """

    def __init__(self):
        """
        Initializes an instance that can be used to invoked the UpdateSpamScore Lambda.
        """
        self.__lambda_arn = os.environ.get('LAMBDA_UPDATE_SPAM_SCORE', default=None)
        if self.__lambda_arn is None:
            raise MissingLambdaArn()
        self.__lambda_client = boto3.client('lambda')

    def invoke(self, payload, algorithm, score):
        """
        Invokes the UpdateSpamScore Lambda, blocks for a response, and returns
        the result.

        If this calls is unsuccessful, a `UpdateSpamScoreFailure` exception
        will be raised.

        :param payload: The image payload whose spam score is being updated.
        :type payload: dict
        :param algorithm: The name of the algorithm reporting its score
        :type algorithm: str
        :param score: The spam score that this algorithm gave to the image.
        :type score: Number

        :return: The response body if the request is successful.
        :rtype: str
        """
        args = {"image_payload": payload, "score": score, "algorithm": algorithm}

        response = self.__lambda_client.invoke(
            FunctionName=self.__lambda_arn,
            InvocationType='RequestResponse',
            Payload=json.dumps(args),
        )
        if response['StatusCode'] != 200:
            raise UpdateSpamScoreFailure(response['StatusCode'])

        return json.loads(response['Payload'].read())['body']


class MissingLambdaArn(Exception):
    """
    Raised if the environment variable containing the Lambda is missing.
    """

    pass


class UpdateSpamScoreFailure(Exception):
    """
    Raised if an invocations of the UpdateSpamScore Lambda fails.
    """

    def __init__(self, status_code):
        """
        Creates an instance.

        :param status_code: The http status code
        :type status_code: Number
        """
        self.__status_code = status_code

    @property
    def status_code(self):
        return self.__status_code
