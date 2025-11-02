from django.core.cache import cache
from .models import Property
import logging
from django_redis import get_redis_connection

def get_all_properties():
    """
    Fetch all Property objects from cache if available,
    otherwise from the database, then store them in cache for 1 hour.
    """
    properties = cache.get('all_properties')
    if not properties:
        properties = list(Property.objects.all())
        cache.set('all_properties', properties, 3600)  # cache for 1 hour (3600 seconds)
    return properties

logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    """
    Retrieve Redis cache hit/miss metrics and calculate the cache hit ratio.
    Returns:
        dict: {'hits': int, 'misses': int, 'hit_ratio': float}
    """
    try:
        # Connect to Redis via Django cache backend
        redis_conn = get_redis_connection("default")
        
        # Fetch stats
        info = redis_conn.info()
        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        
        # Calculate hit ratio safely
        total = hits + misses
        hit_ratio = (hits / total) if total > 0 else 0.0

        metrics = {
            "hits": hits,
            "misses": misses,
            "hit_ratio": round(hit_ratio * 100, 2),  # percentage
        }

        logger.info(f"Redis Cache Metrics → Hits: {hits}, Misses: {misses}, Hit Ratio: {metrics['hit_ratio']}%")
        return metrics

    except Exception as e:
        logger.error(f"Error retrieving Redis metrics: {e}")
        return {"hits": 0, "misses": 0, "hit_ratio": 0.0}
