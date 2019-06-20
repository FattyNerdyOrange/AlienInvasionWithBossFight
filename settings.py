class Settings():
	def __init__(self):
		"""初始化游戏的静态设置"""
		# 飞船设置
		self.screen_width=1280
		self.screen_height=720
		self.bg_color=(230,230,230,255)
		self.ship_speed_factor = 1.5
		self.ship_limit = 3

		#子弹设置
		self.bullet_speed_factor = 3
		self.bullet_width = 3000
		self.bullet_height = 15
		self.bullet_color = 60, 60, 60
		self.bullets_allowed = 3
		
		self.bossbullet_speed_factor = 3
		self.bossbullet_width = 5
		self.bossbullet_height = 15
		self.bossbullet_color = 0, 0, 255
		self.bossbullets_allowed = 3 
		
		# 外星人设置
		self.alien_speed_factor = 1
		self.fleet_drop_speed = 10
		# fleet_direction为1表示向右移，为-1表示向左移
		self.fleet_direction = 1
		
		self.bossalien_direction = 1

		# 以什么样的速度加快游戏节奏
		self.speedup_scale = 1.1		
		# 外星人点数的提高速度
		self.score_scale = 1.5
		
		self.initialize_dynamic_settings()

		
		
	def initialize_dynamic_settings(self):
		
		"""初始化随游戏进行而变化的设置"""
		self.ship_speed_factor = 1.5
		self.bullet_speed_factor = 3
		self.alien_speed_factor = 1
				
		# fleet_direction为1表示向右；为-1表示向左
		self.fleet_direction = 1
		
		# 记分
		self.alien_points = 50
		self.bossalien_points = 5000
			
	def increase_speed(self):
		"""提高速度设置和外星人点数"""
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		
		self.alien_points = int(self.alien_points * self.score_scale)
		print(self.alien_points)

