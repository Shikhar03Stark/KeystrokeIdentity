import keyboard
import time
import csv

def map_to_ascii(key):
    mapping = {
        "shift": 16,
        'backspace': 8,
        'space': 32,
    }
    
    return mapping[key] if key in mapping else ord(key.upper())

ctx = {
    "file_name": "keystrokes_5.csv",
    "buffer": [],
    "allowed_keys": [ chr( ord('A') + i) for i in range(26)] + [ chr( ord('a') + i) for i in range(26)] + ["?", "space", "shift", "'", ",", ".", "backspace", "\""],
    "map_to_ascii_fn": map_to_ascii,
}

def on_keystroke_callback(context):
    print(context)
    last_down = []
    def on_keystroke(event):
        print(event.name)
        if event.name not in context["allowed_keys"]:
            return
        event.name = context["map_to_ascii_fn"](event.name)
        if event.event_type == keyboard.KEY_DOWN:
            if len(last_down) > 0 and last_down[0] == event.name:
                return
            if len(last_down) == 1:
                last_down.pop()
            last_down.append(event.name)
            on_key_down(event, context)
        elif event.event_type == keyboard.KEY_UP:
            if len(last_down) == 1 and last_down[0] == event.name:
                last_down.pop()
            on_key_up(event, context)
    
    return on_keystroke
                
def on_key_down(event, context):
    buffer = context["buffer"]
    buffer.append(["D", event.name, time.time_ns()])
    
def on_key_up(event, context):
    buffer = context["buffer"]
    buffer.append(["U", event.name, time.time_ns()])
    
def prepare_csv(file_name):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["event_type", "key", "timestamp"])
    
def main():
    prepare_csv(ctx["file_name"])
    keyboard.hook(on_keystroke_callback(ctx))
    try:
        keyboard.wait()
    except KeyboardInterrupt:
        keyboard.unhook_all()
        with open(ctx["file_name"], 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(ctx["buffer"])
        print("Exiting...")
        return
    
if __name__ == '__main__':
    main()