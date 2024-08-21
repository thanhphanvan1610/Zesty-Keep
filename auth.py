import gkeepapi
def authenticate(Email, Master_Token):
    keep = gkeepapi.Keep()
    try:
        keep.authenticate(Email, Master_Token)
        print("Authentication successful")
        return keep
    except Exception as e:
        print(f"Error during authentication: {e}")
        return None