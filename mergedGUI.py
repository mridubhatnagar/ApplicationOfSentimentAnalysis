#comsplete working program for sample data set.
from tkinter  import *
from tkinter import messagebox
from createnewtable import *  # file for sentiment analysis , has classify function defined in it
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd
import mysql.connector
from matplotlib.backends.backend_pdf import PdfPages
  

conn = mysql.connector.connect(user="root", password="test123", host="127.0.0.1", database="twitter_database") 
cursor = conn.cursor()
df=pd.read_sql("SELECT * from tweetdata2",conn)

master=Tk()
master.title("Sentiment Analysis of Tweets")

e1 = Entry(master)
Label(master, text="Enter Keyword").pack()
e1.pack()

def get_keyword(df):                          #gives the count of each keyword present in the total tweet records
    keywords = []
    text = df["Tweet"].lower()
    if "demonetization" in text:
        keywords.append("demonetization")
    elif "modi" in text:
    	keywords.append("modi")
    
    return ",".join(keywords)

df["Keywords"] = df.apply(get_keyword,axis=1)
counts = df["Keywords"].value_counts()
print(counts)

def total_sentiment_count(df):				#gives the count of positive,negative and neutral tweets respectively
	sentiment=[]
	text=df["Label"].lower()
	if "positive" in text:
		sentiment.append("positive")
	elif "negative" in text:
		sentiment.append("negative")
	elif "neutral" in text:
		sentiment.append("neutral")
	return ",".join(sentiment)

df["Label"] = df.apply(total_sentiment_count,axis=1)
sentimentcount=df["Label"].value_counts()
print(sentimentcount)

def demonetization_analysis():
	# Total number of positive ,negative and neutral tweets having the word entered in the text box

	
	print(e1.get().lower())

	
	count_positive=df[(df.Keywords == e1.get().lower()) & (df.Label == 'positive')]
	print(len(count_positive))


	count_negative=df[(df.Keywords == e1.get().lower()) & (df.Label == 'negative')]
	print(len(count_negative))

	count_neutral=df[(df.Keywords == e1.get().lower()) & (df.Label == 'neutral')]
	print(len(count_neutral))

	plt.ion()  #used for updating the graph on button click
	global actualFigure
	actualFigure = plt.figure(figsize = (8,8))
	actualFigure.suptitle("Tweets about"+" "+e1.get(), fontsize = 22)


	size=[len(count_positive),len(count_negative),len(count_neutral)]
	colors=['mediumpurple','lightcoral','yellow']
	label=["Positive","Negative","Neutral"]
	explode=(0.1,0,0) # proportion with which to offset each wedge 
	plt.pie(size,explode=explode,labels=label,colors=colors,autopct="%1.1f%%",shadow=True)
	plt.axis("equal")
	plt.draw()

	#canvas = FigureCanvasTkAgg(actualFigure,master=master)
	#canvas.get_tk_widget().pack(side=TOP,fill="x",expand=1)
	#canvas.show()
	#canvas.close()
	


def pdf_report():    #generates a pdf of the graph plotted


	with PdfPages('Report4.pdf',"a") as pdf:
		
		pdf.savefig(actualFigure)
	

def show_entry_fields():
	var=messagebox.showinfo("Sentiment",cl.classify(e1.get().lower()))





Button(master, text='Sentiment', command=show_entry_fields).pack()

Button(master, text='Graph', command=demonetization_analysis).pack()  #graphs

Button(master, text='Report', command=pdf_report).pack()

#Button(master, text='CSV File', command=csv_data).pack()

master.mainloop()