from app import app

def lambda_handler(event, context):
    # Lambda handler function
    return app(event, context)
