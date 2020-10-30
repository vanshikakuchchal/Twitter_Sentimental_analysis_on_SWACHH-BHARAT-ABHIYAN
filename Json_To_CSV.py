import json
import csv
myfile = open('file1.json', 'r')
csvFile=open('raw_data.csv','a')
csvWriter=csv.writer(csvFile)
for i in myfile:
    data = json.loads(i)
    try:
         try:
                 csvWriter.writerow([data['retweeted_status']['full_text']])
         except:
                   print("Encoded Data ")
    except:
         try:
                 csvWriter.writerow([data['full_text']])
         except:
                   print("Encoded Data ")
myfile.close()
csvFile.close()

   
