import os, glob, csv
file_path = os.getcwd()
root = '/mnt/netapp/Rosenthal'
years = os.listdir(root)
files_data = [['Filename','.srt','.txt3','.ocr']]
for year in years:
    if year.isdigit():
        months = os.listdir(os.path.join(root,year))
        for month in months:
            days = os.listdir(os.path.join(root,year,month))
            for day in days:
                os.chdir(os.path.join(root,year,month,day))
                mp4s  = [x.split('.mp4')[0] for x in glob.glob('*.mp4')]
                srts  = [x.split('.srt')[0] for x in glob.glob('*.srt')]
                txt3s = [x.split('.txt3')[0] for x in glob.glob('*.txt3')]
                ocrs  = [x.split('.ocr')[0] for x in glob.glob('*.ocr')]
                for mp4 in mp4s:
                    file_data = [mp4] #Filename
                    if mp4 in srts:
                        file_data.append(1) #.srt
                    else:
                        file_data.append(0) 
                    
                    if mp4 in txt3s:
                        file_data.append(1) #.txt3
                    else:
                        file_data.append(0)

                    if mp4 in ocrs:
                        file_data.append(1) #.ocr
                    else:
                        file_data.append(0)
                    files_data.append(file_data)

os.chdir(file_path)
with open('stats.csv', 'w', newline="") as f:
    writer = csv.writer(f)
    writer.writerows(files_data)
    