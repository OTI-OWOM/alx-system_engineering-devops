#!/usr/bin/python3
"""Module for recursively retrieving hot articles from a Reddit subreddit."""

import requests
import sys


def recurse(subreddit, hot_list=None):
    """
    Recursively retrieve hot articles for a given subreddit.

    Args:
        subreddit (str): Name of the subreddit to query
        hot_list (list, optional): Accumulator for article titles

    Returns:
        list or None: List of hot article titles or None if invalid subreddit
    """
    # Initialize hot_list on first call
    if hot_list is None:
        hot_list = []

    # Reddit API URL and headers
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {
        'User-Agent': 'python:recurse.subreddit:v1.0'
    }

    # Parameters for pagination
    params = {'limit': 100}
    if len(hot_list) > 0:
        params['after'] = f't3_{hot_list[-1]["id"]}' if hot_list else None

    try:
        # Send GET request without redirects
        response = requests.get(
            url, 
            headers=headers, 
            params=params, 
            allow_redirects=False
        )

        # Check for invalid subreddit
        if response.status_code != 200:
            return None

        # Parse response
        results = response.json()

        # Validate response structure
        if 'data' not in results or 'children' not in results['data']:
            return None

        # Extract posts
        posts = results['data']['children']

        # If no more posts, return the list
        if not posts:
            return hot_list if hot_list else None

        # Add posts to the list
        hot_list.extend(posts)

        # Recursive call to get next page
        return recurse(subreddit, hot_list)

    except Exception:
        return None
