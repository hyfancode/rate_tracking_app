# Rate Tracking Service

Stock markets and bond markets typically move in opposite directions. In early 2021, as the 10-Year Treasury Yield rose on expectations of an economic recovery accompanied by climbing inflation, the stock markets fell sharply. Therefore, tracking the essential indexes and rates is more important than ever.

This web application is built to collect rates from public websites and update the data periodically. Users can easily find the rates they need and save time on searching different sites. Feel free to register an account to view all the rates. It is 100% free!

You can access the website through the URL: https://ratetracking.app

First you need to register an account, and then you will be able to click the navigation bar to review all the rates.

## Tools

Technology stack: MongoDB, Python, HTML, CSS, Javascript, and Bootstrap 4.

The web application is mainly built with Flask, a Python-based microframework. The python packages used in the development include:

- Flask 
- Jinja2 
- pymongo 
- beautifulsoup4 
- requests 
- passlib 
- uWSGI 
- python-dotenv 
- urllib3 
- pytz
- plotly

Server: The web application is deployed with uWSGI and nginx on Ubuntu 18.04 (LTS) x64.








