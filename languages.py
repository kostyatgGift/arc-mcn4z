# -*- coding: utf-8 -*-
"""
Мультиязычность для бота
Поддерживаемые языки: RU, EN, UK
"""

LANGUAGES = {
    'ru': {
        # Главное меню
        'profile': '💰 Профиль',
        'shop': '🏪 Магазин',
        'inventory': '🎒 Инвентарь',
        'work': '💼 Работа',
        'daily_reward': '🎁 Ежедневная награда',
        'rating': '🏆 Рейтинг',
        'admin_panel': '⚙️ Админ-панель',
        'back': '◀️ Назад',
        'settings': '⚙️ Настройки',
        
        # Приветствие
        'welcome': '👋 Привет, {name}!\n\nДобро пожаловать в бот!\n\n🎮 Здесь ты можешь:\n• Зарабатывать монеты\n• Покупать предметы в магазине\n• Собирать коллекцию в инвентаре\n• Соревноваться с другими игроками\n\nВыбери действие в меню:',
        
        # Профиль
        'profile_text': '👤 Профиль: {name}\n🆔 ID: {user_id}\n\n💰 Баланс: {balance}₽\n⭐ Уровень: {level}\n✨ Опыт: {exp}\n🎒 Предметов в инвентаре: {items}\n🔥 Серия ежедневных наград: {streak} дней\n\n📅 Регистрация: {reg_date}',
        'profile_not_found': '❌ Профиль не найден. Используй /start',
        
        # Магазин
        'shop_empty': '🏪 Магазин пуст. Скоро добавим товары!',
        'shop_welcome': '🏪 Добро пожаловать в магазин!\n\n',
        'shop_buy_instruction': '\nДля покупки напишите: купить [номер товара]\nПример: купить 1',
        'buy_invalid_format': '❌ Укажите номер товара!\nПример: купить 1',
        'buy_not_found': '❌ Товар с номером {num} не найден!',
        'buy_not_enough': '❌ Недостаточно средств!\n\nНужно: {price}₽\nУ вас: {balance}₽',
        'buy_success': '✅ Покупка успешна!\n\n🛍 Товар: {name}\n💰 Потрачено: {price}₽\n💵 Остаток: {balance}₽',
        'buy_error': '❌ Ошибка: {error}',
        
        # Инвентарь
        'inventory_empty': '🎒 Ваш инвентарь пуст.\n\nЗагляните в магазин!',
        'inventory_text': '🎒 Ваш инвентарь:\n\n',
        
        # Работа
        'work_list': '💼 Доступные работы:\n\n1. 💻 Программист - 50₽\n2. 🚕 Таксист - 30₽\n3. ☕ Бариста - 20₽\n4. 📦 Курьер - 25₽\n5. 🎨 Дизайнер - 40₽\n6. 👨‍🏫 Учитель - 35₽\n\n⏰ Работать можно каждые 2 часа\n\nДля работы напишите: работа [номер]\nПример: работа 1',
        'work_invalid': '❌ Укажите номер работы!\nПример: работа 1',
        'work_not_found': '❌ Работа не найдена! Выберите от 1 до 6',
        'work_cooldown': '⏰ Вы уже работали!\n\nПодождите: {hours}ч {minutes}мин',
        'work_success': '✅ Работа выполнена!\n\n🏢 Должность: {name}\n💰 Заработано: {reward}₽\n\n⏰ Следующая работа через 2 часа',
        
        # Награды
        'daily_already': '❌ Вы уже получили награду сегодня!\n\nПриходите завтра.',
        'daily_success': '🎁 Ежедневная награда получена!\n\n💰 +{reward}₽\n🔥 Серия: {streak} дней\n\nЗаходите каждый день чтобы увеличить награду!',
        
        # Рейтинг
        'rating_text': '🏆 Топ-10 игроков:\n\n',
        
        # Админка
        'admin_panel_text': '⚙️ Админ-панель',
        'stats': '📊 Статистика',
        'broadcast': '📢 Рассылка',
        'manage_shop': '🛠 Управление магазином',
        'create_button': '🎨 Создать кнопку',
        'manage_users': '👤 Управление пользователями',
        'logs': '📝 Логи',
        'no_access': '❌ Нет доступа',
        
        'stats_text': '📊 Статистика бота:\n\n👥 Всего пользователей: {total}\n🚫 Забанено: {banned}\n💰 Общий баланс: {balance}₽\n💸 Транзакций: {transactions}',
        
        'broadcast_prompt': '📢 Отправьте сообщение для рассылки:',
        'broadcast_done': '✅ Рассылка завершена!\n\nОтправлено: {success}/{total}',
        
        'shop_add_name': '🛠 Добавление товара в магазин\n\nВведите название товара:',
        'shop_add_price': '💰 Введите цену товара (число):',
        'shop_add_desc': '📝 Введите описание товара:',
        'shop_add_photo': '📷 Отправьте фото товара (или напишите "нет"):',
        'shop_added': '✅ Товар "{name}" добавлен в магазин!',
        
        'button_add_title': '🎨 Создание кастомной кнопки\n\nВведите текст кнопки:',
        'button_add_text': '💬 Введите текст который будет отправляться при нажатии:',
        'button_add_photo': '📷 Отправьте фото (или напишите "нет"):',
        'button_created': '✅ Кнопка "{title}" создана!\n\nПерезапустите бота для обновления меню.',
        
        'users_menu': '👤 Управление пользователями:',
        'ban_user': '🚫 Забанить',
        'unban_user': '✅ Разбанить',
        'give_balance': '💰 Выдать баланс',
        'users_list': '📋 Список пользователей',
        
        'ban_prompt_id': '🚫 Введите ID пользователя для бана:',
        'ban_prompt_reason': '📝 Введите причину бана:',
        'ban_success': '✅ Пользователь {user_id} забанен!',
        'banned_message': '❌ Вы заблокированы.\n\n📋 Причина: {reason}',
        
        'choose_language': '🌐 Выберите язык:\n\n🇷🇺 Русский\n🇬🇧 English\n🇺🇦 Українська\n\nОтправьте: ru, en или uk',
        'language_changed': '✅ Язык изменен!',
    },
    
    'en': {
        # Main menu
        'profile': '💰 Profile',
        'shop': '🏪 Shop',
        'inventory': '🎒 Inventory',
        'work': '💼 Work',
        'daily_reward': '🎁 Daily Reward',
        'rating': '🏆 Rating',
        'admin_panel': '⚙️ Admin Panel',
        'back': '◀️ Back',
        'settings': '⚙️ Settings',
        
        # Welcome
        'welcome': '👋 Hello, {name}!\n\nWelcome to the bot!\n\n🎮 Here you can:\n• Earn coins\n• Buy items in the shop\n• Collect items in your inventory\n• Compete with other players\n\nChoose an action from the menu:',
        
        # Profile
        'profile_text': '👤 Profile: {name}\n🆔 ID: {user_id}\n\n💰 Balance: {balance}₽\n⭐ Level: {level}\n✨ Experience: {exp}\n🎒 Items in inventory: {items}\n🔥 Daily reward streak: {streak} days\n\n📅 Registration: {reg_date}',
        'profile_not_found': '❌ Profile not found. Use /start',
        
        # Shop
        'shop_empty': '🏪 The shop is empty. Items coming soon!',
        'shop_welcome': '🏪 Welcome to the shop!\n\n',
        'shop_buy_instruction': '\nTo buy, write: buy [item number]\nExample: buy 1',
        'buy_invalid_format': '❌ Specify the item number!\nExample: buy 1',
        'buy_not_found': '❌ Item #{num} not found!',
        'buy_not_enough': '❌ Not enough funds!\n\nNeeded: {price}₽\nYou have: {balance}₽',
        'buy_success': '✅ Purchase successful!\n\n🛍 Item: {name}\n💰 Spent: {price}₽\n💵 Remaining: {balance}₽',
        'buy_error': '❌ Error: {error}',
        
        # Inventory
        'inventory_empty': '🎒 Your inventory is empty.\n\nCheck out the shop!',
        'inventory_text': '🎒 Your inventory:\n\n',
        
        # Work
        'work_list': '💼 Available jobs:\n\n1. 💻 Programmer - 50₽\n2. 🚕 Taxi Driver - 30₽\n3. ☕ Barista - 20₽\n4. 📦 Courier - 25₽\n5. 🎨 Designer - 40₽\n6. 👨‍🏫 Teacher - 35₽\n\n⏰ You can work every 2 hours\n\nTo work, write: work [number]\nExample: work 1',
        'work_invalid': '❌ Specify the job number!\nExample: work 1',
        'work_not_found': '❌ Job not found! Choose from 1 to 6',
        'work_cooldown': '⏰ You already worked!\n\nWait: {hours}h {minutes}m',
        'work_success': '✅ Work completed!\n\n🏢 Position: {name}\n💰 Earned: {reward}₽\n\n⏰ Next work in 2 hours',
        
        # Rewards
        'daily_already': '❌ You already claimed your reward today!\n\nCome back tomorrow.',
        'daily_success': '🎁 Daily reward claimed!\n\n💰 +{reward}₽\n🔥 Streak: {streak} days\n\nCome back every day to increase your reward!',
        
        # Rating
        'rating_text': '🏆 Top-10 players:\n\n',
        
        # Admin
        'admin_panel_text': '⚙️ Admin Panel',
        'stats': '📊 Statistics',
        'broadcast': '📢 Broadcast',
        'manage_shop': '🛠 Manage Shop',
        'create_button': '🎨 Create Button',
        'manage_users': '👤 Manage Users',
        'logs': '📝 Logs',
        'no_access': '❌ No access',
        
        'stats_text': '📊 Bot statistics:\n\n👥 Total users: {total}\n🚫 Banned: {banned}\n💰 Total balance: {balance}₽\n💸 Transactions: {transactions}',
        
        'broadcast_prompt': '📢 Send message for broadcast:',
        'broadcast_done': '✅ Broadcast completed!\n\nSent: {success}/{total}',
        
        'shop_add_name': '🛠 Adding item to shop\n\nEnter item name:',
        'shop_add_price': '💰 Enter item price (number):',
        'shop_add_desc': '📝 Enter item description:',
        'shop_add_photo': '📷 Send item photo (or write "no"):',
        'shop_added': '✅ Item "{name}" added to shop!',
        
        'button_add_title': '🎨 Creating custom button\n\nEnter button text:',
        'button_add_text': '💬 Enter text that will be sent on click:',
        'button_add_photo': '📷 Send photo (or write "no"):',
        'button_created': '✅ Button "{title}" created!\n\nRestart the bot to update the menu.',
        
        'users_menu': '👤 User management:',
        'ban_user': '🚫 Ban',
        'unban_user': '✅ Unban',
        'give_balance': '💰 Give Balance',
        'users_list': '📋 User List',
        
        'ban_prompt_id': '🚫 Enter user ID to ban:',
        'ban_prompt_reason': '📝 Enter ban reason:',
        'ban_success': '✅ User {user_id} banned!',
        'banned_message': '❌ You are blocked.\n\n📋 Reason: {reason}',
        
        'choose_language': '🌐 Choose language:\n\n🇷🇺 Русский\n🇬🇧 English\n🇺🇦 Українська\n\nSend: ru, en or uk',
        'language_changed': '✅ Language changed!',
    },
    
    'uk': {
        # Головне меню
        'profile': '💰 Профіль',
        'shop': '🏪 Магазин',
        'inventory': '🎒 Інвентар',
        'work': '💼 Робота',
        'daily_reward': '🎁 Щоденна нагорода',
        'rating': '🏆 Рейтинг',
        'admin_panel': '⚙️ Адмін-панель',
        'back': '◀️ Назад',
        'settings': '⚙️ Налаштування',
        
        # Привітання
        'welcome': '👋 Привіт, {name}!\n\nЛаскаво просимо до бота!\n\n🎮 Тут ти можеш:\n• Заробляти монети\n• Купувати предмети в магазині\n• Збирати колекцію в інвентарі\n• Змагатися з іншими гравцями\n\nОбери дію в меню:',
        
        # Профіль
        'profile_text': '👤 Профіль: {name}\n🆔 ID: {user_id}\n\n💰 Баланс: {balance}₽\n⭐ Рівень: {level}\n✨ Досвід: {exp}\n🎒 Предметів в інвентарі: {items}\n🔥 Серія щоденних нагород: {streak} днів\n\n📅 Реєстрація: {reg_date}',
        'profile_not_found': '❌ Профіль не знайдено. Використай /start',
        
        # Магазин
        'shop_empty': '🏪 Магазин порожній. Скоро додамо товари!',
        'shop_welcome': '🏪 Ласкаво просимо до магазину!\n\n',
        'shop_buy_instruction': '\nДля покупки напишіть: купити [номер товару]\nПриклад: купити 1',
        'buy_invalid_format': '❌ Вкажіть номер товару!\nПриклад: купити 1',
        'buy_not_found': '❌ Товар з номером {num} не знайдено!',
        'buy_not_enough': '❌ Недостатньо коштів!\n\nПотрібно: {price}₽\nУ вас: {balance}₽',
        'buy_success': '✅ Покупка успішна!\n\n🛍 Товар: {name}\n💰 Витрачено: {price}₽\n💵 Залишок: {balance}₽',
        'buy_error': '❌ Помилка: {error}',
        
        # Інвентар
        'inventory_empty': '🎒 Ваш інвентар порожній.\n\nЗагляньте в магазин!',
        'inventory_text': '🎒 Ваш інвентар:\n\n',
        
        # Робота
        'work_list': '💼 Доступні роботи:\n\n1. 💻 Програміст - 50₽\n2. 🚕 Таксист - 30₽\n3. ☕ Бариста - 20₽\n4. 📦 Кур\'єр - 25₽\n5. 🎨 Дизайнер - 40₽\n6. 👨‍🏫 Вчитель - 35₽\n\n⏰ Працювати можна кожні 2 години\n\nДля роботи напишіть: робота [номер]\nПриклад: робота 1',
        'work_invalid': '❌ Вкажіть номер роботи!\nПриклад: робота 1',
        'work_not_found': '❌ Робота не знайдена! Оберіть від 1 до 6',
        'work_cooldown': '⏰ Ви вже працювали!\n\nЗачекайте: {hours}г {minutes}хв',
        'work_success': '✅ Робота виконана!\n\n🏢 Посада: {name}\n💰 Заробіток: {reward}₽\n\n⏰ Наступна робота через 2 години',
        
        # Нагороди
        'daily_already': '❌ Ви вже отримали нагороду сьогодні!\n\nПриходьте завтра.',
        'daily_success': '🎁 Щоденна нагорода отримана!\n\n💰 +{reward}₽\n🔥 Серія: {streak} днів\n\nЗаходьте кожен день щоб збільшити нагороду!',
        
        # Рейтинг
        'rating_text': '🏆 Топ-10 гравців:\n\n',
        
        # Адмінка
        'admin_panel_text': '⚙️ Адмін-панель',
        'stats': '📊 Статистика',
        'broadcast': '📢 Розсилка',
        'manage_shop': '🛠 Управління магазином',
        'create_button': '🎨 Створити кнопку',
        'manage_users': '👤 Управління користувачами',
        'logs': '📝 Логи',
        'no_access': '❌ Немає доступу',
        
        'stats_text': '📊 Статистика бота:\n\n👥 Всього користувачів: {total}\n🚫 Забанено: {banned}\n💰 Загальний баланс: {balance}₽\n💸 Транзакцій: {transactions}',
        
        'broadcast_prompt': '📢 Надішліть повідомлення для розсилки:',
        'broadcast_done': '✅ Розсилка завершена!\n\nНадіслано: {success}/{total}',
        
        'shop_add_name': '🛠 Додавання товару в магазин\n\nВведіть назву товару:',
        'shop_add_price': '💰 Введіть ціну товару (число):',
        'shop_add_desc': '📝 Введіть опис товару:',
        'shop_add_photo': '📷 Надішліть фото товару (або напишіть "ні"):',
        'shop_added': '✅ Товар "{name}" додано в магазин!',
        
        'button_add_title': '🎨 Створення власної кнопки\n\nВведіть текст кнопки:',
        'button_add_text': '💬 Введіть текст який буде надсилатись при натисканні:',
        'button_add_photo': '📷 Надішліть фото (або напишіть "ні"):',
        'button_created': '✅ Кнопка "{title}" створена!\n\nПерезапустіть бота для оновлення меню.',
        
        'users_menu': '👤 Управління користувачами:',
        'ban_user': '🚫 Забанити',
        'unban_user': '✅ Розбанити',
        'give_balance': '💰 Видати баланс',
        'users_list': '📋 Список користувачів',
        
        'ban_prompt_id': '🚫 Введіть ID користувача для бану:',
        'ban_prompt_reason': '📝 Введіть причину бану:',
        'ban_success': '✅ Користувач {user_id} забанений!',
        'banned_message': '❌ Ви заблоковані.\n\n📋 Причина: {reason}',
        
        'choose_language': '🌐 Оберіть мову:\n\n🇷🇺 Русский\n🇬🇧 English\n🇺🇦 Українська\n\nНадішліть: ru, en або uk',
        'language_changed': '✅ Мову змінено!',
    }
}

def get_text(lang, key, **kwargs):
    """Получить текст на нужном языке"""
    if lang not in LANGUAGES:
        lang = 'ru'
    
    text = LANGUAGES[lang].get(key, LANGUAGES['ru'].get(key, key))
    
    if kwargs:
        try:
            return text.format(**kwargs)
        except:
            return text
    
    return text
