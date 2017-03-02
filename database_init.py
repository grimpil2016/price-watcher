# -*- coding:utf-8 -*-

import pymysql
import config

host = config.host
user = config.user
password = config.password
db = config.db

class TableCreator(object):

	def __init__(self):

		#连接数据库
		self.conn = pymysql.connect(host, user, password, db, port=3306, charset='utf8')
		self.cur = self.conn.cursor()

	def create(self):
		#创建各个表
		self.cur.execute('''
			-- -----------------------------------------------------
			-- Table `products`
			-- -----------------------------------------------------
			CREATE TABLE IF NOT EXISTS `products` (
			  `id` INT NOT NULL AUTO_INCREMENT,
			  `jd_id` INT NOT NULL,
			  `name` VARCHAR(256) NOT NULL,
			  `category` VARCHAR(64) NULL,
			  `unit` VARCHAR(32) NULL,
			  `pieces` INT NULL,
			  PRIMARY KEY (`id`),
			  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
			  UNIQUE INDEX `jd_id_UNIQUE` (`jd_id` ASC))
			ENGINE = InnoDB;


			-- -----------------------------------------------------
			-- Table `user`
			-- -----------------------------------------------------
			CREATE TABLE IF NOT EXISTS `user` (
			  `id` INT NOT NULL AUTO_INCREMENT,
			  `open_id` VARCHAR(64) NOT NULL,
			  `subscribe_time` DATETIME NOT NULL,
			  PRIMARY KEY (`id`),
			  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
			  UNIQUE INDEX `open_id_UNIQUE` (`open_id` ASC))
			ENGINE = InnoDB;


			-- -----------------------------------------------------
			-- Table `price`
			-- -----------------------------------------------------
			CREATE TABLE IF NOT EXISTS `price` (
			  `product_id` INT NOT NULL,
			  `price` FLOAT NOT NULL,
			  `time` DATETIME NOT NULL,
			  `variable_quantity` FLOAT NOT NULL,
			  `variable_range` FLOAT NULL,
			  PRIMARY KEY (`price`, `time`, `product_id`))
			ENGINE = InnoDB;


			-- -----------------------------------------------------
			-- Table `watch_list`
			-- -----------------------------------------------------
			CREATE TABLE IF NOT EXISTS `watch_list` (
			  `user_id` INT NOT NULL,
			  `product_id` INT NOT NULL,
			  `notify_type` VARCHAR(32) NOT NULL,
			  `notify_range` FLOAT NOT NULL,
			  PRIMARY KEY (`user_id`, `product_id`))
			ENGINE = InnoDB;
		''')

init = TableCreator()
init.create()

print('Created tables successfully.')