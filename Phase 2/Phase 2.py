from tkinter import *
import cfscrape
from bs4 import BeautifulSoup


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

        self.master.Explanation_label = Label(self.master, text=self.master.explanation_text, justify='center', font='None 10')
        self.master.Explanation_label.grid(row=1, column=0)

        self.master.Interval_year_label_text = Label(self.master, text=self.master.interval_year_text, justify='center', font='None 10 bold')
        self.master.Interval_year_label_text.grid(row=2, column=0)

        self.master.Interval_year_label = Label(self.master, text=self.master.interval_year, justify='center', font='None 10 bold')
        self.master.Interval_year_label.grid(row=3, column=0)

        self.master.Proceed_button = Button(self.master, text=self.master.proceed_text, width=8)
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


def main():
    # main method
    window = Tk()
    app = OpeningPage(window)
    window.mainloop()
if __name__ == '__main__':
    main()



