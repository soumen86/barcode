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
-- Table structure for table `rsvp_food`
--

DROP TABLE IF EXISTS `rsvp_food`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rsvp_food` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name_Pri` varchar(100) NOT NULL,
  `Name_Sec` varchar(100) DEFAULT NULL,
  `Email` varchar(100) NOT NULL,
  `Member_prev` varchar(45) DEFAULT NULL,
  `Lunch_all` int DEFAULT NULL,
  `Dinner_veg` int DEFAULT NULL,
  `Dinner_nveg` int DEFAULT NULL,
  `Dinner_kid` int DEFAULT NULL,
  `Activity` varchar(45) DEFAULT NULL,
  `Volunteering` varchar(100) DEFAULT NULL,
  `Comments` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rsvp_food`
--

LOCK TABLES `rsvp_food` WRITE;
/*!40000 ALTER TABLE `rsvp_food` DISABLE KEYS */;
INSERT INTO `rsvp_food` VALUES (6,'Abhijit Chatterjee','Nandita Chatterjee','abhijitc00@gmail.com','Yes',2,2,0,0,'','Food Distribution','Looking forward to the event'),(7,'Arun Kundu','Rita Poddar','Ackundu@gmail.com','Yes',2,1,1,0,'','Food Distribution',''),(8,'Biswa Choudhury','','bpchou@gmail.com','Yes',1,1,0,0,'','Food Distribution',''),(9,'Gairika Ghosh','Ravish Sharma','gg5490@gmail.com','Yes',2,1,1,0,'','Food Distribution',''),(10,'indira Chaudhuri','Rajesh Sharma','indiraohiou@gmail.com','Yes',3,3,0,1,'','Food Distribution, Art and Craft Workshop',''),(11,'Jayanta Mukhopadhyaya','Jayanta Mukhopadhyaya','jayanta07@yahoo.com','Yes',2,2,0,0,'','Food Distribution','N/A'),(12,'Moumita Chatterjee','Kausik Ray Chaudhuri','moumitarc@gmail.com','Yes',3,2,1,0,'','Food Distribution',''),(13,'Moumita Chatterjee','Kausik Ray Chaudhuri','moumitarc@gmail.com','Yes',3,2,1,0,'','Food Distribution',''),(14,'Pijush/Indrani','Dewanjee','pijushd@sbcglobal.net','Yes',2,1,1,0,'','Food Distribution','Will be there.'),(15,'Priya kumar','Asif Islam','Chansie16@gmail.com','No',1,2,1,2,'Yes','Food Distribution','Thx'),(16,'Priyanka Mazumdar','','priyankamazumdar1@gmail.com','No',1,0,1,0,'','Food Distribution',''),(17,'Rakesh Sit','','sitrakesh@gmail.com','Yes',3,3,0,0,'','Food Distribution',''),(18,'Sagarika Chakrabarty','Abesh bhattacharjee','sagarikachakrabarty@hotmail.com','Yes',3,2,0,1,'','Food Distribution',''),(19,'Sandep Nanda','Debleena Jana','debleena11@gmail.com','Yes',3,2,0,1,'Yes','Food Distribution','Aadit Nanda, contact number - 61997239874');
/*!40000 ALTER TABLE `rsvp_food` ENABLE KEYS */;
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
