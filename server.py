from src.app import create_app

# Create an application instance using the factory function
app = create_app()

if __name__ == '__main__':
    # Run the application
    app.run(debug=True)
