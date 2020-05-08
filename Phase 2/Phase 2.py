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



*******************************************************************

from tkinter import *
import re


#ALLOWING DIGIS ONLY
def testVal(inStr,acttyp):
    if acttyp == '1': #insert
        if not inStr.isdigit():
            return False
    return True


def clicked():
    global list_data
    list_data = []
    listbox.insert(END, content.get())
    list_data.append(content.get())

def delete_selected():
    global list_data
    selected = listbox.get(listbox.curselection())
    listbox.delete(ANCHOR)
    list_data.pop(list_data.index(selected))


    
if __name__ == "__main__":


    root = Tk()
    CheckVar  = IntVar()
    root.title('Geographical interface')

    

#BROWSE WIDGETS
    Box1 = LabelFrame(root, text=" Browse ")
    Box1.grid(row=3, columnspan=15, sticky='W',padx=5, pady=5, ipadx=5, ipady=5)

    BrowseByVariable = Label(Box1, text="Browse by variable:")
    BrowseByVariable.grid(row=3, column=0, sticky='E', padx=5, pady=2)

    

# VariableList,

    content = StringVar()
    BrowseByVariable = Entry(Box1, width = 40, textvariable=content)
    BrowseByVariable.grid(row=3, column=1, columnspan=7, sticky="WE", pady=2)

    BrowseByVariable = Button(Box1,text="search", command=clicked)
    BrowseByVariable.grid(row=3,column=8, sticky='W', padx=5, pady=2)

    listbox = Listbox(Box1)
    listbox.grid(row=4, column=1,sticky='w')

    BrowseByVariable = Button(Box1, text="Remove selected variable", command=delete_selected)
    BrowseByVariable.grid(row=5, column=1, pady=2, sticky='w')



#YEAR WIDGETS
    Box4 = LabelFrame(root, text="Years")
    Box4.grid(row=1,columnspan=9, sticky='W',padx=5, pady=5, ipadx=5, ipady=5)

    Years = Label(Box4, text="From:")
    Years.grid(row=1, column=0, sticky='E', padx=5, pady=2)

    Years = Entry(Box4, validate="key")
    Years['validatecommand'] = (Years.register(testVal),'%P','%d')
    Years.grid(row=1, column=1, columnspan=1, sticky="WE", pady=2)

    Years = Label(Box4, text="to:")
    Years.grid(row=1, column=2, padx=5, pady=2)

    Years = Entry(Box4, validate="key")
    Years['validatecommand'] = (Years.register(testVal),'%P','%d')
    Years.grid(row=1, column=3, columnspan=1, sticky="WE", pady=2)

#QUEREY WIDGETS
    Box2 = LabelFrame(root, text=" Queries ")
    Box2.grid(row=0, column=17, columnspan=2, rowspan=2, sticky='NS', padx=5, pady=5)

    Queries = Button(Box2, text="Recently Executed Queries")
    Queries.grid(row=0,padx=5, pady=5)

#PRESELECTED VARIBALES WIDGETS
    Box3 = LabelFrame(root, text=" Basic Codebook Variables: ")
    Box3.grid(row=3, column=17, columnspan=3, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)

    Variable1 = Checkbutton(Box3,text="Journal title", variable = CheckVar, state='disabled')
    Variable1.select()
    Variable1.grid(row=3, column=17, sticky='W', padx=5, pady=2)

    Variable2 = Checkbutton(Box3,text="Geographic Coverage of Journal", variable = CheckVar, state='disabled')
    Variable2.select()
    Variable2.grid(row=4, column=17, sticky='W', padx=5)

    Variable3 = Checkbutton(Box3,text="Year", variable = CheckVar, state='disabled')
    Variable3.select()
    Variable3.grid(row=5, column=17, sticky='W', padx=5)

    Variable4 = Checkbutton(Box3,text="Volume", variable = CheckVar, state='disabled')
    Variable4.select()
    Variable4.grid(row=6, column=17, sticky='W', padx=5)
    
    Variable5 = Checkbutton(Box3,text="Issue", variable = CheckVar, state='disabled')
    Variable5.select()
    Variable5.grid(row=7, column=17, sticky='W', padx=5)

    Variable6 = Checkbutton(Box3,text="Title of article", variable = CheckVar, state='disabled')
    Variable6.select()
    Variable6.grid(row=8, column=17, sticky='W', padx=5)

    Variable7 = Checkbutton(Box3,text="Article’s order in issue ", variable = CheckVar, state='disabled')
    Variable7.select()
    Variable7.grid(row=9, column=17, sticky='W', padx=5)

    Box4 = LabelFrame(root, text=" Donwload ")
    Box4.grid(row=10, column=17, columnspan=3, sticky='W', padx=5, pady=5)
    DownloadButton = Button(Box4, text="Download Excel File")
    DownloadButton.grid(row=0,padx=5, pady=5)



root.resizable(0,0)
root.mainloop()
