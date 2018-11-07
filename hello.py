from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify
import atexit
import os
import json

from functions import *
from multiprocessing.pool import ThreadPool
import time
import dropbox


app = Flask(__name__, static_url_path='')

db_name = 'mydb'
client = None
db = None

if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    print('Found VCAP_SERVICES')
    if 'cloudantNoSQLDB' in vcap:
        creds = vcap['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
elif "CLOUDANT_URL" in os.environ:
    client = Cloudant(os.environ['CLOUDANT_USERNAME'], os.environ['CLOUDANT_PASSWORD'], url=os.environ['CLOUDANT_URL'], connect=True)
    db = client.create_database(db_name, throw_on_exists=False)
elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print('Found local VCAP_SERVICES')
        creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))


@app.route('/')
def root():
    return 'Hello World IBM!'


@app.route('/aproximation_local_machine/<int:n_points>')
def aproximation_local_machine(n_points):
    start = time.time()

    number_points = aproximation_pi(n_points)
    t = number_points/n_points
    pi = t * 4.0

    end = time.time()  
    return '<html><body> ' + 'Time: '+ str(float(end) - float(start)) +'<br>'+ 'Value: ' + str(pi) + '</body></html>'



@app.route('/aproximation_one_workers')
def aproximation_one_workers():
    start = time.time()
    pool_1 = ThreadPool(processes=1)

    # Create two threads as follows
    try:
        np_1 = pool_1.apply_async(parallel_work, ('https://test-71413.appspot.com/aproximation_worker/10000000',)) # tuple of args for foo
    except:
        print ("Error: unable to start thread")

    total = 10000000
    t = float(np_1.get())/total
    pi = t * 4

    end = time.time()  
    return '<html><body> ' + 'Time: '+ str(float(end) - float(start)) +'<br>'+ 'Value: ' + str(pi) + '</body></html>'





@app.route('/aproximation_two_workers')
def aproximation_two_workers():
    start = time.time()
    pool_1 = ThreadPool(processes=1)
    pool_2 = ThreadPool(processes=1)

    # Create two threads as follows
    try:
        np_1 = pool_1.apply_async(parallel_work, ('https://test-71413.appspot.com/aproximation_worker/5000000',)) # tuple of args for foo
        np_2 = pool_2.apply_async(parallel_work, ('https://gcloud-37575.appspot.com/aproximation_worker/5000000',)) # tuple of args for foo
    except:
        print ("Error: unable to start thread")

    total = 5000000*2
    t = (float(np_1.get()) + float(np_2.get()))/total
    pi = t * 4

    end = time.time()  
    return '<html><body> ' + 'Time: '+ str(float(end) - float(start)) +'<br>'+ 'Value: ' + str(pi) + '</body></html>'



@app.route('/aproximation_three_workers')
def aproximation_three_workers():
    start = time.time()
    pool_1 = ThreadPool(processes=1)
    pool_2 = ThreadPool(processes=1)
    pool_3 = ThreadPool(processes=1)
    # Create two threads as follows
    try:
        np_1 = pool_1.apply_async(parallel_work, ('https://test-71413.appspot.com/aproximation_worker/3333333',)) # tuple of args for foo
        np_2 = pool_2.apply_async(parallel_work, ('https://gcloud-37575.appspot.com/aproximation_worker/3333333',)) # tuple of args for foo
        np_3 = pool_3.apply_async(parallel_work, ('https://worker3-56911.appspot.com/aproximation_worker/3333333',)) # tuple of args for foo
    except:
        print ("Error: unable to start thread")

    total = 3333333*3
    t = (float(np_1.get()) + float(np_2.get()) +  float(np_3.get()))/total
    pi = t * 4

    end = time.time()  
    return '<html><body> ' + 'Time: '+ str(float(end) - float(start)) +'<br>'+ 'Value: ' + str(pi) + '</body></html>'





@app.route('/aproximation_four_workers')
def aproximation_four_workers():
    start = time.time()
    pool_1 = ThreadPool(processes=1)
    pool_2 = ThreadPool(processes=1)
    pool_3 = ThreadPool(processes=1)
    pool_4 = ThreadPool(processes=1)
    # Create two threads as follows
    try:
        np_1 = pool_1.apply_async(parallel_work, ('https://test-71413.appspot.com/aproximation_worker/2500000',)) # tuple of args for foo
        np_2 = pool_2.apply_async(parallel_work, ('https://gcloud-37575.appspot.com/aproximation_worker/2500000',)) # tuple of args for foo
        np_3 = pool_3.apply_async(parallel_work, ('https://worker3-56911.appspot.com/aproximation_worker/2500000',)) # tuple of args for foo
        np_4 = pool_4.apply_async(parallel_work, ('https://worker4-79065.appspot.com/aproximation_worker/2500000',)) # tuple of args for foo
    except:
        print ("Error: unable to start thread")

    total = 2500000*4
    t = (float(np_1.get()) + float(np_2.get()) + float(np_3.get()) + float(np_4.get()))/total
    pi = t * 4

    end = time.time()  
    return '<html><body> ' + 'Time: '+ str(float(end) - float(start)) +'<br>'+ 'Value: ' + str(pi) + '</body></html>'



