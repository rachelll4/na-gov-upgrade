import csv
from flask import Flask
from flask import abort
from flask import render_template
app = Flask(__name__)
    
def get_arrest_csv():
    #should change this to get ALL files with start 'scraped-umd-police-arrest-log'
    csv_path = './data/all-police-arrests.csv'
    csv_file = open(csv_path, 'r')
    csv_obj = csv.DictReader(csv_file)
    csv_list = list(csv_obj)
    return csv_list
    
def get_activity_csv(arrest_list):
    #should change this to get ALL files with start 'scraped-umd-police-activity-log'
    csv_path = './data/all-police-activity.csv'
    csv_file = open(csv_path, 'r')
    csv_obj = csv.DictReader(csv_file)
    csv_list = list(csv_obj)
    
    arrest_cases = [arrest['UMPD CASE NUMBER'] for arrest in arrest_list]
    for activity in csv_list:
        activity['ARREST'] = "Yes" if (activity['UMPD CASENUMBER'] in arrest_cases) else "No"
        case_date = activity['OCCURRED DATE TIMELOCATION'].split('/')
        year_time = case_date[2].split()
        if (len(year_time[0]) == 2):
            year_time[0] = "20"+ year_time[0]
        if (len(case_date[0]) == 1):
            case_date[0] = '0' + case_date[0]
        if (len(case_date[1]) == 1):
            case_date[1] = '0' + case_date[1]
        if (len(year_time) != 2):
            year_time = year_time + ['00:00']
        activity['CASE_DATE'] = year_time[0] + '-' + case_date[0] + '-' + case_date[1] + '\n' + year_time[1]
        
        report_date = activity['REPORT DATE TIME'].split('/')
        year_time = report_date[2].split()
        if (len(year_time[0]) == 2):
            year_time[0] = "20"+ year_time[0]
        if (len(year_time) != 2):
            year_time = year_time + ['00:00']
        if (len(report_date[0]) == 1):
            report_date[0] = '0' + report_date[0]
        if (len(report_date[1]) == 1):
            report_date[1] = '0' + report_date[1]
        activity['REPORT_DATE'] = year_time[0] + '-' + report_date[0] + '-' + report_date[1] + '\n' + year_time[1]
    return csv_list

@app.route("/")
def index():
    template = 'index.html'
    
    arrest_list = get_arrest_csv()
    activity_list = get_activity_csv(arrest_list)

    return render_template(template, activity_list=activity_list, arrest_list=arrest_list)

@app.route('/<case_number>/')
def detail(case_number):
    template = 'detail.html'
    
    arrest_list = get_arrest_csv()
    activity_list = get_activity_csv(arrest_list)
    
    for activity in activity_list:
        if (activity['UMPD CASENUMBER'] == case_number):
            #if (activity['DISPOSITION'] == "Arrest"):
            arrest_matches = [arrest for arrest in arrest_list if arrest['UMPD CASE NUMBER'] == case_number]
            if (len(arrest_matches) > 0):
                return render_template(template, activity = activity, arrest = arrest_matches[0])
            return render_template(template, activity = activity, arrest = None)
    abort(404)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)