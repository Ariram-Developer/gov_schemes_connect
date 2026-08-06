from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Ensure uploads directory exists
    os.makedirs(os.path.join(app.root_path, 'static', 'uploads'), exist_ok=True)
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)