@app.route('/aproximation_five_workers')
def aproximation_five_workers():
    start = time.time()
    pool_1 = ThreadPool(processes=1)
    pool_2 = ThreadPool(processes=1)
    pool_3 = ThreadPool(processes=1)
    pool_4 = ThreadPool(processes=1)
    pool_5 = ThreadPool(processes=1)
    # Create two threads as follows
    try:
        np_1 = pool_1.apply_async(parallel_work, ('https://test-71413.appspot.com/aproximation_worker/2000000',)) # tuple of args for foo
        np_2 = pool_2.apply_async(parallel_work, ('https://gcloud-37575.appspot.com/aproximation_worker/2000000',)) # tuple of args for foo
        np_3 = pool_3.apply_async(parallel_work, ('https://worker3-56911.appspot.com/aproximation_worker/2000000',)) # tuple of args for foo
        np_4 = pool_4.apply_async(parallel_work, ('https://worker4-79065.appspot.com/aproximation_worker/2000000',)) # tuple of args for foo
        np_5 = pool_5.apply_async(parallel_work, ('https://worker5-75515.appspot.com/aproximation_worker/2000000',)) # tuple of args for foo
    except:
        print ("Error: unable to start thread")

    total = 2000000*5
    t = (float(np_1.get()) + float(np_2.get()) + float(np_3.get()) + float(np_4.get()) + float(np_5.get()))/total
    pi = t * 4

    end = time.time()  
    return '<html><body> ' + 'Time: '+ str(float(end) - float(start)) +'<br>'+ 'Value: ' + str(pi) + '</body></html>'


@app.route('/aproximation_six_workers')
def aproximation_six_workers():
    start = time.time()
    pool_1 = ThreadPool(processes=1)
    pool_2 = ThreadPool(processes=1)
    pool_3 = ThreadPool(processes=1)
    pool_4 = ThreadPool(processes=1)
    pool_5 = ThreadPool(processes=1)
    pool_6 = ThreadPool(processes=1)
    # Create two threads as follows
    try:
        np_1 = pool_1.apply_async(parallel_work, ('https://test-71413.appspot.com/aproximation_worker/1666666',)) # tuple of args for foo
        np_2 = pool_2.apply_async(parallel_work, ('https://gcloud-37575.appspot.com/aproximation_worker/1666666',)) # tuple of args for foo
        np_3 = pool_3.apply_async(parallel_work, ('https://worker3-56911.appspot.com/aproximation_worker/1666666',)) # tuple of args for foo
        np_4 = pool_4.apply_async(parallel_work, ('https://worker4-79065.appspot.com/aproximation_worker/1666666',)) # tuple of args for foo
        np_5 = pool_5.apply_async(parallel_work, ('https://worker5-75515.appspot.com/aproximation_worker/1666666',)) # tuple of args for foo
        np_6 = pool_6.apply_async(parallel_work, ('https://worker6-99278.appspot.com//aproximation_worker/1666666',)) # tuple of args for foo
    except:
        print ("Error: unable to start thread")

    total = 1666666*6
    t = (float(np_1.get()) + float(np_2.get()) + float(np_3.get()) + float(np_4.get()) + float(np_5.get()) + float(np_6.get()))/total
    pi = t * 4

    end = time.time()  
    return '<html><body> ' + 'Time: '+ str(float(end) - float(start)) +'<br>'+ 'Value: ' + str(pi) + '</body></html>'



