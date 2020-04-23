import cfscrape
from bs4 import BeautifulSoup

before_year = '2019'
after_year = '2000'
articles_per_page = 500
british_journal_url = 'https://onlinelibrary.wiley.com/action/doSearch?AfterYear=' + after_year + '&BeforeYear=' + before_year + '&SeriesKey=14684446&content=articlesChapters&countTerms=true&pageSize=500&sortBy=Earliest&startPage=0&target=' + str(articles_per_page)
page_count = 0
count = 0
articles_we_wont_scrape = ['COMMENTARY', 'Commentary', 'Commentaries', 'Review', 'Erratum', 'Corrigendum', 'REVIEW', 'Book',
                           'Notes to contributors', 'Editorial announcement', 'VOLUME INDEX', 'Comments', '– By',
                           'Notes to Contributors', 'Issue Information ‐ Toc', 'Reviews', 'reviews', 'Books reviews',
                           'Issue Information', 'Editorial', 'Issue Information ‐ TOC', 'Early View', 'Editor']





try:
    scraper = cfscrape.create_scraper()
    html_source = scraper.get(british_journal_url).text
    soup = BeautifulSoup(html_source, 'lxml')
    result_count = soup.find('span', class_= 'result__count').text

except:
    print('No articles in this range')


result_count = result_count.replace(',', '')

result_count_int = int(result_count)

page_count = result_count_int / articles_per_page

if page_count.is_integer():
    pass
else:
    page_count = int(page_count) + 1

for i in range(page_count):
    british_journal_url = 'https://onlinelibrary.wiley.com/action/doSearch?AfterYear=' + after_year + '&BeforeYear=' + before_year + '&SeriesKey=14684446&content=articlesChapters&countTerms=true&pageSize=500&sortBy=Earliest&startPage=' + str(i) + '&target=' + str(
        articles_per_page)

    html_source = scraper.get(british_journal_url).text

    soup = BeautifulSoup(html_source, 'lxml')

    for journal in soup.findAll('li', class_ = 'clearfix separator search__item exportCitationWrapper'):
        title_of_article = journal.h2.a.text

        volume_of_article_with_other_data = journal.find('a', class_='publication_meta_volume_issue').text

        try:
            journal_type = journal.find('span',class_='meta__type').text
        except:
            journal_type = ''



        if any(word in journal_type for word in articles_we_wont_scrape):
            pass
        elif any(word in title_of_article for word in articles_we_wont_scrape):

            pass
        elif "Early" in volume_of_article_with_other_data:
                pass

        else:

            journal_title = 'The British Journal of Sociology'   # Variable 1

            geographic_coverage = 2     # Variable 2

            print(title_of_article)    # Variable 6

            year_of_article_with_other_data = journal.p.text
            year_of_article = year_of_article_with_other_data.split(" ")[4]
            year_of_article = year_of_article.replace("\n", "")
            print(year_of_article)  # Variable 3

            volume_of_article_with_other_data = journal.find('a', class_='publication_meta_volume_issue').text



            volume_of_article = volume_of_article_with_other_data.split(" ")[1]

            volume_of_article = volume_of_article.split(",")[0]

            issue_of_article = volume_of_article_with_other_data.split(" ")[3]

            article_issue_list_source = journal.find('a', class_ = 'publication_meta_volume_issue')['href']
            article_issue_list_source_url = 'https://onlinelibrary.wiley.com' + article_issue_list_source

            scraper_2 = cfscrape.create_scraper()

            html_issues_list_source = scraper_2.get(article_issue_list_source_url).text

            soup = BeautifulSoup(html_issues_list_source, 'lxml')

            order_counter = 0
            article_order_in_issue_count = 0

            for article_order_in_issue in soup.findAll('a', class_= 'issue-item__title visitable'):
                if any(word in article_order_in_issue.text for word in articles_we_wont_scrape):
                    pass
                else:

                    order_counter = order_counter + 1

                    if title_of_article in article_order_in_issue.text:

                        article_order_in_issue_count = order_counter



            print("volume is " + volume_of_article)       # Variable 4
            print("issue is " + issue_of_article)       #Variable 5
            count = count + 1




            print("article order " + str(article_order_in_issue_count))  # Variable 7

            print(count)

            print()























