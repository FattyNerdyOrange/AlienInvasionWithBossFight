import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	"""一个对飞船发射的子弹进行管理的类"""
	
	def __init__(self, ai_settings, screen, ship):
		"""在飞船所处的位置创建一个子弹对象"""
		super(Bullet, self).__init__()
		self.screen = screen
		
		# 在(0,0)处创建一个表示子弹的矩形，再设置正确的位置
		self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, 
							ai_settings.bullet_height)
		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.rect.top
		
		#存储用小数表示的子弹位置
		self.y = float(self.rect.y)
		
		self.color = ai_settings.bullet_color
		self.speed_factor = ai_settings.bullet_speed_factor
		
	def update(self):
		"""向上移动子弹"""
		#更新表示子弹位置的小数值
		self.y -= self.speed_factor
		#更新表示子弹的rect的位置
		self.rect.y = self.y
		
	def draw_bullet(self):
		"""在屏幕上绘制子弹"""
		pygame.draw.rect(self.screen, self.color, self.rect)


class BossBullet(Sprite):
	"""Boss发射的子弹"""
	
	def __init__(self, ai_settings, screen, bossalien):
		"""在飞船所处的位置创建一个子弹对象"""
		super(BossBullet, self).__init__()
		self.screen = screen
		
		# 在boss底部中央处创建一个表示子弹的矩形，再设置正确的位置
		self.rect = pygame.Rect(0, 0, ai_settings.bossbullet_width,
								ai_settings.bossbullet_height)
		self.rect.x = bossalien.x
		self.rect.y = bossalien.rect.bottom
		self.width = ai_settings.bossbullet_width
		self.height = ai_settings.bossbullet_height
		
		#存储用小数表示的子弹位置
		self.y = float(self.rect.y)
		
		self.y = bossalien.rect.bottom
		self.x = bossalien.x
		
		self.color = ai_settings.bossbullet_color
		self.speed_factor = ai_settings.bossbullet_speed_factor
		
	def update(self):
		"""向下移动子弹"""
		#更新表示子弹位置的小数值
		self.y += self.speed_factor
		#更新表示子弹的rect的位置
		self.rect.y = self.y

		
	def reset_position(self, bossalien):
		"""（当子弹飞出屏幕底部或者击中飞船时）回到开始的地方"""
		self.y = bossalien.rect.bottom
		self.x = bossalien.x
		#更新rect位置
		self.rect.y = self.y
		self.rect.x = self.x

	def draw_bullet(self):
		"""在屏幕上绘制子弹"""
		pygame.draw.rect(self.screen, self.color, ((self.x,self.y),(self.width,self.height)))

