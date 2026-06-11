# -*- coding: utf-8 -*-
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
import database as db
from languages import get_text

# Конфигурация
API_TOKEN = 'YOUR_BOT_TOKEN_HERE'
ADMIN_IDS = [123456789]  # Замените на ваш Telegram ID

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# FSM состояния
class AdminStates(StatesGroup):
    waiting_broadcast = State()
    waiting_shop_name = State()
    waiting_shop_price = State()
    waiting_shop_desc = State()
    waiting_shop_photo = State()
    waiting_button_title = State()
    waiting_button_text = State()
    waiting_button_photo = State()
    waiting_ban_id = State()
    waiting_ban_reason = State()

class UserStates(StatesGroup):
    choosing_language = State()

# === КЛАВИАТУРЫ ===

def get_user_language(user_id):
    """Получить язык пользователя"""
    user = db.get_user(user_id)
    if user and user.get('language'):
        return user['language']
    return 'ru'

def main_keyboard(user_id):
    """Главная клавиатура с кастомными кнопками"""
    lang = get_user_language(user_id)
    
    kb = [
        [KeyboardButton(text=get_text(lang, 'profile')), KeyboardButton(text=get_text(lang, 'shop'))],
        [KeyboardButton(text=get_text(lang, 'inventory')), KeyboardButton(text=get_text(lang, 'work'))],
        [KeyboardButton(text=get_text(lang, 'daily_reward')), KeyboardButton(text=get_text(lang, 'rating'))],
        [KeyboardButton(text=get_text(lang, 'settings'))],
    ]
    
    # Добавляем кастомные кнопки
    custom = db.get_custom_buttons("main")
    for btn in custom:
        kb.append([KeyboardButton(text=btn['title'])])
    
    if user_id in ADMIN_IDS:
        kb.append([KeyboardButton(text=get_text(lang, 'admin_panel'))])
    
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def admin_keyboard(lang='ru'):
    """Админская клавиатура"""
    kb = [
        [KeyboardButton(text=get_text(lang, 'stats')), KeyboardButton(text=get_text(lang, 'broadcast'))],
        [KeyboardButton(text=get_text(lang, 'manage_shop')), KeyboardButton(text=get_text(lang, 'create_button'))],
        [KeyboardButton(text=get_text(lang, 'manage_users')), KeyboardButton(text=get_text(lang, 'logs'))],
        [KeyboardButton(text=get_text(lang, 'back'))]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def language_keyboard():
    """Клавиатура выбора языка"""
    kb = [
        [KeyboardButton(text="🇷🇺 Русский")],
        [KeyboardButton(text="🇬🇧 English")],
        [KeyboardButton(text="🇺🇦 Українська")],
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

# === MIDDLEWARE для проверки бана ===

@dp.message.middleware()
async def ban_check_middleware(handler, event: types.Message, data: dict):
    user_id = event.from_user.id
    ban_info = db.check_banned(user_id)
    
    if ban_info['banned']:
        lang = get_user_language(user_id)
        reason = ban_info['reason'] or get_text(lang, 'no_access')
        await event.answer(get_text(lang, 'banned_message', reason=reason))
        return
    
    return await handler(event, data)

# === ХЭНДЛЕРЫ ===

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    
    # Проверяем есть ли пользователь
    user = db.get_user(user_id)
    
    if not user:
        # Новый пользователь - выбор языка
        await message.answer(
            "🌐 Welcome! Вітаємо! Добро пожаловать!\n\n"
            "Please choose your language:\n"
            "Оберіть мову:\n"
            "Выберите язык:",
            reply_markup=language_keyboard()
        )
        await state.set_state(UserStates.choosing_language)
        await state.update_data(username=username, first_name=first_name)
    else:
        # Существующий пользователь
        db.update_user_activity(user_id)
        lang = get_user_language(user_id)
        
        await message.answer(
            get_text(lang, 'welcome', name=first_name),
            reply_markup=main_keyboard(user_id)
        )

@dp.message(UserStates.choosing_language)
async def process_language_choice(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    
    # Определяем язык
    text = message.text.lower()
    if 'english' in text or '🇬🇧' in text:
        lang = 'en'
    elif 'українська' in text or '🇺🇦' in text:
        lang = 'uk'
    else:
        lang = 'ru'
    
    # Создаем пользователя
    db.create_user(user_id, data.get('username'), data.get('first_name'))
    db.set_user_language(user_id, lang)
    db.update_user_activity(user_id)
    
    await message.answer(
        get_text(lang, 'welcome', name=data.get('first_name')),
        reply_markup=main_keyboard(user_id)
    )
    await state.clear()

@dp.message(F.text.in_(['💰 Профиль', '💰 Profile', '💰 Профіль']))
async def show_profile(message: types.Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    user = db.get_user(user_id)
    
    if not user:
        await message.answer(get_text(lang, 'profile_not_found'))
        return
    
    # Получаем streak для ежедневных наград
    with db.get_db() as conn:
        cursor = conn.cursor()
        db.safe_execute(cursor, 'SELECT streak FROM daily_rewards WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        streak = row[0] if row else 0
    
    inventory_count = len(db.get_user_inventory(user_id))
    
    await message.answer(
        get_text(lang, 'profile_text',
            name=user['first_name'],
            user_id=user['user_id'],
            balance=user['balance'],
            level=user['level'],
            exp=user['exp'],
            items=inventory_count,
            streak=streak,
            reg_date=user['registration_date'][:10]
        )
    )

@dp.message(F.text.in_(['🏪 Магазин', '🏪 Shop', '🏪 Магазин']))
async def show_shop(message: types.Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    items = db.get_shop_items()
    
    if not items:
        await message.answer(get_text(lang, 'shop_empty'))
        return
    
    text = get_text(lang, 'shop_welcome')
    for i, item in enumerate(items, 1):
        text += f"{i}. {item['name']} - {item['price']}₽\n"
        if item['description']:
            text += f"   {item['description']}\n"
        text += "\n"
    
    text += get_text(lang, 'shop_buy_instruction')
    
    if items and items[0].get('photo_url'):
        await message.answer_photo(photo=items[0]['photo_url'], caption=text)
    else:
        await message.answer(text)

@dp.message(F.text.lower().regexp(r'^(купить|buy|купити)\s+\d+'))
async def process_buy(message: types.Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    
    try:
        parts = message.text.split()
        if len(parts) < 2:
            await message.answer(get_text(lang, 'buy_invalid_format'))
            return
        
        item_num = int(parts[1])
        items = db.get_shop_items()
        
        if item_num < 1 or item_num > len(items):
            await message.answer(get_text(lang, 'buy_not_found', num=item_num))
            return
        
        item = items[item_num - 1]
        user = db.get_user(user_id)
        
        if user['balance'] < item['price']:
            await message.answer(get_text(lang, 'buy_not_enough', price=item['price'], balance=user['balance']))
            return
        
        # Покупка
        db.update_balance(user_id, -item['price'])
        db.add_item_to_inventory(user_id, item['item_id'])
        
        await message.answer(
            get_text(lang, 'buy_success',
                name=item['name'],
                price=item['price'],
                balance=user['balance'] - item['price']
            )
        )
    except ValueError:
        await message.answer(get_text(lang, 'buy_invalid_format'))
    except Exception as e:
        await message.answer(get_text(lang, 'buy_error', error=str(e)))

@dp.message(F.text.in_(['🎒 Инвентарь', '🎒 Inventory', '🎒 Інвентар']))
async def show_inventory(message: types.Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    items = db.get_user_inventory(user_id)
    
    if not items:
        await message.answer(get_text(lang, 'inventory_empty'))
        return
    
    text = get_text(lang, 'inventory_text')
    for item in items:
        text += f"• {item['name']} x{item['quantity']}\n"
    
    await message.answer(text)

@dp.message(F.text.in_(['💼 Работа', '💼 Work', '💼 Робота']))
async def show_work(message: types.Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    
    await message.answer(get_text(lang, 'work_list'))

@dp.message(F.text.lower().regexp(r'^(работа|work|робота)\s+\d+'))
async def process_work(message: types.Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    
    try:
        parts = message.text.split()
        if len(parts) < 2:
            await message.answer(get_text(lang, 'work_invalid'))
            return
        
        work_num = int(parts[1])
        
        work_types = {
            1: ('programmer', '💻 Programmer' if lang == 'en' else '💻 Програміст' if lang == 'uk' else '💻 Программист', 50),
            2: ('taxi', '🚕 Taxi Driver' if lang == 'en' else '🚕 Таксист' if lang == 'uk' else '🚕 Таксист', 30),
            3: ('barista', '☕ Barista' if lang == 'en' else '☕ Бариста' if lang == 'uk' else '☕ Бариста', 20),
            4: ('courier', '📦 Courier' if lang == 'en' else '📦 Кур\'єр' if lang == 'uk' else '📦 Курьер', 25),
            5: ('designer', '🎨 Designer' if lang == 'en' else '🎨 Дизайнер' if lang == 'uk' else '🎨 Дизайнер', 40),
            6: ('teacher', '👨‍🏫 Teacher' if lang == 'en' else '👨‍🏫 Вчитель' if lang == 'uk' else '👨‍🏫 Учитель', 35),
        }
        
        if work_num not in work_types:
            await message.answer(get_text(lang, 'work_not_found'))
            return
        
        work_id, work_name, reward = work_types[work_num]
        
        # Проверяем последнюю работу
        with db.get_db() as conn:
            cursor = conn.cursor()
            db.safe_execute(cursor, '''
                SELECT work_date FROM work_history 
                WHERE user_id = ? 
                ORDER BY work_date DESC LIMIT 1
            ''', (user_id,))
            row = cursor.fetchone()
            
            if row:
                from datetime import datetime, timedelta
                last_work = datetime.fromisoformat(row[0])
                now = datetime.now()
                
                if (now - last_work).total_seconds() < 7200:
                    wait_time = 7200 - (now - last_work).total_seconds()
                    hours = int(wait_time // 3600)
                    minutes = int((wait_time % 3600) // 60)
                    await message.answer(get_text(lang, 'work_cooldown', hours=hours, minutes=minutes))
                    return
        
        db.update_balance(user_id, reward)
        
        # Записываем в историю
        from datetime import datetime
        now = datetime.now().isoformat()
        with db.get_db() as conn:
            cursor = conn.cursor()
            db.safe_execute(cursor, '''
                INSERT INTO work_history (user_id, work_type, earned, work_date)
                VALUES (?, ?, ?, ?)
            ''', (user_id, work_id, reward, now))
        
        await message.answer(get_text(lang, 'work_success', name=work_name, reward=reward))
    except ValueError:
        await message.answer(get_text(lang, 'work_invalid'))
    except Exception as e:
        await message.answer(get_text(lang, 'buy_error', error=str(e)))

@dp.message(F.text.in_(['🎁 Ежедневная награда', '🎁 Daily Reward', '🎁 Щоденна нагорода']))
async def daily_reward(message: types.Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    result = db.claim_daily_reward(user_id)
    
    if not result['success']:
        await message.answer(get_text(lang, 'daily_already'))
        return
    
    await message.answer(
        get_text(lang, 'daily_success', reward=result['reward'], streak=result['streak'])
    )

@dp.message(F.text.in_(['🏆 Рейтинг', '🏆 Rating', '🏆 Рейтинг']))
async def show_rating(message: types.Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    top = db.get_top_users(10)
    
    text = get_text(lang, 'rating_text')
    for i, user in enumerate(top, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        name = user['first_name'] or user['username'] or "Аноним"
        text += f"{medal} {name} - {user['balance']}₽\n"
    
    await message.answer(text)

@dp.message(F.text.in_(['⚙️ Настройки', '⚙️ Settings', '⚙️ Налаштування']))
async def show_settings(message: types.Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    
    await message.answer(
        get_text(lang, 'choose_language'),
        reply_markup=language_keyboard()
    )

@dp.message(F.text.in_(['🇷🇺 Русский', '🇬🇧 English', '🇺🇦 Українська']))
async def change_language(message: types.Message):
    user_id = message.from_user.id
    
    text = message.text.lower()
    if 'english' in text or '🇬🇧' in text:
        lang = 'en'
    elif 'українська' in text or '🇺🇦' in text:
        lang = 'uk'
    else:
        lang = 'ru'
    
    db.set_user_language(user_id, lang)
    
    await message.answer(
        get_text(lang, 'language_changed'),
        reply_markup=main_keyboard(user_id)
    )

# === ОБРАБОТКА КАСТОМНЫХ КНОПОК ===

@dp.message(F.text)
async def handle_custom_buttons(message: types.Message):
    button_title = message.text
    
    # Ищем кнопку в базе
    with db.get_db() as conn:
        cursor = conn.cursor()
        db.safe_execute(cursor, '''
            SELECT * FROM custom_buttons WHERE title = ? AND active = 1
        ''', (button_title,))
        row = cursor.fetchone()
        
        if row:
            button = dict(row)
            
            # Отправляем ответ
            if button['photo_url']:
                await message.answer_photo(
                    photo=button['photo_url'],
                    caption=button['text']
                )
            else:
                await message.answer(button['text'])

# === АДМИНКА ===

@dp.message(F.text.in_(['⚙️ Админ-панель', '⚙️ Admin Panel', '⚙️ Адмін-панель']))
async def admin_panel(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        lang = get_user_language(message.from_user.id)
        await message.answer(get_text(lang, 'no_access'))
        return
    
    lang = get_user_language(message.from_user.id)
    await message.answer(get_text(lang, 'admin_panel_text'), reply_markup=admin_keyboard(lang))

@dp.message(F.text.in_(['📊 Статистика', '📊 Statistics', '📊 Статистика']))
async def show_stats(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    
    lang = get_user_language(message.from_user.id)
    stats = db.get_stats()
    
    await message.answer(
        get_text(lang, 'stats_text',
            total=stats['total_users'],
            banned=stats['banned_users'],
            balance=stats['total_balance'],
            transactions=stats['total_transactions']
        )
    )

@dp.message(F.text.in_(['📢 Рассылка', '📢 Broadcast', '📢 Розсилка']))
async def start_broadcast(message: types.Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return
    
    lang = get_user_language(message.from_user.id)
    await message.answer(get_text(lang, 'broadcast_prompt'))
    await state.set_state(AdminStates.waiting_broadcast)

@dp.message(AdminStates.waiting_broadcast)
async def process_broadcast(message: types.Message, state: FSMContext):
    users = db.get_all_users()
    success = 0
    
    for user in users:
        try:
            await bot.send_message(user['user_id'], message.text)
            success += 1
            await asyncio.sleep(0.05)
        except:
            pass
    
    lang = get_user_language(message.from_user.id)
    await message.answer(get_text(lang, 'broadcast_done', success=success, total=len(users)))
    await state.clear()

@dp.message(F.text.in_(['🛠 Управление магазином', '🛠 Manage Shop', '🛠 Управління магазином']))
async def manage_shop(message: types.Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return
    
    lang = get_user_language(message.from_user.id)
    await message.answer(get_text(lang, 'shop_add_name'))
    await state.set_state(AdminStates.waiting_shop_name)

@dp.message(AdminStates.waiting_shop_name)
async def shop_get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    lang = get_user_language(message.from_user.id)
    await message.answer(get_text(lang, 'shop_add_price'))
    await state.set_state(AdminStates.waiting_shop_price)

@dp.message(AdminStates.waiting_shop_price)
async def shop_get_price(message: types.Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    if not message.text.isdigit():
        await message.answer(get_text(lang, 'shop_add_price'))
        return
    
    await state.update_data(price=int(message.text))
    await message.answer(get_text(lang, 'shop_add_desc'))
    await state.set_state(AdminStates.waiting_shop_desc)

@dp.message(AdminStates.waiting_shop_desc)
async def shop_get_desc(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    lang = get_user_language(message.from_user.id)
    await message.answer(get_text(lang, 'shop_add_photo'))
    await state.set_state(AdminStates.waiting_shop_photo)

@dp.message(AdminStates.waiting_shop_photo)
async def shop_get_photo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    
    photo_url = ""
    if message.photo:
        photo_url = message.photo[-1].file_id
    
    # Генерируем ID товара
    import random
    item_id = f"item_{random.randint(1000, 9999)}"
    
    db.add_shop_item(
        item_id=item_id,
        name=data['name'],
        price=data['price'],
        description=data['description'],
        photo_url=photo_url
    )
    
    lang = get_user_language(message.from_user.id)
    await message.answer(get_text(lang, 'shop_added', name=data['name']))
    await state.clear()

@dp.message(F.text.in_(['🎨 Создать кнопку', '🎨 Create Button', '🎨 Створити кнопку']))
async def create_button(message: types.Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return
    
    lang = get_user_language(message.from_user.id)
    await message.answer(get_text(lang, 'button_add_title'))
    await state.set_state(AdminStates.waiting_button_title)

@dp.message(AdminStates.waiting_button_title)
async def button_get_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    lang = get_user_language(message.from_user.id)
    await message.answer(get_text(lang, 'button_add_text'))
    await state.set_state(AdminStates.waiting_button_text)

@dp.message(AdminStates.waiting_button_text)
async def button_get_text(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    lang = get_user_language(message.from_user.id)
    await message.answer(get_text(lang, 'button_add_photo'))
    await state.set_state(AdminStates.waiting_button_photo)

@dp.message(AdminStates.waiting_button_photo)
async def button_get_photo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    
    photo_url = ""
    if message.photo:
        photo_url = message.photo[-1].file_id
    
    import random
    button_id = f"btn_{random.randint(1000, 9999)}"
    
    db.add_custom_button(
        button_id=button_id,
        title=data['title'],
        text=data['text'],
        photo_url=photo_url
    )
    
    lang = get_user_language(message.from_user.id)
    await message.answer(get_text(lang, 'button_created', title=data['title']))
    await state.clear()

@dp.message(F.text.in_(['👤 Управление пользователями', '👤 Manage Users', '👤 Управління користувачами']))
async def manage_users(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    
    lang = get_user_language(message.from_user.id)
    
    kb = [
        [KeyboardButton(text=get_text(lang, 'ban_user')), KeyboardButton(text=get_text(lang, 'unban_user'))],
        [KeyboardButton(text=get_text(lang, 'give_balance')), KeyboardButton(text=get_text(lang, 'users_list'))],
        [KeyboardButton(text=get_text(lang, 'back'))]
    ]
    
    await message.answer(get_text(lang, 'users_menu'), reply_markup=ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))

@dp.message(F.text.in_(['🚫 Забанить', '🚫 Ban', '🚫 Забанити']))
async def admin_ban(message: types.Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return
    lang = get_user_language(message.from_user.id)
    await message.answer(get_text(lang, 'ban_prompt_id'))
    await state.set_state(AdminStates.waiting_ban_id)

@dp.message(AdminStates.waiting_ban_id)
async def ban_get_id(message: types.Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    if not message.text.isdigit():
        await message.answer(get_text(lang, 'ban_prompt_id'))
        return
    
    await state.update_data(ban_user_id=int(message.text))
    await message.answer(get_text(lang, 'ban_prompt_reason'))
    await state.set_state(AdminStates.waiting_ban_reason)

@dp.message(AdminStates.waiting_ban_reason)
async def ban_get_reason(message: types.Message, state: FSMContext):
    data = await state.get_data()
    db.ban_user(data['ban_user_id'], message.text)
    
    lang = get_user_language(message.from_user.id)
    await message.answer(get_text(lang, 'ban_success', user_id=data['ban_user_id']))
    await state.clear()

@dp.message(F.text.in_(['◀️ Назад', '◀️ Back', '◀️ Назад']))
async def back_to_main(message: types.Message):
    await message.answer("Menu:", reply_markup=main_keyboard(message.from_user.id))

# === ЗАПУСК ===

async def main():
    db.init_db()
    print("🚀 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
