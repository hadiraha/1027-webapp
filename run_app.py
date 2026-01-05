import sys
import os
import traceback
import webbrowser

print("=== APP STARTING ===")
print("Python executable:", sys.executable)
print("Working dir:", os.getcwd())

try:
    import uvicorn
    print("Uvicorn imported OK")
except Exception as e:
    print("FAILED importing uvicorn")
    traceback.print_exc()
    input("Press Enter to exit...")
    sys.exit(1)

try:
    webbrowser.open("http://127.0.0.1:8000")
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        log_level="debug"
    )
except Exception as e:
    print("FAILED starting server")
    traceback.print_exc()
    input("Press Enter to exit...")