from tkinter import *
from tkinter import messagebox
import MySQLdb
import cfscrape
from bs4 import BeautifulSoup

class DatabaseConnector:
    # connecting to mysql
    def __init__(self):
        self.host = "sql7.freesqldatabase.com"
        self.port = 3306
        self.name = "sql7338613"
        self.user = "sql7338613"
        self.password = "a8jjmKwfqU"
        self.conn = None

    def get_conn(self):
        if self.conn is None:
            self.conn = MySQLdb.connect(host = self.host,
                                    port = self.port,
                                    db = self.name,
                                    user = self.user,
                                    passwd = self.password)
        return self.conn



class OpeningPage:
    # Class for the Opening frame
    def __init__(self, master):

        self.master = master

        self.master.title('Geographic Markers Research Project')

        self.master.logo = PhotoImage(file='Journal logo.gif')

        self.master.explanation_text = '''Geographic Markers Research Project is a project led by Dr. Murat Ergin, Sevil Togay, and another
        assistant from the Comparative History and Society department at Koç University. The main 
        aim is uncovering how neo-colonial power relations continue to operate on academic 
        writing practices of various scholars across the world'''

        self.master.interval_year_text = '\n\nInterval year'

        self.master.interval_year = 'xxxx'

        self.master.proceed_text = 'Proceed'

        self.frame = Frame(self.master)

        self.master.Logo_label = Label(self.master, image=self.master.logo)
        self.master.Logo_label.grid(row=0, column=0)

        self.master.Explanation_label = Label(self.master, text=self.master.explanation_text, justify='center',
                                              font='None 10')
        self.master.Explanation_label.grid(row=1, column=0)

        self.master.Interval_year_label_text = Label(self.master, text=self.master.interval_year_text, justify='center',
                                                     font='None 10 bold')
        self.master.Interval_year_label_text.grid(row=2, column=0)

        self.master.Interval_year_label = Label(self.master, text=self.master.interval_year, justify='center',
                                                font='None 10 bold')
        self.master.Interval_year_label.grid(row=3, column=0)

        self.master.Proceed_button = Button(self.master, text=self.master.proceed_text, width=8,
                                            command=self.open_login_window)
        self.master.Proceed_button.grid(row=5, column=0, padx=10, pady=10)

        self.fetch_interval_year()

    def fetch_interval_year(self):
        # Dynamically Fetching interval year
        british_journal_url = 'https://onlinelibrary.wiley.com/action/showPublications?PubType=journal&alphabetRange=b&pageSize=200&startPage=0'
        scraper = cfscrape.create_scraper()
        html_source = scraper.get(british_journal_url).text
        soup = BeautifulSoup(html_source, 'lxml')

        date = []
        count = 0
        for articles in soup.findAll('div', class_='item__body clearfix'):
            try:
                if 'The British Journal of Sociology' in articles.h3.a.text:
                    for journal_date in articles.findAll('span', class_='meta__date'):
                        date.append(journal_date.text)
                        count = count + 1
            except:
                pass
        self.master.Interval_year_label.config(text=date[1] + ' to ' + date[0])

    def open_login_window(self):
        self.newWindow = Toplevel(self.master)
        self.app = LogInPage(self.newWindow)