@app.route('/aproximation_seven_workers')
def aproximation_seven_workers():
    start = time.time()
    pool_1 = ThreadPool(processes=1)
    pool_2 = ThreadPool(processes=1)
    pool_3 = ThreadPool(processes=1)
    pool_4 = ThreadPool(processes=1)
    pool_5 = ThreadPool(processes=1)
    pool_6 = ThreadPool(processes=1)
    pool_7 = ThreadPool(processes=1)
    # Create two threads as follows
    try:
        np_1 = pool_1.apply_async(parallel_work, ('https://test-71413.appspot.com/aproximation_worker/1428571',)) # tuple of args for foo
        np_2 = pool_2.apply_async(parallel_work, ('https://gcloud-37575.appspot.com/aproximation_worker/1428571',)) # tuple of args for foo
        np_3 = pool_3.apply_async(parallel_work, ('https://worker3-56911.appspot.com/aproximation_worker/1428571',)) # tuple of args for foo
        np_4 = pool_4.apply_async(parallel_work, ('https://worker4-79065.appspot.com/aproximation_worker/1428571',)) # tuple of args for foo
        np_5 = pool_5.apply_async(parallel_work, ('https://worker5-75515.appspot.com/aproximation_worker/1428571',)) # tuple of args for foo
        np_6 = pool_6.apply_async(parallel_work, ('https://worker6-99278.appspot.com/aproximation_worker/1428571',)) # tuple of args for foo
        np_7 = pool_7.apply_async(parallel_work, ('https://worker7-77738.appspot.com/aproximation_worker/1428571',)) # tuple of args for foo
    except:
        print ("Error: unable to start thread")

    total = 1428571*7
    t = (float(np_1.get()) + float(np_2.get()) + float(np_3.get()) + float(np_4.get()) + float(np_5.get()) + float(np_6.get()) + float(np_7.get()))/total
    pi = t * 4

    end = time.time()  
    return '<html><body> ' + 'Time: '+ str(float(end) - float(start)) +'<br>'+ 'Value: ' + str(pi) + '</body></html>'


@app.route('/aproximation_eight_workers')
def aproximation_eight_workers():
    start = time.time()
    pool_1 = ThreadPool(processes=1)
    pool_2 = ThreadPool(processes=1)
    pool_3 = ThreadPool(processes=1)
    pool_4 = ThreadPool(processes=1)
    pool_5 = ThreadPool(processes=1)
    pool_6 = ThreadPool(processes=1)
    pool_7 = ThreadPool(processes=1)
    pool_8 = ThreadPool(processes=1)
    # Create two threads as follows
    try:
        np_1 = pool_1.apply_async(parallel_work, ('https://test-71413.appspot.com/aproximation_worker/1250000',)) # tuple of args for foo
        np_2 = pool_2.apply_async(parallel_work, ('https://gcloud-37575.appspot.com/aproximation_worker/1250000',)) # tuple of args for foo
        np_3 = pool_3.apply_async(parallel_work, ('https://worker3-56911.appspot.com/aproximation_worker/1250000',)) # tuple of args for foo
        np_4 = pool_4.apply_async(parallel_work, ('https://worker4-79065.appspot.com/aproximation_worker/1250000',)) # tuple of args for foo
        np_5 = pool_5.apply_async(parallel_work, ('https://worker5-75515.appspot.com/aproximation_worker/1250000',)) # tuple of args for foo
        np_6 = pool_6.apply_async(parallel_work, ('https://worker6-99278.appspot.com/aproximation_worker/1250000',)) # tuple of args for foo
        np_7 = pool_7.apply_async(parallel_work, ('https://worker7-77738.appspot.com/aproximation_worker/1250000',)) # tuple of args for foo
        np_8 = pool_8.apply_async(parallel_work, ('https://worker8-35692.appspot.com/aproximation_worker/1250000',)) # tuple of args for foo
    except:
        print ("Error: unable to start thread")

    total = 1250000*8
    t = (float(np_1.get()) + float(np_2.get()) + float(np_3.get()) + float(np_4.get()) + float(np_5.get()) + float(np_6.get()) + float(np_7.get()) + float(np_8.get()))/total
    pi = t * 4

    end = time.time()  
    return '<html><body> ' + 'Time: '+ str(float(end) - float(start)) +'<br>'+ 'Value: ' + str(pi) + '</body></html>'



@app.route('/aproximation_nine_workers')
def aproximation_nine_workers():
    start = time.time()
    pool_1 = ThreadPool(processes=1)
    pool_2 = ThreadPool(processes=1)
    pool_3 = ThreadPool(processes=1)
    pool_4 = ThreadPool(processes=1)
    pool_5 = ThreadPool(processes=1)
    pool_6 = ThreadPool(processes=1)
    pool_7 = ThreadPool(processes=1)
    pool_8 = ThreadPool(processes=1)
    pool_9 = ThreadPool(processes=1)
    # Create two threads as follows
    try:
        np_1 = pool_1.apply_async(parallel_work, ('https://test-71413.appspot.com/aproximation_worker/1111111',)) # tuple of args for foo
        np_2 = pool_2.apply_async(parallel_work, ('https://gcloud-37575.appspot.com/aproximation_worker/1111111',)) # tuple of args for foo
        np_3 = pool_3.apply_async(parallel_work, ('https://worker3-56911.appspot.com/aproximation_worker/1111111',)) # tuple of args for foo
        np_4 = pool_4.apply_async(parallel_work, ('https://worker4-79065.appspot.com/aproximation_worker/1111111',)) # tuple of args for foo
        np_5 = pool_5.apply_async(parallel_work, ('https://worker5-75515.appspot.com/aproximation_worker/1111111',)) # tuple of args for foo
        np_6 = pool_6.apply_async(parallel_work, ('https://worker6-99278.appspot.com/aproximation_worker/1111111',)) # tuple of args for foo
        np_7 = pool_7.apply_async(parallel_work, ('https://worker7-77738.appspot.com/aproximation_worker/1111111',)) # tuple of args for foo
        np_8 = pool_8.apply_async(parallel_work, ('https://worker8-35692.appspot.com/aproximation_worker/1111111',)) # tuple of args for foo
        np_9 = pool_9.apply_async(parallel_work, ('https://worker9-51543.appspot.com/aproximation_worker/1111111',)) # tuple of args for foo
    except:
        print ("Error: unable to start thread")

    total = 1111111*9
    t = (float(np_1.get()) + float(np_2.get()) + float(np_3.get()) + float(np_4.get()) + float(np_5.get()) + float(np_6.get()) + float(np_7.get()) + float(np_8.get()) + float(np_9.get()))/total
    pi = t * 4

    end = time.time()  
    return '<html><body> ' + 'Time: '+ str(float(end) - float(start)) +'<br>'+ 'Value: ' + str(pi) + '</body></html>'


