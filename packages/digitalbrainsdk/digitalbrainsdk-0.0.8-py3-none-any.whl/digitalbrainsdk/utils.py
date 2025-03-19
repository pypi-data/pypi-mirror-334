def validate_data(data):
    # Implement validation logic for the input data
    if not isinstance(data, (list, dict)):
        raise ValueError("Data must be a list or a dictionary.")
    return True

def format_output(output):
    # Implement formatting logic for the output
    if isinstance(output, dict):
        return "\n".join(f"{key}: {value}" for key, value in output.items())
    return str(output)