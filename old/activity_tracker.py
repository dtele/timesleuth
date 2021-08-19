import datetime
import json
import time
from os import getcwd, mkdir
from tkinter import Tk, TclError

from psutil import Process, NoSuchProcess
from win32gui import GetForegroundWindow, GetWindowText
from win32process import GetWindowThreadProcessId


if __name__ == '__main__':
    print(rf'Run with {getcwd()}\gui.py')
    exit()

root = Tk()


def get_activity():
    # Gets process and window names every second, appends to session_log when change is detected.
    active_time = 0
    try:
        active_process_name = Process(
            GetWindowThreadProcessId(GetForegroundWindow())[-1]).name()
    except (NoSuchProcess, ValueError):
        active_process_name = 'NoSuchProcess'
    active_window_name = GetWindowText(GetForegroundWindow()) or 'NoSuchWindow'
    session_log, output_db = {}, {}
    datetime_start = str(datetime.datetime.now()).split()
    output_db.update({'start_date': datetime_start[0], 'start_time': datetime_start[1]})
    while True:
        try:
            root.update()
        except TclError:
            pass
        start = time.time()
        activity_now = (active_process_name, active_window_name)
        try:
            active_process_name = Process(
                GetWindowThreadProcessId(GetForegroundWindow())[-1]).name()
        except (NoSuchProcess, ValueError):
            active_process_name = 'NoSuchProcess'
        active_window_name = GetWindowText(GetForegroundWindow()) or 'NoSuchWindow'
        if activity_now == (active_process_name, active_window_name):
            active_time += 1
        else:
            if activity_now not in session_log.keys():
                session_log.update({activity_now: active_time + 1})
            elif activity_now in session_log.keys():
                session_log[activity_now] += active_time + 1
            active_time = 0
        time.sleep(1 - (time.time() - start))
        if activity_now == ('python.exe', 'Stopping Logging'):
            break
    datetime_end = str(datetime.datetime.now()).split()
    output_db.update({'activity': list(session_log.items())})
    output_db.update({'end_date': datetime_end[0], 'end_time': datetime_end[1]})
    return output_db


def log_to(output_db=None, file=rf'{getcwd()}\logs\{str(datetime.datetime.now()).split()[0]}.json'):
    # Logs output to a specified JSON file. If not found, makes one.
    try:
        mkdir(rf'{getcwd()}\logs')
    except FileExistsError:
        pass
    try:
        open(file, 'r').close()
    except FileNotFoundError:
        open(file, 'w').close()
    if not output_db:
        output_db = get_activity()
    with open(file, 'r+', encoding='utf-8') as json_decode_fix:
        if not json_decode_fix.read():
            json_decode_fix.write('[]')
    with open(file, 'r+', encoding='utf-8') as activity_log_json:
        db_raw = [*json.load(activity_log_json), [output_db]]
        activity_log_json.seek(0)
        activity_log_json.truncate()
        activity_log_json.write(str(json.dump(db_raw, activity_log_json, sort_keys=True, indent=4)) * False)
    output_db_copy = output_db['activity']
    print(f'Saved {len(output_db_copy)} entries to {file}')
    return json.dumps(output_db, sort_keys=True)


def _read_from(file=rf'{getcwd()}\logs\{str(datetime.datetime.now()).split()[0]}.json'):
    # Returns activity data from specified file as a list of dicts.
    activity_data = []
    try:
        with open(file, 'r+', encoding='utf-8') as activity_log:
            json_file = json.load(activity_log)
            for j in range(len(json_file)):
                for i in dict(*json_file[j])['activity']:
                    activity_data.append({tuple(i[0]): i[1]})
    except json.decoder.JSONDecodeError:
        print(f'Empty file or Syntax Error in {file}')
    except FileNotFoundError:
        print('File not found.')
    return activity_data


def _process_log(activity_data=None, file=rf'{getcwd()}\logs\{str(datetime.datetime.now()).split()[0]}.json'):
    # Totals the time spent per activity and
    # returns final dict with key:value pairs of activity:time in seconds.
    if not activity_data:
        activity_data = _read_from(file=file)
    json_items_raw = [{j: k} for i in activity_data for j, k in i.items()]
    json_items_processed = {}
    for i in json_items_raw:
        for j, k in i.items():
            if j not in json_items_processed:
                json_items_processed.update({j: k})
            elif j in json_items_processed:
                json_items_processed[j] += k
    return json_items_processed


def group(json_items_processed=None, return_by=None,
          file=rf'{getcwd()}\logs\{str(datetime.datetime.now()).split()[0]}.json'):
    # Groups data separately by process and window name.
    if not json_items_processed:
        json_items_processed = _process_log(file=file)
    total_by_process, total_by_window = {}, {}
    for k, v in json_items_processed.items():
        if k[0] not in total_by_process:
            total_by_process.update({k[0]: v})
        elif k[0] in total_by_process:
            total_by_process[k[0]] += v
        if k[1] not in total_by_window:
            total_by_window.update({k[1]: v})
        elif k[1] in total_by_window:
            total_by_window[k[1]] += v
    total_by_window = {k: v for k, v in reversed(sorted(total_by_window.items(), key=lambda i: i[1]))}
    total_by_process = {k: v for k, v in reversed(sorted(total_by_process.items(), key=lambda i: i[1]))}
    for k, v in total_by_window.items():
        total_by_window[k] = datetime.timedelta(seconds=v)
    for k, v in total_by_process.items():
        total_by_process[k] = datetime.timedelta(seconds=v)
    if return_by == 'process':
        return total_by_process
    elif return_by == 'window':
        return total_by_window
    else:
        return total_by_process, total_by_window
