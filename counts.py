from flask import Flask, redirect, render_template
import threading
import urllib2, gzip, csv, datetime, time

#flask globals


#date class

class date_query:
    '''
    queries all previous files from start_date to today and keeps a log

    then may be called once a day and will automatically download file and add current day to log
    '''
    def __init__(self, start_date):
        self.start_date = start_date
        self.current_date = start_date
        self.queried = []
        self.counts = []

    def get_backlog(self): #run once when starting up
        for day in xrange((datetime.date.today() - self.start_date).days):

            csvfile = self.download(self.current_date)

            count = self.count(csvfile)

            self.counts.append((self.current_date, count))

            self.queried.append(self.current_date)

            self.current_date += datetime.timedelta(days=1)

    def download(self, day):
        base_path = 'http://cran-logs.rstudio.com/'
        gzpath = day.isoformat() + '.csv.gz'

        try:
            with gzip.open(gzpath) as f:
                csvfile = f.read().split('\n')
            return csvfile
        except:
            day_path = base_path + str(day.year) + '/' + day.isoformat() + '.csv.gz'

            gzfile = urllib2.urlopen(day_path)

            with open(gzpath, 'wb') as output:
                output.write(gzfile.read())
            try:
                with gzip.open(gzpath) as f:
                    csvfile = f.read().split('\n')
                return csvfile
            except:
                print 'whoops'

    def count(self, csvfile):
        rdr = csv.reader(csvfile)
        header = rdr.next()
        pkg_col = header.index('package')

        pkgs = []

        for row in rdr:
            try:
                pkgs.append(row[pkg_col])
            except:
                pass

        return pkgs.count('Blaunet')

    def update(self):
        day = datetime.date.today()
        if day not in self.queried:
            print 'update queried'
            try:
                csvfile = self.download(day)

                count = self.count(csvfile)

                self.counts.append((self.current_date, count))

                self.queried.append(self.current_date)
            except:
                pass


    def run(self):
        self.get_backlog()

        while True:
            self.update()
            time.sleep(43200)

app = Flask(__name__)

#flask
@app.route('/')
def draw_counts():
    counts = a.counts

    counts = sum([x[1] for x in counts])

    return "There have been {} downloads of Blaunet".format(counts)


if __name__ == "__main__":
    a = date_query(datetime.date(2014,1,1))
    t3 = threading.Thread(target=a.run)
    t3.start()
    app.run()