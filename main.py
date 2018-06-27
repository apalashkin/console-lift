import threading
import graphics
import logic


def main(floors=5, lift_count=2):
    screen = graphics.open_screen()
    effects = graphics.build_building(screen, floors, lift_count)
    effects = graphics.insert_lifts(screen, effects, floors, lift_count)
    # centre = (screen.width // 2, screen.height // 2)
    t = threading.Thread(target=logic.loop)
    t.start()
    screen.play(graphics.make_scenes(effects), stop_on_resize=True)
    t.join()


if __name__ == '__main__':
    main()
