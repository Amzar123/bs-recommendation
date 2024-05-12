import sqlite3

class User:
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

    def save(self):
        # Implement the logic to save the user object to the database
        # For example, you can use an ORM like SQLAlchemy or execute SQL queries directly
        # Here's a simple example using SQLite3:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (id, username, email) VALUES (?, ?, ?)",
                       (self.id, self.username, self.email))
        conn.commit()
        conn.close()

    def delete(self):
        # Implement the logic to delete the user object from the database
        # For example, you can use an ORM like SQLAlchemy or execute SQL queries directly
        # Here's a simple example using SQLite3:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=?", (self.id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_id(id):
        # Implement the logic to retrieve a user object by its ID from the database
        # For example, you can use an ORM like SQLAlchemy or execute SQL queries directly
        # Here's a simple example using SQLite3:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id=?", (id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return User(result[0], result[1], result[2])
        else:
            return None

    @staticmethod
    def get_by_username(username):
        # Implement the logic to retrieve a user object by its username from the database
        # For example, you can use an ORM like SQLAlchemy or execute SQL queries directly
        # Here's a simple example using SQLite3:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return User(result[0], result[1], result[2])
        else:
            return None

    @staticmethod
    def get_by_email(email):
        # Implement the logic to retrieve a user object by its email from the database
        # For example, you can use an ORM like SQLAlchemy or execute SQL queries directly
        # Here's a simple example using SQLite3:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return User(result[0], result[1], result[2])
        else:
            return None