import time

from DataFileManager import DataFileManager
import datetime


def is_between(current_time, time_range):
    if time_range[1] < time_range[0]:
        return current_time >= time_range[0] or current_time <= time_range[1]
    return time_range[0] <= current_time <= time_range[1]


def split_time(time_rules):
    store = [''] * 5
    for i in time_rules.split():
        if i[0] == 'F':
            store[0] = i[1:]
        elif i[0] == 'T':
            store[1] = i[1:]
        elif i[0] == 'D':
            store[2] = i[1:]
        elif i[0] == 'I':
            store[3] = i[1:]
        elif i[0] == 'S':
            store[4] = i[1:]
    return store


class TimeManager(DataFileManager):
    def __init__(self, data_file, key_file):
        DataFileManager.__init__(self, data_file, key_file)
        self.data = self.get_data()
        self.curr_time_rule = self.load_curr_time_rule()

    def update_data(self):
        self.data = self.get_data()

    def load_curr_time_rule(self):
        return self.data['curr_time_rule']

    def save_curr_time_rule(self):
        timeout = time.time() + 1
        while self.is_writing():
            if time.time() > timeout:
                break
        self.data['curr_time_rule'] = self.curr_time_rule
        self.save_data(self.data)

    def update_curr_time_rule(self):
        if self.curr_time_rule[4] != '' and self.curr_time_rule[4] != '0':
            temp = int(self.curr_time_rule[4])
            temp -= 1
            self.curr_time_rule[4] = str(temp)
        if self.curr_time_rule[6] != '' and self.curr_time_rule[6] != '0':
            temp = int(self.curr_time_rule[6])
            temp -= 1
            self.curr_time_rule[6] = str(temp)
        self.save_curr_time_rule()

    def one_min_left(self):
        result = False
        if self.curr_time_rule[4] == '1':
            result = True
        elif self.curr_time_rule[6] == '1':
            result = True
        else:
            now = datetime.datetime.now()
            time_limit_list = self.curr_time_rule[3].split(':')
            time_limit = now.replace(hour=int(time_limit_list[0]), minute=int(time_limit_list[1]))
            distance = time_limit - now
            minute_range = distance.total_seconds() / 60
            if minute_range == 1:
                result = True
        return result

    def search_time_rule(self, now):
        result = []
        curr_day = now.strftime('%a')
        if curr_day in self.data:
            for time_rule in self.data[curr_day]:
                store = split_time(time_rule)
                if is_between(now.strftime('%H:%M'), store[:2]):
                    result = store
                    break
        if result:
            result.insert(0, now.strftime('%d/%m/%Y'))
            result.insert(0, '')
        return result

    def curr_time_rule_reset(self):
        self.curr_time_rule = ['' for _ in range(7)]
        self.save_curr_time_rule()

    def get_use_time(self):
        out_duration = False
        now = datetime.datetime.now()
        time_range_list = self.curr_time_rule[3].split(':')
        time_range_limit = now.replace(hour=int(time_range_list[0]), minute=int(time_range_list[1]))
        distance = (time_range_limit - now).total_seconds() / 60
        if self.curr_time_rule[6]:
            time_total = now + datetime.timedelta(minutes=int(self.curr_time_rule[6]))
            temp = (time_total - now).total_seconds() / 60
            if temp < distance:
                distance = temp
        if self.curr_time_rule[4]:
            time_duration = now + datetime.timedelta(minutes=int(self.curr_time_rule[4]))
            temp = (time_duration - now).total_seconds() / 60
            if temp < distance:
                distance = temp
                out_duration = True

        result = ""
        result += f'Time range: {self.curr_time_rule[2]} - {self.curr_time_rule[3]}\n'
        if out_duration:
            wait_time = now + datetime.timedelta(minutes=int(self.curr_time_rule[5]) + distance)
            wait_time = wait_time.strftime('%H:%M')
            result += f'Duration time left: {distance} minute(s)\n'
            result += f'Total time left: {self.curr_time_rule[6]} minute(s)\n'
            result += f'Next available time: {wait_time}'
        else:
            result += f'Total time left: {distance} minute(s)\n'
            result += f'{self.get_time_rule_today()}'
        return result

    def get_time_rule_today(self):
        result = ""
        now = datetime.datetime.now()
        curr_day = now.strftime('%a')
        result += f'{curr_day}:\n'
        if len(self.data[curr_day]) != 0:
            for time_rule in self.data[curr_day]:
                store = split_time(time_rule)
                result += f'{store[0]} - {store[1]}\n'
        else:
            result += "Not allowed to use today\n"
        return result

    def cant_use_reason(self):
        result = ""
        if self.curr_time_rule[0] != "":
            wait_time = datetime.datetime.strptime(self.curr_time_rule[0], '%d/%m/%Y %H:%M')
            wait_time.strftime('%H:%M')
            result += f'\nNext available time: {wait_time}'
        if self.curr_time_rule[6] == '0':
            result += f'\nOut of total time in current time rule'
        result += f'\nTime rule today:\n{self.get_time_rule_today()}'
        return result

    def in_use_time(self):
        now = datetime.datetime.now()
        result = True
        if self.curr_time_rule[0]:
            waiting_time = datetime.datetime.strptime(self.curr_time_rule[0], '%d/%m/%Y %H:%M')
            if now >= waiting_time:
                self.curr_time_rule[0] = ''
                self.save_curr_time_rule()
                return self.in_use_time()
            else:
                result = False
        else:
            if self.curr_time_rule[1]:
                rule_date = datetime.datetime.strptime(self.curr_time_rule[1], '%d/%m/%Y')
                if rule_date.date() < now.date() or not is_between(now.strftime('%H:%M'), self.curr_time_rule[2:4]):
                    self.curr_time_rule_reset()
                    return self.in_use_time()
                else:
                    if self.curr_time_rule[6] == '0':
                        result = False
                        return result
                    if self.curr_time_rule[4] == '0':
                        wait_minutes = int(self.curr_time_rule[5])
                        waiting_time = now + datetime.timedelta(minutes=wait_minutes)
                        self.curr_time_rule[0] = waiting_time.strftime('%d/%m/%Y %H:%M')
                        self.curr_time_rule[4] = self.search_time_rule(now)[4]
                        self.save_curr_time_rule()
                        return self.in_use_time()
            else:
                self.curr_time_rule = self.search_time_rule(now)
                if len(self.curr_time_rule) == 0:
                    self.curr_time_rule_reset()
                    result = False
        return result

    def set_penalty(self, minute):
        now = datetime.datetime.now()
        penalty_time = now + datetime.timedelta(minutes=minute)
        self.data['penalty'] = penalty_time.strftime('%d/%m/%Y %H:%M')
        self.save_data(self.data)

    def remove_penalty(self):
        self.data['penalty'] = ""
        self.save_data(self.data)

    def get_penalty(self):
        pen_time = ''
        if self.data['penalty'] != '':
            pen_time = datetime.datetime.strptime(self.data['penalty'], '%d/%m/%Y %H:%M').strftime('%H:%M')
        return pen_time

    def in_penalty(self):
        result = False
        if self.data['penalty'] != "":
            now = datetime.datetime.now()
            penalty_time = datetime.datetime.strptime(self.data['penalty'], '%d/%m/%Y %H:%M')
            if now < penalty_time:
                result = True
            else:
                self.data['penalty'] = ""
            self.save_data(self.data)
        return result
