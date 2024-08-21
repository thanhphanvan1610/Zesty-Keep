import gpsoauth

# Your credentials
email = 'thanhphanvan1610@gmail.com'
token = 'oauth2_4/0AQlEd8yK7pMfFwE476j_fPWdT5XYtzQDEtW-UBTH9vtikJKsUIXgyrinyGOBDfZu1pBpvw'
android_id = '3e6a5f43bd80ea6'  # Your Android ID

# Exchange the OAuth token for a master token
try:
    master_response = gpsoauth.exchange_token(email, token, android_id)
    if 'Token' in master_response:
        master_token = master_response['Token']
        print('Master Token:', master_token)
    else:
        print('Failed to obtain master token:', master_response)
        exit(1)
except Exception as e:
    print('Error during token exchange:', str(e))
    exit(1)