import json

from lambda_common import UpdateSpamScoreStub

_update_spam_score = UpdateSpamScoreStub()


def handler(event, _context):
    print('request: {}'.format(json.dumps(event)))

    message = json.loads(event['Records'][0]['Sns']['Message'])
    print('message: {}'.format(json.dumps(message)))

    root_trace_id = message['RootTraceID']
    print(f'RootTraceID: {root_trace_id}')

    # The first argument should be the image payload.  Leaving blank for now.
    response = _update_spam_score.invoke(dict(), "detect_adult_content", 5.0)

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/plain'},
        'body': 'Hello, Detect Adult Content Friend, you have reached {}.  '
        'Update response was {}\n'.format(event['path'], response),
    }
