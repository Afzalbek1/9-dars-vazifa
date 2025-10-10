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
        cursor.execute("""
            INSERT OR IGNORE INTO users(chat_id, name, phone, username)
            VALUES (?, ?, ?, ?)
        """, (chat_id, fullname, phone, username))
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
