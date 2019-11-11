import subprocess
import string

import pynag.Utils

def build_threshold_range_string(the_value, the_offset=1, the_inverted_flag=False):
    a_threshold_str = str(the_value - the_offset) + ":" + str(the_value + the_offset)
    if the_inverted_flag:
        a_threshold_str = string.join('@', a_threshold_str)
    return a_threshold_str 

def build_threshold_range_strings(the_value=100, the_offset_step=1):
    a_warning_threshold = build_threshold_range_string(the_value, the_offset_step)
    a_critical_threshold = build_threshold_range_string(the_value, the_offset_step*2)
    return a_warning_threshold, a_critical_threshold

def build_threshold_alert_low_string(the_value, the_offset=0):
    a_threshold_str = str(the_value + the_offset) + ":"
    return a_threshold_str

def build_threshold_alert_low_strings(the_value=100, the_offset_step=-1):
    a_warning_threshold = build_threshold_alert_low_string(the_value, the_offset_step)
    a_critical_threshold = build_threshold_alert_low_string(the_value, the_offset_step*2)
    return a_warning_threshold, a_critical_threshold

def build_threshold_alert_above_string(the_value, the_offset=0, the_zero_flag=False):
    a_threshold_str = str(the_value + the_offset)
    if not the_zero_flag:
        a_threshold_str = "~:" + a_threshold_str
    return a_threshold_str

def build_threshold_alert_above_strings(the_value=100, the_offset_step=1):
    a_warning_threshold = build_threshold_alert_above_string(the_value, the_offset_step)
    a_critical_threshold = build_threshold_alert_above_string(the_value, the_offset_step*2)
    return a_warning_threshold, a_critical_threshold

def call_and_check(the_plugin_path, the_check_type, thresholds, expected_substring, expected_subsummary):
    warning_thres, critical_thres = thresholds
    p=subprocess.Popen(
        the_plugin_path
        + " -H localhost:1234 -t '" + the_check_type + "'"
        + " --threshold metric=" + the_check_type + ",warning=" + warning_thres + ",critical=" + critical_thres
        , shell=True, stdout=subprocess.PIPE)
    a_plugin_return = p.stdout.read()
    assert expected_substring in a_plugin_return
    assert expected_subsummary in a_plugin_return

def check_within_range(
        the_plugin_path
        , the_check_type
        , the_expected_value
        , the_plugin_summary):
    call_and_check(the_plugin_path, the_check_type, build_threshold_range_strings(the_expected_value + 1), "OK - ", the_plugin_summary)
    call_and_check(the_plugin_path, the_check_type, build_threshold_range_strings(the_expected_value - 1), "OK - ", the_plugin_summary)
    call_and_check(the_plugin_path, the_check_type, build_threshold_range_strings(the_expected_value + 2, ), "Warning - ", the_plugin_summary)
    call_and_check(the_plugin_path, the_check_type, build_threshold_range_strings(the_expected_value - 2), "Warning - ", the_plugin_summary)
    call_and_check(the_plugin_path, the_check_type, build_threshold_range_strings(the_expected_value + 3, ), "Critical - ", the_plugin_summary)
    call_and_check(the_plugin_path, the_check_type, build_threshold_range_strings(the_expected_value - 3), "Critical - ", the_plugin_summary)

def check_below_threshold(
        the_plugin_path
        , the_check_type
        , the_expected_value
        , the_plugin_summary):
    call_and_check(the_plugin_path, the_check_type, build_threshold_alert_low_strings(the_expected_value + 1), "OK - ", the_plugin_summary)
    call_and_check(the_plugin_path, the_check_type, build_threshold_alert_low_strings(the_expected_value + 2), "Warning - ", the_plugin_summary)
    call_and_check(the_plugin_path, the_check_type, build_threshold_alert_low_strings(the_expected_value + 3), "Critical - ", the_plugin_summary)

def check_above_threshold(
        the_plugin_path
        , the_check_type
        , the_expected_value
        , the_plugin_summary):
    call_and_check(the_plugin_path, the_check_type, build_threshold_alert_above_strings(the_expected_value - 1), "OK - ", the_plugin_summary)
    call_and_check(the_plugin_path, the_check_type, build_threshold_alert_above_strings(the_expected_value - 2), "Warning - ", the_plugin_summary)
    call_and_check(the_plugin_path, the_check_type, build_threshold_alert_above_strings(the_expected_value - 3), "Critical - ", the_plugin_summary)

def check_performance_data(
        the_plugin_path
        , the_check_type
        , the_expected_value):

    '''
    TODO add more checks for the performance data. Eg. check for invalid chars 
    '''
    warning_thres, critical_thres = build_threshold_range_strings(the_expected_value)
    p=subprocess.Popen(
        the_plugin_path
        + " -H localhost:1234 -t '" + the_check_type + "'"
        + " --threshold metric=" + the_check_type + ",warning=" + warning_thres + ",critical=" + critical_thres
        , shell=True, stdout=subprocess.PIPE)
    
    # check if plugin return value contains performance data
    # performance data is separated from summary by a pipe character
    a_plugin_return = p.stdout.read()
    
    a_pluginoutput = pynag.Utils.PluginOutput(a_plugin_return)
    assert(a_pluginoutput.perfdata)
    
def check_value_without_thresholds(
        the_plugin_path
        , the_check_type
        , the_expected_state
        , the_plugin_summary):
 
#    warning_thres, critical_thres = build_threshold_alert_above_strings(the_expected_value-1)
    p=subprocess.Popen(
        the_plugin_path
        + " -H localhost:1234 -t " + the_check_type
        , shell=True, stdout=subprocess.PIPE)
    a_plugin_return = p.stdout.read()
    assert the_expected_state in a_plugin_return 
    assert the_plugin_summary in a_plugin_return