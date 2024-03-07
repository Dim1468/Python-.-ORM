import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import Publisher, Book, Stock, Shop, Sale

#Установка соединения с базой данных
def create_connection(sqlsystem, login, password, host, port, db_name):
    try:
        engine = sqlalchemy.create_engine(f'{sqlsystem}://{login}:{password}@{host}:{port}/{db_name}')
        print('Соединение установлено')
    except:
        print(f'Ошибка подключения')
    return engine

# Создание соединения
engine = create_connection('postgresql', 'postgres', 'password', 'localhost', 5432, 'ORM')
Session = sessionmaker(bind=engine)
session = Session()

# Определение функции для вывода фактов покупки книг целевого издателя
def sale_list(search=input('Введите идентификатор или имя издателя: ')):
    search = search
    if search.isnumeric():
        results = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale) \
            .join(Publisher, Publisher.id == Book.id_publisher) \
            .join(Stock, Stock.id_book == Book.id) \
            .join(Shop, Shop.id == Stock.id_shop) \
            .join(Sale, Sale.id_stock == Stock.id) \
            .filter(Publisher.id == search).all()
        for book, shop, price, date in results:
            print(f'{book: <40} | {shop: <10} | {price: <10} | {date}')
    else:
        results = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale) \
            .join(Publisher, Publisher.id == Book.id_publisher) \
            .join(Stock, Stock.id_book == Book.id) \
            .join(Shop, Shop.id == Stock.id_shop) \
            .join(Sale, Sale.id_stock == Stock.id) \
            .filter(Publisher.name == search).all()
        for book, shop, price, date in results:
            print(f'{book: <40} | {shop: <10} | {price: <10} | {date}')

# Вызов функции для вывода фактов покупки
sale_list()

# Закрытие сессии
session.close()