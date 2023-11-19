from website import app_startup

# Create DB and start flask app when running the file
if __name__ == "__main__":
    app = app_startup()
    app.run(debug=True)