@app.route('/aproximation_ten_workers')
def aproximation_ten_workers():
    start = time.time()
    pool_1 = ThreadPool(processes=1)
    pool_2 = ThreadPool(processes=1)
    pool_3 = ThreadPool(processes=1)
    pool_4 = ThreadPool(processes=1)
    pool_5 = ThreadPool(processes=1)
    pool_6 = ThreadPool(processes=1)
    pool_7 = ThreadPool(processes=1)
    pool_8 = ThreadPool(processes=1)
    pool_9 = ThreadPool(processes=1)
    pool_10 = ThreadPool(processes=1)
    # Create two threads as follows
    try:
        np_1 = pool_1.apply_async(parallel_work, ('https://test-71413.appspot.com/aproximation_worker/1000000',)) # tuple of args for foo
        np_2 = pool_2.apply_async(parallel_work, ('https://gcloud-37575.appspot.com/aproximation_worker/1000000',)) # tuple of args for foo
        np_3 = pool_3.apply_async(parallel_work, ('https://worker3-56911.appspot.com/aproximation_worker/1000000',)) # tuple of args for foo
        np_4 = pool_4.apply_async(parallel_work, ('https://worker4-79065.appspot.com/aproximation_worker/1000000',)) # tuple of args for foo
        np_5 = pool_5.apply_async(parallel_work, ('https://worker5-75515.appspot.com/aproximation_worker/1000000',)) # tuple of args for foo
        np_6 = pool_6.apply_async(parallel_work, ('https://worker6-99278.appspot.com/aproximation_worker/1000000',)) # tuple of args for foo
        np_7 = pool_7.apply_async(parallel_work, ('https://worker7-77738.appspot.com/aproximation_worker/1000000',)) # tuple of args for foo
        np_8 = pool_8.apply_async(parallel_work, ('https://worker8-35692.appspot.com/aproximation_worker/1000000',)) # tuple of args for foo
        np_9 = pool_9.apply_async(parallel_work, ('https://worker9-51543.appspot.com/aproximation_worker/1000000',)) # tuple of args for foo
        np_10 = pool_10.apply_async(parallel_work, ('https://worker10-65182.appspot.com/aproximation_worker/1000000',)) # tuple of args for foo
    except:
        print ("Error: unable to start thread")

    total = 1000000*10
    t = (float(np_1.get()) + float(np_2.get()) + float(np_3.get()) + float(np_4.get()) + float(np_5.get()) + float(np_6.get()) + float(np_7.get()) + float(np_8.get()) + float(np_9.get()) + float(np_10.get()))/total
    pi = t * 4

    end = time.time()  
    return '<html><body> ' + 'Time: '+ str(float(end) - float(start)) +'<br>'+ 'Value: ' + str(pi) + '</body></html>'





