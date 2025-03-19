class ApiModule:
    def __init__(self):
        self.name = "API Module"

    def get_data(self):
        return {"message": "Hello from the API!"}

    def post_data(self, data):
        return {"received": data}