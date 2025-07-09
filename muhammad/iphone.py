port
psycopg2


class ToDo:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='water',
            user='postgres',
            password='0700',
            host='localhost',
            port='5432'
        )
        self.cur = self.conn.cursor()
        self.user_id = None

    def royxatdan_ot(self, username, password):
        try:
            self.cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            self.conn.commit()
            print("Ro'yxatdan o'tildi.")
        except psycopg2.errors.UniqueViolation:
            self.conn.rollback()
            print("Username band.")

    def login(self, username, password):
        self.cur.execute("SELECT id FROM users WHERE username = %s AND password = %s", (username, password))
        user = self.cur.fetchone()
        if user:
            self.user_id = user[0]
            print(f"Xush kelibsiz, {username}!")
            return True
        else:
            print("Login yoki parol xato")
            return False

    def qoshish(self, vazifa):
        self.cur.execute("INSERT INTO todolist (user_id, vazifa) VALUES (%s, %s)", (self.user_id, vazifa))
        self.conn.commit()
        print("Vazifa qo'shildi.")

    def korish(self):
        try:
            self.cur.execute("SELECT id, vazifa, bajarildi FROM todolist WHERE user_id = %s AND deleted = FALSE",
                             (self.user_id,))
            tasks = self.cur.fetchall()
            if not tasks:
                print("Vazifalar yo'q")
            else:
                for row in tasks:
                    status = "✅" if row[2] else "❌"
                    print(f"{row[0]}. {row[1]} - {status}")

        except Exception as e:
            self.conn.rollback()
            print("Xatolik yuz berdi:")

    def bajarilgan(self, id):
        self.cur.execute("UPDATE todolist SET balarildi = TRUE WHERE id = %s AND user_id = %s AND deleted = FALSE",
                         (id, self.user_id))
        if self.cur.rowcount:
            self.conn.commit()
            print("Bajarildi deb belgilandi.")
        else:
            print("Vazifa topilmadi.")

    def ochirish(self, id):
        self.cur.execute("UPDATE todolist SET deleted = TRUE WHERE id = %s AND user_id = %s", (id, self.user_id))
        if self.cur.rowcount:
            self.conn.commit()
            print("Vazifa o'chirildi.")
        else:
            print("Vazifa topilmadi.")

    def __del__(self):
        self.cur.close()
        self.conn.close()


def asosiy_menyu():
    app = ToDo()

    while True:
        print("\n------------TO DO LIST--------------")
        print("1.Ro'yxatdan o'tish")
        print("2.Kirish")
        print("3.Chiqish")
        tanlash = input("Tanlang: ")

        if tanlash == "1":
            u = input("Username: ")
            p = str(input("Parol: "))
            app.royxatdan_ot(u, p)

        elif tanlash == "2":
            u = input("Username: ")
            p = str(input("Parol: "))
            app.login(u, p)
            if app.login(u, p):
                foydalanuvchi_menyu(app)

        elif tanlash == "3":
            print("Dasturldan chiqildi.")
            break

        else:
            print("Tanlov noto'g'ri")


def foydalanuvchi_menyu(app):
    while True:
        print("\n---------VAZIFALAR MENYUSI-------------")
        print("1. Vazifa qo'shish")
        print("2. Vazifani korish")
        print("3. Bajarilgan deb belgilash")
        print("4. Vazifani o'chirish")
        print("0. Chiqish")

        tanlash = input("Tanlang: ")

        if tanlash == "1":
            v = input("Vazifa qo'shing: ")
            app.qoshish(v)
        elif tanlash == "2":
            app.korish()
        elif tanlash == "3":
            try:
                id = int(input("Vazifa ID: "))
                app.bajarilgan(id)
            except:
                print("ID raqam bo'lishi kerak.")
        elif tanlash == "4":
            try:
                id = int(input("O'chirish uchun ID: "))
                app.ochirish(id)
            except:
                print("ID raqam bo'lishi kerak")

        elif tanlash == "0":
            break
        else:
            print("Tanlov no'to'g'ri")


asosiy_menyu()