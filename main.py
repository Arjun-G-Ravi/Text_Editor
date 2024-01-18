import keyboard

def on_key_event(e):
    print(f'Key {e.name} {e.event_type}')

keyboard.hook(on_key_event)

# Keep the program running
keyboard.wait('esc')
