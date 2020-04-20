import os
import csv
import pandas as pd
from datetime import datetime

def minutes_between_date(ini_date,end_date):
    daysDiff = (end_date-ini_date).days
    # Convert days to minutes
    minutesDiff = daysDiff * 24 * 60
    return minutesDiff

def update_param_value(dic,f1,f2):
    for line in f1:
        if line[0:line.find('=')] in dic:
            f2.write(line.replace(line,line[0:line.find('=')]+" = "+dic[line[0:line.find('=')]]))
        elif line[0:line.find('=')-1] in dic:
            f2.write(line.replace(line, line[0:line.find('=')-1]+" = "+dic[ line[0:line.find('=')-1]]))
        elif line[0:line.find('=')-2] in dic:
            f2.write(line.replace(line, line[0:line.find('=')-2]+"  = "+dic[ line[0:line.find('=')-2]]))
        elif line[0:line.find('=')-3] in dic:
            f2.write(line.replace(line, line[0:line.find('=')-3]+"   = "+dic[ line[0:line.find('=')-3]]))
        else:
            f2.write(line)
    return f2

def csv_to_wind(path, ini_date, end_date, output):
    data = pd.read_csv(path,delimiter=';')
    data['date'] = pd.to_datetime(data['date'])
    f = open(output, 'w')
    line = ''
    #Check date
    if (data['date'].min() <= ini_date):
        i = 0
        while i < len(data['date']):
            if (data['date'][i] >= ini_date) and (data['date'][i] <= end_date):
                if (len(line) == 0) and (data['date'][i] != ini_date):
                    line = "0 %5.3f %5.3f\n" % (data['speed'][i],data['dir'][i])
                    f.write(line)
                line = "%i %5.3f %5.3f\n" % ((data['date'][i]-ini_date).seconds/60, data['speed'][i],data['dir'][i])
                if ((data['date'][i]-ini_date).seconds/60) == 0 and i>0:
                    line = "%i %5.3f %5.3f\n" % (minutes_between_date(ini_date,end_date), data['speed'][i],data['dir'][i])
                f.write(line)
            i = i + 1
        if (data['date'][i-1] != end_date):
            line = "%i %5.3f %5.3f\n" % (minutes_between_date(ini_date,end_date), data['speed'][i-1],data['dir'][i-1])
            f.write(line)
    else:
        print('Invalid wind file')
    f.close()

def csv_to_tem(path, ini_date, end_date, output):
    data = pd.read_csv(path,delimiter=';')
    data['date'] = pd.to_datetime(data['date'])
    f = open(output, 'w')
    line = ''
    #Check date
    if (data['date'].min() <= ini_date):
        i = 0
        while i < len(data['date']):
            if (data['date'][i] >= ini_date) and (data['date'][i] <= end_date):
                if (len(line) == 0) and (data['date'][i] != ini_date):
                    line = "0 %5.2f %5.2f 0 %5.5f\n" % (data['hum'][i],data['temp'][i],data['rad'][i])
                    f.write(line)
                line = "%i %5.2f %5.2f 0 %5.5f\n" % ((data['date'][i]-ini_date).seconds/60, data['hum'][i],data['temp'][i],data['rad'][i])
                if ((data['date'][i]-ini_date).seconds/60) == 0 and i>0:
                    line = "%i %5.2f %5.2f 0 %5.5f\n" % (minutes_between_date(ini_date,end_date), data['hum'][i],data['temp'][i],data['rad'][i])
                f.write(line)
            i = i + 1
        if (data['date'][i-1] != end_date):
            line = "%i %5.2f %5.2f 0 %5.5f\n" % (minutes_between_date(ini_date,end_date), data['hum'][i-1],data['temp'][i-1],data['rad'][i-1])
            f.write(line)
    else:
        print('Invalid radiation file')
    f.close()

def gen_ini_value(k,value):
    values = ''
    for i in range(0,k):
        values = values + ('    %5.3f\n' % value)
    return values

