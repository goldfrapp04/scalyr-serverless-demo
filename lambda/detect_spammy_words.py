import json


def handler(event, context):
    print('request: {}'.format(json.dumps(event)))
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/plain'},
        'body': 'Hello, Detect Spammy Words Friend, you have reached {}\n'.format(event['path']),
    }
