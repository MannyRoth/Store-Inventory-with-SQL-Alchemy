
from itertools import product
from models import Base, session, Inventory, engine
import datetime
import csv

def menu():
    while True:
        print('INVENTORY\nv) View Details of Product\na) Add New Product\nb) Make of backup of entire Database\nc) Exit')
        choice = input('Select an Option: ').lower()
        if choice in ['v', 'a', 'b','c']:
            return choice
        else:
            input('Please choose one of the options above')



def clean_price(price_str):
    split_price = price_str.split('$')
    price_float = float(split_price[1])
    return int(price_float * 100)
    

def clean_date(date_str):
    split_date = date_str.split('/')
    print(split_date)
    month = int(split_date[0])
    day = int(split_date[1])
    year = int(split_date[2])
    return datetime.date(year, month, day)


def add_csv():
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        next(data)
        for row in data:
            product_in_db = session.query(Inventory).filter(Inventory.product_name==row[0]).one_or_none()
            if product_in_db == None:
                product_name = row[0]
                product_price = clean_price(row[1])
                product_quantity = row[2]
                date_updated = clean_date(row[3])
                new_product = Inventory(product_name = product_name, product_price = product_price, product_quantity = product_quantity, date_updated = date_updated)
                session.add(new_product)
        session.commit()
            





def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'v':
            pass
        elif choice == 'a':
            pass
        elif choice == 'b':
            pass
        else:
            print('Goodbye')
            app_running = False






if __name__ == '__main__':
    Base.metadata.create_all(engine)
    #app()
    add_csv()
    
    for item in session.query(Inventory):
        print(item)
