# Конфигурация бота

# Токен бота (получить у @BotFather)
API_TOKEN = 'YOUR_BOT_TOKEN_HERE'

# ID администраторов (список Telegram ID)
ADMIN_IDS = [
    123456789,  # Замените на ваш ID
]

# Настройки экономики
ECONOMY = {
    'start_balance': 100,  # Стартовый баланс
    'daily_reward_base': 50,  # Базовая ежедневная награда
    'daily_reward_streak_bonus': 10,  # Бонус за каждый день streak
    'daily_reward_max': 500,  # Максимальная награда
    'work_cooldown': 7200,  # Кулдаун работы (секунды)
    'level_exp_base': 100,  # Базовый опыт для уровня
    'level_exp_multiplier': 1.5,  # Множитель опыта
}

# Работы и их награды
WORK_TYPES = {
    'programmer': {'name': '💻 Программист', 'reward': 50},
    'taxi': {'name': '🚕 Таксист', 'reward': 30},
    'barista': {'name': '☕ Бариста', 'reward': 20},
    'courier': {'name': '📦 Курьер', 'reward': 25},
    'designer': {'name': '🎨 Дизайнер', 'reward': 40},
    'teacher': {'name': '👨‍🏫 Учитель', 'reward': 35},
}

# Категории магазина
SHOP_CATEGORIES = [
    'general',  # Общее
    'premium',  # Премиум
    'special',  # Специальное
    'limited',  # Лимитированное
]

# Настройки
SETTINGS = {
    'enable_referral': True,  # Реферальная система
    'referral_bonus': 50,  # Бонус за реферала
    'enable_achievements': True,  # Достижения
    'enable_levels': True,  # Уровни
}
