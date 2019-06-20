import sys
import pygame
from bullet import *
from alien import *
from time import sleep

def check_keydown_events(event, ai_settings, screen, ship, bullets):
	"""响应按键"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right =True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:
		sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
	"""如果还没有到达限制，就发射一颗子弹"""
	# 创建一颗子弹，并将其加入到编组bullets中
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)
		#ME.添加发射音效
		pygame.mixer.init()
		sound = pygame.mixer.Sound('sounds/firebullets.wav')
		sound.play()

def bossalien_fire_bullet(ai_settings, screen, bossalien, bossbullet, ship):
	"""ME.BOSS发射子弹"""
	#创建一颗子弹
	bossbullet = BossBullet(ai_settings, screen, bossalien)

	
def check_bossbullet_bottom(ai_settings, screen, stats, sb, ship, aliens, bossalien, bullets, bossbullet):
	"""当子弹飞出屏幕底部时，重置BOSS子弹位置"""
	screen_rect = screen.get_rect()
	if bossbullet.y >= screen_rect.bottom:
		bossbullet.reset_position(bossalien)
		
def check_keyup_events(event, ship):
	"""响应松开"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, quit_button, ship, aliens,
				bullets):
	"""响应按键和鼠标事件"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			
			check_play_button(ai_settings, screen, stats, sb, play_button,
							ship, aliens, bullets, mouse_x, mouse_y)
			check_quit_button(ai_settings, screen, stats, sb, quit_button,
							ship, aliens, bullets, mouse_x, mouse_y)
				
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bossalien,
					bullets, bossbullet, play_button, quit_button):
						
	screen.fill(ai_settings.bg_color)
	ship.blitme()
	
	# 在飞船和外星人后面重绘所有子弹
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	
	#ME.如果进入BOSS关，则绘制BOSS外星人，其他关卡绘制普通外星人
	if stats.level == stats.bosslevel:
		bossalien.blitme()
		bossalien.draw_health_bar(screen)
		
		bossbullet.draw_bullet()
		bossalien_fire_bullet(ai_settings, screen, bossalien, bossbullet, ship)
		
		check_bossbullet_bottom(ai_settings, screen, stats, sb, ship, aliens, bossalien, bullets, bossbullet)
	else: aliens.draw(screen)
	
	# 显示得分
	sb.show_score()
		
	#ME.如果游戏处于非活动状态，就绘制Play按钮，ME.绘制Quit按钮
	if not stats.game_active:
		play_button.draw_button()
		quit_button.draw_button()
		
	
	# 让最近绘制的屏幕可见
	pygame.display.flip()
	
	
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, bossalien, bossbullet):
	"""更新子弹的位置，并删除已消失的子弹"""
	# 更新子弹的位置
	bullets.update()
	
	if stats.level == stats.bosslevel:
		bossbullet.update()
		
	# 删除已消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)


	check_bullet_collisions(ai_settings, screen, stats, sb, ship,
								aliens, bossalien, bullets, bossbullet)
	
def check_bullet_collisions(ai_settings, screen, stats, sb, ship,
								aliens, bossalien, bullets, bossbullet):
	"""响应子弹和外星人的碰撞，以及外星人子弹和船的碰撞"""
	#ME.只有在非BOSS关才启用
	if stats.level != stats.bosslevel :
	
		# 删除发生碰撞的子弹和外星人
		collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
		
		if collisions:
			for aliens in collisions.values():
				stats.score += ai_settings.alien_points * len(aliens)
				sb.prep_score()
			check_high_score(stats, sb)
		
		if len(aliens) == 0:
			# 如果整群外星人都被消灭，就提高一个等级
			bullets.empty()
			ai_settings.increase_speed()
			
			#ME.播放音效
			pygame.mixer.init()
			sound = pygame.mixer.Sound('sounds/levelup.wav')
			sound.play()
			
			# 提高等级
			stats.level += 1
			sb.prep_level()
			
			#如果当前关卡下一关是BOSS关就不要再生成舰队
			if stats.level != stats.bosslevel-1: 
				create_fleet(ai_settings, screen, ship, aliens)
			else: pass

	#ME.只有在BOSS关才启用
	elif stats.level == stats.bosslevel:
		
		#子弹击中BOSS外星人，BOSS外星人失去一定血量
		for bullet in bullets:
			if pygame.Rect.colliderect(bullet.rect, bossalien.rect):
				bossalien.health -=100
				bullets.remove(bullet)
			
		#生命值为0时删除该BOSS
		if bossalien.health <= 0:
			
			#提高等级，加分
			stats.level += 1
			sb.prep_level()
			stats.score += ai_settings.bossalien_points
			sb.prep_score()
			check_high_score(stats, sb)
			
			create_fleet(ai_settings, screen, ship, aliens)
	
		#BOSS发射子弹和船碰撞

		if pygame.Rect.colliderect(bossbullet.rect, ship.rect):
			ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, bossalien, bossbullet)

def create_fleet(ai_settings, screen, ship, aliens):
	"""创建外星人群"""
	# 创建一个外星人，并计算一行可容纳多少个外星人
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height,
									alien.rect.height)
									
	# 创建外星人群
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_number, row_number)
		
		

def get_number_aliens_x(ai_settings, alien_width):
	"""计算每行可容纳多少个外星人"""
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x
	
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	"""创建一个外星人并将其放在当前行"""
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)
	
def get_number_rows(ai_settings, ship_height, alien_height):
	"""计算屏幕可容纳多少行外星人"""
	available_space_y = (ai_settings.screen_height -
							(3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, bossalien, bossbullet):
	"""
	检查是否有外星人位于屏幕边缘，并更新整群外星人的位置
	"""
	#ME.在非BOSS关卡时检查
	if stats.level != stats.bosslevel :
		check_fleet_edges(ai_settings, aliens)
		aliens.update()
		
		# 检查是否有外星人到达屏幕底端
		check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)
		
		# 检测外星人和飞船之间的碰撞
		if pygame.sprite.spritecollideany(ship, aliens):
			ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, bossalien, bossbullet)
	
	else:
		check_bossalien_edges(ai_settings, bossalien)
		bossalien.update()


def check_fleet_edges(ai_settings, aliens):
	"""有外星人到达边缘时采取相应的措施"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break
			
