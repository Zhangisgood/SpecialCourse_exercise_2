import sqlite3

stephen_king_adaptations_list = []
with open('stephen_king_adaptations.txt', 'r') as file:
    for line in file:
        movie_info = line.strip().split(',')
        stephen_king_adaptations_list.append(movie_info)

conn = sqlite3.connect('stephen_king_adaptations.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table (
                  movieID TEXT PRIMARY KEY,
                  movieName TEXT,
                  movieYear INTEGER,
                  imdbRating REAL
                )''')

insert_query = "INSERT INTO stephen_king_adaptations_table (movieID, movieName, movieYear, imdbRating) VALUES (?, ?, ?, ?)"
cursor.executemany(insert_query, stephen_king_adaptations_list)
conn.commit()

while True:
    print("\nPlease choose one choice:")
    print("1. Search by movie name")
    print("2. Search by movie year")
    print("3. Search by movie rating")
    print("4. Stop")
    option = input("Please input a number: ")

    if option == '1':
        movie_name = input("Please input movie name: ")
        cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieName = ?", (movie_name,))
        result = cursor.fetchone()
        if result:
            print("Movie details：")
            print(f"Movie name: {result[1]}")
            print(f"Movie year: {result[2]}")
            print(f"IMDB Rating: {result[3]}")
        else:
            print("No such movie exists in our database.")

    elif option == '2':
        movie_year = int(input("Please input movie year: "))
        cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieYear = ?", (movie_year,))
        results = cursor.fetchall()
        if results:
            print(f"Movie lists of {movie_year} ：")
            for result in results:
                print(f"Movie name: {result[1]}, IMDB Rating: {result[3]}")
        else:
            print("No movies were found for that year in our database.")

    elif option == '3':
        rating_limit = float(input("Please input a minimum movie rating: "))
        cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE imdbRating >= ?", (rating_limit,))
        results = cursor.fetchall()
        if results:
            print(f"Movie lists whose IMDB rating is greater than or equal to {rating_limit}：")
            for result in results:
                print(f"Movie name: {result[1]}, IMDB Rating: {result[3]}")
        else:
            print(f"No movies at or above {rating_limit} were found in the database.")

    elif option == '4':
        break

conn.close()