@app.route('/aproximation_eleven_workers')
def aproximation_eleven_workers():
    start = time.time()
    pool_1 = ThreadPool(processes=1)
    pool_2 = ThreadPool(processes=1)
    pool_3 = ThreadPool(processes=1)
    pool_4 = ThreadPool(processes=1)
    pool_5 = ThreadPool(processes=1)
    pool_6 = ThreadPool(processes=1)
    pool_7 = ThreadPool(processes=1)
    pool_8 = ThreadPool(processes=1)
    pool_9 = ThreadPool(processes=1)
    pool_10 = ThreadPool(processes=1)
    pool_11 = ThreadPool(processes=1)
    # Create two threads as follows
    try:
        np_1 = pool_1.apply_async(parallel_work, ('https://test-71413.appspot.com/aproximation_worker/909090',)) # tuple of args for foo
        np_2 = pool_2.apply_async(parallel_work, ('https://gcloud-37575.appspot.com/aproximation_worker/909090',)) # tuple of args for foo
        np_3 = pool_3.apply_async(parallel_work, ('https://worker3-56911.appspot.com/aproximation_worker/909090',)) # tuple of args for foo
        np_4 = pool_4.apply_async(parallel_work, ('https://worker4-79065.appspot.com/aproximation_worker/909090',)) # tuple of args for foo
        np_5 = pool_5.apply_async(parallel_work, ('https://worker5-75515.appspot.com/aproximation_worker/909090',)) # tuple of args for foo
        np_6 = pool_6.apply_async(parallel_work, ('https://worker6-99278.appspot.com/aproximation_worker/909090',)) # tuple of args for foo
        np_7 = pool_7.apply_async(parallel_work, ('https://worker7-77738.appspot.com/aproximation_worker/909090',)) # tuple of args for foo
        np_8 = pool_8.apply_async(parallel_work, ('https://worker8-35692.appspot.com/aproximation_worker/909090',)) # tuple of args for foo
        np_9 = pool_9.apply_async(parallel_work, ('https://worker9-51543.appspot.com/aproximation_worker/909090',)) # tuple of args for foo
        np_10 = pool_10.apply_async(parallel_work, ('https://worker10-65182.appspot.com/aproximation_worker/909090',)) # tuple of args for foo
        np_11 = pool_11.apply_async(parallel_work, ('https://worker11-81873.appspot.com/aproximation_worker/909090',)) # tuple of args for foo
    except:
        print ("Error: unable to start thread")

    total = 909090*11
    t = (float(np_1.get()) + float(np_2.get()) + float(np_3.get()) + float(np_4.get()) + float(np_5.get()) + float(np_6.get()) + float(np_7.get()) + float(np_8.get()) + float(np_9.get()) + float(np_10.get()) + float(np_11.get()))/total
    pi = t * 4

    end = time.time()  
    return '<html><body> ' + 'Time: '+ str(float(end) - float(start)) +'<br>'+ 'Value: ' + str(pi) + '</body></html>'



@app.route('/aproximation_twelve_workers')
def aproximation_twelve_workers():
    start = time.time()
    pool_1 = ThreadPool(processes=1)
    pool_2 = ThreadPool(processes=1)
    pool_3 = ThreadPool(processes=1)
    pool_4 = ThreadPool(processes=1)
    pool_5 = ThreadPool(processes=1)
    pool_6 = ThreadPool(processes=1)
    pool_7 = ThreadPool(processes=1)
    pool_8 = ThreadPool(processes=1)
    pool_9 = ThreadPool(processes=1)
    pool_10 = ThreadPool(processes=1)
    pool_11 = ThreadPool(processes=1)
    pool_12 = ThreadPool(processes=1)
    # Create two threads as follows
    try:
        np_1 = pool_1.apply_async(parallel_work, ('https://test-71413.appspot.com/aproximation_worker/833333',)) # tuple of args for foo
        np_2 = pool_2.apply_async(parallel_work, ('https://gcloud-37575.appspot.com/aproximation_worker/833333',)) # tuple of args for foo
        np_3 = pool_3.apply_async(parallel_work, ('https://worker3-56911.appspot.com/aproximation_worker/833333',)) # tuple of args for foo
        np_4 = pool_4.apply_async(parallel_work, ('https://worker4-79065.appspot.com/aproximation_worker/833333',)) # tuple of args for foo
        np_5 = pool_5.apply_async(parallel_work, ('https://worker5-75515.appspot.com/aproximation_worker/833333',)) # tuple of args for foo
        np_6 = pool_6.apply_async(parallel_work, ('https://worker6-99278.appspot.com/aproximation_worker/833333',)) # tuple of args for foo
        np_7 = pool_7.apply_async(parallel_work, ('https://worker7-77738.appspot.com/aproximation_worker/833333',)) # tuple of args for foo
        np_8 = pool_8.apply_async(parallel_work, ('https://worker8-35692.appspot.com/aproximation_worker/833333',)) # tuple of args for foo
        np_9 = pool_9.apply_async(parallel_work, ('https://worker9-51543.appspot.com/aproximation_worker/833333',)) # tuple of args for foo
        np_10 = pool_10.apply_async(parallel_work, ('https://worker10-65182.appspot.com/aproximation_worker/833333',)) # tuple of args for foo
        np_11 = pool_11.apply_async(parallel_work, ('https://worker11-81873.appspot.com/aproximation_worker/833333',)) # tuple of args for foo
        np_12 = pool_12.apply_async(parallel_work, ('https://worker12-68759.appspot.com/aproximation_worker/833333',)) # tuple of args for foo
    except:
        print ("Error: unable to start thread")

    total = 833333*12
    t = (float(np_1.get()) + float(np_2.get()) + float(np_3.get()) + float(np_4.get()) + float(np_5.get()) + float(np_6.get()) + float(np_7.get()) + float(np_8.get()) + float(np_9.get()) + float(np_10.get()) + float(np_11.get()) + float(np_12.get()))/total
    pi = t * 4

    end = time.time()  
    return '<html><body> ' + 'Time: '+ str(float(end) - float(start)) +'<br>'+ 'Value: ' + str(pi) + '</body></html>'




