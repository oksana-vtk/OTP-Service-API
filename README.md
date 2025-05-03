
# OTP Service API (One-Time Password)

This project implements a RESTful service for generating and validating One-Time Passwords (OTP) based on the user's phone number. 
It is built with Python (Flask) and uses a SQL-based database to store OTP codes.
This OTP Service API was used for implementation in client's application.

## Features

- Generate a unique 4-digit OTP code per user
- Limit OTP generation (no more than 10 codes per user within 2 hours)
- Ensure code uniqueness per user
- Validate only the most recent and unused code
- Prevent code reuse
- Log every request to a log file

## Technologies

- Python 3.8+
- Flask
- SQLite or any other SQL-based database
- REST API