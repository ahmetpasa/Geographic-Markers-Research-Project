Geographic Markers Research Project Companion App.
This software was built to aid to assist the researchers working on the Geo Markers Project with collection and analysis of data from the British Journal of Sociology via The Online Wiley Library. The data that can be retrieved are classified as variables. The program was developed in python and uses an SQL database for storing queries and users.

Dependencies 
-	codecs
-	Csv
-	tkinter 
-	pymysql
-	cfscrape
-	universities
-	Beautiful Soup4
-	Threading
-	geograpy3
-	nltk
-	lxml
-	numpy
-	openpyxl
-	pandas

Installation and Use
The software can be installed in two ways. 
Firstly, the software will have a packaged exe file that can be run on windows machines which can be downloaded from
https://www.dropbox.com/s/liqqjpqfs5w8st7/GeoMarkersApp.zip?dl=0

Alternatively, the source code can be accessed and run after installing all dependencies above from https://github.com/Areezy/Geographic-Markers-Research-Project/tree/master/Phase%202 

Regarding Usage
The program displays an introductory page with a brief description of the project and displays the interval year. This interval year is updated dynamically and shows the valid years with which the software should be used. On clicking proceed, a sign-in page is displayed and a sign-up page is also available. 

These pages are used to create a user to store queries performed for future reference and thus, not much emphasis was placed on security and other error script checking you would expect from a regular page of this kind.

Once you have successfully been signed up, a main page is displayed. On this page the interval year can be given. It works the same as how it looks on the introductory page, in descending order. For example, 2019 – 1999 or 2002 – 2001. 

The basic variables are explained by hovering your mouse over the items on the right side of the screen while the advanced variables are explained on a new page as they are more complicated. 
The basic variables are fetched by default as they are basic data that make up a codebook while the advanced variables are searched by giving keywords to the Browse Variable Text Field and clicking Select. The keywords are to be entered in the following the formats.

Variable xx
variable xx
vxx

*where xx is the advanced variable number.

Once the required variables are given, the Download Excel File button is used to get the data and they are saved into an excel and csv sheet and saved to the project path if using the source code and the exe directory if using the exe file.

There is also a previous queries button to display your previous queries with the interval year.


Special thanks to Sevil Togay for mentoring us and giving us an opportunity to work on this project and design this software to aid her research.

