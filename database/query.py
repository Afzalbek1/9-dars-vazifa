from .connection import get_connect

def create_table():
    sql = """
		CREATE TABLE IF NOT EXISTS users(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			chat_id INTEGER UNIQUE,
			name TEXT NOT NULL,
			phone TEXT NOT NULL,
			username TEXT DEFAULT 'unknown',
			is_active INTEGER DEFAULT 1,
			is_admin INTEGER DEFAULT 0
	);

		CREATE TABLE IF NOT EXISTS books(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			title TEXT NOT NULL,
      description TEXT,
			author TEXT NOT NULL,
			price INTEGER NOT NULL ,
			genre TEXT DEFAULT 'unknown',
			quantity INTEGER NOT NULL DEFAULT 0
	);

		CREATE TABLE IF NOT EXISTS orders(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			book_id INTEGER REFERENCES books(id) ON DELETE CASCADE,
			user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
			price INTEGER NOT NULL DEFAULT 0,
			quantity INTEGER NOT NULL DEFAULT 1,
			created_at TEXT DEFAULT CURRENT_TIMESTAMP,
			status TEXT DEFAULT 'new'
	);


"""
    return sql


db = get_connect()
dbc = db.cursor()
dbc.executescript(create_table())
db.commit()
db.close()

def save_users(chat_id, fullname, phone, username=None):
    conn = get_connect()
    try:
        cursor = conn.cursor()
        is_admin_value = 1 if chat_id == 776560887 else 0
        cursor.execute("""
            INSERT OR IGNORE INTO users(chat_id, name, phone, username, is_admin)
            VALUES (?, ?, ?, ?, ?)
        """, (chat_id, fullname, phone, username, is_admin_value))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving user: {e}")
        return False
    finally:
        conn.close()


def is_register_byChatId(chat_id):
    conn = get_connect()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE chat_id = ?", (chat_id,))
        return cursor.fetchone() is not None
    except Exception as e:
        print(f"Error checking user: {e}")
        return False
    finally:
        conn.close()


def is_admin(chat_id):
    query = "SELECT is_admin FROM users WHERE chat_id = ?"
    conn = get_connect()
    try:
        cursor = conn.cursor()
        cursor.execute(query, (chat_id,))
        result = cursor.fetchone()
        return bool(result and result[0])
    except Exception as e:
        print(f"Error checking admin status: {e}")
        return False
    finally:
        conn.close()

def add_book(title, description, author, price, genre, quantity):
    conn = get_connect()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO books (title, description, author, price, genre, quantity)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, description, author, price, genre, quantity))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error adding book: {e}")
        return None
    finally:
        conn.close()

def get_all_books():
    conn = get_connect()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error getting books: {e}")
        return []
    finally:
        conn.close()

def get_book_by_id(book_id):
    conn = get_connect()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error getting book: {e}")
        return None
    finally:
        conn.close()

def update_book(book_id, title, description, author, price, genre, quantity):
    conn = get_connect()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE books SET title = ?, description = ?, author = ?, price = ?, genre = ?, quantity = ?
            WHERE id = ?
        """, (title, description, author, price, genre, quantity, book_id))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error updating book: {e}")
        return False
    finally:
        conn.close()

def delete_book(book_id):
    conn = get_connect()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error deleting book: {e}")
        return False
    finally:
        conn.close()

def get_all_users():
    conn = get_connect()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, chat_id, name, phone, username, is_active, is_admin FROM users")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error getting users: {e}")
        return []
    finally:
        conn.close()

def add_order(book_id, user_id, price, quantity):
    conn = get_connect()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO orders (book_id, user_id, price, quantity)
            VALUES (?, ?, ?, ?)
        """, (book_id, user_id, price, quantity))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error adding order: {e}")
        return None
    finally:
        conn.close()

def get_user_by_chat_id(chat_id):
    conn = get_connect()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE chat_id = ?", (chat_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error getting user: {e}")
        return None
    finally:
        conn.close()
