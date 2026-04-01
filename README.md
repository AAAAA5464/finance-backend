# Finance Backend System

## Overview
This is a Python-based finance tracking backend built using FastAPI. It allows users to manage financial transactions and view analytics.

## Features
- CRUD operations (Create, Read, Update, Delete)
- Filtering by type, category, and date
- Financial analytics:
  - Total income
  - Total expenses
  - Balance
  - Category-wise breakdown
  - Monthly summary
  - Recent transactions
- Role-based access control:
  - Viewer: read only
  - Analyst: filter + analytics
  - Admin: full access

## Tech Stack
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic

## Project Structure
- main.py → API routes
- services.py → business logic
- models.py → database models
- schemas.py → validation

## How to Run
pip install fastapi uvicorn sqlalchemy pydantic  
python -m uvicorn main:app --reload  

## API Docs
http://127.0.0.1:8000/docs

## Design Decisions
- Used FastAPI for performance and auto documentation
- Used modular structure for clean code
- Implemented role-based access for security