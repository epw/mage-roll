from waveapi import events
from waveapi import robot
from waveapi import appengine_robot_runner
import logging

import re, mroll

NAME = "mage-roll"
ROOT = "http://%s.appspot.com" % NAME

def parse_roll (param):
    regex = re.match (r'(\d+) diff (\d+)', param)
    diff = None
    botch = False
    if regex:
        diff = int(regex.group(2))
        result = mroll.roll (int(regex.group(1)), diff, False)
    else:
        regex = re.match (r'(\d+)/(\d+)', param)
        if regex:
            diff = int (regex.group (2))
            result = mroll.roll (int(regex.group(1)), diff, False)
        else:
            regex = re.match (r'(\d+)', param)
            if regex:
                diff = None
                result = mroll.roll (int(regex.group(1)), diff, False)
            else:
                result = [None, (0)]
    rolls = ' '.join (map (str, result[1]))
    successes = result[0]
    if successes != None:
        if successes < 0:
            successes = 0
        if diff:
            if successes == 0 and not filter (lambda r: r >= diff, result[1]) \
               and len (filter (lambda r: r == 1, result[1])) > 0:
                botch = True
    else:
        return ": %s" % rolls

    botchstr = ""
    if botch:
        botchstr = " BOTCH!"
    return ": %s; successes: %d%s" % (rolls, successes, botchstr)

def blip_submitted (event, wavelet):
    params = re.findall (r'\[roll ([^\]:]*)\]', event.blip.text)
    loc = 0
    for param in params:
        loc = event.blip.text.find ("[roll " + param, loc)
        end = event.blip.text.find ("]", loc)
        event.blip.at(end).insert (parse_roll (param))
        loc = end
            
if __name__ == "__main__":

    self_robot = robot.Robot (NAME,
                           image_url="%s/assets/icon.png" % ROOT,
                           profile_url=ROOT)

    self_robot.register_handler (events.BlipSubmitted, blip_submitted)

    appengine_robot_runner.run (self_robot)