def check_bossalien_edges(ai_settings, bossalien):
	"""检查BOSS外星人是否碰到边缘"""
	if bossalien.check_edges():
		change_bossalien_direction(ai_settings, bossalien)
		
			
def change_fleet_direction(ai_settings, aliens):
	"""将整群外星人下移，并改变它们的方向"""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1
		
def change_bossalien_direction(ai_settings, bossalien):
	"""改变BOSS外星人的方向"""
	ai_settings.bossalien_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, bossalien, bossbullet):
	"""响应被外星人撞到的飞船"""
	if stats.ships_left > 0:
		#ME.播放失去生命值音效
		pygame.mixer.init()
		sound = pygame.mixer.Sound('sounds/loselifes.wav')
		sound.play()
		
		# 将ships_left减1
		stats.ships_left -= 1
		
		# 更新记分牌
		sb.prep_ships()
		
		# 清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()

		#ME.如果不是BOSS关，就创建一群新的外星人，并将飞船放到屏幕底端中央
		if stats.level != stats.bosslevel:
			create_fleet(ai_settings, screen, ship, aliens)
			ship.center_ship()
		#ME.如果是BOSS关，直接创建一个飞船继续，并且重置撞击到飞船的子弹的位置
		else: 
			ship.center_ship()
			bossbullet.reset_position(bossalien)
		
		
		# 暂停
		sleep(0.5)
		
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)
		
		#ME.播放游戏结束音效
		pygame.mixer.music.stop()
		pygame.mixer.init()
		sound = pygame.mixer.Sound('sounds/gameover.wav')
		sound.play()
		
		
	
def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens,
						bullets):
	"""检查是否有外星人到达了屏幕底端"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# 像飞船被撞到一样进行处理
			ship_hit(ai_settings, screen, stats, sb, ship, aliens, bossalien, bullets)
			break

def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
					aliens, bullets, mouse_x, mouse_y):
	"""在玩家单击Play按钮时开始新游戏"""
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		
		#ME.播放音效
		pygame.mixer.init()
		sound = pygame.mixer.Sound('sounds/clickbuttons.wav')
		sound.play()
		
		# 重置游戏设置
		ai_settings.initialize_dynamic_settings()
		# 隐藏光标
		pygame.mouse.set_visible(False)
		# 重置游戏统计信息
		stats.reset_stats()
		stats.game_active = True
		
		# 重置记分牌图像
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()

		# 清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()
		
		# 创建一群新的外星人，并让飞船居中
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

def check_quit_button(ai_settings, screen, stats, sb, quit_button, ship,
					aliens, bullets, mouse_x, mouse_y):
	"""ME.玩家点击quit按钮时结束游戏"""
	button_clicked = quit_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		sys.exit()



def check_high_score(stats, sb):
	"""检查是否诞生了新的最高得分"""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()