@app.route('/aproximation_thirteen_workers')
def aproximation_thirteen_workers():
    start = time.time()
    pool_1 = ThreadPool(processes=1)
    pool_2 = ThreadPool(processes=1)
    pool_3 = ThreadPool(processes=1)
    pool_4 = ThreadPool(processes=1)
    pool_5 = ThreadPool(processes=1)
    pool_6 = ThreadPool(processes=1)
    pool_7 = ThreadPool(processes=1)
    pool_8 = ThreadPool(processes=1)
    pool_9 = ThreadPool(processes=1)
    pool_10 = ThreadPool(processes=1)
    pool_11 = ThreadPool(processes=1)
    pool_12 = ThreadPool(processes=1)
    pool_13 = ThreadPool(processes=1)
    # Create two threads as follows
    try:
        np_1 = pool_1.apply_async(parallel_work, ('https://test-71413.appspot.com/aproximation_worker/769230',)) # tuple of args for foo
        np_2 = pool_2.apply_async(parallel_work, ('https://gcloud-37575.appspot.com/aproximation_worker/769230',)) # tuple of args for foo
        np_3 = pool_3.apply_async(parallel_work, ('https://worker3-56911.appspot.com/aproximation_worker/769230',)) # tuple of args for foo
        np_4 = pool_4.apply_async(parallel_work, ('https://worker4-79065.appspot.com/aproximation_worker/769230',)) # tuple of args for foo
        np_5 = pool_5.apply_async(parallel_work, ('https://worker5-75515.appspot.com/aproximation_worker/769230',)) # tuple of args for foo
        np_6 = pool_6.apply_async(parallel_work, ('https://worker6-99278.appspot.com/aproximation_worker/769230',)) # tuple of args for foo
        np_7 = pool_7.apply_async(parallel_work, ('https://worker7-77738.appspot.com/aproximation_worker/769230',)) # tuple of args for foo
        np_8 = pool_8.apply_async(parallel_work, ('https://worker8-35692.appspot.com/aproximation_worker/769230',)) # tuple of args for foo
        np_9 = pool_9.apply_async(parallel_work, ('https://worker9-51543.appspot.com/aproximation_worker/769230',)) # tuple of args for foo
        np_10 = pool_10.apply_async(parallel_work, ('https://worker10-65182.appspot.com/aproximation_worker/769230',)) # tuple of args for foo
        np_11 = pool_11.apply_async(parallel_work, ('https://worker11-81873.appspot.com/aproximation_worker/769230',)) # tuple of args for foo
        np_12 = pool_12.apply_async(parallel_work, ('https://worker12-68759.appspot.com/aproximation_worker/769230',)) # tuple of args for foo
        np_13 = pool_13.apply_async(parallel_work, ('https://worker13-26221.appspot.com/aproximation_worker/769230',)) # tuple of args for foo
    except:
        print ("Error: unable to start thread")

    total = 769230*13
    t = (float(np_1.get()) + float(np_2.get()) + float(np_3.get()) + float(np_4.get()) + float(np_5.get()) + float(np_6.get()) + float(np_7.get()) + float(np_8.get()) + float(np_9.get()) + float(np_10.get()) + float(np_11.get()) + float(np_12.get()) + float(np_13.get()))/total
    pi = t * 4

    end = time.time()  
    return '<html><body> ' + 'Time: '+ str(float(end) - float(start)) +'<br>'+ 'Value: ' + str(pi) + '</body></html>'




@app.route('/integration_local_machine')
def integration_local_machine():
    start = time.time()

    integrated_value = integration_exp(1000000, 0.0, 12.0)

    end = time.time()  
    return '<html><body> ' + 'Time: '+ str(float(end) - float(start)) +'<br>'+ 'Integrated value: ' + str(integrated_value) + '</body></html>'



