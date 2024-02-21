-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: algaprekins
-- ------------------------------------------------------
-- Server version	8.0.36

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
-- Table structure for table `alga`
--

DROP TABLE IF EXISTS `alga`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alga` (
  `ID_alga` int NOT NULL,
  `uznemums` varchar(45) NOT NULL,
  `neto_alga` decimal(10,0) NOT NULL,
  `darbinieks_ID` int NOT NULL,
  `darba_devejs_ID` int NOT NULL,
  PRIMARY KEY (`ID_alga`),
  UNIQUE KEY `darba_devejs_ID_UNIQUE` (`darba_devejs_ID`),
  UNIQUE KEY `darbinieks_ID_UNIQUE` (`darbinieks_ID`),
  CONSTRAINT `darba_devejs_ID` FOREIGN KEY (`darba_devejs_ID`) REFERENCES `darba_devejs` (`ID_darba_devejs`),
  CONSTRAINT `darbinieks_ID` FOREIGN KEY (`darbinieks_ID`) REFERENCES `darbinieks` (`ID_darbinieks`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alga`
--

LOCK TABLES `alga` WRITE;
/*!40000 ALTER TABLE `alga` DISABLE KEYS */;
/*!40000 ALTER TABLE `alga` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `darba_devejs`
--

DROP TABLE IF EXISTS `darba_devejs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `darba_devejs` (
  `ID_darba_devejs` int NOT NULL,
  `darba_devejs_vards` varchar(45) NOT NULL,
  `darb_devejs_uzvards` varchar(45) NOT NULL,
  PRIMARY KEY (`ID_darba_devejs`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `darba_devejs`
--

LOCK TABLES `darba_devejs` WRITE;
/*!40000 ALTER TABLE `darba_devejs` DISABLE KEYS */;
/*!40000 ALTER TABLE `darba_devejs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `darbinieks`
--

DROP TABLE IF EXISTS `darbinieks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `darbinieks` (
  `ID_darbinieks` int NOT NULL,
  `darbinieks_vards` varchar(45) NOT NULL,
  `darbinieks_uzvards` varchar(45) NOT NULL,
  `darbinieks_pk` varchar(12) NOT NULL,
  `darbinieks_berni` int NOT NULL,
  `darbinieks_alga` decimal(10,0) NOT NULL,
  PRIMARY KEY (`ID_darbinieks`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `darbinieks`
--

LOCK TABLES `darbinieks` WRITE;
/*!40000 ALTER TABLE `darbinieks` DISABLE KEYS */;
/*!40000 ALTER TABLE `darbinieks` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-24 13:40:55
