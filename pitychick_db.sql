-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Nov 18, 2025 at 02:22 AM
-- Server version: 8.4.3
-- PHP Version: 8.3.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pitychick_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `admint`
--

CREATE TABLE `admint` (
  `id` int NOT NULL,
  `username` varchar(55) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `password` varchar(55) COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `category_id` int NOT NULL,
  `category` varchar(55) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`category_id`, `category`) VALUES
(421, 'Original'),
(422, 'Add'),
(423, 'Snack'),
(424, 'Beverage');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `id` int NOT NULL,
  `username` varchar(55) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `password` varchar(55) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `email` varchar(55) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `phone` varchar(13) COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `kitchen`
--

CREATE TABLE `kitchen` (
  `id` int NOT NULL,
  `username` varchar(55) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `password` varchar(55) COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `kitchen`
--

INSERT INTO `kitchen` (`id`, `username`, `password`) VALUES
(7546, 'kitchen', '8888');

-- --------------------------------------------------------

--
-- Table structure for table `menus`
--

CREATE TABLE `menus` (
  `product_id` int NOT NULL,
  `category_id` int DEFAULT NULL,
  `menu` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `price` int DEFAULT NULL,
  `category` varchar(9) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `menus`
--

INSERT INTO `menus` (`product_id`, `category_id`, `menu`, `price`, `category`) VALUES
(1, 421, 'Dada', 17000, 'Original'),
(2, 421, 'Paha Atas', 17000, 'Original'),
(3, 421, 'Paha Bawah', 10000, 'Original'),
(4, 421, 'Sayap', 12000, 'Original'),
(11, 422, 'Krisbar', 3000, 'Add'),
(12, 422, 'Geprek Alapity', 3000, 'Add'),
(13, 422, 'Spicy Cheese', 4000, 'Add'),
(14, 422, 'Saus Bangkok', 3000, 'Add'),
(15, 422, 'Brown Creamy', 3000, 'Add'),
(16, 422, 'Krisbar Rendang', 3000, 'Add'),
(17, 422, 'Spicy Mayo Burn', 3000, 'Add'),
(18, 422, 'Blackpepper', 3000, 'Add'),
(21, 423, 'French Fries', 10000, 'Snack'),
(22, 423, 'Spicy Wings', 10000, 'Snack'),
(23, 423, 'Cheese Wings', 15000, 'Snack'),
(24, 423, 'Hot Wings', 15000, 'Snack'),
(31, 424, 'Teh', 4000, 'Beverage'),
(32, 424, 'Teh Kampul', 5000, 'Beverage'),
(33, 424, 'Jeruk', 5000, 'Beverage'),
(34, 424, 'Air Mineral', 5000, 'Beverage'),
(35, 424, 'Cola', 8000, 'Beverage'),
(36, 424, 'Es Cokelat', 10000, 'Beverage'),
(37, 424, 'Es Susu Tape Ketan', 11000, 'Beverage'),
(38, 424, 'Es Susu Tape Ketan Cokelat', 12000, 'Beverage');

-- --------------------------------------------------------

--
-- Table structure for table `payment`
--

CREATE TABLE `payment` (
  `payment_id` int NOT NULL,
  `customer_id` int DEFAULT NULL,
  `total_amount` decimal(10,2) DEFAULT NULL,
  `payment_proof` varchar(55) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `status` varchar(55) COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `purchase_history`
--

CREATE TABLE `purchase_history` (
  `purchase_id` int NOT NULL,
  `payment_id` int DEFAULT NULL,
  `product_id` int DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `purchase_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admint`
--
ALTER TABLE `admint`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`category_id`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `kitchen`
--
ALTER TABLE `kitchen`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `menus`
--
ALTER TABLE `menus`
  ADD PRIMARY KEY (`product_id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indexes for table `payment`
--
ALTER TABLE `payment`
  ADD PRIMARY KEY (`payment_id`),
  ADD KEY `customer_id` (`customer_id`);

--
-- Indexes for table `purchase_history`
--
ALTER TABLE `purchase_history`
  ADD PRIMARY KEY (`purchase_id`),
  ADD KEY `purchase_id` (`purchase_id`,`payment_id`,`product_id`),
  ADD KEY `purchase_history_ibfk_1` (`payment_id`),
  ADD KEY `purchase_history_ibfk_2` (`product_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admint`
--
ALTER TABLE `admint`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `category_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=425;

--
-- AUTO_INCREMENT for table `customer`
--
ALTER TABLE `customer`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `kitchen`
--
ALTER TABLE `kitchen`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7547;

--
-- AUTO_INCREMENT for table `menus`
--
ALTER TABLE `menus`
  MODIFY `product_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- AUTO_INCREMENT for table `payment`
--
ALTER TABLE `payment`
  MODIFY `payment_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `purchase_history`
--
ALTER TABLE `purchase_history`
  MODIFY `purchase_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `menus`
--
ALTER TABLE `menus`
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`);

--
-- Constraints for table `payment`
--
ALTER TABLE `payment`
  ADD CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`);

--
-- Constraints for table `purchase_history`
--
ALTER TABLE `purchase_history`
  ADD CONSTRAINT `purchase_history_ibfk_1` FOREIGN KEY (`payment_id`) REFERENCES `payment` (`payment_id`),
  ADD CONSTRAINT `purchase_history_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `menus` (`product_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