def gen_uniform_output_bct(out_dic,output,ini_date,end_date):
    f = open(output, 'w')
    for e in out_dic:
        f.write("table-name           'Boundary Section : %i'\n" % e)
        f.write("contents             'Logarithmic         '\n")
        f.write("location             '" + out_dic[e]['Name'] + "               '\n")
        f.write("time-function        'non-equidistant'\n")
        f.write("reference-time       " + ini_date.strftime("%Y%m%d") + "\n")
        f.write("time-unit            'minutes'\n")
        f.write("interpolation        'linear'\n")
        f.write("parameter            'time                '                     unit '[min]'\n")
        f.write("parameter            'total discharge (t)  end A'               unit '[m3/s]'\n")
        f.write("parameter            'total discharge (t)  end B'               unit '[m3/s]'\n")
        f.write("records-in-table     2\n")
        f.write("0 %5.2f 9.9999900e+002\n" % out_dic[e]['Flow'])
        f.write("%i %5.2f 9.9999900e+002\n" % (minutes_between_date(ini_date,end_date),out_dic[e]['Flow']))
    f.close()

def csv_to_bct(out_dic,output,input_csv,ini_date,end_date):
    f = open(output, 'w')
    for e in out_dic:
        data = pd.read_csv(input_csv+out_dic[e]['Name']+'.csv',delimiter=';')
        print("Opening ",input_csv+out_dic[e]['Name']+'.csv')
        data['date'] = pd.to_datetime(data['date'])
        line = ''
        #Check date
        if (data['date'].min() <= ini_date):
            i = 0
            f.write("table-name           'Boundary Section : %i'\n" % e)
            f.write("contents             'Logarithmic         '\n")
            f.write("location             '" + out_dic[e]['Name'] + "               '\n")
            f.write("time-function        'non-equidistant'\n")
            f.write("reference-time       " + ini_date.strftime("%Y%m%d") + "\n")
            f.write("time-unit            'minutes'\n")
            f.write("interpolation        'linear'\n")
            f.write("parameter            'time                '                     unit '[min]'\n")
            f.write("parameter            'total discharge (t)  end A'               unit '[m3/s]'\n")
            f.write("parameter            'total discharge (t)  end B'               unit '[m3/s]'\n")
            if (data['date'][len(data['date'])-1] < end_date):
                f.write("records-in-table    %i\n" % (len(data['date'])+1))
            else:
                f.write("records-in-table    %i\n" % len(data['date']))
            while i < len(data['date']):
                if (data['date'][i] >= ini_date) and (data['date'][i] <= end_date):
                    if (len(line) == 0) and (data['date'][i] != ini_date):
                        line = "0 %5.2f 9.9999900e+002\n" % (data['Flow'][i])
                        f.write(line)
                    line = "%i %5.2f 9.9999900e+002\n" % ((data['date'][i]-ini_date).seconds/60, data['Flow'][i])
                    f.write(line)
                i = i + 1
            if (data['date'][i-1] != end_date):
                line = "%i %5.2f 9.9999900e+002\n" % (minutes_between_date(ini_date,end_date), data['Flow'][i-1])
                f.write(line)
        else:
            print('Invalid Output flow file')
    f.close()

def gen_uniform_output_bcc(out_dic,output,ini_date,end_date):
    f = open(output, 'w')
    for e in out_dic:
        if "Salinity" in out_dic[e]:
            f.write("table-name           'Boundary Section : %i'\n" % e)
            f.write("contents             'Uniform         '\n")
            f.write("location             '" + out_dic[e]['Name'] + "               '\n")
            f.write("time-function        'non-equidistant'\n")
            f.write("reference-time       " + ini_date.strftime("%Y%m%d") + "\n")
            f.write("time-unit            'minutes'\n")
            f.write("interpolation        'linear'\n")
            f.write("parameter            'time                '  unit '[min]'\n")
            f.write("parameter            'Salinity            end A uniform'               unit '[ppt]'\n")
            f.write("parameter            'Salinity            end B uniform'               unit '[ppt]'\n")
            f.write("records-in-table     2\n")
            f.write("0 %5.2f %5.2f\n" % (out_dic[e]['Salinity'],out_dic[e]['Salinity']))
            f.write("%i %5.2f %5.2f\n" % (minutes_between_date(ini_date,end_date),out_dic[e]['Salinity'],out_dic[e]['Salinity']))
        if "Temperature" in out_dic[e]:
            f.write("table-name           'Boundary Section : %i'\n" % e)
            f.write("contents             'Uniform         '\n")
            f.write("location             '" + out_dic[e]['Name'] + "               '\n")
            f.write("time-function        'non-equidistant'\n")
            f.write("reference-time       " + ini_date.strftime("%Y%m%d") + "\n")
            f.write("time-unit            'minutes'\n")
            f.write("interpolation        'linear'\n")
            f.write("parameter            'time                '  unit '[min]'\n")
            f.write("parameter            'Temperature           end A uniform'               unit '[C]'\n")
            f.write("parameter            'Temperature           end B uniform'               unit '[C]'\n")
            f.write("records-in-table     2\n")
            f.write("0 %5.2f %5.2f\n" % (out_dic[e]['Temperature'],out_dic[e]['Temperature']))
            f.write("%i %5.2f %5.2f\n" % (minutes_between_date(ini_date,end_date),out_dic[e]['Temperature'],out_dic[e]['Temperature']))
        else:
            print("ERROR: Missing Salinity/Temperature for bcc")  
        
    f.close()

