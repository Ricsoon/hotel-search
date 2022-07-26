def normalize_path_params(city=None, rank_min=0,rank_max=5, daily_min=0, daily_max=10000, limit=50, offset=0, **data):
    if city:
        return {
            "rank_min": rank_min,
            "rank_max": rank_max,
            "daily_min": daily_min,
            "daily_max": daily_max,
            "city": city,
            "limit": limit,
            "offset": offset
        }
    return {
            "rank_min": rank_min,
            "rank_max": rank_max,
            "daily_min": daily_min,
            "daily_max": daily_max,
            "limit": limit,
            "offset": offset
        }

query_without_city = "SELECT * FROM hotels WHERE (rank >= ? and rank <= ?) and (daily >= ? and daily <= ?) LIMIT ? OFFSET ?"

query_with_city = "SELECT * FROM hotels WHERE (rank >= ? and rank <= ?) and (daily >= ? and daily <= ?) and city = ? LIMIT ? OFFSET ?"