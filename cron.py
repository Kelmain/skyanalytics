from crontab import CronTab
#creating a CronTab instance with the user
jobScheduler = CronTab(user='Work')
#creating a new cron job with the scheduler
job = jobScheduler.new(command=r'python3 C:\Users\Work\Desktop\projects\skyanalytics\download.py')
#schedule the job
job.setall("0 17 * * *")
jobScheduler.write()