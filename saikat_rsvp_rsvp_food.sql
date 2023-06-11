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
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rsvp_food`
--

LOCK TABLES `rsvp_food` WRITE;
/*!40000 ALTER TABLE `rsvp_food` DISABLE KEYS */;
INSERT INTO `rsvp_food` VALUES (20,'Sagarika Chakrabarty','Abesh Bhattacharjee','sagarikachakrabarty@hotmail.com','Yes',4,0,0,0,'','Food',''),(21,'Abhijit Chatterjee','Nandita Chatterjee','abhijitc00@gmail.com','Yes',2,0,0,0,'0','Food',''),(22,'Animesh Datta','Rima chatterjee','anidatta@gmail.com','Yes',5,0,0,0,'0','Games',''),(23,'Anindya Bhattacharya','Bidisha','anindyacb79@gmail.com','Yes',5,0,0,0,'0','',''),(24,'Arindom Sarkar','Sudipta Bag','Arindom.sarkar@gmail.com','Yes',3,0,0,0,'0','Food',''),(25,'Arun K Datta','Purabi Datta','arundatta1@gmail.com','Yes',3,0,0,0,'0','Food',''),(26,'Avijit Chakraborty','Gouri Chakraborty','avijitc@gmail.com','Yes',4,0,0,0,'0','Food',''),(27,'Avijit Pradhan','Avijit Pradhan','9.7avijit@gmail.com','Yes',1,0,0,0,'0','Food',''),(28,'Banikumar Maiti','Manisha Maiti','manisha_maiti@yahoo.com','Yes',4,0,0,0,'0','',''),(29,'Suchismita Roy','Barun Das','roy.suchismita2011@gmail.com','Yes',3,0,0,0,'0','Food',''),(30,'Binayak Lahiri','Ananya Banerjee','binayak.lahiri@gmail.com','Yes',3,0,0,0,'0','Food',''),(31,'Debanjan Dhar','Dhrubamitra Chatterjee','debanjan13@gmail.com','Yes',5,0,0,0,'0','',''),(32,'Debaprasun Chakraborty','Esha Chatterjee Chakraborty','esha21says@gmail.com','Yes',4,0,0,0,'0','',''),(33,'Debopriyo Chowdhury','Debopriyo Chowdhury','debopriyo@gmail.com','Yes',3,0,0,0,'0','Food',''),(34,'Diapk Gupta','Munia Gupta','dgupta@sdsu.edu','Yes',3,0,0,0,'0','Food',''),(35,'Hari Khatuya','Nilima Bisws','hkhatuya@yahoo.com','Yes',3,0,0,0,'0','Food',''),(36,'Jayanta Mukhopadhyaya','Keya Bandyopadhyay','jayanta07@yahoo.com','Yes',2,0,0,0,'0','Food',''),(37,'Kajal Chowdhury','Urmi Banerjee','U_banerjee@hotmail.com','Yes',2,0,0,0,'0','Food',''),(38,'Bobby Ghoshal','Devashi Ghoshal','jayati.ghoshal@gmail.com','Yes',2,0,0,0,'0','',''),(39,'Debarati Poddar','Kaushik Kundu','Debarati.kk@gmail.com','Yes',3,0,0,0,'0','',''),(40,'Koushik Das','Susmita Chandra','d.koushik@gmail.com','Yes',6,0,0,0,'0','',''),(41,'Mriganka Mondal','Mriganka Mondal','Contact.mriganka@gmail.com','Yes',2,0,0,0,'0','',''),(42,'Nandan Das','Lopamudra Das','nandan@gmail.com','Yes',5,0,0,0,'0','',''),(43,'Partha Ray','Partha Ray','Sumana13@hotmail.com','Yes',4,0,0,0,'0','',''),(44,'Pijush Dewanjee ','Pijush Dewanjee ','pijushd@sbcglobal.net','Yes',1,0,0,0,'0','set up',''),(45,'Chandana sur','Pradip sur','pradipsur4@gmail.com','Yes',2,0,0,0,'0','',''),(46,'Pranab Dutt','Shefali Dutt','duttps@aol.com','Yes',3,0,0,0,'0','',''),(47,'Probir Paul','Reba Paul','Probir5463@gmail.com','Yes',2,0,0,0,'0','',''),(48,'Raja Govindarajan','Sukanya Govindarajan','raja.govindarajan@gmail.com','Yes',2,0,0,0,'0','Games',''),(49,'Rakesh Sit','Suparna Sit','sitrakesh@gmail.com','Yes',3,0,0,0,'0','',''),(50,'Ranjan Raha,Anjuman Raha','Suparna Raha','suparna_raha@yahoo.com','Yes',3,0,0,0,'0','',''),(51,'Samit Dutta','Rajashree ','dutta.samit@gmail.com','Yes',3,0,0,0,'0','',''),(52,'Sandep Nanda','Debleena Jana','debleena11@gmail.com','Yes',3,0,0,0,'0','',''),(53,'Shoubhik Mukhopadhyay','Madhura Basu Majumder','madhurabasu@gmail.com','Yes',3,0,0,0,'0','',''),(54,'Shouvik Das','Pritha Sen','Shouvik86.das@gmail.com','Yes',3,0,0,0,'0','Food',''),(55,'Shubhadip Paul','Amrita Paul','shubhadippaul@gmail.com','Yes',3,0,0,0,'0','',''),(56,'Shyama Prasad Mondal','Rumela Roy','spmondal08@gmail.com','Yes',3,0,0,0,'0','',''),(57,'Soumen Ghosh','Soumen Ghosh','ghosh.soumen86@gmail.com','Yes',3,0,0,0,'0','',''),(58,'Subhadeep Guha','Priyanka Guha','subhadeep.guha@gmail.com','Yes',5,0,0,0,'0','',''),(59,'Anuradha De ','Subrato De','subratokde2002@gmail.com','Yes',3,0,0,0,'0','',''),(60,'Sumit Debnath','Moumita Debnath','debnath.sumit@outlook.com','Yes',3,0,0,0,'0','',''),(61,'Surya De','Surya De','desurya125@gmail.com','Yes',1,0,0,0,'0','',''),(62,'Sushil Mahata','Manjula Mahata','smahata@health.ucsd.edu','Yes',3,0,0,0,'0','',''),(63,'Tirtha Ghosh','Tirtha Ghosh','gtirtha@gmail.com','Yes',1,0,0,0,'0','',''),(64,'Amarnath Gupta','Nupur Roy','roy.nupur@gmail.com','Yes',2,0,0,0,'0','',NULL),(65,'Shantanu Sinha','Usha Sinha','shsinha@ucsd.edu','Yes',2,0,0,0,'0','',NULL),(66,'Siladitya Ray Chaudhuri','Anushka Ray Chowdhury','raychas@gmail.com','Yes',2,0,0,0,'0',NULL,NULL),(67,'Arunava Chaudhuri','Amrita Chatterjee','arunava.chaudhuri@gmail.com','Yes',1,0,0,0,'0','',NULL),(68,'Gautam Bandyopadhyay','Gautam Bandyopadhyay','gbandy4911@gmail.com','Yes',3,0,0,0,'0','',NULL);
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

-- Dump completed on 2023-06-11  7:50:09
