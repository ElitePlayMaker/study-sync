"""Legacy entry point — delegates to Study Sync app factory."""

from run import app

if __name__ == "__main__":
    app.run(debug=True)
