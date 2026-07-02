"""Application entry point for Study Sync."""

from study_sync import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
