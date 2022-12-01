# -*- encoding: utf-8 -*-

from App import app
import os

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))

