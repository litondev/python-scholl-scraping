import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="data_dapodik"
)

mycursor = mydb.cursor()

# mycursor.execute("CREATE DATABASE data_dapodik")

mycursor.execute("SET FOREIGN_KEY_CHECKS = 0")
mycursor.execute("DROP TABLE IF EXISTS provinces")
mycursor.execute("DROP TABLE IF EXISTS citys")
mycursor.execute("DROP TABLE IF EXISTS districts")
mycursor.execute("DROP TABLE IF EXISTS schools")

mycursor.execute("""
CREATE TABLE `provinces` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
)""")

mycursor.execute("""
CREATE TABLE `citys` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) DEFAULT NULL,
  `province_id` bigInt(20) unsigned NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `citys_province_id_foreign` (`province_id`),
  CONSTRAINT `citys_province_id_foreign` FOREIGN KEY (`province_id`) REFERENCES `provinces` (`id`)
)""")

mycursor.execute("""
CREATE TABLE `districts` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255)  DEFAULT NULL,
  `city_id` bigInt(20) unsigned NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `districts_city_id_foreign` (`city_id`),
  CONSTRAINT `districts_city_id_foreign` FOREIGN KEY (`city_id`) REFERENCES `citys` (`id`)
)""")

mycursor.execute("""
CREATE TABLE `schools` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `district_id` bigInt(20) unsigned NULL DEFAULT NULL,
  `name` VARCHAR(255)  DEFAULT NULL,
  `member` bigInt(20) DEFAULT 0,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `schools_district_id_foreign` (`district_id`),
  CONSTRAINT `schools_district_id_foreign` FOREIGN KEY (`district_id`) REFERENCES `districts` (`id`)
)""")