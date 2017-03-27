#!/usr/bin/python
# -*- coding: utf-8 -*-
# This algorithm water counter in the house.
# Needs to work on the counter with a reed switch.
# I used the Raspberry Pi 2B
# email: rva.moscow@gmail.com

if __name__ == '__main__':

    import RPi.GPIO as GPIO
    import time
    import sqlite3
    import smtplib

    OUT_C = 11
    OUT_H = 12
    IN_C = 15
    IN_H = 16

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(OUT_H, GPIO.OUT, initial=False)
    GPIO.setup(OUT_C, GPIO.OUT, initial=False)
    GPIO.setup(IN_H, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(IN_C, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    DB = 'counter.db'


    def create_table_counter_hot():
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS table_counter_hot(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT,
            value INTEGER,
            correction BLOB
            )''')
        con.commit()
        cur.close()
        con.close()


    def create_table_counter_cold():
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS table_counter_cold(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT,
            value INTEGER,
            correction BLOB
            )''')
        con.commit()
        cur.close()
        con.close()


    def create_table_restart():
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS table_restart(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT
            )''')
        con.commit()
        cur.close()
        con.close()


    def create_table_days():
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS table_days(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            value_hot INTEGER,
            value_cold INTEGER,
            difference_hot INTEGER,
            difference_cold INTEGER
            )''')
        con.commit()
        cur.close()
        con.close()


    def time_restart():
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute('''INSERT INTO table_restart (datetime) VALUES (?)''',
            (time.strftime('%Y-%m-%d %H:%M:%S'),))
        con.commit()
        cur.close()
        con.close()


    def write_value_H():
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute('''SELECT MAX(id),
            datetime, value
            FROM table_counter_hot
            ''')
        data = cur.fetchone()
        cur.execute('''INSERT INTO table_counter_hot (datetime, value) VALUES (?,?)''',
            (time.strftime('%Y-%m-%d %H:%M:%S'), 0 if data[2] is None else data[2] + 1))
        print('Hot  - ', 0 if data[2] is None else data[2] + 1, 'liters')
        con.commit()
        cur.close()
        con.close()


    def write_value_C():
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute('''SELECT MAX(id),
            datetime, value
            FROM table_counter_cold
            ''')
        data = cur.fetchone()
        cur.execute('''INSERT INTO table_counter_cold (datetime, value) VALUES (?,?)''',
            (time.strftime('%Y-%m-%d %H:%M:%S'), 0 if data[2] is None else data[2] + 1))
        print('cold - ', 0 if data[2] is None else data[2] + 1, 'liters')
        con.commit()
        cur.close()
        con.close()


    def create_all_table():
        create_table_counter_hot()
        create_table_counter_cold()
        create_table_days()
        create_table_restart()
        time_restart()


    def correction():
        while True:
            inp_1 = input('Do you want to make changes to the counters? (Y/N):')
            if inp_1 in ['Y', 'y']:
                while True:
                    inp_2 = input('What is the value you want to edit? 1(HOT), 2(COLD), 3(BOTH):')
                    if inp_2 in ['1', 'HOT', 'hot']:
                        while True:
                            inp_3 = input('Enter a value (HOT) in liters (ex.> 123456)([C]ancel):')
                            if inp_3 in ['C', 'c']:
                                print('Closed corection process')
                                return
                            try:
                                inp_3 = int(inp_3)
                                con = sqlite3.connect(DB)
                                cur = con.cursor()
                                cur.execute('''INSERT INTO table_counter_hot 
                                    (datetime, value, correction) VALUES (?,?,?)''',
                                    (time.strftime('%Y-%m-%d %H:%M:%S'), inp_3, 1))
                                con.commit()
                                cur.close()
                                con.close()
                                print('You updated the value (HOT)!: %s' % inp_3)
                                return
                            except:
                                print('Incorrect type. Try again.')
                    elif inp_2 in ['2', 'COLD', 'cold']:
                        while True:
                            inp_4 = input('Enter a value (COLD) in liters (ex.> 123456)([C]ancel):')
                            if inp_4 in ['C', 'c']:
                                print('Closed corection process')
                                return
                            try:
                                inp_4 = int(inp_4)
                                con = sqlite3.connect(DB)
                                cur = con.cursor()
                                cur.execute('''INSERT INTO table_counter_cold 
                                    (datetime, value, correction) VALUES (?,?,?)''',
                                    (time.strftime('%Y-%m-%d %H:%M:%S'), inp_4, 1))
                                con.commit()
                                cur.close()
                                con.close()
                                print('You updated the value (COLD)!: %s' % inp_4)
                                return
                            except:
                                print('Incorrect type. Try again.')
                    elif inp_2 in ['3', 'BOTH', 'both']:
                        while True:
                            inp_5 = input('First enter a value (HOT) in liters (ex.> 123456)([C]ancel):')
                            if inp_5 in ['C', 'c']:
                                print('Closed corection process')
                                break
                            try:
                                inp_5 = int(inp_5)
                                con = sqlite3.connect(DB)
                                cur = con.cursor()
                                cur.execute('''INSERT INTO table_counter_hot 
                                    (datetime, value, correction) VALUES (?,?,?)''',
                                    (time.strftime('%Y-%m-%d %H:%M:%S'), inp_5, 1))
                                con.commit()
                                cur.close()
                                con.close()
                                print('You updated the value (HOT)!: %s' % inp_5)
                                break
                            except:
                                print('Incorrect type. Try again.')
                                continue
                        while True:
                            inp_6 = input('Then enter a value (COLD) in liters (ex.> 123456)([C]ancel):')
                            if inp_6 in ['C', 'c']:
                                print('Closed corection process')
                                return
                            try:
                                inp_6 = int(inp_6)
                                con = sqlite3.connect(DB)
                                cur = con.cursor()
                                cur.execute('''INSERT INTO table_counter_cold 
                                    (datetime, value, correction) VALUES (?,?,?)''',
                                    (time.strftime('%Y-%m-%d %H:%M:%S'), inp_6, 1))
                                con.commit()
                                cur.close()
                                con.close()
                                print('You updated the value (COLD)!: %s' % inp_6)
                                return
                            except:
                                print('Incorrect type. Try again.')
                    else:
                        print('Incorrect value. Try again.')
            elif inp_1 in ['N', 'n']:
                print('Closed corection process')
                return
            else:
                print('Incorrect value. Try again.')


    def update_value_day():
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute('''SELECT MAX(id), value FROM table_counter_hot''')
        data_hot = cur.fetchone()
        print('Write day value  (HOT):', data_hot[1])
        cur.execute('''SELECT MAX(id), value FROM table_counter_cold''')
        data_cold = cur.fetchone()
        cur.execute('''SELECT MAX(id), value_hot, value_cold FROM table_days''')
        data_old_values = cur.fetchone()
        print('Write day value (COLD):', data_cold[1])
        cur.execute('''INSERT INTO table_days (date, value_hot, value_cold, difference_hot, difference_cold) VALUES (?,?,?,?,?)''', 
                    (time.strftime('%Y-%m-%d'),
                    (0 if data_hot[1] is None else data_hot[1]),
                    (0 if data_cold[1] is None else data_cold[1]),
                    ((0 if data_hot[1] is None else data_hot[1]) - (data_hot[1] if data_old_values[1] is None else data_old_values[1])),
                    ((0 if data_cold[1] is None else data_cold[1]) - (data_cold[1] if data_old_values[2] is None else data_old_values[2]))))
        con.commit()
        cur.close()
        con.close()


    def get_day():
        try:
            con = sqlite3.connect(DB)
            
            cur = con.cursor()
            cur.execute('''SELECT MAX(id), date FROM table_days''')
            data = cur.fetchone()
            con.commit()
            cur.close()
            con.close()
            return data[1][8:10]
        except:
            return None


    def post_mail():
        smtp_server = "smtp.gmail.com"
        smtp_port   = 587
        smtp_user   = 'youremail@gmail.com'
        smtp_pwd    = 'yourpwemail'
        mail_list = [
            'blank@gmail.com',
            'blank2@gmail.com'
            ]
        try:
            con = sqlite3.connect(DB)
            cur = con.cursor()
            cur.execute('''SELECT MAX(id), date, difference_hot, difference_cold FROM table_days''')
            data = cur.fetchone()
            con.commit()
            cur.close()
            con.close()
            smtpOdj = smtplib.SMTP(smtp_server, smtp_port)
            smtpOdj.starttls()
            smtpOdj.login(smtp_user, smtp_pwd)            
            text = '''From: %s \r\n
                To: %s \r\n
                Content-Type: text/html; charset="utf-8"\r\n
                Subject: Counter water \r\n
                Date %s \r\n
                Hot  value - %s \r\n
                Cold value - %s \r\n''' % (smtp_user, mail_list, data[1], data[2], data[3])
            smtpOdj.sendmail(smtp_user, mail_list, text)
            print('Send new mail!')
            smtpOdj.quit()
        except:
            smtpOdj = smtplib.SMTP(smtp_server, smtp_port)
            smtpOdj.starttls()
            smtpOdj.login(smtp_user, smtp_pwd)
            mail_list = [
                'blank@gmail.com',
                'blank2@gmail.com'
                ]
            text = 'Error send mail =('
            smtpOdj.sendmail(smtp_user, mail_list, text)
            print('Error send mail =(')
            smtpOdj.quit()

    # Execution program

    create_all_table()
    correction()

    date_now = get_day()
    h_false = 0
    h_true = 0
    c_false = 0
    c_true = 0
    h_check_write = 0
    c_check_write = 0
    limit = 50

    while True:
        if GPIO.input(IN_H) == False:
            if h_true < limit:
                h_true = 0
            if h_false < limit:
                h_false += 1
            else:
                h_true = 0
                if h_check_write == 0:
                    write_value_H()
                    h_check_write = 1
        elif GPIO.input(IN_H) == True:
            if h_false < limit:
                h_false = 0
            if h_true < limit:
                h_true += 1
            else:
                h_false = 0
                h_check_write = 0

        if GPIO.input(IN_C) == False:
            if c_true < limit:
                c_true = 0
            if c_false < limit:
                c_false += 1
            else:
                c_true = 0
                if c_check_write == 0:
                    write_value_C()
                    c_check_write = 1
        elif GPIO.input(IN_C) == True:
            if c_false < limit:
                c_false = 0
            if c_true < limit:
                c_true += 1
            else:
                c_false = 0
                c_check_write = 0

        if date_now != time.strftime('%d'):
            date_now = time.strftime('%d')
            update_value_day()
            #post_mail()
            
        time.sleep(.01)

    GPIO.cleanup()
