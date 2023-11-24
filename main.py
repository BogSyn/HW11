from collections import UserDict
from datetime import datetime, date


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value: str):
        if len(value) == 10 and value.isdigit():
            Field.value.fset(self, value)
        else:
            raise ValueError(f'Phone {self.value} not valid')


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value: str):
        if len(value.split('.')) == 3 and all(part.isdigit() for part in value.split('.')) and len(value.split('.')[0]) == 4:
            Field.value.fset(self, datetime.strptime(value, '%Y.%m.%d').date())
        else:
            raise ValueError('Date format should be: year.month.day')


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthdays = []

    # повертає кількість днів до наступного дня народження
    def days_to_birthday(self):
        if self.birthdays:
            today = date.today()
            birhtday = [p.value for p in john_record.birthdays]
            if today.month > birhtday[0].month:
                result = birhtday[0].replace(year=today.year+1) - today
                return f"{self.name.value}'s birthday in {result.days} days"
            else:
                result = birhtday[0].replace(year=today.year) - today
                return f"{self.name.value}'s birthday in {result.days} days"
        else:
            return f"{self.name.value}'s birthday has not been added"

    # метод додавання дня народження
    def add_birthday(self, input_date: str):
        birthday = Birthday(input_date)
        if not self.birthdays:
            self.birthdays.append(birthday)
            print(f"Birthday of {self.name.value} successfully added.")
        else:
            print(f"Birthday of {self.name.value} is already added.")

    # метод додавання телефону
    def add_phone(self, input_phone: str):
        phone = Phone(input_phone)
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            print(f"{phone} successfully added.")
        else:
            print(f"{phone} is already added.")

    # видаляє телефон, або виводить, що немає номеру в всписку
    def remove_phone(self, phone: str):
        if phone in [p.value for p in self.phones]:
            self.phones.remove(
                self.phones[[p.value for p in self.phones].index(phone)])
            print(f"{phone} successfully removed")
        else:
            print(f"{phone} not found in the list of phones.")

    # редагує номер
    def edit_phone(self, old_phone, new_phone):
        phone = Phone(new_phone)
        if old_phone in [p.value for p in self.phones]:
            position = [p.value for p in self.phones].index(old_phone)
            self.phones.remove(self.phones[position])
            self.phones.insert(position, phone)
            print(f"{phone} successfully adited.")
        else:
            raise ValueError(f"{phone} not found in the list of phones.")

    # пошук номеру телефону
    def find_phone(self, phone):
        phone = Phone(phone)
        if phone.value in [p.value for p in self.phones]:
            print(f"{self.name.value}: {phone}")
            return phone
        else:
            print(f"{phone} not in {self.name.value} contacts")

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    # додає запис до self.data.
    def add_record(self, record):
        self.data[record.name.value] = record

    # знаходить за ім'ям.
    def find(self, name):
        if name in self.data.keys():
            return self.data[name]
        else:
            print(f"{name} not found")

    # видаляє запис за ім'ям.
    def delete(self, name):
        if name in self.data.keys():
            del self.data[name]
            print(f"{name} is delete")
        else:
            print(f"{name} not found")

    # повертає генератор за записами;
    # якщо кількість контактів запиту більша за кількість контактів в словнику -> всі контакти;
    def iterator(self, quantity):
        counter = 0
        result = ''
        if len(self.data) < quantity:
            for record in self.data.values():
                result += f'\n{record}'
            yield result
        else:
            for record in self.data.values():
                result += f'\n{record}'
                counter += 1
                if counter >= quantity:
                    yield result
                    counter = 0
                    result = ''


if __name__ == "__main__":
    book = AddressBook()
    john_record = Record("John")
    jane_record = Record("Jane")
    jack_record = Record("Jack")
    julia_record = Record("Julia")

    john_record.add_phone("0934567890")
    john_record.add_phone("0987654321")
    jane_record.add_phone("0506543210")
    jack_record.add_phone("0676554610")
    julia_record.add_phone("0956543210")

    print('-'*30)
    john_record.add_birthday('1987.12.25')
    print('-'*30)
    print(john_record.days_to_birthday())

    book.add_record(john_record)
    book.add_record(jane_record)
    book.add_record(jack_record)
    book.add_record(julia_record)

    print("All contacts", '-'*30)
    for name, record in book.data.items():
        print(record)

    print("Pagination", '-'*30)
    BOOK = book.iterator(2)
    for group in BOOK:
        print(group)
