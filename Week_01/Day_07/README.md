# Day 07 - MyLife Dashboard

## What I Built
Personal finance + bookshelf tracker built with Streamlit and SQLite.

## Features
- Multi-account expense tracking (SBI + Rajkot Bank)
- Monthly budget with progress bar
- Bookshelf via Open Library API
- Web scraping with BeautifulSoup

## What I Learned
- Single Responsibility Principle (split save/get functions)
- SQLite commit() is mandatory or data doesn't persist
- Streamlit reruns entire page on every interaction

## Tech Used
Python, Streamlit, SQLite, BeautifulSoup, Open Library API

## Run
pip install streamlit
streamlit run app.py
