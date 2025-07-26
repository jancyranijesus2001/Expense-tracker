-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Feb 04, 2025 at 12:55 PM
-- Server version: 8.3.0
-- PHP Version: 8.2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";
USE sql8791991;



/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `expenses`
--

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
CREATE TABLE IF NOT EXISTS `category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cate` varchar(100) NOT NULL,
  `subcat` varchar(30) NOT NULL,
  `priority` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`id`, `cate`, `subcat`, `priority`) VALUES
(1, 'General', 'Food (Grocery)', 'High'),
(2, 'General', 'Education', 'High'),
(3, 'General', 'Utilities(Rent,Water,EB,Phone ', 'High'),
(4, 'General', 'Investments(Loan, LIC,EMI,Tax)', 'High'),
(5, 'General', 'Travel Expenses(Bike,Car)', 'Medium'),
(6, 'General', 'Medical Expenses', 'Medium'),
(7, 'General', 'TV Dish Nexflix Recharges ', 'Low'),
(8, 'General', 'Maid Salary', 'Low'),
(9, 'Others', 'Online Offline Shopping', 'Low'),
(10, 'Others', 'Festival Shopping', 'High'),
(11, 'Others', 'Temple or Function Trip', 'High'),
(12, 'Others', 'Tours and Travels', 'Medium'),
(13, 'Others', 'Entertainment Theaters or Outd', 'Low'),
(14, 'Others', 'Foods(Junk,Cool Drinks)', 'Low'),
(15, 'Others', 'Fitness Yoga', 'High'),
(16, 'Others', 'Alcohol Cigarette', 'Poor'),
(17, 'Others', 'Parties or Friends Meet', 'Medium'),
(18, 'Others', 'Investments(Share Market,Rummy', 'Low');

-- --------------------------------------------------------

--
-- Table structure for table `incomedet`
--

DROP TABLE IF EXISTS `incomedet`;
CREATE TABLE IF NOT EXISTS `incomedet` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_id` int NOT NULL,
  `amount` bigint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `incomedet`
--

INSERT INTO `incomedet` (`id`, `date`, `user_id`, `amount`) VALUES
(1, '2025-01-21 18:23:36', 9, 50000),
(2, '2025-01-21 18:27:47', 9, 50000),
(3, '2025-01-21 18:23:36', 3, 10000),
(4, '2025-01-27 19:06:30', 10, 100000),
(5, '2025-01-27 19:09:14', 11, 100000),
(6, '2025-02-04 11:38:58', 12, 100000),
(7, '2025-02-04 11:39:12', 12, 50000);

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
CREATE TABLE IF NOT EXISTS `transactions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `amount` int NOT NULL DEFAULT '0',
  `description` varchar(255) DEFAULT NULL,
  `category` varchar(255) DEFAULT NULL,
  `subcat` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`id`, `user_id`, `amount`, `description`, `category`, `subcat`, `date`) VALUES
(16, 8, 2000, 'Fees', 'General', 'Education', '2024-11-20 03:49:00'),
(10, 9, 5000, 'Semester Fees', 'General', 'Education', '2024-11-18 11:57:00'),
(8, 9, 200, 'Fees', 'General', 'Education', '2024-12-19 11:32:13'),
(34, 9, 500, 'Friends', 'Others', 'Alcohol Cigarette', '2025-01-23 17:36:18'),
(33, 9, 4000, 'Birthday Party', 'Others', 'Alcohol Cigarette', '2025-01-22 16:58:06'),
(35, 9, 1000, 'Flim', 'Others', 'Entertainment Theaters or Outd', '2025-01-23 17:36:49'),
(32, 9, 500, 'Friends', 'Others', 'Foods(Junk,Cool Drinks)', '2025-01-22 16:57:46'),
(29, 9, 4000, 'LIC', 'General', 'Investments(Loan, LIC,EMI,Tax)', '2025-01-21 18:25:46'),
(28, 9, 600, 'for Amma', 'General', 'Medical Expenses', '2025-01-21 13:09:53'),
(31, 9, 600, 'Gym', 'Others', 'Fitness Yoga', '2025-01-22 12:02:00'),
(36, 9, 2000, 'Tour', 'Others', 'Tours and Travels', '2025-01-23 18:44:34'),
(37, 9, 2000, 'Tour', 'Others', 'Tours and Travels', '2025-01-23 18:45:26'),
(38, 10, 500, 'fg', 'General', 'Utilities(Rent,Water,EB,Phone ', '2025-01-27 19:07:23'),
(39, 11, 500, 'EB', 'General', 'Utilities(Rent,Water,EB,Phone ', '2025-01-27 19:09:29'),
(40, 11, 2000, 'friends', 'Others', 'Alcohol Cigarette', '2025-01-27 19:09:45'),
(41, 11, 5000, 'Tour', 'Others', 'Tours and Travels', '2025-01-27 19:09:59'),
(42, 11, 2500, 'Friends', 'Others', 'Foods(Junk,Cool Drinks)', '2025-01-27 13:40:00'),
(43, 12, 2000, 'Rent', 'General', 'Utilities(Rent,Water,EB,Phone ', '2025-02-04 11:39:35'),
(44, 12, 1000, 'Tablets', 'General', 'Medical Expenses', '2025-02-04 11:39:50'),
(45, 12, 5000, 'Family Tour', 'Others', 'Tours and Travels', '2025-02-04 11:40:09'),
(46, 12, 3000, 'Friends Meet', 'Others', 'Foods(Junk,Cool Drinks)', '2025-02-04 11:40:24'),
(47, 12, 5000, 'Party', 'Others', 'Alcohol Cigarette', '2025-02-04 11:40:37'),
(48, 12, 4000, 'Tours', 'Others', 'Tours and Travels', '2025-02-04 11:42:14'),
(49, 12, 5000, 'Party', 'Others', 'Alcohol Cigarette', '2025-02-04 11:42:58');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fname` varchar(100) DEFAULT NULL,
  `lname` varchar(100) DEFAULT NULL,
  `email` text,
  `uname` varchar(100) DEFAULT NULL,
  `pswd` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_unique` (`email`(200))
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `fname`, `lname`, `email`, `uname`, `pswd`) VALUES
(12, 'janani', 'Ramu', 'janani@gmail.com', 'janani', 'janani'),
(11, 'yuva', 'yuva', 'yuva@gmail.com', 'yuva', 'yuva'),
(10, 'varsan', 'varsan', 'varsan@gmail.com', 'varsan', 'varsan'),
(8, 'karthi', 'ram', 'karthi@gmail.com', 'karthi', 'karthi'),
(9, 'manju', 'manju', 'manju@gmail.com', 'manju', 'manju');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
