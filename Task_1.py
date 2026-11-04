
import random
import time

#Hash table (open addressing and linear probing)
class HashTable:
    def __init__(self, size=100):
        self.size = size
        self.slots = [None] * size  #None means empty slot
        self.count = 0

    def hash(self, key):
        return key % self.size

    def insert(self, product):
        """Returns slot index, -1 if the ID already exists, None if table is full."""
        if self.count == self.size:
            return None
        index = self.hash(product.id)
        while self.slots[index] is not None:
            if self.slots[index].id == product.id:
                return -1
            index = (index + 1) % self.size   #linear probing
        self.slots[index] = product
        self.count += 1
        return index

    def search(self, key):
        index = self.hash(key)
        for _ in range(self.size):
            if self.slots[index] is None:     #empty slot means when not in table
                return None
            if self.slots[index].id == key:
                return self.slots[index]
            index = (index + 1) % self.size   #linear probing
        return None


#Entity class and pre-defined records
class Product:
    def __init__(self, id, name, price, stock):
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock

    def __str__(self):
        return (f"ID: {self.id} | Name: {self.name} | "
                f"Price: RM{self.price:.2f} | Stock: {self.stock}")


def load_default_records(table, array):
    records = [
        Product(1001, "Ibuprofen 400mg", 8.90, 150),
        Product(1002, "Amoxicillin 500mg", 18.00, 80),
        Product(1003, "Cetirizine 10mg", 7.20, 120),
        Product(1101, "Omeprazole 20mg", 15.40, 60),    #collides with 1001 (slot 1)
        Product(1102, "Vitamin C 1000mg", 22.00, 110),  #collides with 1002 (slot 2)
    ]
    for p in records:
        table.insert(p)
        array.append(p)


#Command-line inventory system
def array_search(array, key):
    for product in array:
        if product.id == key:
            return product
    return None


def read_number(prompt, cast):
    while True:
        try:
            value = cast(input(prompt))
            if value < 0:
                raise ValueError
            return value
        except ValueError:
            print("Invalid input, please enter a non-negative number.")


def run_inventory():
    table = HashTable(100)
    array = []
    load_default_records(table, array)

    while True:
        print("==== Pharmacy Inventory System ====")
        print("1. Insert Product")
        print("2. Search Product")
        print("3. Run Performance Comparison")
        print("4. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            pid = read_number("Enter Product ID: ", int)
            name = input("Enter Product Name: ")
            price = read_number("Enter Price: ", float)
            stock = read_number("Enter Stock Quantity: ", int)
            product = Product(pid, name, price, stock)
            slot = table.insert(product)
            if slot is None:
                print("Hash table is full!\n")
            elif slot == -1:
                print("Product ID already exists!\n")
            else:
                array.append(product)  #same data goes into the array
                print(f"Product inserted successfully into slot [{slot}]\n")

        elif choice == "2":
            pid = read_number("Enter Product ID to search: ", int)

            start = time.perf_counter()
            product = table.search(pid)
            hash_time = time.perf_counter() - start

            start = time.perf_counter()
            array_search(array, pid)
            array_time = time.perf_counter() - start

            if product:
                print("Product Found!")
                print(product)
                print(f"Search completed in {hash_time:.6f} seconds (Hash Table)")
                print(f"Search completed in {array_time:.6f} seconds (Array - same record)\n")
            else:
                print("Product not found.\n")

        elif choice == "3":
            run_benchmark()

        elif choice == "4":
            print("Exiting Inventory System. Goodbye!")
            break

        else:
            print("Invalid choice.\n")

#Performance comparison: Hash Table vs One-Dimensional Array
def run_benchmark():
    random.seed(1)
    searches = 500
    print("\n=== Search time: Hash Table vs 1-D Array (500 searches each) ===")
    print(f"{'N':>7} | {'Case':<10} | {'Array (ms)':>11} | {'Hash (ms)':>10} | {'Speedup':>8}")
    print("-" * 58)

    for n in (100, 1000, 10000, 50000):
        ids = random.sample(range(1000, 10_000_000), n)
        table = HashTable(n * 2)                  #load factor 0.5
        array = []
        for pid in ids:
            p = Product(pid, "Drug", 10.0, 100)
            table.insert(p)
            array.append(p)

        found_keys = [random.choice(ids) for _ in range(searches)]
        missing_keys = [-i - 1 for i in range(searches)]   #IDs that do not exist

        for label, keys in (("found", found_keys), ("not found", missing_keys)):
            start = time.perf_counter()
            for k in keys:
                array_search(array, k)
            t_array = (time.perf_counter() - start) * 1000

            start = time.perf_counter()
            for k in keys:
                table.search(k)
            t_hash = (time.perf_counter() - start) * 1000

            print(f"{n:>7} | {label:<10} | {t_array:>11.3f} | {t_hash:>10.3f} | "
                  f"{t_array / t_hash:>7.1f}x")
        print("-" * 58)

if __name__ == "__main__":
    run_inventory()