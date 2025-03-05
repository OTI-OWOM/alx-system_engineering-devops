#!/usr/bin/python3
"""Module for recursively counting keywords in Reddit subreddit hot articles."""

import re
import requests


def count_words(subreddit, word_list, after=None, word_count=None):
    """
    Recursively count keywords in hot articles of a given subreddit.

    Args:
        subreddit (str): Name of the subreddit to query
        word_list (list): List of keywords to count
        after (str, optional): Pagination token for next page of results
        word_count (dict, optional): Accumulator for keyword counts

    Returns:
        dict: Dictionary of keyword counts
    """
    # Initialize word_count on first call
    if word_count is None:
        # Normalize word_list: lowercase and remove duplicates
        word_list = list(set(word.lower() for word in word_list))
        word_count = {word: 0 for word in word_list}

    # Reddit API endpoint
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    
    # Request parameters
    params = {'limit': 100}
    if after:
        params['after'] = after

    # Headers to prevent blocking
    headers = {
        'User-Agent': 'python:subreddit.keyword.counter:v1.0'
    }

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

        # If no posts, process final results
        if not posts:
            # Filter and sort results
            sorted_counts = sorted(
                [(word, count) for word, count in word_count.items() if count > 0],
                key=lambda x: (-x[1], x[0])
            )
            
            # Print results
            for word, count in sorted_counts:
                print(f"{word}: {count}")
            
            return word_count

        # Count keywords in titles
        for post in posts:
            title = post['data']['title'].lower()
            
            # Count words, ensuring whole word matches
            for word in word_list:
                # Use regex to match whole words only
                matches = re.findall(r'\b{}\b'.format(re.escape(word)), title)
                word_count[word] += len(matches)

        # Get next page token
        after = results['data']['after']

        # Recursive call to next page
        return count_words(subreddit, word_list, after, word_count)

    except Exception:
        return None
