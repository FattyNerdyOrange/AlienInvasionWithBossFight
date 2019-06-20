import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	"""表示单个外星人的类"""
	
	def __init__(self, ai_settings, screen):
		"""初始化外星人并设置其起始位置"""
		super(Alien, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		
		# 加载外星人图像，并设置其rect属性
		self.image = pygame.image.load('images/alien.png')
		self.rect = self.image.get_rect()
		# 每个外星人最初都在屏幕左上角附近
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		# 存储外星人的准确位置
		self.x = float(self.rect.x)
		
	def blitme(self):
		"""在指定位置绘制外星人"""
		self.screen.blit(self.image, self.rect)
		

	def check_edges(self):
		"""如果外星人位于屏幕边缘，就返回True"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True


	def update(self):
		"""向左或向右移动外星人"""
		self.x += (self.ai_settings.alien_speed_factor *
							self.ai_settings.fleet_direction)
		self.rect.x = self.x

class BossAlien(Sprite):
	"""BOSS外星人"""
	
	def __init__(self, ai_settings, screen, health=500):
		"""初始化外星人并设置其起始位置"""
		self.screen = screen
		self.ai_settings = ai_settings
		self.health = health
		
		# 加载外星人图像，并设置其rect属性
		self.image = pygame.image.load('images/bossalien.png')
		self.rect = self.image.get_rect()
		self.screen_rect=screen.get_rect()
		
		self.rect.x = 550
		self.rect.y = 100
		
		# 存储外星人的准确位置
		self.x = float(self.rect.x)
		
		# #设置生命值
		# health=100
		
	def blitme(self):
		"""在指定位置绘制外星人"""
		self.screen.blit(self.image, (self.rect.x,self.rect.y))	
		
		
	def draw_health_bar(self, screen):
		"""显示血条"""
		#参数依次表示：在SCREEN上面绘制，颜色，（该图案左上角的坐标，长度和高度）
		
		#灰色的空白血条
		pygame.draw.rect(screen, (0, 230, 0), ((380, 100), (500, 10)) )
		#红色的现有血量
		pygame.draw.rect(screen, (255, 0, 0), ((380, 100), (self.health, 10)) )


	def check_edges(self):
		"""如果外星人位于屏幕边缘，就返回True"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True


	def update(self):
		"""向左或向右移动外星人"""
		self.x += (self.ai_settings.alien_speed_factor *
							self.ai_settings.bossalien_direction)
		self.rect.x = self.x
