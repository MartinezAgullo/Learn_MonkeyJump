from game import Game

play = Game()
play.initialize_game()

while play.running:
    play.update()

pygame.quit()
sys.exit()
