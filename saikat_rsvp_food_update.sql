-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: saikat_rsvp
-- ------------------------------------------------------
-- Server version	8.0.32

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

--
-- Table structure for table `food_update`
--

DROP TABLE IF EXISTS `food_update`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `food_update` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `rsvp_userid` int NOT NULL,
  `lunch` varchar(45) DEFAULT NULL,
  `dinnerv` varchar(45) DEFAULT NULL,
  `dinnernv` varchar(45) DEFAULT NULL,
  `dinnerkid` varchar(45) DEFAULT NULL,
  `rsvp_email` varchar(200) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  KEY `rsvp_email` (`rsvp_email`),
  KEY `food_update_idx` (`rsvp_userid`),
  CONSTRAINT `food_update` FOREIGN KEY (`rsvp_userid`) REFERENCES `rsvp_food` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `food_update`
--

LOCK TABLES `food_update` WRITE;
/*!40000 ALTER TABLE `food_update` DISABLE KEYS */;
INSERT INTO `food_update` VALUES (4,6,'N','N','N','N','abhijitc00@gmail.com'),(5,7,'N','N','N','N','Ackundu@gmail.com'),(6,8,'N','N','N','N','bpchou@gmail.com'),(7,9,'N','N','N','N','gg5490@gmail.com'),(8,10,'N','N','N','N','indiraohiou@gmail.com'),(9,11,'Y','N','N','N','jayanta07@yahoo.com'),(10,12,'N','N','N','N','moumitarc@gmail.com'),(11,13,'N','N','N','N','moumitarc@gmail.com'),(12,14,'N','N','N','N','pijushd@sbcglobal.net'),(13,15,'N','N','N','N','Chansie16@gmail.com'),(14,16,'N','N','N','N','priyankamazumdar1@gmail.com'),(15,17,'N','N','N','N','sitrakesh@gmail.com'),(16,18,'N','N','N','N','sagarikachakrabarty@hotmail.com'),(17,19,'N','N','N','N','debleena11@gmail.com');
/*!40000 ALTER TABLE `food_update` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-04-16 17:15:18
