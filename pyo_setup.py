from pyo import *

print("Audio host APIs:")
pa_list_host_apis()
print(f"\n------------------------------------------------------------------\n")
pa_list_devices()
print(f"\n------------------------------------------------------------------\n")
print("Default input device: %i" % pa_get_default_input())
print(f"\n------------------------------------------------------------------\n")
print("Default output device: %i" % pa_get_default_output())