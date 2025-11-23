-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Nov 23, 2025 at 01:23 PM
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
-- Database: `atm_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `transaction_date` datetime DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `initial_balance` decimal(10,2) DEFAULT NULL,
  `final_balance` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`id`, `user_id`, `transaction_date`, `type`, `amount`, `initial_balance`, `final_balance`) VALUES
(1, 4, '2025-11-23 19:32:24', 'setor', 500000.00, 4.00, 500004.00),
(2, 4, '2025-11-23 19:33:53', 'setor', 400000.00, 4.00, 400004.00),
(3, 4, '2025-11-23 19:35:17', 'setor', 500000.00, 4.00, 500004.00),
(4, 4, '2025-11-23 19:37:26', 'setor', 500000.00, 4.00, 500004.00),
(5, 4, '2025-11-23 19:39:36', 'setor', 500000.00, 4.00, 500004.00),
(6, 4, '2025-11-23 19:48:59', 'setor', 50000.00, 4.00, 50004.00),
(7, 5, '2025-11-23 19:56:25', 'setor', 50000.00, 5.00, 50005.00),
(8, 4, '2025-11-23 19:58:59', 'setor', 500000.00, 4.00, 500004.00),
(9, 4, '2025-11-23 20:02:06', 'setor', 50.00, 4.00, 54.00),
(10, 4, '2025-11-23 20:02:48', 'setor', 500.00, 4.00, 504.00),
(11, 4, '2025-11-23 20:05:31', 'setor', 50.00, 4.00, 54.00),
(12, 4, '2025-11-23 20:09:18', 'setor', 50000.00, 4.00, 50004.00),
(13, 4, '2025-11-23 20:09:39', 'setor', 600000.00, 4.00, 600004.00),
(14, 4, '2025-11-23 20:10:00', 'setor', 50000.00, 4.00, 50004.00),
(15, 4, '2025-11-23 20:12:49', 'setor', 50000.00, 50004.00, 100004.00),
(16, 4, '2025-11-23 20:19:04', 'setor', 50000.00, 100004.00, 150004.00),
(17, 4, '2025-11-23 20:19:18', 'tarik', 50000.00, 150004.00, 100004.00),
(18, 4, '2025-11-23 20:19:27', 'tarik', 50000.00, 100004.00, 50004.00);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `username` varchar(50) NOT NULL,
  `pin` varchar(4) NOT NULL,
  `role` enum('nasabah','admin') NOT NULL,
  `saldo` decimal(10,2) DEFAULT '0.00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `pin`, `role`, `saldo`) VALUES
(1, 'admin123', '0000', 'admin', 0.00),
(2, '12345678', '1111', 'nasabah', 500000.00),
(4, 'admin1234', '4444', 'nasabah', 50004.00),
(5, 'bahlil', '5678', 'nasabah', 50005.00),
(6, '225216678', '1888', 'nasabah', 0.00);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `transactions`
--
ALTER TABLE `transactions`
  ADD CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
