import logging
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    """
    Retrieve Redis cache hit/miss metrics and calculate the cache hit ratio.
    Returns:
        dict: {'hits': int, 'misses': int, 'hit_ratio': float}
    """
    try:
        redis_conn = get_redis_connection("default")
        info = redis_conn.info()

        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total_requests = hits + misses

        hit_ratio = hits / total_requests if total_requests > 0 else 0

        metrics = {
            "hits": hits,
            "misses": misses,
            "hit_ratio": round(hit_ratio * 100, 2)
        }

        logger.info(f"Redis Cache Metrics → Hits: {hits}, Misses: {misses}, Hit Ratio: {metrics['hit_ratio']}%")
        return metrics

    except Exception as e:
        logger.error(f"Error retrieving Redis metrics: {e}")
        return {"hits": 0, "misses": 0, "hit_ratio": 0.0}
