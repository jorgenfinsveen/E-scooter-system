-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: s687.loopia.se
-- Generation Time: 04. Mai, 2025 20:11 PM
-- Tjener-versjon: 10.11.11-MariaDB-log
-- PHP Version: 8.1.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ttm4115-team-16-test-db`
--
CREATE DATABASE IF NOT EXISTS `ttm4115-team-16-test-db` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `ttm4115-team-16-test-db`;

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `corider`
--

CREATE TABLE `corider` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `scooter_id` int(11) NOT NULL,
  `session_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `multisession`
--

CREATE TABLE `multisession` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `start_time` timestamp NULL DEFAULT NULL ON UPDATE current_timestamp(),
  `end_time` timestamp NULL DEFAULT NULL,
  `isActive` tinyint(1) DEFAULT NULL,
  `longtitude` float NOT NULL,
  `latitude` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `rentals`
--

CREATE TABLE `rentals` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `scooter_id` int(11) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `start_time` timestamp NULL DEFAULT NULL,
  `end_time` timestamp NULL DEFAULT NULL,
  `total_price` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `scooters`
--

CREATE TABLE `scooters` (
  `uuid` int(11) NOT NULL,
  `latitude` float NOT NULL,
  `longtitude` float NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dataark for tabell `scooters`
--

INSERT INTO `scooters` (`uuid`, `latitude`, `longtitude`, `status`) VALUES
(1, 63.4197, 10.4018, 0),
(2, 63.4153, 10.3995, 0),
(3, 63.4197, 10.4018, 1),
(4, 63.4197, 10.4018, 2),
(5, 63.4197, 10.4018, 3),
(6, 63.4197, 10.4018, 11);

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `funds` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dataark for tabell `users`
--

INSERT INTO `users` (`id`, `name`, `funds`) VALUES
(1, 'John Appleseed', 450.0),
(2, 'Kari Nordmann', 600.0),
(3, 'Albert Einstein', 75.5),


--
-- Indexes for dumped tables
--

--
-- Indexes for table `corider`
--
ALTER TABLE `corider`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_user_id` (`user_id`),
  ADD KEY `fk_scooter_id` (`scooter_id`),
  ADD KEY `fk_session_id` (`session_id`);

--
-- Indexes for table `multisession`
--
ALTER TABLE `multisession`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_multisession_user_id` (`user_id`);

--
-- Indexes for table `rentals`
--
ALTER TABLE `rentals`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `scooter_id` (`scooter_id`);

--
-- Indexes for table `scooters`
--
ALTER TABLE `scooters`
  ADD PRIMARY KEY (`uuid`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `corider`
--
ALTER TABLE `corider`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `multisession`
--
ALTER TABLE `multisession`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `rentals`
--
ALTER TABLE `rentals`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=227;

--
-- AUTO_INCREMENT for table `scooters`
--
ALTER TABLE `scooters`
  MODIFY `uuid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Begrensninger for dumpede tabeller
--

--
-- Begrensninger for tabell `corider`
--
ALTER TABLE `corider`
  ADD CONSTRAINT `fk_scooter_id` FOREIGN KEY (`scooter_id`) REFERENCES `scooter` (`id`),
  ADD CONSTRAINT `fk_session_id` FOREIGN KEY (`session_id`) REFERENCES `multisession` (`id`),
  ADD CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Begrensninger for tabell `multisession`
--
ALTER TABLE `multisession`
  ADD CONSTRAINT `fk_multisession_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Begrensninger for tabell `rentals`
--
ALTER TABLE `rentals`
  ADD CONSTRAINT `rentals_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `rentals_ibfk_2` FOREIGN KEY (`scooter_id`) REFERENCES `scooters` (`uuid`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
