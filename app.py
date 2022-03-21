from sqlalchemy import Integer
from models import Base, session, Inventory, engine
import time
import datetime
import csv

def menu():
    while True:
        print('\nINVENTORY\nv) View Details of Product\na) Add New Product\nb) Make of backup of entire Database\nc) Exit')
        choice = input('Select an Option: ').lower()
        if choice in ['v', 'a', 'b','c']:
            return choice
        else:
            input('Please choose one of the options above')


#where I clean all the data
def clean_price(price_str):
    try:
        for letter in price_str:
            if letter[0] == '$':
                split_price = price_str.split('$') 
                price_float = float(split_price[1])
                return_price = int(price_float * 100)
                return return_price
            else:
                price_float = float(price_str)
                return_price = int(price_float * 100)
                return return_price
    except IndexError or ValueError:
        print('Please input correctly formmatted Price')
        return
            


def clean_id(id_str, options):
    try:
        product_id = int(id_str)
    except ValueError:
        print('Please type a Number')
    else:
        if product_id in options:
            return product_id
        else:
            print('\nPlease select a Number above')


def clean_date(date_str):
    split_date = date_str.split('/')
    try:
        month = int(split_date[0])
        day = int(split_date[1])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except ValueError:
        print('Please input correctly formmatted Date')
        return
    else:
        return return_date


#adding the data to the database
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
            id_options = []
            for item in session.query(Inventory):
                id_options.append(item.product_id)
            while True:
                id_choice = input(f'ID Options: {id_options}\nBook ID: ')
                id_choice = clean_id(id_choice, id_options)
                if id_choice != None:
                    break
            the_product = (session.query(Inventory).filter(Inventory.product_id==id_choice).first())
            print(f'ID:{item.product_id} | NAME:{the_product.product_name} | QUANTITY:{the_product.product_quantity} | PRICE:{the_product.product_price} | DATE UPDATED:{the_product.date_updated}')
            input('Press Enter to return to Main Menu')
            
            
        elif choice == 'a':
            product_name = input('Product Name: ')
            product_quantity = input('Product Quantity: ')
            
            while True:
                product_price = input('Price (ex:12.99): ')  
                product_price_int = clean_price(product_price)
                if product_price_int != None:
                    break
            while True:
                date_updated = input('Current Date (ex:1/22/3333): ')
                date_updated = clean_date(date_updated)
                if type(date_updated) == datetime.date:
                    break
            new_product = Inventory(product_name = product_name, product_price = product_price, product_quantity = product_quantity, date_updated = date_updated)
            session.add(new_product)
            session.commit()
            print('Product Added!')
            time.sleep(1.5)

        elif choice == 'b':
            with open('backup.csv', 'a') as csv_file:
                header = ['name', ' quantity', ' price', ' date updated']
                writer = csv.writer(csv_file)
                writer.writerow(header)
                products = session.query(Inventory)
                for product in products:
                    data = [product.product_name, product.product_quantity, product.product_price, product.date_updated]
                    writer.writerow(data)
                input('Backup File was Created. Press Enter to continue')

        elif choice == 'c':
            print('Goodbye')
            app_running = False






if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()
    

    for item in session.query(Inventory):
        print(item)

