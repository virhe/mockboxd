from website import create_db, create_flask_app

if __name__ == "__main__":
    app = create_flask_app()
    app.run(debug=True)
