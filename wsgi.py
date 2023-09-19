"""App entry point."""
from games import create_app

app = create_app({'WTF_CSRF_ENABLED': False}) #remove csrf parameter, temporary

if __name__ == "__main__":
    app.run(host='localhost', port=5000, threaded=False)
