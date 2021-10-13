CREATE DATABASE  IF NOT EXISTS `art_catalog` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `art_catalog`;
-- MySQL dump 10.13  Distrib 8.0.20, for macos10.15 (x86_64)
--
-- Host: database-2.clbmc2tqyqce.us-east-2.rds.amazonaws.com    Database: art_catalog
-- ------------------------------------------------------
-- Server version	8.0.23

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '';

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `item_id` int NOT NULL,
  `artist` varchar(65) DEFAULT NULL,
  `title` varchar(45) DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  `width` int DEFAULT NULL,
  `height` int DEFAULT NULL,
  `price` float DEFAULT NULL,
  `img_url` varchar(100) DEFAULT NULL,
  `comments` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'Garry','CORDOBA 8x8','Oil & Graphite on Canvas',8,8,400,'CORDOBA_8X8_M',''),(2,'Garry','CORDOBA 24x24','Oil & Graphite on Canvas',24,24,1200,'CORDOBA_24X24_R',''),(3,'Garry','DEHLI 16x24','Oil & Graphite on Canvas',16,24,1500,'DEHLI_16X24_M',''),(4,'Garry','DEHLI 32x32','Oil & Graphite on Canvas',32,32,3500,'DEHLI_32X32_M',''),(5,'Garry','FLORENCE 8x8','Oil & Graphite on Canvas',8,8,400,'FLORENCE_8X8_M','2021 Mamaroneck Artist\'s Guild Small Works Exhibition, 2nd Place Award'),(6,'Garry','FLORENCE 24x24','Oil & Graphite on Canvas',24,24,1500,'FLORENCE_24X24_R','2021 Carriage Barn Arts Center, Color+Art+Design Exhibition, New Canaan'),(7,'Garry','MONTEREY 8x8','Oil & Graphite on Canvas',8,8,400,'MONTEREY_8X8_M',''),(8,'Garry','MONTEREY 8x48 GREY','Oil & Graphite on Canvas',8,48,800,'MONTEREY_8X48_GREY_R',''),(9,'Garry','MONTEREY 8x48 COLOR','Oil & Graphite on Canvas',8,48,1200,'MONTEREY_8X48_COLOR_R','2021 Arts Westchester, Calling All Creatives Exhibition'),(10,'Garry','ROCINHA 4x16x16','Oil & Graphite on Canvas',33,33,2400,'ROCINHA_4X16X16_M',''),(11,'Garry','ROCINHA 8x8','Oil & Graphite on Canvas',8,8,400,'ROCINHA_8X8_M',''),(12,'Garry','ROCINHA 12x12','Oil & Graphite on Canvas',12,12,600,'ROCINHA_12X12_R',''),(13,'Garry','ROCINHA 16x16','Oil & Graphite on Canvas',12,12,800,'ROCINHA_16X16_R',''),(14,'Garry','ROCINHA 32x32','Oil & Graphite on Canvas',32,32,5000,'ROCINHA_32X32_M','2021 Providence Art Club National Open Juried Exhibition'),(15,'Garry','TIMBUKTU 8x8','Oil & Graphite on Canvas',8,8,400,'TIMBUKTU_8X8_M',''),(16,'Garry','TIMBUKTU 36X36','Oil & Graphite on Canvas',36,36,3000,'TIMBUKTU_36X36_R',''),(17,'Garry','TOLEDO 8x8','Oil & Graphite on Canvas',8,8,400,'TOLEDO_8X8_M',''),(18,'Garry','TOLEDO 12X12','Oil & Graphite on Canvas',12,12,600,'TOLEDO_12X12_R',''),(19,'Garry','TOLEDO 16X16','Oil & Graphite on Canvas',16,16,800,'TOLEDO_16X16_R',''),(20,'Garry','TOLEDO 24X24','Oil & Graphite on Canvas',24,24,800,'TOLEDO_24X24_R','');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-10-10 20:46:57
