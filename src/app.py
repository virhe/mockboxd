from website import create_db, create_flask_app

# Create DB and start flask app when running the file
if __name__ == "__main__":
    create_db()
    app = create_flask_app()
    app.run(debug=True)
