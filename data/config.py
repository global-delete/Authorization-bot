from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
ip = env.str("ip")  # Тоже str, но для айпи адреса хоста
DATABASE = env.str("DATABASE")
PGUSER = env.str("PGUSER")
PGPASSWORD = env.str("PGPASSWORD")
POSTGRES_PORT = env.int("POSTGRES_PORT", default=5432)
POSTGRES_URL = f"postgresql://{PGUSER}:{PGPASSWORD}@{ip}:{POSTGRES_PORT}/{DATABASE}"
