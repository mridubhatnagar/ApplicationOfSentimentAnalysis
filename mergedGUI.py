#complete working program for sample data set.
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
df=pd.read_sql("SELECT * from tweetdata7",conn)

def get_keyword(df):                          #gives the count of each keyword present in the total tweet records
    keywords = []
    text = df["Tweet"].lower()
    if "demonetization" in text:
        keywords.append("demonetization")
    if "modi" in text:
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
	# Total number of positive tweets having word demonetization

	global count_positive,count_negative,count_neutral

	
	count_positive=df[(df.Keywords == "demonetization") & (df.Label == 'positive')]
	print(len(count_positive))

	#Total number of negative tweets having word demonetization
	count_negative=df[(df.Keywords == "demonetization") & (df.Label == 'negative')]
	print(len(count_negative))

	count_neutral=df[(df.Keywords == "demonetization") & (df.Label == 'neutral')]
	print(len(count_neutral))

	global actualFigure
	actualFigure = plt.figure(figsize = (4,4))
	actualFigure.suptitle("Tweets about Demonetization", fontsize = 22)

	size=[len(count_positive),len(count_negative),len(count_neutral)]
	colors=['mediumpurple','lightcoral','yellow']
	label=["Positive","Negative","Neutral"]
	explode=(0.1,0,0) # proportion with which to offset each wedge 
	plt.pie(size,explode=explode,labels=label,colors=colors,autopct="%1.1f%%",shadow=True)
	plt.axis("equal")

	canvas = FigureCanvasTkAgg(actualFigure,master=master)
	canvas.get_tk_widget().pack(side=TOP,fill="x",expand=1)
	canvas.show()

	

	modi_analysis()

def modi_analysis():
	# Total number of positive tweets having word demonetization
	global count_positive1,count_negative1,count_neutral1

	count_positive1=df[(df.Keywords == "modi") & (df.Label == 'positive')]
	print(len(count_positive1))

	#Total number of negative tweets having word demonetization
	count_negative1=df[(df.Keywords == "modi") & (df.Label == 'negative')]
	print(len(count_negative1))

	count_neutral1=df[(df.Keywords == "modi") & (df.Label == 'neutral')]
	print(len(count_neutral1))

	

	actualFigure1 = plt.figure(figsize = (4,4))
	actualFigure1.suptitle("Tweets about Modi after Demonetization", fontsize = 22)

	size=[len(count_positive1),len(count_negative1),len(count_neutral1)]
	colors=['orange','pink','white']
	label=["Positive","Negative","Neutral"]
	explode=(0.1,0,0) # proportion with which to offset each wedge 
	plt.pie(size,explode=explode,labels=label,colors=colors,autopct="%1.1f%%",shadow=True)
	plt.axis("equal")

	
	#master.mainloop()
	canvas = FigureCanvasTkAgg(actualFigure1,master=master)
	canvas.get_tk_widget().pack(side=TOP,fill="x",expand=1)
	canvas.show()

	master.mainloop()






def time_analysis():
	c=df.sort_values(['created_at'], ascending=True)
	print(c)
	mid_point=len(df['created_at'])/2
	print(int(mid_point))
	positive_counter=0
	negative_counter=0
	neutral_counter=0
	for a in range(int(mid_point)+1):
		if(df['Label'][a]=="positive"):
			positive_counter+=1
		elif(df['Label'][a]=="negative"):
			negative_counter+=1
		elif(df['Label'][a]=="neutral"):
			neutral_counter+=1

	size=[positive_counter,negative_counter,neutral_counter]
	colors=["mediumpurple","lightcoral","yellow"]
	labels=["Positive","Negative","Neutral"]
	explode=(0.1,0,0)
	plt.pie(size,explode=explode,labels=labels,colors=colors,autopct="%1.1f%%",shadow=True)
	plt.axis("equal")
	plt.title("Variation of opinion with time")
	plt.show()

	#do for next half as well


def pdf_report():


	with PdfPages('Report4.pdf',"a") as pdf:
		#As many times as you like, create a figure fig and save it:
		actualFigure=plt.figure(figsize=(8,8))
		actualFigure.suptitle("Tweets about Demonetization", fontsize = 22)

		size=[len(count_positive),len(count_negative),len(count_neutral)]
		colors=['mediumpurple','lightcoral','yellow']
		label=["Positive","Negative","Neutral"]
		explode=(0.1,0,0) # proportion with which to offset each wedge 
		plt.pie(size,explode=explode,labels=label,colors=colors,autopct="%1.1f%%",shadow=True)
		plt.axis("equal")
		pdf.savefig(actualFigure)
		actualFigure1=plt.figure(figsize=(8,8))
		actualFigure1.suptitle("Tweets about Modi after Demonetization", fontsize = 22)

		size=[len(count_positive1),len(count_negative1),len(count_neutral1)]
		colors=['orange','pink','white']
		label=["Positive","Negative","Neutral"]
		explode=(0.1,0,0) # proportion with which to offset each wedge 
		plt.pie(size,explode=explode,labels=label,colors=colors,autopct="%1.1f%%",shadow=True)
		plt.axis("equal")
		pdf.savefig(actualFigure1) # saves 










def show_entry_fields():
	var=messagebox.showinfo("Sentiment",cl.classify(e1.get()))


master=Tk()
master.title("Sentiment Analysis of Tweets")

e1 = Entry(master)
Label(master, text="Enter Keyword").pack()
e1.pack()


Button(master, text='Sentiment', command=show_entry_fields).pack()

Button(master, text='Graph', command=demonetization_analysis).pack()  #graphs

Button(master, text='Report', command=pdf_report).pack()

#Button(master, text='CSV File', command=csv_data).pack()




master.mainloop()