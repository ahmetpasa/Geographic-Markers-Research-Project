from tkinter import *
from tkinter import messagebox
import csv
import codecs
import pandas as pd  # You must also import "openpyxl" for running this, if you do not setup yet, it gives an error

import threading
import cfscrape
from bs4 import BeautifulSoup

root = Tk()


def Fetch_Articles(before_year, after_year):

    statusbar = Label(root, text="Fetching....", bd=1, relief=SUNKEN, anchor=W)
    statusbar.pack(side=BOTTOM, fill=X)
    before_year = before_year
    after_year = after_year
    british_journal_url = 'https://onlinelibrary.wiley.com/loi/14684446/year/'
    articles_we_wont_scrape = ['COMMENTARY', 'Commentary', 'Commentaries', 'Review', 'Erratum', 'Corrigendum', 'REVIEW',
                               'Book',
                               'Notes to contributors', 'Editorial announcement', 'VOLUME INDEX', 'Comments', '– By',
                               'Replies', 'Notes to Contributors', 'Issue Information ‐ Toc', 'Reviews', 'reviews',
                               'Books reviews', '– Edited by', 'Issue Information', 'Editorial',
                               'Issue Information ‐ TOC',
                               'Early View', 'Editor', 'commentators', 'Reply']

    scraper = cfscrape.create_scraper()
    scraper_2 = cfscrape.create_scraper()
    html_source = scraper.get(british_journal_url).text
    soup = BeautifulSoup(html_source, 'lxml')

    journal_title = soup.find('span', 'journalTitle').text.split(',')[1].lstrip()  # Variable 1
    csv_title = journal_title + '_' + str(before_year) + '_' + str(after_year)
    csv_file = codecs.open(csv_title + '.csv', 'w', encoding='utf-8')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow( ['Journal Title', 'Coverage', 'Year', 'Volume', 'Issue', 'Title of Article', 'Variable 7'])# Column names are arranged as example

    if journal_title in 'The British Journal of Sociology':  # These codes are arranged as codebook
        journal_title_code = 6  # it's not coded in codebook so we give 6
    elif journal_title in 'American Sociological Review':
        journal_title_code = 1
    elif journal_title in 'New Perspectives on Turkey':
        journal_title_code = 3
    elif journal_title in 'European Sociological Review':
        journal_title_code = 5
    elif journal_title in 'Modern China':
        journal_title_code = 4
    elif journal_title in 'Social Science Japan Journal':
        journal_title_code = 2

    if journal_title in 'American Sociological Review' or 'British Journal of Sociology':
        geographic_coverage = 2
    elif journal_title in 'Gender Society' or 'Social Forces':
        geographic_coverage = 1
    elif journal_title in 'European Sociological Review':
        geographic_coverage = 3
    elif journal_title in 'Modern China or New Perspectives on Turkey':
        geographic_coverage = 4

    for i in range(before_year, after_year - 1, -1):

        html_source = scraper.get(british_journal_url + str(i)).text
        soup = BeautifulSoup(html_source, 'lxml')

        for journal in soup.findAll('li', class_='card clearfix'):

            issue_url = 'https://onlinelibrary.wiley.com' + journal.find('a')['href']
            issue_and_volume_info = journal.find('a', class_='visitable').text
            issue_and_volume_info = issue_and_volume_info.split(" ")
            volume_number = issue_and_volume_info[1].split(',')[0]
            issue_number = issue_and_volume_info[3]
            year = i

            html_source_2 = scraper_2.get(issue_url).text
            article_soup = BeautifulSoup(html_source_2, 'lxml')

            article_order_counter = 0

            for articles in article_soup.findAll('div', class_='card issue-items-container exportCitationWrapper'):
                if not articles.find('h3'):
                    for article_order_in_issue in articles.findAll('a', class_='issue-item__title visitable'):
                        if any(word in article_order_in_issue.h2.text for word in articles_we_wont_scrape):
                            pass
                        else:
                            article_order_counter = article_order_counter + 1

                            title_of_article = article_order_in_issue.h2.text

                            csv_writer.writerow([journal_title_code, geographic_coverage, year, volume_number, str(issue_number),
                                                 title_of_article, str(article_order_counter)])

                else:
                    if any(word in articles.h3.text for word in articles_we_wont_scrape):
                        pass
                    else:
                        for article_order_in_issue in articles.findAll('a', class_='issue-item__title visitable'):
                            if any(word in article_order_in_issue.h2.text for word in articles_we_wont_scrape):
                                pass
                            else:

                                title_of_article = article_order_in_issue.h2.text
                                article_order_counter = article_order_counter + 1

                                csv_writer.writerow([journal_title_code, geographic_coverage, year, volume_number, str(issue_number),
                                                     title_of_article, str(article_order_counter)])
    csv_file.close()
    read_file = pd.read_csv(csv_title + '.csv')
    read_file.to_excel(csv_title + '_excel_format_' + '.xlsx', index=None,
                       header=True)  # Formatting the CSV to XLSX(Excel Table)

    messagebox.showinfo('Confirmation', 'Articles Fetched and Saved')
    root.quit()


root.title("Fetcher")
root.geometry('400x300')
frame = Frame()


# ALLOWING DIGIS ONLY
def testVal(inStr, acttyp):
    if acttyp == '1':  # insert
        if not inStr.isdigit():
            return False
    return True


# TEXTS USED
label_1 = Label(frame, text="The British Journal of Sociology Fetcher", font=('Arial Bold', 14))
label_1.grid(row=0, columnspan=4, pady=(10, 30))

label_2 = Label(frame, text="From")
label_2.grid(row=1, column=0, sticky=E)

label_3 = Label(frame, text="To")
label_3.grid(row=1, column=1, sticky=E, padx=(0, 3))

# ENTRY BOXES -ALLOWSS DIGITS ONLY-

startYear = Entry(frame, validate="key")
startYear['validatecommand'] = (startYear.register(testVal), '%P', '%d')
startYear.grid(row=1, column=1, stick=W)

finishYear = Entry(frame, validate="key")
finishYear['validatecommand'] = (finishYear.register(testVal), '%P', '%d')

finishYear.grid(row=1, column=2, sticky=W)

fetchButton = Button(frame, text="Fetch Articles", command=threading.Thread(
    target=lambda: Fetch_Articles(int(startYear.get()), int(finishYear.get()))).start)

fetchButton.grid(row=3, columnspan=4, pady=(10))

frame.place(relx=0.5, rely=0.5, anchor=CENTER)

root.mainloop()