@app.route('/integration_two_workers')
def integration_two_workers():
    start = time.time()
    pool_1 = ThreadPool(processes=1)
    pool_2 = ThreadPool(processes=1)

    # Create two threads as follows
    try:
        np_1 = pool_1.apply_async(parallel_work, ('https://test-71413.appspot.com/integration_worker/1000000/0.0/1.0',)) # tuple of args for foo
        np_2 = pool_2.apply_async(parallel_work, ('https://gcloud-37575.appspot.com/integration_worker/1000000/0.0/1.0',)) # tuple of args for foo
    except:
        print ("Error: unable to start thread")

    integrated_value = (float(np_1.get()) + float(np_2.get()))

    end = time.time()  
    return '<html><body> '  + 'Time: '+ str(float(end) - float(start)) +'<br>'+ 'Integrated value: ' + str(integrated_value) + '</body></html>'



@app.route('/integration_three_workers')
def integration_three_workers():
    start = time.time()
    pool_1 = ThreadPool(processes=1)
    pool_2 = ThreadPool(processes=1)
    pool_3 = ThreadPool(processes=1)

    # Create two threads as follows
    try:
        np_1 = pool_1.apply_async(parallel_work, ('https://test-71413.appspot.com/integration_worker/1000000/0.0/1.0',)) # tuple of args for foo
        np_2 = pool_2.apply_async(parallel_work, ('https://gcloud-37575.appspot.com/integration_worker/1000000/0.0/1.0',)) # tuple of args for foo
        np_3 = pool_3.apply_async(parallel_work, ('https://gcloud-37575.appspot.com/integration_worker/1000000/0.0/1.0',)) # tuple of args for foo
    except:
        print ("Error: unable to start thread")

    integrated_value = (float(np_1.get()) + float(np_2.get()) + float(np_3.get()))

    end = time.time()  
    return '<html><body> '  + 'Time: '+ str(float(end) - float(start)) +'<br>'+ 'Integrated value: ' + str(integrated_value) + '</body></html>'



@app.route('/integration_four_workers')
def integration_four_workers():
    start = time.time()
    pool_1 = ThreadPool(processes=1)
    pool_2 = ThreadPool(processes=1)
    pool_3 = ThreadPool(processes=1)
    pool_4 = ThreadPool(processes=1)

    # Create two threads as follows
    try:
        np_1 = pool_1.apply_async(parallel_work, ('https://test-71413.appspot.com/integration_worker/1000000/0.0/1.0',)) # tuple of args for foo
        np_2 = pool_2.apply_async(parallel_work, ('https://gcloud-37575.appspot.com/integration_worker/1000000/0.0/1.0',)) # tuple of args for foo
        np_3 = pool_3.apply_async(parallel_work, ('https://gcloud-37575.appspot.com/integration_worker/1000000/0.0/1.0',)) # tuple of args for foo
        np_4 = pool_4.apply_async(parallel_work, ('https://gcloud-37575.appspot.com/integration_worker/1000000/0.0/1.0',)) # tuple of args for foo
    except:
        print ("Error: unable to start thread")

    integrated_value = (float(np_1.get()) + float(np_2.get()) + float(np_3.get()) + float(np_4.get()))

    end = time.time()  
    return '<html><body> '  + 'Time: '+ str(float(end) - float(start)) +'<br>'+ 'Integrated value: ' + str(integrated_value) + '</body></html>'



@app.route('/integration_five_workers')
def integration_five_workers():
    start = time.time()
    pool_1 = ThreadPool(processes=1)
    pool_2 = ThreadPool(processes=1)
    pool_3 = ThreadPool(processes=1)
    pool_4 = ThreadPool(processes=1)
    pool_5 = ThreadPool(processes=1)

    # Create two threads as follows
    try:
        np_1 = pool_1.apply_async(parallel_work, ('https://test-71413.appspot.com/integration_worker/1000000/0.0/1.0',)) # tuple of args for foo
        np_2 = pool_2.apply_async(parallel_work, ('https://gcloud-37575.appspot.com/integration_worker/1000000/0.0/1.0',)) # tuple of args for foo
        np_3 = pool_3.apply_async(parallel_work, ('https://gcloud-37575.appspot.com/integration_worker/1000000/0.0/1.0',)) # tuple of args for foo
        np_4 = pool_4.apply_async(parallel_work, ('https://gcloud-37575.appspot.com/integration_worker/1000000/0.0/1.0',)) # tuple of args for foo
        np_5 = pool_5.apply_async(parallel_work, ('https://gcloud-37575.appspot.com/integration_worker/1000000/0.0/1.0',)) # tuple of args for foo
    except:
        print ("Error: unable to start thread")

    integrated_value = (float(np_1.get()) + float(np_2.get()) + float(np_3.get()) + float(np_4.get()) + float(np_5.get()))

    end = time.time()  
    return '<html><body> '  + 'Time: '+ str(float(end) - float(start)) +'<br>'+ 'Integrated value: ' + str(integrated_value) + '</body></html>'





