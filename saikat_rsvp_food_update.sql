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
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `food_update`
--

LOCK TABLES `food_update` WRITE;
/*!40000 ALTER TABLE `food_update` DISABLE KEYS */;
INSERT INTO `food_update` VALUES (18,20,'N','N','N','N','sagarikachakrabarty@hotmail.com'),(19,21,'N','N','N','N','abhijitc00@gmail.com'),(20,22,'N','N','N','N','anidatta@gmail.com'),(21,23,'N','N','N','N','anindyacb79@gmail.com'),(22,24,'N','N','N','N','Arindom.sarkar@gmail.com'),(23,25,'N','N','N','N','arundatta1@gmail.com'),(24,26,'N','N','N','N','avijitc@gmail.com'),(25,27,'N','N','N','N','9.7avijit@gmail.com'),(26,28,'N','N','N','N','manisha_maiti@yahoo.com'),(27,29,'N','N','N','N','roy.suchismita2011@gmail.com'),(28,30,'N','N','N','N','binayak.lahiri@gmail.com'),(29,31,'N','N','N','N','debanjan13@gmail.com'),(30,32,'N','N','N','N','esha21says@gmail.com'),(31,33,'N','N','N','N','debopriyo@gmail.com'),(32,34,'N','N','N','N','dgupta@sdsu.edu'),(33,35,'N','N','N','N','hkhatuya@yahoo.com'),(34,36,'N','N','N','N','jayanta07@yahoo.com'),(35,37,'N','N','N','N','U_banerjee@hotmail.com'),(36,38,'N','N','N','N','jayati.ghoshal@gmail.com'),(37,39,'N','N','N','N','Debarati.kk@gmail.com'),(38,40,'N','N','N','N','d.koushik@gmail.com'),(39,41,'N','N','N','N','Contact.mriganka@gmail.com'),(40,42,'N','N','N','N','nandan@gmail.com'),(41,43,'N','N','N','N','Sumana13@hotmail.com'),(42,44,'N','N','N','N','pijushd@sbcglobal.net'),(43,45,'N','N','N','N','pradipsur4@gmail.com'),(44,46,'N','N','N','N','duttps@aol.com'),(45,47,'N','N','N','N','Probir5463@gmail.com'),(46,48,'N','N','N','N','raja.govindarajan@gmail.com'),(47,49,'N','N','N','N','sitrakesh@gmail.com'),(48,50,'N','N','N','N','suparna_raha@yahoo.com'),(49,51,'N','N','N','N','dutta.samit@gmail.com'),(50,52,'N','N','N','N','debleena11@gmail.com'),(51,53,'N','N','N','N','madhurabasu@gmail.com'),(52,54,'N','N','N','N','Shouvik86.das@gmail.com'),(53,55,'N','N','N','N','shubhadippaul@gmail.com'),(54,56,'N','N','N','N','spmondal08@gmail.com'),(55,57,'N','N','N','N','ghosh.soumen86@gmail.com'),(56,58,'N','N','N','N','subhadeep.guha@gmail.com'),(57,59,'N','N','N','N','subratokde2002@gmail.com'),(58,60,'N','N','N','N','debnath.sumit@outlook.com'),(59,61,'N','N','N','N','desurya125@gmail.com'),(60,62,'N','N','N','N','smahata@health.ucsd.edu'),(61,63,'N','N','N','N','gtirtha@gmail.com');
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

-- Dump completed on 2023-06-09 10:43:45