def gen_uniform_intput_dis(in_dic,output,ini_date,end_date):
    f = open(output, 'w')
    for e in in_dic:
        f.write("table-name          'Discharge : %i'\n" % e)
        f.write("contents            'walking   '\n")
        f.write("location            '"+ in_dic[e]['Name'] + "               '\n")
        f.write("time-function       'non-equidistant'\n")
        f.write("reference-time       " + ini_date.strftime("%Y%m%d") + "\n")
        f.write("time-unit           'minutes'\n")
        f.write("interpolation       'block'\n")
        f.write("parameter           'time                '                     unit '[min]'\n")
        f.write("parameter           'flux/discharge rate '                     unit '[m3/s]'\n")
        f.write("parameter           'Salinity            '                     unit '[ppt]'\n")
        f.write("parameter           'Temperature         '                     unit '[C]'\n")
        f.write("records-in-table    2\n")
        f.write("0 %5.2f %5.2f %5.2f\n" % (in_dic[e]['Flow'],in_dic[e]['Salinity'],in_dic[e]['Temperature']))
        f.write("%i %5.2f %5.2f %5.2f\n" % (minutes_between_date(ini_date,end_date),in_dic[e]['Flow'],in_dic[e]['Salinity'],in_dic[e]['Temperature']))
    f.close()

def csv_to_dis(in_dic,output_folder,output_name,ini_date,end_date):
    f = open(output_name, 'w')

    for e in in_dic:
        data = pd.read_csv(output_folder+in_dic[e]['Name']+'.csv',delimiter=';')
        print("Opening ",output_folder+e+'.csv')
        data['date'] = pd.to_datetime(data['date'])
        line = ''
        #Check date
        if (data['date'].min() <= ini_date):
            i = 0
            f.write("table-name          'Discharge : %i'\n" % e)
            f.write("contents            'walking   '\n")
            f.write("location            '"+ in_dic[e]['Name'] + "               '\n")
            f.write("time-function       'non-equidistant'\n")
            f.write("reference-time       " + ini_date.strftime("%Y%m%d") + "\n")
            f.write("time-unit           'minutes'\n")
            f.write("interpolation       'block'\n")
            f.write("parameter           'time                '                     unit '[min]'\n")
            f.write("parameter           'flux/discharge rate '                     unit '[m3/s]'\n")
            f.write("parameter           'Salinity            '                     unit '[ppt]'\n")
            f.write("parameter           'Temperature         '                     unit '[C]'\n")
            if (data['date'][len(data['date'])-1] < end_date):
                f.write("records-in-table    %i\n" % (len(data['date'])+1))
            else:
                f.write("records-in-table    %i\n" % len(data['date']))
            while i < len(data['date']):
                if (data['date'][i] >= ini_date) and (data['date'][i] <= end_date):
                    if (len(line) == 0) and (data['date'][i] != ini_date):
                        line = "0 %5.2f %5.2f %5.2f\n" % (data['Flow'][i],data['Sal'][i],data['Temp'][i])
                        f.write(line)
                    line = "%i %5.2f %5.2f %5.2f\n" % ((data['date'][i]-ini_date).seconds/60, data['Flow'][i],data['Sal'][i],data['Temp'][i])
                    f.write(line)
                i = i + 1
            if (data['date'][i-1] != end_date):
                line = "%i %5.2f %5.2f %5.2f\n" % (minutes_between_date(ini_date,end_date), data['Flow'][i-1],data['Sal'][i-1],data['Temp'][i-1])
                f.write(line)
        else:
            print('Invalid Tributary file')

    f.close()
