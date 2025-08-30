from django.core.cache import cache
from properties.models import Property
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    """
    Returns all Property objects, cached in Redis for 1 hour.
    """
    properties = cache.get('all_properties')
    if properties is None:
        properties = list(Property.objects.all())
        cache.set('all_properties', properties, 3600)
    return properties


def get_redis_cache_metrics():
    """
    Retrieves Redis cache hit/miss metrics and logs the hit ratio.
    Returns a dictionary with hits, misses, and hit ratio.
    """
    client = cache.client.get_client(write=True) # type: ignore
    
    info = client.info(section='stats')
    hits = info.get('keyspace_hits', 0)
    misses = info.get('keyspace_misses', 0)

    total = hits + misses
    hit_ratio = (hits / total) if total > 0 else 0.0

    metrics = {
        'hits': hits,
        'misses': misses,
        'hit_ratio': hit_ratio,
    }

    logger.info(f"Redis Cache Metrics: Hits={hits}, Misses={misses}, Hit Ratio={hit_ratio:.2f}")
    
    return metrics
