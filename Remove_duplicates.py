with open('raw_data.csv','r') as in_file, open('final_tweet_data.csv','w') as out_file:
    seen=set()
    for line in in_file:
        if line in seen: continue 
        seen.add(line)
        out_file.write(line)
in_file.close()
out_file.close()

