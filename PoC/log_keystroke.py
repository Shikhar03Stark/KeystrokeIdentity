import keyboard
import time
import csv

def map_special_keys(key):
    mapping = {
        "space": "@",
        "shift": "$",
        "'": "#",
    }
    
    return mapping[key] if key in mapping.keys() else key

ctx = {
    "file_name": "keystrokes.csv",
    "buffer": [],
    "allowed_keys": [ chr( ord('A') + i) for i in range(26)] + [ chr( ord('a') + i) for i in range(26)] + ["space", "shift", "'"] ,
    "map_special_keys_fn": map_special_keys,
}

def on_keystroke_callback(context):
    print(ctx)
    def on_keystroke(event):
        print(event.name)
        if event.name not in context["allowed_keys"]:
            return
        event.name = context["map_special_keys_fn"](event.name)
        if event.event_type == keyboard.KEY_DOWN:
            on_key_down(event, context)
        elif event.event_type == keyboard.KEY_UP:
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
    prepare_csv("keystrokes.csv")
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