class LogInPage:
    # class for Log In page
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)

        self.sign_in_text = 'Sign In Page'
        self.username_label_text = 'Username'
        self.password_label_text = 'Password'
        self.sign_in_button_text = 'Sign In'
        self.sign_up_button_text = 'Sign Up'

        self.username_var = StringVar()
        self.password_var = StringVar()

        self.master.Sign_In_label = Label(self.master, text=self.sign_in_text, justify='center',
                                          font=('Arial Bold', 14))
        self.master.Sign_In_label.grid(row=0, column=1, padx=10, pady=10)

        self.master.Username_label = Label(self.master, text=self.username_label_text, font=12)
        self.master.Username_label.grid(row=1, column=0, padx=10, pady=10)

        self.master.Username_Entry = Entry(self.master, textvariable=self.username_var)
        self.master.Username_Entry.grid(row=1, column=1, padx=10, pady=10)

        self.master.Password_label = Label(self.master, text=self.password_label_text, font=12)
        self.master.Password_label.grid(row=2, column=0, padx=10, pady=10)

        self.master.Password_Entry = Entry(self.master, textvariable=self.password_var, show='*')
        self.master.Password_Entry.grid(row=2, column=1, padx=10, pady=10)

        self.master.Sign_In_button = Button(self.master, text=self.sign_in_button_text, width=7, command=self.login)
        self.master.Sign_In_button.grid(row=3, column=1, padx=10, pady=10)

        self.master.Sign_Up_button = Button(self.master, text=self.sign_up_button_text, width=7,
                                            command=self.open_signup_window)
        self.master.Sign_Up_button.grid(row=4, column=1, padx=10, pady=10)

    def open_signup_window(self):
        # Opening the sign up page from the log in page
        self.master.withdraw()
        self.newWindow = Toplevel(self.master)
        self.app = SignUpPage(self.newWindow)

    def login(self):
        # getting the values
        data = (
            self.username_var.get(),
            self.password_var.get()
        )
        if self.username_var.get() == "":
            self.messagebox.showinfo("Alert!", "You must insert username first!")
        elif self.password_var.get() == "":
            self.messagebox.showinfo("Alert!", "You must insert password first!")
        else:


            self.database_connection = DatabaseConnector().get_conn()
            self.cursor = self.database_connection.cursor()

            try:
                self.cursor.execute("SELECT * FROM user_login_info WHERE username=%s AND password=%s", data)
                self.result = self.cursor.fetchone()
            except:
                self.result = False
            if self.result:
                messagebox.showinfo("Message", "You logged in successfully!")
            else:
                messagebox.showinfo("Alert", "Wrong username or password!")


class SignUpPage:
    # Class for the Sign Up page
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)

        self.sign_up_text = 'Sign Up Page'
        self.username_label_text = 'Username'
        self.password_label_text = 'Password'
        self.sign_up_button_text = 'Sign Up'

        self.username_var2 = StringVar()
        self.password_var2 = StringVar()

        self.master.Sign_Up_label = Label(self.master, text=self.sign_up_text, justify='center',
                                          font=('Arial Bold', 14))
        self.master.Sign_Up_label.grid(row=0, column=1, padx=10, pady=10)

        self.master.Username_label = Label(self.master, text=self.username_label_text, font=12)
        self.master.Username_label.grid(row=1, column=0, padx=10, pady=10)

        self.master.Username_Entry = Entry(self.master, textvariable=self.username_var2)
        self.master.Username_Entry.grid(row=1, column=1, padx=10, pady=10)

        self.master.Password_label = Label(self.master, text=self.password_label_text, font=12)
        self.master.Password_label.grid(row=2, column=0, padx=10, pady=10)

        self.master.Password_Entry = Entry(self.master, textvariable=self.password_var2, show='*')
        self.master.Password_Entry.grid(row=2, column=1, padx=10, pady=10)

        self.master.Sign_Up_button = Button(self.master, text=self.sign_up_button_text, width=7, command=self.signup)
        self.master.Sign_Up_button.grid(row=3, column=1, padx=10, pady=10)


    def signup(self):
        # function for taking input and checks

        self.username = self.username_var2.get()
        self.password = self.password_var2.get()
        values = (self.username, self.password)

        data2 = self.username_var2.get()
        if self.username_var2.get() == "":
            messagebox.showinfo("Alert!", "You must enter a username first!")
        elif self.password_var2.get() == "":
            messagebox.showinfo("Alert!", "You must enter a password first!")
        else:
            self.database_connection = DatabaseConnector().get_conn()
            self.cursor = self.database_connection.cursor()

            try:

                query = "SELECT * FROM user_login_info WHERE username=%(username)s"
                self.cursor.execute(query, {'username': self.username})
                self.check = self.cursor.fetchone()
            except:
                self.check= False

            if self.check:
                messagebox.showinfo("Alert", "Already have a user with this username!")
            else:

                try:
                    self.cursor.execute("INSERT INTO user_login_info (username, password) VALUES (%s, %s)", values)
                    self.database_connection.commit()

                except:
                    self.database_connection.rollback()
                messagebox.showinfo("Message", "You signed up successfully!")

                self.master.withdraw()
                self.newWindow = Toplevel(self.master)
                self.app = LogInPage(self.newWindow)




def main():
    # main method
    window = Tk()
    app = OpeningPage(window)
    window.mainloop()


if __name__ == '__main__':
    main()
