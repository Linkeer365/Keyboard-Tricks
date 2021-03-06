
from os.path import exists, join
import os, threading

from jca.qter.qter_test import *
from jca.qter.core.link_browser import LinkBrowser
from jca.files.all_files.all_files import all_files
from jca.files import my_paths

import pyHook
import pythoncom

class v:
    keys_pressed = []
    searching = False

def info_handler(attrs):
    def event_info(e):
        if e.MessageName == 'key down':
            v.keys_pressed.append(e.Key)
            limit = 100
            if len(v.keys_pressed) > limit:  
                v.keys_pressed = v.keys_pressed[-limit:]
            word = ''
            for ch in v.keys_pressed[::-1]:
                if ch == 'Space':  break
                word = ch + word
            print 'word: ', word
            if len(word) > 4 and not v.searching:
                v.search_thread = threading.Thread(target=lambda: search(word))
                v.search_thread.start()
        return True
    return event_info

def search(text):
    v.searching = True
    link_browser.setPlainText('')
    for path in all_files(my_paths.jca, pattern='*.py', ignore_dirs=True, 
                          recursive=True):
        with open(path) as file:
            if text.lower() in unicode(file.read().lower(), 
                                       'ascii', 'replace'):
                link_browser.add_line('"%s"' % path)
    link_browser.repaint()
    v.searching = False
 
start_if_havent()
hm = pyHook.HookManager()
hm.KeyDown = info_handler(['Ascii', 'Key', 'KeyID', 'ScanCode', 'Extended',
                           'Injected', 'Alt', 'Transition'])
hm.HookKeyboard()

t = threading.Thread(target=pythoncom.PumpMessages, args=[], kwargs={})
t.start()

link_browser = LinkBrowser()
link_browser.show()
launch_if_havent()