@app.route('/aproximation_storage')
def aproximation_storage():
    dbx = dropbox.Dropbox('1YMC8yjIDW8AAAAAAAAAj0qjLQHR5MQtek52CxmkzqELw9Inrmx5hKBzN_FDWAEb')

    pool_1 = ThreadPool(processes=1)
    pool_2 = ThreadPool(processes=1)
    pool_3 = ThreadPool(processes=1)
    pool_4 = ThreadPool(processes=1)
    pool_5 = ThreadPool(processes=1)
    pool_6 = ThreadPool(processes=1)
    pool_7 = ThreadPool(processes=1)
    pool_8 = ThreadPool(processes=1)
    pool_9 = ThreadPool(processes=1)
    pool_10 = ThreadPool(processes=1)
    # Create two threads as follows
    try:
        np_1 = pool_1.apply_async(parallel_work, ('https://test-71413.appspot.com/aproximation_worker/1000000',)) # tuple of args for foo
        np_2 = pool_2.apply_async(parallel_work, ('https://gcloud-37575.appspot.com/aproximation_worker/1000000',)) # tuple of args for foo
        np_3 = pool_3.apply_async(parallel_work, ('https://worker3-56911.appspot.com/aproximation_worker/1000000',)) # tuple of args for foo
        np_4 = pool_4.apply_async(parallel_work, ('https://worker4-79065.appspot.com/aproximation_worker/1000000',)) # tuple of args for foo
        np_5 = pool_5.apply_async(parallel_work, ('https://worker5-75515.appspot.com/aproximation_worker/1000000',)) # tuple of args for foo
        np_6 = pool_6.apply_async(parallel_work, ('https://worker6-99278.appspot.com/aproximation_worker/1000000',)) # tuple of args for foo
        np_7 = pool_7.apply_async(parallel_work, ('https://worker7-77738.appspot.com/aproximation_worker/1000000',)) # tuple of args for foo
        np_8 = pool_8.apply_async(parallel_work, ('https://worker8-35692.appspot.com/aproximation_worker/1000000',)) # tuple of args for foo
        np_9 = pool_9.apply_async(parallel_work, ('https://worker9-51543.appspot.com/aproximation_worker/1000000',)) # tuple of args for foo
        np_10 = pool_10.apply_async(parallel_work, ('https://worker10-65182.appspot.com/aproximation_worker/1000000',)) # tuple of args for foo
    except:
        print ("Error: unable to start thread")

    file = open('aprox_pi.txt', 'w')
    file.write(str(np_1.get()) + '\t')
    file.write(str(np_2.get()) + '\t')
    file.write(str(np_3.get()) + '\t')
    file.write(str(np_4.get()) + '\t')
    file.write(str(np_5.get()) + '\t')
    file.write(str(np_6.get()) + '\t')
    file.write(str(np_7.get()) + '\t')
    file.write(str(np_8.get()) + '\t')
    file.write(str(np_9.get()) + '\t')
    file.write(str(np_10.get()) + '\t')
    file.close()

    with open("aprox_pi.txt", "rb") as f:
        dbx.files_upload(f.read(), '/aprox_pi.txt', autorename=False, client_modified=None, mute=False)

    return '<html><body>' + 'Success values saved in Dropbox!' + '</body></html>'


@app.route('/aproximation_query')
def aproximation_query():

    start = time.time()
    dbx = dropbox.Dropbox('1YMC8yjIDW8AAAAAAAAAj0qjLQHR5MQtek52CxmkzqELw9Inrmx5hKBzN_FDWAEb')
    md, res = dbx.files_download('/aprox_pi.txt')

    floats = [float(x) for x in str(res.content).split()]

    t = sum(floats)/10000000.0
    pi = t*4

    end = time.time()  
    return '<html><body> Pi value retrived from Dropbox is ' + str(pi) + ' Time: '+ str(float(end) - float(start)) + '</body></html>'


    

# /* Endpoint to greet and add a new visitor to database.
# * Send a POST request to localhost:8000/api/visitors with body
# * {
# *     "name": "Bob"
# * }
# */
@app.route('/api/visitors', methods=['GET'])
def get_visitor():
    if client:
        return jsonify(list(map(lambda doc: doc['name'], db)))
    else:
        print('No database')
        return jsonify([])

# /**
#  * Endpoint to get a JSON array of all the visitors in the database
#  * REST API example:
#  * <code>
#  * GET http://localhost:8000/api/visitors
#  * </code>
#  *
#  * Response:
#  * [ "Bob", "Jane" ]
#  * @return An array of all the visitor names
#  */
@app.route('/api/visitors', methods=['POST'])
def put_visitor():
    user = request.json['name']
    data = {'name':user}
    if client:
        my_document = db.create_document(data)
        data['_id'] = my_document['_id']
        return jsonify(data)
    else:
        print('No database')
        return jsonify(data)

@atexit.register
def shutdown():
    if client:
        client.disconnect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
