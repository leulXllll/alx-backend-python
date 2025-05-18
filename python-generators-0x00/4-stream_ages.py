seed = __import__('seed')

def stream_user_ages():
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    for (age,) in cursor:
        yield age
    cursor.close()
    connection.close()

def calculate_average_age():
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1
    if count > 0:
        average = total / count
        print(f"Average age of users: {average:.2f}")
    else:
        print("No user data available.")

# Run the function
if __name__ == "__main__":
    calculate_average_age()
