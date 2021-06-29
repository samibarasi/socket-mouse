import mouse

def handler(event):
	print(event)
	
mouse.hook(handler)
#mouse.on_button(handler, ('s'), ('left'), ('down', 'up'))
if __name__ == "__main__":
	
	while True:
		if mouse.is_pressed(button='?'):
			print(mouse.get_position())

