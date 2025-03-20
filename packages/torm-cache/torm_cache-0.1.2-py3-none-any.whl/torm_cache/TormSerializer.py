from functools import partial

import orjson
from requests_cache.serializers.pipeline import SerializerPipeline, Stage
from requests_cache.serializers.preconf import make_stage

_orjson_pre = make_stage('cattr.preconf.orjson')

def torm_serializer():
    return SerializerPipeline(
        stages=[
            _orjson_pre,
            Stage(dumps=partial(orjson.dumps), loads=orjson.loads),
        ],
        name="torm_serializer",
        is_binary=False
    )
