#!/usr/bin/python3
"""
Module to query Reddit API and retrieve top 10 hot posts for a given subreddit.
This module provides a function to fetch and print titles of hot posts.
"""

import requests
import sys


def top_ten(subreddit):
    """
    Queries the Reddit API and prints the titles of the first 10 hot posts
    for a given subreddit.

    Args:
        subreddit (str): The name of the subreddit to query
    """
    # Reddit API endpoint for hot posts
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"

    # Custom headers to mimic a browser request and avoid potential blocking
    headers = {
        'User-Agent': 'python:subreddit.top.ten:v1.0'
    }

    try:
        # Send GET request to Reddit API
        response = requests.get(url, headers=headers, allow_redirects=False)

        # Check if the request was successful
        if response.status_code != 200:
            print(None)
            return

        # Parse the JSON response
        data = response.json()

        # Check if the 'data' and 'children' keys exist
        if 'data' not in data or 'children' not in data['data']:
            print(None)
            return

        # Get the list of posts
        posts = data['data']['children']

        # Print titles of the first 10 posts
        for post in posts:
            print(post['data']['title'])

    except Exception:
        # Handle any errors
        print(None)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please pass an argument (subreddit name)')
    else:
        top_ten(sys.argv[1])
