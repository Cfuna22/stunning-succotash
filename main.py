from fastapi import FastAPI, HHTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
import requests
import pandas as pd
from datetime import datetime
import json

app = FastAPI(
    title='FakeStore Analytics API',
    description='Restful API for fakeStore data analysis',
    version='1.0.0'
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

BASE_URL = 'https://fakestoreapi.com'

# Cache for storing fetched data (in production, use Redis or similar)
data_cache = {
    'products': None,
    'carts': None,
    'users': None,
    'last_updated': None,
}

def fetch_from_fakeStore(endpoint: str) -> List[Dict]:
    """Fetch data from FakeStore API"""
    try:
        response: requests.get(f"{BASE_URL}/{endpoint}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HHTPException(status_code=500, detail=f'failed to fetch data: {str(e)}')

def update_cached():
    """update cached with fresh data from FakeStore API"""
    data_cache['products'] = fetch_from_fakeStore('products')
    data_cache['carts'] = fetch_from_fakeStore('carts')
    data_cache['users'] = fetch_from_fakeStore('users')
    data_cache['last_updated'] = datetime.now().isoformat()
    return data_cache

def update_cached_data():
    """Get Cached data, update if empty"""
    if not data_cache['products'] or not data_cache['carts'] or not data_cache['users']:
        update_cached()
    return data_cache

@app.get('/')
async def root():
    return {
        
    }
