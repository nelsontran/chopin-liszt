#!/usr/bin/env python3

if __name__ == "__main__":
    from app import app
    app.secret_key = 'DEVELOPMENT'
    app.run(debug=True)
