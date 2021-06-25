from pynput import mouse

with mouse.Events() as events:
	for event in events:
		if isinstance(event, mouse.Events.Click): 
			if event.button == mouse.Button.right:
				break
			else:
				print('Received event {}'.format(event))

