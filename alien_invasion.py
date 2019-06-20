import pygame
from game_stats import GameStats
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import *
from button import *
from bullet import *
from scoreboard import Scoreboard

def run_game():
	

	pygame.init()
	ai_settings=Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")


	# 创建一艘飞船、一个子弹编组和一个外星人编组
	ship = Ship(ai_settings, screen)
	bullets = Group()
	alien = Alien(ai_settings, screen)
	aliens = Group()
	bossalien = BossAlien(ai_settings, screen)
	bossbullet = BossBullet(ai_settings, screen, bossalien)
	
	# 创建外星人群
	gf.create_fleet(ai_settings, screen, ship, aliens)
	
	# 创建存储游戏统计信息的实例，并创建记分牌
	stats = GameStats(ai_settings)	
	sb = Scoreboard(ai_settings, screen, stats)
	
	# 创建Play按钮
	play_button = Play_Button(ai_settings, screen, "Play")
	
	#ME.创建Quit按钮
	quit_button = Quit_Button(ai_settings, screen, "Quit")

	#ME.播放背景音乐
	pygame.mixer.music.load('music/Synth_Element.ogg')  
	pygame.mixer.music.play(-1) #重复播放
	
	# 开始游戏主循环
	while True:
		
		gf.check_events(ai_settings, screen, stats, sb, play_button, quit_button, ship,
					aliens, bullets)
		
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
							bullets, bossalien, bossbullet)
			gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens,
							bullets, bossalien, bossbullet)
			
		gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bossalien,
						bullets, bossbullet, play_button, quit_button)
		

run_game()
