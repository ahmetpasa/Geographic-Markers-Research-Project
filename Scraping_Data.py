import cfscrape
import csv
import codecs
import pandas as pd # You must also import "openpyxl" for running this, if you do not setup yet, it gives an error
from bs4 import BeautifulSoup

before_year = 2019
after_year = 2000
british_journal_url = 'https://onlinelibrary.wiley.com/loi/14684446/year/'
articles_we_wont_scrape = ['COMMENTARY', 'Commentary', 'Commentaries', 'Review', 'Erratum', 'Corrigendum', 'REVIEW', 'Book',
                           'Notes to contributors', 'Editorial announcement', 'VOLUME INDEX', 'Comments', '– By',
                           'Replies', 'Notes to Contributors', 'Issue Information ‐ Toc', 'Reviews', 'reviews',
                           'Books reviews', '– Edited by', 'Issue Information', 'Editorial', 'Issue Information ‐ TOC',
                           'Early View', 'Editor', 'commentators', 'Reply', 'reply']

scraper = cfscrape.create_scraper()
scraper_2 = cfscrape.create_scraper()
html_source = scraper.get(british_journal_url).text
soup = BeautifulSoup(html_source, 'lxml')

csv_file = codecs.open('ex_codebook.csv', 'w', encoding='utf-8')

csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Journal Title', 'Coverage', 'Year', 'Volume', 'Issue', 'Title of Article', 'Variable 7']) # Column names are arranged as example

journal_title = soup.find('span', 'journalTitle').text.split(',')[1].lstrip()  # Variable 1

if journal_title in 'The British Journal of Sociology': # These codes are arranged as codebook
    journal_title_code = 6 # it's not coded in codebook so we give 6
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

print(geographic_coverage) # Variable 2

print()

count = 0
for i in range(before_year, after_year - 1, -1):

    html_source = scraper.get(british_journal_url + str(i)).text
    soup = BeautifulSoup(html_source, 'lxml')

    for journal in soup.findAll('li', class_= 'card clearfix'):

        issue_url = 'https://onlinelibrary.wiley.com' + journal.find('a')['href']
        issue_and_volume_info = journal.find('a', class_ = 'visitable').text
        issue_and_volume_info = issue_and_volume_info.split(" ")
        volume_number = issue_and_volume_info[1].split(',')[0]
        issue_number = issue_and_volume_info[3]
        year = i

        html_source_2 = scraper_2.get(issue_url).text
        article_soup = BeautifulSoup(html_source_2, 'lxml')

        article_order_counter = 0

        for articles in article_soup.findAll('div', class_='card issue-items-container exportCitationWrapper'):
            if not articles.find('h3'):
                for article_order_in_issue in articles.findAll('a',class_='issue-item__title visitable'):
                    if any(word in article_order_in_issue.h2.text for word in articles_we_wont_scrape):
                        pass
                    else:
                        article_order_counter = article_order_counter + 1

                        title_of_article = article_order_in_issue.h2.text
                        print(title_of_article)
                        print(year)
                        print('volume number is ' + volume_number)
                        print('issue number is ' + issue_number)
                        print('order in issue is ' + str(article_order_counter))
                        print()

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
                            print(title_of_article) # Variable 6
                            print(year)     # Variable 3
                            print('volume number is ' + volume_number) # Variable 4
                            print('issue number is ' + issue_number) # Variable 5
                            print('order in issue is ' + str(article_order_counter)) # Variable 7
                            print()
                            csv_writer.writerow(
                                [journal_title_code, geographic_coverage, year, volume_number, issue_number,
                                 title_of_article, str(article_order_counter)])
                            # It is printing in the console but it also gives a CSV file in the project directory

csv_file.close()

read_file = pd.read_csv ('ex_codebook.csv')
read_file.to_excel ('new_codebook.xlsx', index = None, header=True) # Formatting the CSV to XLSX(Excel Table) and opens a new file in same directory.






