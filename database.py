import sqlite3
import time
import threading
from contextlib import contextmanager
from datetime import datetime

DB_NAME = 'bot_database.db'
_local = threading.local()

def get_connection():
    """Получить thread-safe соединение с базой"""
    if not hasattr(_local, 'conn'):
        _local.conn = sqlite3.connect(DB_NAME, timeout=30.0, check_same_thread=False)
        _local.conn.row_factory = sqlite3.Row
        _local.conn.execute('PRAGMA journal_mode=WAL')
        _local.conn.execute('PRAGMA synchronous=NORMAL')
    return _local.conn

@contextmanager
def get_db():
    """Context manager для безопасной работы с БД"""
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e

def safe_execute(cursor, query, params=(), retries=5):
    """Выполнить запрос с retry при locked"""
    for i in range(retries):
        try:
            cursor.execute(query, params)
            return cursor
        except sqlite3.OperationalError as e:
            if 'locked' in str(e) and i < retries - 1:
                time.sleep(0.1 * (i + 1))
            else:
                raise

def init_db():
    """Инициализация всех таблиц"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Пользователи
        safe_execute(cursor, '''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                balance INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                exp INTEGER DEFAULT 0,
                registration_date TEXT,
                last_activity TEXT,
                referrer_id INTEGER,
                banned INTEGER DEFAULT 0,
                ban_reason TEXT,
                language TEXT DEFAULT 'ru'
            )
        ''')
        
        # Инвентарь
        safe_execute(cursor, '''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                item_id TEXT,
                quantity INTEGER DEFAULT 1,
                purchase_date TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Магазин
        safe_execute(cursor, '''
            CREATE TABLE IF NOT EXISTS shop_items (
                item_id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                price INTEGER,
                photo_url TEXT,
                category TEXT,
                available INTEGER DEFAULT 1
            )
        ''')
        
        # Кастомные кнопки
        safe_execute(cursor, '''
            CREATE TABLE IF NOT EXISTS custom_buttons (
                button_id TEXT PRIMARY KEY,
                title TEXT,
                text TEXT,
                photo_url TEXT,
                parent_menu TEXT,
                position INTEGER DEFAULT 0,
                active INTEGER DEFAULT 1
            )
        ''')
        
        # Транзакции
        safe_execute(cursor, '''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount INTEGER,
                type TEXT,
                description TEXT,
                date TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Достижения
        safe_execute(cursor, '''
            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                achievement_id TEXT,
                unlock_date TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Ежедневные награды
        safe_execute(cursor, '''
            CREATE TABLE IF NOT EXISTS daily_rewards (
                user_id INTEGER PRIMARY KEY,
                last_claim TEXT,
                streak INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Работы
        safe_execute(cursor, '''
            CREATE TABLE IF NOT EXISTS work_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                work_type TEXT,
                earned INTEGER,
                work_date TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        conn.commit()

# === USERS ===

def create_user(user_id, username=None, first_name=None):
    """Создать нового пользователя"""
    with get_db() as conn:
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        safe_execute(cursor, '''
            INSERT OR IGNORE INTO users (user_id, username, first_name, registration_date, last_activity)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, first_name, now, now))

def get_user(user_id):
    """Получить данные пользователя"""
    with get_db() as conn:
        cursor = conn.cursor()
        safe_execute(cursor, 'SELECT * FROM users WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def update_user_activity(user_id):
    """Обновить время последней активности"""
    with get_db() as conn:
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        safe_execute(cursor, 'UPDATE users SET last_activity = ? WHERE user_id = ?', (now, user_id))

def update_balance(user_id, amount):
    """Изменить баланс пользователя"""
    with get_db() as conn:
        cursor = conn.cursor()
        safe_execute(cursor, 'UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, user_id))
        
        # Логируем транзакцию
        now = datetime.now().isoformat()
        desc = "Пополнение" if amount > 0 else "Списание"
        safe_execute(cursor, '''
            INSERT INTO transactions (user_id, amount, type, description, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, amount, 'balance_change', desc, now))

def ban_user(user_id, reason="Нарушение правил"):
    """Забанить пользователя"""
    with get_db() as conn:
        cursor = conn.cursor()
        safe_execute(cursor, 'UPDATE users SET banned = 1, ban_reason = ? WHERE user_id = ?', (reason, user_id))

def unban_user(user_id):
    """Разбанить пользователя"""
    with get_db() as conn:
        cursor = conn.cursor()
        safe_execute(cursor, 'UPDATE users SET banned = 0, ban_reason = NULL WHERE user_id = ?', (user_id,))

def check_banned(user_id):
    """Проверить забанен ли пользователь"""
    user = get_user(user_id)
    if user:
        return {'banned': bool(user['banned']), 'reason': user['ban_reason']}
    return {'banned': False, 'reason': None}

def get_all_users():
    """Получить всех пользователей"""
    with get_db() as conn:
        cursor = conn.cursor()
        safe_execute(cursor, 'SELECT * FROM users ORDER BY registration_date DESC')
        return [dict(row) for row in cursor.fetchall()]

def get_top_users(limit=10):
    """Получить топ пользователей по балансу"""
    with get_db() as conn:
        cursor = conn.cursor()
        safe_execute(cursor, 'SELECT * FROM users ORDER BY balance DESC LIMIT ?', (limit,))
        return [dict(row) for row in cursor.fetchall()]

# === INVENTORY ===

def add_item_to_inventory(user_id, item_id, quantity=1):
    """Добавить предмет в инвентарь"""
    with get_db() as conn:
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        
        # Проверяем есть ли уже такой предмет
        safe_execute(cursor, 'SELECT * FROM inventory WHERE user_id = ? AND item_id = ?', (user_id, item_id))
        existing = cursor.fetchone()
        
        if existing:
            safe_execute(cursor, '''
                UPDATE inventory SET quantity = quantity + ? WHERE user_id = ? AND item_id = ?
            ''', (quantity, user_id, item_id))
        else:
            safe_execute(cursor, '''
                INSERT INTO inventory (user_id, item_id, quantity, purchase_date)
                VALUES (?, ?, ?, ?)
            ''', (user_id, item_id, quantity, now))

def get_user_inventory(user_id):
    """Получить инвентарь пользователя"""
    with get_db() as conn:
        cursor = conn.cursor()
        safe_execute(cursor, '''
            SELECT i.*, s.name, s.description, s.photo_url
            FROM inventory i
            LEFT JOIN shop_items s ON i.item_id = s.item_id
            WHERE i.user_id = ?
        ''', (user_id,))
        return [dict(row) for row in cursor.fetchall()]

def remove_item_from_inventory(user_id, item_id, quantity=1):
    """Удалить предмет из инвентаря"""
    with get_db() as conn:
        cursor = conn.cursor()
        safe_execute(cursor, 'SELECT quantity FROM inventory WHERE user_id = ? AND item_id = ?', (user_id, item_id))
        row = cursor.fetchone()
        
        if row:
            current = row[0]
            if current <= quantity:
                safe_execute(cursor, 'DELETE FROM inventory WHERE user_id = ? AND item_id = ?', (user_id, item_id))
            else:
                safe_execute(cursor, '''
                    UPDATE inventory SET quantity = quantity - ? WHERE user_id = ? AND item_id = ?
                ''', (quantity, user_id, item_id))

# === SHOP ===

def add_shop_item(item_id, name, price, description="", photo_url="", category="general"):
    """Добавить товар в магазин"""
    with get_db() as conn:
        cursor = conn.cursor()
        safe_execute(cursor, '''
            INSERT OR REPLACE INTO shop_items (item_id, name, description, price, photo_url, category, available)
            VALUES (?, ?, ?, ?, ?, ?, 1)
        ''', (item_id, name, description, price, photo_url, category))

def get_shop_items(category=None):
    """Получить товары магазина"""
    with get_db() as conn:
        cursor = conn.cursor()
        if category:
            safe_execute(cursor, 'SELECT * FROM shop_items WHERE category = ? AND available = 1', (category,))
        else:
            safe_execute(cursor, 'SELECT * FROM shop_items WHERE available = 1')
        return [dict(row) for row in cursor.fetchall()]

def get_shop_item(item_id):
    """Получить товар по ID"""
    with get_db() as conn:
        cursor = conn.cursor()
        safe_execute(cursor, 'SELECT * FROM shop_items WHERE item_id = ?', (item_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

# === CUSTOM BUTTONS ===

def add_custom_button(button_id, title, text, photo_url="", parent_menu="main", position=0):
    """Создать кастомную кнопку"""
    with get_db() as conn:
        cursor = conn.cursor()
        safe_execute(cursor, '''
            INSERT OR REPLACE INTO custom_buttons (button_id, title, text, photo_url, parent_menu, position, active)
            VALUES (?, ?, ?, ?, ?, ?, 1)
        ''', (button_id, title, text, photo_url, parent_menu, position))

def get_custom_buttons(parent_menu="main"):
    """Получить кнопки для меню"""
    with get_db() as conn:
        cursor = conn.cursor()
        safe_execute(cursor, '''
            SELECT * FROM custom_buttons WHERE parent_menu = ? AND active = 1 ORDER BY position
        ''', (parent_menu,))
        return [dict(row) for row in cursor.fetchall()]

def delete_custom_button(button_id):
    """Удалить кнопку"""
    with get_db() as conn:
        cursor = conn.cursor()
        safe_execute(cursor, 'DELETE FROM custom_buttons WHERE button_id = ?', (button_id,))

# === DAILY REWARDS ===

def claim_daily_reward(user_id):
    """Получить ежедневную награду"""
    with get_db() as conn:
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        today = datetime.now().date().isoformat()
        
        safe_execute(cursor, 'SELECT * FROM daily_rewards WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        
        if row:
            last_claim = row['last_claim']
            streak = row['streak']
            
            if last_claim and last_claim.startswith(today):
                return {'success': False, 'reason': 'already_claimed'}
            
            # Проверяем streak
            from datetime import timedelta
            yesterday = (datetime.now() - timedelta(days=1)).date().isoformat()
            if last_claim and last_claim.startswith(yesterday):
                streak += 1
            else:
                streak = 1
            
            safe_execute(cursor, '''
                UPDATE daily_rewards SET last_claim = ?, streak = ? WHERE user_id = ?
            ''', (now, streak, user_id))
        else:
            streak = 1
            safe_execute(cursor, '''
                INSERT INTO daily_rewards (user_id, last_claim, streak) VALUES (?, ?, ?)
            ''', (user_id, now, streak))
        
        # Награда зависит от streak
        reward = min(100 + (streak - 1) * 10, 500)
        update_balance(user_id, reward)
        
        return {'success': True, 'reward': reward, 'streak': streak}

# === STATS ===

def get_stats():
    """Получить общую статистику"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        safe_execute(cursor, 'SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()[0]
        
        safe_execute(cursor, 'SELECT COUNT(*) FROM users WHERE banned = 1')
        banned_users = cursor.fetchone()[0]
        
        safe_execute(cursor, 'SELECT SUM(balance) FROM users')
        total_balance = cursor.fetchone()[0] or 0
        
        safe_execute(cursor, 'SELECT COUNT(*) FROM transactions')
        total_transactions = cursor.fetchone()[0]
        
        return {
            'total_users': total_users,
            'banned_users': banned_users,
            'total_balance': total_balance,
            'total_transactions': total_transactions
        }

def set_user_language(user_id, language):
    """Установить язык пользователя"""
    with get_db() as conn:
        cursor = conn.cursor()
        safe_execute(cursor, 'UPDATE users SET language = ? WHERE user_id = ?', (language, user_id))

# Инициализация при импорте
init_db()
