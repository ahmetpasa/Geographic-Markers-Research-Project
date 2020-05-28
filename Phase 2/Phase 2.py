import codecs
import csv
from tkinter import *
from tkinter import messagebox
import pymysql
import cfscrape
from bs4 import BeautifulSoup
import pandas as pd
import threading
import geograpy
import universities


# new library for defining geography
# mysqldb connector changed due to its problematic nature, pymysql is now used


class DatabaseConnector:
    # connecting to mysql
    # new online database hoster used for better performance
    def __init__(self):
        self.host = "remotemysql.com"
        self.port = 3306
        self.name = "0nuRjoWBcJ"
        self.user = "0nuRjoWBcJ"
        self.password = "kM1idJBY20"
        self.conn = None

    def get_conn(self):
        if self.conn is None:
            self.conn = pymysql.connect(host=self.host,
                                        port=self.port,
                                        db=self.name,
                                        user=self.user,
                                        passwd=self.password)
        return self.conn


class OpeningPage:
    # Class for the Opening frame
    def __init__(self, master):

        self.master = master

        self.master.title('Geographic Markers Research Project')

        self.master.logo = PhotoImage(file='Journal logo.gif')

        self.master.explanation_text = '''Geographic Markers Research Project is a project led by Dr. Murat Ergin, Sevil Togay, and Didar 
        Tutan from the Comparative History and Society department at Koç University. The main 
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

        self.master.geometry("300x250")

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
        self.username_variable_Lp = self.username_var.get()
        data = (
            self.username_var.get(),
            self.password_var.get()
        )
        if self.username_var.get() == "":
            messagebox.showinfo("Alert!", "You must insert username first!")
        elif self.password_var.get() == "":
            messagebox.showinfo("Alert!", "You must insert password first!")
        else:

            self.database_connection = DatabaseConnector().get_conn()
            self.cursor = self.database_connection.cursor()

            try:
                self.cursor.execute("SELECT * FROM user_login_info WHERE username=%s AND password=%s", data)
                self.result = self.cursor.fetchone()
            except:
                self.result = False
            if self.result:
                self.master.withdraw()
                self.newWindow = Toplevel(self.master)
                self.app = MainPage(self.newWindow, self.username_variable_Lp)
            else:
                messagebox.showinfo("Alert", "Wrong username or password!")

            self.database_connection.close()
            self.cursor.close()


class SignUpPage:
    # Class for the Sign Up page
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)

        self.master.geometry("300x250")

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
                self.check = False

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

            self.database_connection.close()
            self.cursor.close()


class MainPage:

    def Fetch_Variable_8(self, active, before_year, after_year):
        # Fetching variable 8

        # Values to be inserted into the file are stored here
        self.variable_8 = []

        # Defining the geographic coverage
        self.geography_coverage = ['UK', 'United Kingdom', 'England', 'Britain']

        self.file = self.csv_title + '.csv'

        self.update_index = 0

        self.update_file = pd.read_csv(self.file)

        # Defining the supranationals

        self.supranationals = ['EU', 'European Union', 'NATO', 'North Atlantic Treaty Organization',
                               'North American Free Trade Agreement', 'NAFTA', 'UN',
                               'United Nations', 'Arab League', 'OECD',
                               'Organisation for Economic Co-operation and Development', 'OPEC', 'Islamic Cooperation',
                               'ASEAN', 'Association of Southeast Asian Nations', 'SAARC',
                               'South Asian Association for Regional Cooperation', 'African Union']

        if active is True:
            self.database_connection = DatabaseConnector().get_conn()
            self.cursor = self.database_connection.cursor()

            self.query = 'SELECT MAX(id) FROM queries WHERE user_id = %s'
            self.values = self.user_id
            self.cursor.execute(self.query, self.values)
            self.max_id = self.cursor.fetchone()

            self.query = 'UPDATE queries SET variable_8 = %s WHERE id = %s'
            self.values = ("variable 8", self.max_id[0])
            self.cursor.execute(self.query, self.values)

            self.database_connection.commit()
            self.database_connection.close()
            self.cursor.close()

            for i in range(before_year, after_year - 1, -1):

                self.html_source = self.scraper.get(self.british_journal_url + str(i)).text
                self.soup = BeautifulSoup(self.html_source, 'lxml')

                for self.journal in self.soup.findAll('li', class_='card clearfix'):

                    self.issue_url = 'https://onlinelibrary.wiley.com' + self.journal.find('a')['href']
                    self.issue_and_volume_info = self.journal.find('a', class_='visitable').text

                    self.html_source_2 = self.scraper_2.get(self.issue_url).text
                    self.article_soup = BeautifulSoup(self.html_source_2, 'lxml')

                    for self.articles in self.article_soup.findAll('div',
                                                                   class_='card issue-items-container exportCitationWrapper'):
                        if not self.articles.find('h3'):
                            for self.article_order_in_issue in self.articles.findAll('a',
                                                                                     class_='issue-item__title visitable'):
                                if any(self.word in self.article_order_in_issue.h2.text for self.word in
                                       self.articles_we_wont_scrape):
                                    pass
                                else:

                                    try:
                                        self.abstract_scrape = self.article_order_in_issue.find_next_sibling('div',
                                                                                                             class_='content-item-format-links')

                                        self.abstract_scrape_2 = self.abstract_scrape.find('a', title='Abstract')[
                                            'href']
                                        self.title_of_article = self.article_order_in_issue.h2.text

                                        self.places = geograpy.get_place_context(text=self.title_of_article)

                                        # Defining the conditions for coding

                                        if len(self.places.country_mentions) > 0 and self.places.country_mentions[0][
                                            0] in self.supranationals:
                                            self.variable_8.append('7')
                                        elif len(self.places.country_mentions) == 1:
                                            if self.places.country_mentions[0][0] in self.geography_coverage:
                                                self.variable_8.append('3')
                                            else:
                                                self.variable_8.append('4')
                                        elif len(self.places.country_mentions) < 3 and (
                                                len(self.places.city_mentions) > 0 or len(
                                            self.places.region_mentions) > 0):
                                            if len(self.places.city_mentions) == 1 or len(
                                                    self.places.region_mentions) == 1:
                                                self.variable_8.append('1')
                                            else:
                                                self.variable_8.append('2')
                                        elif len(self.places.country_mentions) >= 3:
                                            self.variable_8.append('5')
                                        elif len(self.places.country_mentions) == 0 and len(
                                                self.places.city_mentions) == 0 and len(
                                            self.places.region_mentions) == 0:
                                            self.variable_8.append('0')
                                        else:
                                            self.variable_8.append('6')
                                    except:
                                        pass

                        else:
                            if any(self.word in self.articles.h3.text for self.word in self.articles_we_wont_scrape):
                                pass
                            else:
                                for self.article_order_in_issue in self.articles.findAll('a',
                                                                                         class_='issue-item__title visitable'):
                                    if any(self.word in self.article_order_in_issue.h2.text for self.word in
                                           self.articles_we_wont_scrape):
                                        pass
                                    else:

                                        try:
                                            self.abstract_scrape = self.article_order_in_issue.find_next_sibling('div',
                                                                                                                 class_='content-item-format-links')

                                            self.abstract_scrape_2 = self.abstract_scrape.find('a', title='Abstract')[
                                                'href']

                                            self.title_of_article = self.article_order_in_issue.h2.text

                                            self.places = geograpy.get_place_context(text=self.title_of_article)

                                            # Defining the conditions for coding

                                            if len(self.places.country_mentions) > 0 and \
                                                    self.places.country_mentions[0][0] in self.supranationals:
                                                self.variable_8.append('7')
                                            elif len(self.places.country_mentions) == 1:
                                                if self.places.country_mentions[0][0] in self.geography_coverage:
                                                    self.variable_8.append('3')
                                                else:
                                                    self.variable_8.append('4')
                                            elif len(self.places.country_mentions) < 3 and (
                                                    len(self.places.city_mentions) > 0 or len(
                                                self.places.region_mentions) > 0):
                                                if len(self.places.city_mentions) == 1 or len(
                                                        self.places.region_mentions) == 1:
                                                    self.variable_8.append('1')
                                                else:
                                                    self.variable_8.append('2')
                                            elif len(self.places.country_mentions) >= 3:
                                                self.variable_8.append('5')
                                            elif len(self.places.country_mentions) == 0 and len(
                                                    self.places.city_mentions) == 0 and len(
                                                self.places.region_mentions) == 0:
                                                self.variable_8.append('0')
                                            else:
                                                self.variable_8.append('6')
                                        except:
                                            pass

            # Inserting the values into the file
            self.update_file['Variable 8'] = self.variable_8

            self.update_file.to_csv(self.file, index=False)

            self.update_file.to_excel(self.csv_title + '_excel_format_' + '.xlsx', index=None, header=True)



        else:
            pass

    def Fetch_Variable_9(self, active, before_year, after_year):
        self.variable_9 = []  # Values are recorded in this list
        self.file = self.csv_title + '.csv'

        self.update_index = 0

        self.update_file = pd.read_csv(self.file)

        if active is True:
            self.database_connection = DatabaseConnector().get_conn()
            self.cursor = self.database_connection.cursor()

            self.query = 'SELECT MAX(id) FROM queries WHERE user_id = %s'
            self.values = self.user_id
            self.cursor.execute(self.query, self.values)
            self.max_id = self.cursor.fetchone()

            self.query = 'UPDATE queries SET variable_9 = %s WHERE id = %s'
            self.values = ("variable 9", self.max_id[0])
            self.cursor.execute(self.query, self.values)

            self.database_connection.commit()
            self.database_connection.close()
            self.cursor.close()

            for i in range(before_year, after_year - 1, -1):

                self.html_source = self.scraper.get(self.british_journal_url + str(i)).text
                self.soup = BeautifulSoup(self.html_source, 'lxml')

                for self.journal in self.soup.findAll('li', class_='card clearfix'):

                    self.issue_url = 'https://onlinelibrary.wiley.com' + self.journal.find('a')['href']
                    self.issue_and_volume_info = self.journal.find('a', class_='visitable').text

                    self.html_source_2 = self.scraper_2.get(self.issue_url).text
                    self.article_soup = BeautifulSoup(self.html_source_2, 'lxml')

                    for self.articles in self.article_soup.findAll('div',
                                                                   class_='card issue-items-container exportCitationWrapper'):
                        if not self.articles.find('h3'):
                            for self.article_order_in_issue in self.articles.findAll('a',
                                                                                     class_='issue-item__title visitable'):
                                if any(self.word in self.article_order_in_issue.h2.text for self.word in
                                       self.articles_we_wont_scrape):
                                    pass
                                else:
                                    try:
                                        self.abstract_scrape = self.article_order_in_issue.find_next_sibling('div',
                                                                                                             class_='content-item-format-links')

                                        self.abstract_scrape_2 = self.abstract_scrape.find('a', title='Abstract')[
                                            'href']

                                        self.title_of_article = self.article_order_in_issue.h2.text

                                        # All titles are coded in here
                                        # If we see an interval, we can say easily that includes year
                                        # but also for extreme cases(ex. 3-5) it's coded as 4 digit nums

                                        match = re.search(r'.*([1-3][0-9]{3})(-|–).*([1-3][0-9]{3})',
                                                          self.title_of_article)

                                        # if there's no interval, we search the year, coding philosophy is the same

                                        match2 = re.search(r'.*([1-3][0-9]{3})', self.title_of_article)

                                        # Then we search "century" phrase but for all cases we search "th century"
                                        # Uppercase cases are also included

                                        match3 = re.search(
                                            r'(rd|st|nd|th) \bCentur[a-z]*\b|(rd|st|nd|th) \bcentur[a-z]*\b',
                                            self.title_of_article)

                                        # If there is a year or century phrase, this is enough for code as '1'

                                        if match is not None:
                                            self.variable_9.append('1')
                                        elif match2 is not None:
                                            self.variable_9.append('1')
                                        elif match3 is not None:
                                            self.variable_9.append('1')
                                        else:
                                            self.variable_9.append('0')
                                    except:
                                        pass
                        else:
                            if any(self.word in self.articles.h3.text for self.word in self.articles_we_wont_scrape):
                                pass
                            else:
                                for self.article_order_in_issue in self.articles.findAll('a',
                                                                                         class_='issue-item__title visitable'):
                                    if any(self.word in self.article_order_in_issue.h2.text for self.word in
                                           self.articles_we_wont_scrape):
                                        pass
                                    else:
                                        try:
                                            self.abstract_scrape = self.article_order_in_issue.find_next_sibling('div',
                                                                                                                 class_='content-item-format-links')

                                            self.abstract_scrape_2 = self.abstract_scrape.find('a', title='Abstract')[
                                                'href']

                                            self.title_of_article = self.article_order_in_issue.h2.text

                                            # Same approach as upper lines

                                            match = re.search(r'.*([1-3][0-9]{3})(-|–).*([1-3][0-9]{3})',
                                                              self.title_of_article)
                                            match2 = re.search(r'.*([1-3][0-9]{3})', self.title_of_article)
                                            match3 = re.search(
                                                r'(rd|st|nd|th) \bCentur[a-z]*\b|(rd|st|nd|th) \bcentur[a-z]*\b',
                                                self.title_of_article)
                                            if match is not None:
                                                self.variable_9.append('1')
                                            elif match2 is not None:
                                                self.variable_9.append('1')
                                            elif match3 is not None:
                                                self.variable_9.append('1')
                                            else:
                                                self.variable_9.append('0')
                                        except:
                                            pass

            # Inserting the values into the file
            self.update_file['Variable 9'] = self.variable_9

            self.update_file.to_csv(self.file, index=False)

            self.update_file.to_excel(self.csv_title + '_excel_format_' + '.xlsx', index=None, header=True)
        else:
            pass



    def Fetch_Variable_10(self, active, before_year, after_year):
        # Fetching variable 10

        # Values to be inserted into the file are stored here
        self.variable_10 = []

        # Defining the geographic coverage
        self.geography_coverage = ['UK', 'United Kingdom', 'England', 'Britain']

        self.file = self.csv_title + '.csv'

        self.update_index = 0

        self.update_file = pd.read_csv(self.file)

        # Defining the supranationals

        self.supranationals = ['EU', 'European Union', 'NATO', 'North Atlantic Treaty Organization',
                               'North American Free Trade Agreement', 'NAFTA', 'UN',
                               'United Nations', 'Arab League', 'OECD',
                               'Organisation for Economic Co-operation and Development', 'OPEC', 'Islamic Cooperation',
                               'ASEAN', 'Association of Southeast Asian Nations', 'SAARC',
                               'South Asian Association for Regional Cooperation', 'African Union']

        if active is True:
            self.database_connection = DatabaseConnector().get_conn()
            self.cursor = self.database_connection.cursor()

            self.query = 'SELECT MAX(id) FROM queries WHERE user_id = %s'
            self.values = self.user_id
            self.cursor.execute(self.query, self.values)
            self.max_id = self.cursor.fetchone()

            self.query = 'UPDATE queries SET variable_10 = %s WHERE id = %s'
            self.values = ("variable 10", self.max_id[0])
            self.cursor.execute(self.query, self.values)

            self.database_connection.commit()
            self.database_connection.close()
            self.cursor.close()

            for i in range(before_year, after_year - 1, -1):

                self.html_source = self.scraper.get(self.british_journal_url + str(i)).text
                self.soup = BeautifulSoup(self.html_source, 'lxml')

                for self.journal in self.soup.findAll('li', class_='card clearfix'):

                    self.issue_url = 'https://onlinelibrary.wiley.com' + self.journal.find('a')['href']
                    self.issue_and_volume_info = self.journal.find('a', class_='visitable').text

                    self.html_source_2 = self.scraper_2.get(self.issue_url).text
                    self.article_soup = BeautifulSoup(self.html_source_2, 'lxml')

                    for self.articles in self.article_soup.findAll('div',
                                                                   class_='card issue-items-container exportCitationWrapper'):
                        if not self.articles.find('h3'):
                            for self.article_order_in_issue in self.articles.findAll('a',
                                                                                     class_='issue-item__title visitable'):
                                if any(self.word in self.article_order_in_issue.h2.text for self.word in
                                       self.articles_we_wont_scrape):
                                    pass
                                else:

                                    try:
                                        self.abstract_scrape = self.article_order_in_issue.find_next_sibling('div',
                                                                                                             class_='content-item-format-links')

                                        self.abstract_scrape_2 = self.abstract_scrape.find('a', title='Abstract')[
                                            'href']

                                        self.abstract_url = 'https://onlinelibrary.wiley.com' + self.abstract_scrape_2

                                        self.abstract_html_source = self.scraper.get(self.abstract_url).text
                                        self.abstract_soup = BeautifulSoup(self.abstract_html_source, 'lxml')

                                        self.article_abstract = self.abstract_soup.find('div',
                                                                                        class_='article-section__content en main').p.text

                                        self.places = geograpy.get_place_context(text=self.article_abstract)

                                        # Defining the conditions for coding

                                        if len(self.places.country_mentions) > 0 and self.places.country_mentions[0][
                                            0] in self.supranationals:
                                            self.variable_10.append('7')
                                        elif len(self.places.country_mentions) == 1:
                                            if self.places.country_mentions[0][0] in self.geography_coverage:
                                                self.variable_10.append('3')
                                            else:
                                                self.variable_10.append('4')
                                        elif len(self.places.country_mentions) < 3 and (
                                                len(self.places.city_mentions) > 0 or len(
                                                self.places.region_mentions) > 0):
                                            if len(self.places.city_mentions) == 1 or len(
                                                    self.places.region_mentions) == 1:
                                                self.variable_10.append('1')
                                            else:
                                                self.variable_10.append('2')
                                        elif len(self.places.country_mentions) >= 3:
                                            self.variable_10.append('5')
                                        elif len(self.places.country_mentions) == 0 and len(
                                                self.places.city_mentions) == 0 and len(
                                            self.places.region_mentions) == 0:
                                            self.variable_10.append('0')
                                        else:
                                            self.variable_10.append('6')
                                    except:
                                        pass

                        else:
                            if any(self.word in self.articles.h3.text for self.word in self.articles_we_wont_scrape):
                                pass
                            else:
                                for self.article_order_in_issue in self.articles.findAll('a',
                                                                                         class_='issue-item__title visitable'):
                                    if any(self.word in self.article_order_in_issue.h2.text for self.word in
                                           self.articles_we_wont_scrape):
                                        pass
                                    else:

                                        try:
                                            self.abstract_scrape = self.article_order_in_issue.find_next_sibling('div',
                                                                                                                 class_='content-item-format-links')

                                            self.abstract_scrape_2 = self.abstract_scrape.find('a', title='Abstract')[
                                                'href']

                                            self.abstract_url = 'https://onlinelibrary.wiley.com' + self.abstract_scrape_2

                                            self.abstract_html_source = self.scraper.get(self.abstract_url).text
                                            self.abstract_soup = BeautifulSoup(self.abstract_html_source, 'lxml')

                                            self.article_abstract = self.abstract_soup.find('div',
                                                                                            class_='article-section__content en main').p.text

                                            self.places = geograpy.get_place_context(text=self.article_abstract)

                                            # Defining the conditions for coding

                                            if len(self.places.country_mentions) > 0 and \
                                                    self.places.country_mentions[0][0] in self.supranationals:
                                                self.variable_10.append('7')
                                            elif len(self.places.country_mentions) == 1:
                                                if self.places.country_mentions[0][0] in self.geography_coverage:
                                                    self.variable_10.append('3')
                                                else:
                                                    self.variable_10.append('4')
                                            elif len(self.places.country_mentions) < 3 and (
                                                    len(self.places.city_mentions) > 0 or len(
                                                    self.places.region_mentions) > 0):
                                                if len(self.places.city_mentions) == 1 or len(
                                                        self.places.region_mentions) == 1:
                                                    self.variable_10.append('1')
                                                else:
                                                    self.variable_10.append('2')
                                            elif len(self.places.country_mentions) >= 3:
                                                self.variable_10.append('5')
                                            elif len(self.places.country_mentions) == 0 and len(
                                                    self.places.city_mentions) == 0 and len(
                                                self.places.region_mentions) == 0:
                                                self.variable_10.append('0')
                                            else:
                                                self.variable_10.append('6')
                                        except:
                                            pass

            # Inserting the values into the file
            self.update_file['Variable 10'] = self.variable_10

            self.update_file.to_csv(self.file, index=False)

            self.update_file.to_excel(self.csv_title + '_excel_format_' + '.xlsx', index=None, header=True)



        else:
            pass

    def Fetch_Variable_11(self, active, before_year, after_year):
        # Fetching variable 11

        # Values to be inserted into the file are stored here
        self.variable_11 = []


        # Storing the data section texts

        self.datatexts = []


        # Defining the data section keywords
        self.data_section_keywords = ['Method', 'method', 'conduct', 'Data', 'data', 'case studies', 'Case studies', 'Methodological background']

        self.file = self.csv_title + '.csv'

        self.update_file = pd.read_csv(self.file)

        # Defining the supranationals

        self.supranationals = ['EU', 'European Union', 'NATO', 'North Atlantic Treaty Organization',
                               'North American Free Trade Agreement', 'NAFTA', 'UN',
                               'United Nations', 'Arab League', 'OECD',
                               'Organisation for Economic Co-operation and Development', 'OPEC', 'Islamic Cooperation',
                               'ASEAN', 'Association of Southeast Asian Nations', 'SAARC',
                               'South Asian Association for Regional Cooperation', 'African Union']

        if active is True:
            self.database_connection = DatabaseConnector().get_conn()
            self.cursor = self.database_connection.cursor()

            self.query = 'SELECT MAX(id) FROM queries WHERE user_id = %s'
            self.values = self.user_id
            self.cursor.execute(self.query, self.values)
            self.max_id = self.cursor.fetchone()

            self.query = 'UPDATE queries SET variable_11 = %s WHERE id = %s'
            self.values = ("variable 11", self.max_id[0])
            self.cursor.execute(self.query, self.values)

            self.database_connection.commit()
            self.database_connection.close()
            self.cursor.close()

            for i in range(before_year, after_year - 1, -1):

                self.html_source = self.scraper.get(self.british_journal_url + str(i)).text
                self.soup = BeautifulSoup(self.html_source, 'lxml')

                for self.journal in self.soup.findAll('li', class_='card clearfix'):

                    self.issue_url = 'https://onlinelibrary.wiley.com' + self.journal.find('a')['href']
                    self.issue_and_volume_info = self.journal.find('a', class_='visitable').text

                    self.html_source_2 = self.scraper_2.get(self.issue_url).text
                    self.article_soup = BeautifulSoup(self.html_source_2, 'lxml')

                    for self.articles in self.article_soup.findAll('div',
                                                                   class_='card issue-items-container exportCitationWrapper'):
                        if not self.articles.find('h3'):
                            for self.article_order_in_issue in self.articles.findAll('a',
                                                                                     class_='issue-item__title visitable'):
                                if any(self.word in self.article_order_in_issue.h2.text for self.word in
                                       self.articles_we_wont_scrape):
                                    pass
                                else:

                                    try:

                                        self.abstract_scrape = self.article_order_in_issue.find_next_sibling('div',
                                                                                                             class_='content-item-format-links')

                                        self.abstract_scrape_2 = self.abstract_scrape.find('a', title='Abstract')[
                                            'href']

                                        self.full_text_title = '''
                                        Full text
                                    '''

                                        if not self.abstract_scrape.find('a', title=self.full_text_title):

                                            # Defining articles without aa text form for full text as N/A

                                            self.variable_11.append('N\A')
                                        else:

                                            self.full_text_scrape = \
                                            self.abstract_scrape.find('a', title=self.full_text_title)['href']

                                            self.full_text_url = 'https://onlinelibrary.wiley.com' + self.full_text_scrape

                                            # Fetching data section from Full Text

                                            self.full_text_html_source = self.scraper.get(self.full_text_url).text

                                            self.full_text_soup = BeautifulSoup(self.full_text_html_source, 'lxml')

                                            self.full_text = self.full_text_soup.findAll('section',
                                                                                         class_='article-section__content')

                                            for self.data_sections_text in self.full_text:
                                                for self.data_section_to_scrape in self.data_sections_text.findAll('h2',
                                                                                                                   class_='article-section__title section__title section1'):
                                                    for self.data in self.data_section_keywords:
                                                        if self.data in self.data_section_to_scrape.text:
                                                            for self.data_text in self.data_sections_text.findAll('p'):
                                                                self.datatexts.append(self.data_text.text)

                                            # Turning entire Data Section into one String to be analyzed

                                            if len(self.datatexts) > 0:
                                                self.data_section_string = ''.join(self.datatexts)

                                                self.places = geograpy.get_place_context(
                                                    text=self.data_section_string)

                                                # Defining the conditions for coding

                                                if len(self.places.country_mentions) > 0:
                                                    for i in range(len(self.places.country_mentions)):
                                                        if self.places.country_mentions[i][0] in self.supranationals:
                                                            self.variable_11.append('7')
                                                            self.data_section_string = ''
                                                            self.datatexts = []
                                                            break
                                                        elif self.places.country_mentions[i][
                                                            0] in self.geography_coverage:
                                                            self.variable_11.append('3')
                                                            self.data_section_string = ''
                                                            self.datatexts = []
                                                            break
                                                        else:
                                                            self.variable_11.append('4')
                                                            self.data_section_string = ''
                                                            self.datatexts = []
                                                            break
                                                elif len(self.places.country_mentions) == 0 and len(
                                                        self.places.city_mentions) == 0 and len(
                                                    self.places.region_mentions) == 0:
                                                    self.variable_11.append('0')
                                                    self.data_section_string = ''
                                                    self.datatexts = []

                                                elif len(self.places.city_mentions) > 0 or len(
                                                        self.places.region_mentions) > 0:
                                                    if len(self.places.city_mentions) == 1 or len(
                                                            self.places.region_mentions) == 1:
                                                        self.variable_11.append('1')
                                                        self.data_section_string = ''
                                                        self.datatexts = []
                                                    else:
                                                        self.variable_11.append('2')
                                                        self.data_section_string = ''
                                                        self.datatexts = []
                                                else:
                                                    self.variable_11.append('5')
                                                    self.data_section_string = ''
                                                    self.datatexts = []

                                            else:
                                                self.variable_11.append('N\A')
                                                self.data_section_string = ''
                                                self.datatexts = []

                                    except:
                                        pass

                        else:
                            if any(self.word in self.articles.h3.text for self.word in self.articles_we_wont_scrape):
                                pass
                            else:
                                for self.article_order_in_issue in self.articles.findAll('a',
                                                                                         class_='issue-item__title visitable'):
                                    if any(self.word in self.article_order_in_issue.h2.text for self.word in
                                           self.articles_we_wont_scrape):
                                        pass
                                    else:

                                        try:

                                                self.abstract_scrape = self.article_order_in_issue.find_next_sibling('div',
                                                                                                                     class_='content-item-format-links')

                                                self.abstract_scrape_2 = self.abstract_scrape.find('a', title='Abstract')[
                                                    'href']

                                                self.full_text_title ='''
            Full text
        '''

                                                if not self.abstract_scrape.find('a', title=self.full_text_title):
                                                    # Articles without Full text in text form are coded as N\A
                                                    self.variable_11.append('N\A')
                                                else:

                                                    # Fetching data section from Full Text

                                                    self.full_text_scrape = self.abstract_scrape.find('a', title=self.full_text_title)['href']

                                                    self.full_text_url = 'https://onlinelibrary.wiley.com' + self.full_text_scrape

                                                    self.full_text_html_source = self.scraper.get(self.full_text_url).text

                                                    self.full_text_soup = BeautifulSoup(self.full_text_html_source, 'lxml')



                                                    self.full_text = self.full_text_soup.findAll('section',
                                                                                                 class_='article-section__content')

                                                    for self.data_sections_text in self.full_text:
                                                        for self.data_section_to_scrape in self.data_sections_text.findAll('h2',
                                                                                                                           class_='article-section__title section__title section1'):
                                                            for self.data in self.data_section_keywords:
                                                                if self.data in self.data_section_to_scrape.text:
                                                                    for self.data_text in self.data_sections_text.findAll('p'):
                                                                        self.datatexts.append(self.data_text.text)



                                                    if len(self.datatexts) > 0:
                                                        # Turning entire Data Section into one String to be analyzed
                                                        self.data_section_string = ''.join(self.datatexts)

                                                        self.places = geograpy.get_place_context(
                                                            text=self.data_section_string)

                                                        # Defining the conditions for coding

                                                        if len(self.places.country_mentions) > 0:
                                                            for i in range(len(self.places.country_mentions)):
                                                                if self.places.country_mentions[i][0] in self.supranationals:
                                                                    self.variable_11.append('7')
                                                                    self.data_section_string = ''
                                                                    self.datatexts = []
                                                                    break
                                                                elif self.places.country_mentions[i][0] in self.geography_coverage:
                                                                    self.variable_11.append('3')
                                                                    self.data_section_string = ''
                                                                    self.datatexts = []
                                                                    break
                                                                else:
                                                                    self.variable_11.append('4')
                                                                    self.data_section_string = ''
                                                                    self.datatexts = []
                                                                    break
                                                        elif len(self.places.country_mentions) == 0 and len(
                                                                self.places.city_mentions) == 0 and len(
                                                            self.places.region_mentions) == 0:
                                                            self.variable_11.append('0')
                                                            self.data_section_string = ''
                                                            self.datatexts = []

                                                        elif len(self.places.city_mentions) > 0 or len(self.places.region_mentions) > 0:
                                                            if len(self.places.city_mentions) == 1 or len(self.places.region_mentions) == 1:
                                                                    self.variable_11.append('1')
                                                                    self.data_section_string = ''
                                                                    self.datatexts = []
                                                            else:
                                                                self.variable_11.append('2')
                                                                self.data_section_string = ''
                                                                self.datatexts = []
                                                        else:
                                                            self.variable_11.append('5')
                                                            self.data_section_string = ''
                                                            self.datatexts = []



                                                    else:
                                                        self.variable_11.append('N\A')
                                                        self.data_section_string = ''
                                                        self.datatexts = []

                                        except:
                                            pass





            # Inserting the values into the file
            self.update_file['Variable 11'] = self.variable_11



            self.update_file.to_csv(self.file, index=False)

            self.update_file.to_excel(self.csv_title + '_excel_format_' + '.xlsx', index=None, header=True)

        else:
            pass

    def Fetch_Variable_12(self, active, before_year, after_year):
        self.variable_12 = []
        self.uk = ['Lancaster University', 'University of Missouri‐St Louis',
                   'Durham University', 'Oxford University', 'Sociology Department University of Manchester',
                   'Ludwig‐Maximilian University and London School of Economics and Politial Science',
                   'Department of Sociology University of Lancaster', 'London South Bank University.',
                   'London School of Economcis and Political Science', 'Department of Sociology Lancaster University'
                   'Darwin College University of Kent', 'Bangor University', 'Buckinghamshire Chilterns University College',
                   'Cardiff University Business School', 'Cardiff University School of Social Sciences'
                   'Department of Sociology University of Manchester', 'Department of Sociology University of Surrey'] # this schools are not recognized by python university library
       
        self.file = self.csv_title + '.csv'
        self.update_file = pd.read_csv(self.file)
        self.update_index = 0
        
        if active is True:
            self.database_connection = DatabaseConnector().get_conn()
            self.cursor = self.database_connection.cursor()

            self.query = 'SELECT MAX(id) FROM queries WHERE user_id = %s'
            self.values = self.user_id
            self.cursor.execute(self.query, self.values)
            self.max_id = self.cursor.fetchone()

            self.query = 'UPDATE queries SET variable_12 = %s WHERE id = %s'
            self.values = ("variable 12", self.max_id[0])
            self.cursor.execute(self.query, self.values)

            self.database_connection.commit()
            self.database_connection.close()
            self.cursor.close()
            
            for i in range(before_year, after_year - 1, -1):
 
                 self.html_source = self.scraper.get(self.british_journal_url + str(i)).text
                 self.soup = BeautifulSoup(self.html_source, 'lxml')
 
                 for self.journal in self.soup.findAll('li', class_='card clearfix'):
 
                     self.issue_url = 'https://onlinelibrary.wiley.com' + self.journal.find('a')['href']
                     self.issue_and_volume_info = self.journal.find('a', class_='visitable').text
 
 
                     self.html_source_2 = self.scraper_2.get(self.issue_url).text
                     self.article_soup = BeautifulSoup(self.html_source_2, 'lxml')
                     
                     
                     
                     for self.articles in self.article_soup.findAll('div',class_='card issue-items-container exportCitationWrapper'):
                         if not self.articles.find('h3'):
                             for self.article_order_in_issue in self.articles.findAll('a',class_='issue-item__title visitable'):
                                 if any(self.word in self.article_order_in_issue.h2.text for self.word in self.articles_we_wont_scrape):
                                     pass
                                 else:
                                     try:
                                         
                                         
                                         self.abstract_scrape = self.article_order_in_issue.find_next_sibling('div',class_='content-item-format-links')

                                         self.abstract_scrape_2 = self.abstract_scrape.find('a', title='Abstract')['href']
                                        
                                         if (self.abstract_scrape_2):
                                             
                                        
                                             self.link = self.article_order_in_issue.get('href')
                                             
                                             self.var12_url = 'https://onlinelibrary.wiley.com' + self.link
                                             
                                             variable12 = Variable12(self.var12_url) # new object is created
                                           
                                             if (variable12.country == None):
                                                 
                                                                                                                                                       
                                                 if variable12.tempName in self.uk: 
                    
                                                    self.variable_12.append('United Kingdom')
                                                
                                                 else:
                                                     
                                                     self.variable_12.append(variable12.tempName)
                                                     
                                                 
                                             else:
                                                 self.variable_12.append(variable12.country)
                                                 

                                     except:
                                         pass
                                         
                                     
                        
                        
                         else:
                             
                             if any(self.word in self.articles.h3.text for self.word in self.articles_we_wont_scrape):
                                 pass
                             else:
                                 for self.article_order_in_issue in self.articles.findAll('a',class_='issue-item__title visitable'):
                                     if any(self.word in self.article_order_in_issue.h2.text for self.word in
                                            self.articles_we_wont_scrape):
                                         pass
                                     else:
                                         
                                         try:
                                             
                                             self.abstract_scrape = self.article_order_in_issue.find_next_sibling('div',class_='content-item-format-links')

                                             self.abstract_scrape_2 = self.abstract_scrape.find('a', title='Abstract')['href']
                                             
                                             if (self.abstract_scrape_2):
                                                                                              
                                                 self.link = self.article_order_in_issue.get('href')
                                                 
                                                 self.var12_url = 'https://onlinelibrary.wiley.com' + self.link
                                                 
                                                 variable12 = Variable12(self.var12_url) # new object is created
                                                 
                                                 if (variable12.country == None):
                                                     
                                                     if variable12.tempName in self.uk: 
                    
                                                         self.variable_12.append('United Kingdom')
                                                
                                                     else:
                                                         
                                                         self.variable_12.append(variable12.tempName)
                                                         
                                                 
                                                 else:
                                                     self.variable_12.append(variable12.country)
                                                                                               
                                          
                                         except:
                                             pass
                     
            self.update_file['Variable 12'] = self.variable_12 # 

            self.update_file.to_csv(self.file, index=False)

            self.update_file.to_excel(self.csv_title + '_excel_format_' + '.xlsx', index=None, header=True)

        else:
            pass        
        
    def isSpecialIssue(self, row):
        # Defining if a row is part of a special issue
        try:
            if 's' in row['Issue']:
                self.value = 1
            elif 'S' in row['Issue']:
                self.value = 1
            else:
                self.value = 0
        except:
            self.value = 0
        return self.value

    def Fetch_Variable_13(self, active):

        # Fetching Variable 13

        if active is True:

            self.database_connection = DatabaseConnector().get_conn()
            self.cursor = self.database_connection.cursor()

            self.query = 'SELECT MAX(id) FROM queries WHERE user_id = %s'
            self.values = self.user_id
            self.cursor.execute(self.query, self.values)
            self.max_id = self.cursor.fetchone()

            self.query = 'UPDATE queries SET variable_13 = %s WHERE id = %s'
            self.values = ("variable 13", self.max_id[0])
            self.cursor.execute(self.query, self.values)

            self.database_connection.commit()

            self.database_connection.close()
            self.cursor.close()

            self.file = self.csv_title + '.csv'

            self.update_index = 0

            # reading the file to be edited
            self.update_file = pd.read_csv(self.file)

            # writing the results in a new row in the csv and excel files

            self.update_file['Variable 13'] = self.update_file.apply(self.isSpecialIssue, axis=1)

            self.update_file.to_csv(self.file, index=False)

            self.update_file.to_excel(self.csv_title + '_excel_format_' + '.xlsx', index=None, header=True)

        else:
            pass


    def Fetch_Articles(self, before_year, after_year):

        # Fetching article code from phase 1

        self.statusbar = Label(self.master, text="Fetching....", bd=1, relief=SUNKEN, anchor=W)
        self.statusbar.grid(row=10, column=0)

        self.database_connection = DatabaseConnector().get_conn()
        self.cursor = self.database_connection.cursor()

        values = (self.basic_variables,
                  int(self.user_id),
                  int(before_year),
                  int(after_year))

        # inserting the details of the basic variables query to the database
        self.cursor.execute(
            "INSERT INTO queries (basic_variables, user_id, from_year, to_year) VALUES (%s, %s, %s, %s)", values)
        self.database_connection.commit()
        self.database_connection.close()
        self.cursor.close()

        self.before_year = before_year
        self.after_year = after_year
        self.british_journal_url = 'https://onlinelibrary.wiley.com/loi/14684446/year/'
        self.articles_we_wont_scrape = ['COMMENTARY', 'Commentary', 'Commentaries', 'Review', 'Erratum', 'Corrigendum',
                                        'REVIEW',
                                        'Book',
                                        'Notes to contributors', 'Editorial announcement', 'VOLUME INDEX', 'Comments',
                                        '– By', 'Replies', 'Notes to Contributors', 'Issue Information ‐ Toc',
                                        'Reviews', 'reviews',
                                        'Books reviews', '– Edited by', 'Issue Information', 'Editorial',
                                        'Issue Information ‐ TOC',
                                        'Early View', 'Editor', 'commentators', 'Reply']

        self.geography_coverage = ['UK', 'United Kingdom', 'England', 'Britain']

        self.suprantionals = ['EU', 'European Union', 'NATO', 'North Atlantic Treaty Organization',
                              'North American Free Trade Agreement', 'NAFTA', 'UN',
                              'United Nations', 'Arab League', 'OECD',
                              'Organisation for Economic Co-operation and Development', 'OPEC', 'Islamic Cooperation',
                              'ASEAN', 'Association of Southeast Asian Nations', 'SAARC',
                              'South Asian Association for Regional Cooperation', 'African Union']

        self.scraper = cfscrape.create_scraper()
        self.scraper_2 = cfscrape.create_scraper()
        self.html_source = self.scraper.get(self.british_journal_url).text
        self.soup = BeautifulSoup(self.html_source, 'lxml')

        self.journal_title = self.soup.find('span', 'journalTitle').text.split(',')[1].lstrip()  # Variable 1
        self.csv_title = self.journal_title + '_' + str(before_year) + '_' + str(after_year)
        self.csv_file = codecs.open(self.csv_title + '.csv', 'w', encoding='utf-8')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['Journal Title', 'Coverage', 'Year', 'Volume', 'Issue', 'Title of Article',
                                  'Variable 7'])  # Column names are arranged as example

        if self.journal_title in 'The British Journal of Sociology':  # These codes are arranged as codebook
            self.journal_title_code = 6  # it's not coded in codebook so we give 6
        elif self.journal_title in 'American Sociological Review':
            self.journal_title_code = 1
        elif self.journal_title in 'New Perspectives on Turkey':
            self.journal_title_code = 3
        elif self.journal_title in 'European Sociological Review':
            self.journal_title_code = 5
        elif self.journal_title in 'Modern China':
            self.journal_title_code = 4
        elif self.journal_title in 'Social Science Japan Journal':
            self.journal_title_code = 2

        if self.journal_title in 'American Sociological Review' or 'British Journal of Sociology':
            self.geographic_coverage = 2
        elif self.journal_title in 'Gender Society' or 'Social Forces':
            self.geographic_coverage = 1
        elif self.journal_title in 'European Sociological Review':
            self.geographic_coverage = 3
        elif self.journal_title in 'Modern China or New Perspectives on Turkey':
            self.geographic_coverage = 4

        for i in range(before_year, after_year - 1, -1):

            self.html_source = self.scraper.get(self.british_journal_url + str(i)).text
            self.soup = BeautifulSoup(self.html_source, 'lxml')

            for self.journal in self.soup.findAll('li', class_='card clearfix'):

                self.issue_url = 'https://onlinelibrary.wiley.com' + self.journal.find('a')['href']
                self.issue_and_volume_info = self.journal.find('a', class_='visitable').text
                self.issue_and_volume_info = self.issue_and_volume_info.split(" ")
                self.volume_number = self.issue_and_volume_info[1].split(',')[0]
                self.issue_number = self.issue_and_volume_info[3]
                self.year = i

                self.html_source_2 = self.scraper_2.get(self.issue_url).text
                self.article_soup = BeautifulSoup(self.html_source_2, 'lxml')

                self.article_order_counter = 0

                for self.articles in self.article_soup.findAll('div',
                                                               class_='card issue-items-container exportCitationWrapper'):
                    if not self.articles.find('h3'):
                        for self.article_order_in_issue in self.articles.findAll('a',
                                                                                 class_='issue-item__title visitable'):
                            if any(self.word in self.article_order_in_issue.h2.text for self.word in
                                   self.articles_we_wont_scrape):
                                pass
                            else:
                                try:
                                    self.abstract_scrape = self.article_order_in_issue.find_next_sibling('div',
                                                                                                         class_='content-item-format-links')

                                    self.abstract_scrape_2 = self.abstract_scrape.find('a', title='Abstract')['href']

                                    self.article_order_counter = self.article_order_counter + 1

                                    self.title_of_article = self.article_order_in_issue.h2.text

                                    self.csv_writer.writerow(
                                        [self.journal_title_code, self.geographic_coverage, self.year,
                                         self.volume_number, str(self.issue_number),
                                         self.title_of_article, str(self.article_order_counter)])

                                except:
                                    pass
                    else:
                        if any(self.word in self.articles.h3.text for self.word in self.articles_we_wont_scrape):
                            pass
                        else:
                            for self.article_order_in_issue in self.articles.findAll('a',
                                                                                     class_='issue-item__title visitable'):
                                if any(self.word in self.article_order_in_issue.h2.text for self.word in
                                       self.articles_we_wont_scrape):
                                    pass
                                else:

                                    try:
                                        self.abstract_scrape = self.article_order_in_issue.find_next_sibling('div',
                                                                                                             class_='content-item-format-links')

                                        self.abstract_scrape_2 = self.abstract_scrape.find('a', title='Abstract')[
                                            'href']

                                        self.article_order_counter = self.article_order_counter + 1

                                        self.title_of_article = self.article_order_in_issue.h2.text

                                        self.csv_writer.writerow(
                                            [self.journal_title_code, self.geographic_coverage, self.year,
                                             self.volume_number, str(self.issue_number),
                                             self.title_of_article, str(self.article_order_counter)])

                                    except:
                                        pass
        self.csv_file.close()
        self.read_file = pd.read_csv(self.csv_title + '.csv')
        self.read_file.to_excel(self.csv_title + '_excel_format_' + '.xlsx', index=None,
                                header=True)  # Formatting the CSV to XLSX(Excel Table)

        self.Fetch_Variable_8(True, self.before_year, self.after_year)
        self.Fetch_Variable_9(True, self.before_year, self.after_year)
        self.Fetch_Variable_10(True, self.before_year, self.after_year)
        self.Fetch_Variable_11(True, self.before_year, self.after_year)
        self.Fetch_Variable_12(True, self.before_year, self.after_year)        
        self.Fetch_Variable_13(True)
        self.statusbar.destroy()
        messagebox.showinfo('Confirmation', 'Articles Fetched and Saved')

        self.DownloadButton.config(state="disabled")

    # ALLOWING DIGIS ONLY
    def testVal(self, inStr, acttyp):
        if acttyp == '1':  # insert
            if not inStr.isdigit():
                return False
        return True

    def clicked(self):
        global list_data
        list_data = []
        self.listbox.insert(END, self.content.get())
        list_data.append(self.content.get())

    def delete_selected(self):
        global list_data
        selected = self.listbox.get(self.listbox.curselection())
        self.listbox.delete(ANCHOR)
        list_data.pop(list_data.index(selected))

    def __init__(self, master, username):

        self.username_variable = username

        self.database_connection = DatabaseConnector().get_conn()
        self.cursor = self.database_connection.cursor()

        # creating the query to get the id of the current user logged in

        query = "SELECT id FROM user_login_info WHERE username=%(username)s"
        self.cursor.execute(query, {'username': self.username_variable})
        self.check = self.cursor.fetchone()

        result_id = ' '.join([str(x) for x in self.check])

        self.basic_variables = 'basic variables'

        self.user_id = result_id

        self.database_connection.close()
        self.cursor.close()

        self.CheckVar = IntVar()
        self.master = master
        self.frame = Frame(self.master)

        # BROWSE WIDGETS
        self.Box1 = LabelFrame(self.master, text=" Browse ")
        self.Box1.grid(row=3, columnspan=15, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)

        self.BrowseByVariable = Label(self.Box1, text="Browse by variable:")
        self.BrowseByVariable.grid(row=3, column=0, sticky='E', padx=5, pady=2)

        # VariableList

        self.content = StringVar()
        self.BrowseByVariable = Entry(self.Box1, width=40, textvariable=self.content)
        self.BrowseByVariable.grid(row=3, column=1, columnspan=7, sticky="WE", pady=2)

        self.BrowseByVariable = Button(self.Box1, text="Select", command=self.clicked)
        self.BrowseByVariable.grid(row=3, column=8, sticky='W', padx=5, pady=2)

        self.listbox = Listbox(self.Box1)
        self.listbox.grid(row=4, column=1, sticky='w')

        self.BrowseByVariable = Button(self.Box1, text="Remove selected variable", command=self.delete_selected)
        self.BrowseByVariable.grid(row=5, column=1, pady=2, sticky='w')

        # YEAR WIDGETS
        self.Box4 = LabelFrame(self.master, text="Years")
        self.Box4.grid(row=1, columnspan=9, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)

        self.Years = Label(self.Box4, text="From:")
        self.Years.grid(row=1, column=0, sticky='E', padx=5, pady=2)

        self.From_Years = Entry(self.Box4, validate="key")
        self.From_Years['validatecommand'] = (self.Years.register(self.testVal), '%P', '%d')
        self.From_Years.grid(row=1, column=1, columnspan=1, sticky="WE", pady=2)

        self.Years = Label(self.Box4, text="to:")
        self.Years.grid(row=1, column=2, padx=5, pady=2)

        self.To_Years = Entry(self.Box4, validate="key")
        self.To_Years['validatecommand'] = (self.Years.register(self.testVal), '%P', '%d')
        self.To_Years.grid(row=1, column=3, columnspan=1, sticky="WE", pady=2)

        # QUEREY WIDGETS
        self.Box2 = LabelFrame(self.master, text=" Queries ")
        self.Box2.grid(row=0, column=17, columnspan=2, rowspan=2, sticky='NS', padx=5, pady=5)

        self.Queries = Button(self.Box2, text="Recently Executed Queries", command=self.OpenPreviousQueriesPage)
        self.Queries.grid(row=0, padx=5, pady=5)

        # PRESELECTED VARIBALES WIDGETS
        self.Box3 = LabelFrame(self.master, text=" Basic Codebook Variables: ")
        self.Box3.grid(row=3, column=17, columnspan=3, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)

        self.Variable1 = Checkbutton(self.Box3, text="Variable 1", variable=self.CheckVar, state='disabled')
        self.Variable1.select()
        self.Variable1.grid(row=3, column=17, sticky='W', padx=5, pady=2)
        self.Variable1.bind("<Enter>", self.on_enter_variable_1)
        self.Variable1.bind("<Leave>", self.on_leave_variable_1)

        self.Variable2 = Checkbutton(self.Box3, text="Variable 2", variable=self.CheckVar, state='disabled')
        self.Variable2.select()
        self.Variable2.grid(row=4, column=17, sticky='W', padx=5)
        self.Variable2.bind("<Enter>", self.on_enter_variable_2)
        self.Variable2.bind("<Leave>", self.on_leave_variable_2)

        self.Variable3 = Checkbutton(self.Box3, text="Variable 3", variable=self.CheckVar, state='disabled')
        self.Variable3.select()
        self.Variable3.grid(row=5, column=17, sticky='W', padx=5)
        self.Variable3.bind("<Enter>", self.on_enter_variable_3)
        self.Variable3.bind("<Leave>", self.on_leave_variable_3)

        self.Variable4 = Checkbutton(self.Box3, text="Variable 4", variable=self.CheckVar, state='disabled')
        self.Variable4.select()
        self.Variable4.grid(row=6, column=17, sticky='W', padx=5)
        self.Variable4.bind("<Enter>", self.on_enter_variable_4)
        self.Variable4.bind("<Leave>", self.on_leave_variable_4)

        self.Variable5 = Checkbutton(self.Box3, text="Variable 5", variable=self.CheckVar, state='disabled')
        self.Variable5.select()
        self.Variable5.grid(row=7, column=17, sticky='W', padx=5)
        self.Variable5.bind("<Enter>", self.on_enter_variable_5)
        self.Variable5.bind("<Leave>", self.on_leave_variable_5)

        self.Variable6 = Checkbutton(self.Box3, text="Variable 6", variable=self.CheckVar, state='disabled')
        self.Variable6.select()
        self.Variable6.grid(row=8, column=17, sticky='W', padx=5)
        self.Variable6.bind("<Enter>", self.on_enter_variable_6)
        self.Variable6.bind("<Leave>", self.on_leave_variable_6)

        self.Variable7 = Checkbutton(self.Box3, text="Variable 7", variable=self.CheckVar, state='disabled')
        self.Variable7.select()
        self.Variable7.grid(row=9, column=17, sticky='W', padx=5)
        self.Variable7.bind("<Enter>", self.on_enter_variable_7)
        self.Variable7.bind("<Leave>", self.on_leave_variable_7)

        self.Box4 = LabelFrame(self.master, text=" Donwload ")
        self.Box4.grid(row=10, column=17, columnspan=3, sticky='W', padx=5, pady=5)

        self.DownloadButton = Button(self.Box4, text="Download Excel File", command=threading.Thread(
            target=lambda: self.Fetch_Articles(int(self.From_Years.get()), int(self.To_Years.get()))).start)

        self.DownloadButton.grid(row=0, padx=5, pady=5)

    def OpenPreviousQueriesPage(self):
        self.master.withdraw()
        self.newWindow = Toplevel(self.master)
        self.app = PreviousQueriesPage(self.newWindow, self.user_id)

    def on_enter_variable_1(self, event):
        self.Variable1.configure(text="Journal Title")

    def on_leave_variable_1(self, enter):
        self.Variable1.configure(text="Variable 1")

    def on_enter_variable_2(self, event):
        self.Variable2.configure(text="Geographic Coverage of Journal")

    def on_leave_variable_2(self, enter):
        self.Variable2.configure(text="Variable 2")

    def on_enter_variable_3(self, event):
        self.Variable3.configure(text="Year")

    def on_leave_variable_3(self, enter):
        self.Variable3.configure(text="Variable 3")

    def on_enter_variable_4(self, event):
        self.Variable4.configure(text="Volume")

    def on_leave_variable_4(self, enter):
        self.Variable4.configure(text="Variable 4")

    def on_enter_variable_5(self, event):
        self.Variable5.configure(text="Issue")

    def on_leave_variable_5(self, enter):
        self.Variable5.configure(text="Variable 5")

    def on_enter_variable_6(self, event):
        self.Variable6.configure(text="Title of article")

    def on_leave_variable_6(self, enter):
        self.Variable6.configure(text="Variable 6")

    def on_enter_variable_7(self, event):
        self.Variable7.configure(text="Article’s order in issue ")

    def on_leave_variable_7(self, enter):
        self.Variable7.configure(text="Variable 7")


class PreviousQueriesPage:
    # Previous Queries Page

    def __init__(self, master, user_id):
        self.master = master
        self.frame = Frame(self.master)

        self.users_id = user_id

        self.canvas = Canvas(self.master, height=600, width=400)
        self.canvas.pack()

        self.frame = Frame(self.master)
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=0.3)

        self.label = Label(self.frame, text="Previous Queries", font=("Arial", 18))
        self.label.place(relx=0.25, rely=0.20, relwidth=0.5, relheight=0.5)

        self.frame2 = Frame(self.master, bg='light grey')
        self.frame2.place(rely=0.25, relwidth=1, relheight=0.74)

        self.label2 = Label(self.frame2, text='TEST DATA', bg='white')
        self.label2.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)

        self.scrollbar = Scrollbar(self.label2)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.mylist = Listbox(self.label2, yscrollcommand=self.scrollbar.set)

        self.database_connection = DatabaseConnector().get_conn()
        self.cursor = self.database_connection.cursor()

        # Retrieving previous queries information from database
        query = "select basic_variables, variable_8, variable_9, variable_10, variable_11, variable_12, variable_13, from_year, to_year from queries where user_id =%(user_id)s"
        self.cursor.execute(query, {'user_id': self.users_id})
        self.check = self.cursor.fetchall()

        results = []
        count = 0

        # displaying them on screen
        if self.check:
            for tuples in self.check:
                single_tuples = ' '.join([str(x) for x in tuples])
                results.append(single_tuples)
                results[count] = results[count].replace('None', '')
                self.mylist.insert('end', results[count])
                count = count + 1
        else:
            self.mylist.insert('end', "No Available Queries")

        self.mylist.pack(fill="both", expand="yes")

        self.scrollbar.config(command=self.mylist.yview)

        self.database_connection.close()
        self.cursor.close()
class Variable12():
    
    def __init__(self, url):
        
        self.url = url
        self.uni= universities.API()
        self.scraper = cfscrape.create_scraper()
        self.source = self.scraper.get(url).text
        self.soup = BeautifulSoup(self.source, 'lxml')
        self.authors = self.soup.find('div', class_="author-info accordion-tabbed__content") # this class have common for all articles
        self.flag = False
        self.country = None
        self.tempName = "None"
       
        
        self.main()  
        
   
    def orcidAccount(self):
        # fetching data from article cointains class_='orcid-account
        
        b = self.authors.find('p', class_='orcid-account') # key class
        c = b.find_next('p').text
        d = c.split(",")
        self.iterator(d)
        
    
    def authorType(self):
        # fetching data from article cointains class_='author-type'
        b = self.authors.find('p', class_='author-type') # key class
        c = b.find_next('p').text
        d = c.split(",")
        self.iterator(d)
    
    
    def random(self):
        # fetching data from selected part I am not sure this part contains author info.
        b = self.authors.find_all('p')
        try:
            
            c = b[3].text # we do not now maybe b[2] or b[4] has info about author
            d = c.split(",")
            self.iterator(d)
        except:
            pass
    def general(self):
        # fetching data from article only has "author-info accordion-tabbed__content" class
        b = self.authors.find_all('p')
        c = None 
        for i in b:

            if any("University" in s for s in i): # we only universtiy has containd "University" word
                c = i.text 
                break
        if (c != None):    
            d = c.split(",")
            self.iterator(d)
    
    def University(self, s):
        # remove empty character
        t = 0 # counter
        l = len(s)
        while l > t: # this loop remove empty character in s string
            
            if s[t] != " ":
                break
            
            t = t+1
            
        e = s[t:]  # return substring of d 
        if ("University" in e):
            self.tempName = e  # if university library return "None" I will use name of university 
        
        z=self.uni.lucky(name = e) 
        return z



    def iterator(self, d):
        
        l = len(d)
        t = 0
        c = None
        
        while (l > t and self.flag==False):
                         
             
             if ("University" in d[t]) :
                 
     
                 c = self.University(d[t])
                 self.flag = True
                 break
             
             elif ("London School of " in d[t]): # London School of Economcis and Political Science sentence is not contain word of "University"
                 c = self.University(d[t])       # and this school is so much popular in BSJ.Thus, I check this condition in particular
                 self.flag = True
                 break             
             
             t += 1    
        
        if (c == None):
            pass
        else:
            
            self.flag = True           
            self.country = c.country
            return self.country   
    
    def main(self):
        
        try:
            
            
            if (self.authors.find('p', class_='orcid-account')):
                self.orcidAccount()
            
            elif (self.authors.find('p', class_='author-type')):
                self.authorType()
                
                
            if (self.country == None): 
                
                self.random()
            
            if (self.country == None):
                                
                self.general()
                
         
        except:
            
            pass
        

def main():
    # main method
    window = Tk()
    app = OpeningPage(window)
    window.mainloop()


if __name__ == '__main__':
    main()
