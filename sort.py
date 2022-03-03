from astropy.io import fits
import os
import datetime
dates = {}

for file in os.listdir('fits'):
    if 'tmp' not in file:            
        file = fits.open(f"./fits/{file}")
        date = file[0].header['DATE-LOC'].split('T')[0]
        if date not in dates:
            dates[date] = {
                "pictures": 1,
                "telescopeUsed": file[0].header['TELESCOP'],
                "dates": [file[0].header['DATE-LOC']]
            }
        else:
            dates[date]['pictures'] += 1
            dates[date]['dates'].append(file[0].header['DATE-LOC'])
            if(dates[date]['telescopeUsed'] != file[0].header['TELESCOP']):
                print('telescope mismatch')
        
        '''
        date = file[0].header['DATE-LOC'].split('T')[0]

        print(file[0].header['DATE-LOC'].split('T')[0])
        if(file[0].header['DATE-LOC'].split('T')[0] not in dates):
            dates.append(file[0].header['DATE-LOC'].split('T')[0])
        '''


print(dates)

for date, value in dates.items():
    print(date)
    lowestTime = {"value": 24, "string": None}
    highestTime = {"value": 0, "string": None}
    for iso in value['dates']:
        time = iso.split('T')[1].split('-')
        hour = time[0]
        minute = time[1]
        second = time[2]
        time = int(hour) + int(minute)/60 + float(second)/3600
        print(time)
        if time > highestTime['value']:
            highestTime['string'] = f"{hour}:{minute}:{second}"
            highestTime['value'] = time
        elif time < lowestTime['value']:
            lowestTime['string'] = f"{hour}:{minute}:{second}"
            lowestTime['value'] = time

print(highestTime, lowestTime)