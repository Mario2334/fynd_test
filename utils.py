from bson import json_util
import json as json_parser


def parse_json(data):
    return json_parser.loads(json_util.dumps(data))