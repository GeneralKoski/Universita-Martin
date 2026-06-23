-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Creato il: Gen 10, 2025 alle 20:49
-- Versione del server: 10.4.28-MariaDB
-- Versione PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dreamcity`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `Buildings`
--

CREATE TABLE `Buildings` (
  `id` int(11) NOT NULL,
  `Brole_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `color` varchar(15) NOT NULL,
  `width` int(5) NOT NULL,
  `height` int(5) NOT NULL,
  `happiness` int(5) NOT NULL,
  `cost` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `Buildings`
--

INSERT INTO `Buildings` (`id`, `Brole_id`, `name`, `color`, `width`, `height`, `happiness`, `cost`) VALUES
(1, 1, 'TOWNHALL', '#000000', 160, 160, 100, 0),
(2, 2, 'ROAD', '#7F7F7F', 200, 20, 1, 10),
(3, 2, 'ROUNDABOUT', '#AAAAAA', 80, 80, 2, 15),
(4, 3, 'FACTORY', '#FF6600', 340, 135, 25, 200),
(5, 6, 'HOUSE', '#FFFF00', 150, 60, 8, 50),
(6, 6, 'HUT', '#996600', 40, 40, 4, 20),
(7, 2, 'WATER', '#00BFFF', 30, 30, 1, 10),
(8, 7, 'HOSPITAL', '#FF9999', 200, 150, 50, 300),
(9, 9, 'POWER PLANT', '#8F00FF', 170, 140, 15, 200),
(10, 8, 'SCHOOL', '#800000', 180, 120, 30, 120),
(11, 9, 'HYDRAULIC POWER PLANT', '#191170', 150, 100, 10, 150),
(12, 8, 'LIBRARY', '#06402B', 120, 80, 20, 100),
(13, 10, 'BUS STOP', '#FF1493', 50, 50, 5, 30),
(14, 10, 'METRO STOP', '#BF86A3', 100, 100, 20, 200),
(15, 10, 'TRAM STOP', '#C0C0C0', 75, 75, 15, 40),
(16, 3, 'SHOPPING CENTER', '#D2691E', 300, 175, 40, 350),
(17, 4, 'CINEMA', '#8B4513', 130, 50, 35, 225),
(18, 4, 'MUSEUM', '#FFD700', 215, 80, 20, 180),
(19, 4, 'THEATER', '#A52A2A', 100, 50, 25, 200),
(20, 5, 'STADIUM', '#F0E68C', 450, 200, 90, 500),
(21, 5, 'GYM', '#C71585', 135, 60, 70, 350),
(22, 8, 'UNIVERSITY', '#D2B48C', 300, 100, 15, 190),
(23, 11, 'POLICE STATION', '#D2B48C', 180, 90, 10, 75),
(24, 12, 'FARM', '#F4A460', 450, 135, 5, 30),
(25, 12, 'GREENHOUSE', '#00FF00', 80, 35, 10, 75),
(26, 3, 'SUPERMARKET', '#0091FF', 275, 120, 35, 200);

-- --------------------------------------------------------

--
-- Struttura della tabella `Departments`
--

CREATE TABLE `Departments` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `Dmap_id` int(11) NOT NULL,
  `Drole_id` int(11) DEFAULT NULL,
  `budget` int(10) NOT NULL DEFAULT 10000
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `Departments`
--

INSERT INTO `Departments` (`id`, `user_id`, `Dmap_id`, `Drole_id`, `budget`) VALUES
(1,1,1,9,10000),
(2,1,2,11,10000),
(3,1,3,12,10000),
(4,1,4,4,10000),
(5,1,5,1,10000),
(6,1,6,3,10000),
(7,1,7,8,10000),
(8,1,8,2,10000),
(9,1,9,6,10000),
(10,1,10,7,10000),
(11,2,1,10,10000),
(12,2,2,12,10000),
(13,2,3,1,10000),
(14,2,4,5,10000),
(15,2,5,2,10000),
(16,2,6,4,10000),
(17,2,7,9,10000),
(18,2,8,3,10000),
(19,2,9,7,10000),
(20,2,10,8,10000),
(21,3,1,11,10000),
(22,3,2,1,10000),
(23,3,3,2,10000),
(24,3,4,6,10000),
(25,3,5,3,10000),
(26,3,6,5,10000),
(27,3,7,10,10000),
(28,3,8,4,10000),
(29,3,9,8,10000),
(30,3,10,9,10000),
(31,4,1,12,10000),
(32,4,2,2,10000),
(33,4,3,3,10000),
(34,4,4,7,10000),
(35,4,5,4,10000),
(36,4,6,6,10000),
(37,4,7,11,10000),
(38,4,8,5,10000),
(39,4,9,9,10000),
(40,4,10,10,10000),
(41,5,1,1,10000),
(42,5,2,3,10000),
(43,5,3,4,10000),
(44,5,4,8,10000),
(45,5,5,5,10000),
(46,5,6,7,10000),
(47,5,7,12,10000),
(48,5,8,6,10000),
(49,5,9,10,10000),
(50,5,10,11,10000),
(51,6,1,2,10000),
(52,6,2,4,10000),
(53,6,3,5,10000),
(54,6,4,9,10000),
(55,6,5,6,10000),
(56,6,6,8,10000),
(57,6,7,1,10000),
(58,6,8,7,10000),
(59,6,9,11,10000),
(60,6,10,3,10000),
(61,7,1,3,10000),
(62,7,2,5,10000),
(63,7,3,6,10000),
(64,7,4,10,10000),
(65,7,5,7,10000),
(66,7,6,9,10000),
(67,7,7,2,10000),
(68,7,8,8,10000),
(69,7,9,12,10000),
(70,7,10,4,10000),
(71,8,1,4,10000),
(72,8,2,6,10000),
(73,8,3,7,10000),
(74,8,4,11,10000),
(75,8,5,8,10000),
(76,8,6,10,10000),
(77,8,7,3,10000),
(78,8,8,9,10000),
(79,8,9,1,10000),
(80,8,10,12,10000),
(81,9,1,5,10000),
(82,9,2,7,10000),
(83,9,3,8,10000),
(84,9,4,12,10000),
(85,9,5,9,10000),
(86,9,6,11,10000),
(87,9,7,4,10000),
(88,9,8,10,10000),
(89,9,9,2,10000),
(90,9,10,1,10000),
(91,10,1,6,10000),
(92,10,2,8,10000),
(93,10,3,9,10000),
(94,10,4,1,10000),
(95,10,5,10,10000),
(96,10,6,12,10000),
(97,10,7,5,10000),
(98,10,8,11,10000),
(99,10,9,3,10000),
(100,10,10,2,10000);

-- --------------------------------------------------------

--
-- Struttura della tabella `MapBuildings`
--

CREATE TABLE `MapBuildings` (
  `id` int(11) NOT NULL,
  `MBmap_id` int(11) NOT NULL,
  `MBbuilding_id` int(11) NOT NULL,
  `x_coordinate` int(11) NOT NULL,
  `y_coordinate` int(11) NOT NULL,
  `rotated` enum('yes','no') NOT NULL DEFAULT 'no'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- --------------------------------------------------------

--
-- Struttura della tabella `MapClicks`
--

CREATE TABLE `MapClicks` (
  `id` int(11) NOT NULL,
  `Cmap_id` int(11) NOT NULL,
  `Cuser_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `MapClicks`
--

INSERT INTO `MapClicks` (`id`, `Cmap_id`, `Cuser_id`) VALUES
(1,4,2),
(2,4,3),
(3,4,4),
(4,4,5),
(5,4,6),
(6,4,7),
(7,4,8),
(8,4,9),
(9,4,10);

-- --------------------------------------------------------

--
-- Struttura della tabella `Maps`
--

CREATE TABLE `Maps` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` varchar(500) NOT NULL,
  `image` varchar(1000) NOT NULL,
  `happiness` int(10) NOT NULL,
  `citizens` int(11) NOT NULL DEFAULT 0,
  `lastLogin` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `Maps`
--

INSERT INTO `Maps` (`id`, `name`, `description`, `image`, `happiness`, `citizens`, `lastLogin`) VALUES
(1, 'Mappa 1','Descrizione della mappa 1','Mappa 1_1738707674.jpg',10,0,'2025-02-04 22:21:14'),
(2, 'Mappa 2','Descrizione della mappa 2','Mappa 2_1738707692.jpg',501,0,'2025-02-04 22:21:32'),
(3, 'Mappa 3','Descrizione della mappa 3','Mappa 3_1738707710.jpeg',1200,0,'2025-02-04 22:21:50'),
(4, 'Mappa 4','Descrizione della mappa 4','Mappa 4_1738707729.jpeg',0,0,'2025-02-04 22:22:09'),
(5, 'Mappa 5','Descrizione della mappa 5','Mappa 5_1738707748.jpeg',190,0,'2025-02-04 22:22:28'),
(6, 'Mappa 6','Descrizione della mappa 6','Mappa 6_1738707766.png',1000,0,'2025-02-04 22:22:46'),
(7, 'Mappa 7','Descrizione della mappa 7','Mappa 7_1738707785.png',200,0,'2025-02-04 22:23:05'),
(8, 'Mappa 8','Descrizione della mappa 8','Mappa 8_1738707842.jpg',400,0,'2025-02-04 22:24:02'),
(9, 'Mappa 9','Descrizione della mappa 9','Mappa 9_1738707858.png',500,0,'2025-02-04 22:24:18'),
(10, 'Mappa 10','Descrizione della mappa 10','Mappa 10_1738707904.png',100,0,'2025-02-04 22:25:04');

-- --------------------------------------------------------

--
-- Struttura della tabella `Messages`
--

CREATE TABLE `Messages` (
  `id` int(11) NOT NULL,
  `title` varchar(100) NOT NULL,
  `content` varchar(1000) NOT NULL,
  `type` enum('Message','Invite','ChangeRole') NOT NULL DEFAULT 'Message',
  `sender_id` int(11) NOT NULL,
  `receiver_id` int(11) NOT NULL,
  `Mmap_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `Messages`
--

INSERT INTO `Messages` (`id`, `title`, `content`, `type`, `sender_id`, `receiver_id`, `Mmap_id`) VALUES
   (1,'Cambio Ruolo - Accetta','Questo è un messaggio di tipo Cambio Ruolo, quando lo accetta verrà reindirizzato alla mappa 3 e avrà il ruolo cambiato in Riscossione delle tasse e ripartizione degli introiti','ChangeRole',2,1,3),
	 (2,'Cambio Ruolo - Rifiuta','Questo è un messaggio di tipo Cambio Ruolo, quando lo rifiuta il messaggio verrà cancellato','ChangeRole',2,1,3),
	 (3,'Invito - Accetta','Questo è un messaggio di tipo invito, quando lo accetta verrà reindirizzato alla mappa 3','Invite',2,1,3),
	 (4,'Invito - Rifiuta','Questo è un messaggio di tipo Invito, quando lo rifiuta il messaggio verrà cancellato','Invite',2,1,3),
	 (5,'Messaggio normale','Questo è un messaggio normale usato per la comunicazione tra gli utenti','Message',2,1,3);

-- --------------------------------------------------------

--
-- Struttura della tabella `Roles`
--

CREATE TABLE `Roles` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `department_desc` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `Roles`
--

INSERT INTO `Roles` (`id`, `name`, `department_desc`) VALUES
(1, 'Riscossione delle tasse e ripartizione degli introiti', 'Utente che riscuote le tasse e suddivide gli introiti ai vari ruoli'),
(2, 'Gestione delle strade', 'Utente che si occupa di costruire le strade, i fiumi e i laghi in tutta la mappa'),
(3, 'Attività commerciali', 'Utente che si occupa di costruire le attività commerciali'),
(4, 'Spettacoli', 'Utente che si occupa di costruire i musei, teatri e cinema'),
(5, 'Sport', 'Utente che si occupa di costruire i centri sportivi'),
(6, 'Edilizia', 'Utente che si occupa di costruire le case'),
(7, 'Sanità', 'Utente che si occupa della costruzione degli ospedali'),
(8, 'Istruzione', 'Utente che si occupa della costruzione di scuole e biblioteche.'),
(9, 'Servizi Urbani', 'Utente adibito alla costruzione di centrali elettriche, centrali idrauliche e centrali nucleari.'),
(10, 'Trasporti', 'Utente che si occuperà della costruzione di fermate dell autobus, fermate della metropolitana e fermate del tram'),
(11, 'Difesa', 'Utente adibito alla sicurezza pubblica, quindi alla costruzione di edifici delle forze armate.'),
(12, 'Agricoltura e allevamento', 'Utente che gestirà le varie strutture agricole e di allevamento.');

-- --------------------------------------------------------

--
-- Struttura della tabella `Users`
--

CREATE TABLE `Users` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `avatar` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `Users`
--

INSERT INTO `Users` (`id`, `username`, `password`, `avatar`) VALUES
(1, 'user1','$argon2i$v=19$m=65536,t=4,p=1$cmtSMlMvZzdIZ0NMbG9VZw$iHpTa+5ob2+CaqdBJFHqRTVsNlH3Gy0AB0yXTLnIUOk','user1_1738707032.jpg'),
(2, 'user2','$argon2i$v=19$m=65536,t=4,p=1$T29IUXZQVmNaYXdWSkhUWg$T7aZv6wE5+CUp5GhzmHznMelUlVcuJ1hUuvOf+AFA6A','user2_1738707045.jpeg'),
(3, 'user3','$argon2i$v=19$m=65536,t=4,p=1$VVlWOWxTcy5UcmFCbGJzRg$J0PZ2+/mLQ3jJ0S3B2T8tNlBciqLWSaExI5E4D5O5mI','user3_1738707053.jpg'),
(4, 'user4','$argon2i$v=19$m=65536,t=4,p=1$T2FnZE0uNjUvV2x5bWVMTw$JroNGAkDxeGWenHV9Jfe2SMukbhZtBz94K2YSqwjkiI','user4_1738707079.jpeg'),
(5, 'user5','$argon2i$v=19$m=65536,t=4,p=1$Wkl1QlpuUkY2NlV2QWtMdw$HW/CGMdeKLh6j3xv9BV6r6qIQlc638QnHiHW0tf6zrs','user5_1738707100.jpeg'),
(6, 'user6','$argon2i$v=19$m=65536,t=4,p=1$RjJsbWF0a01QWjVOU2w1Rw$3Vk7uwpl944RYwJnskMHRxFIY7RofdsoWZGw/oaPmmA','user6_1738707125.jpg'),
(7, 'user7','$argon2i$v=19$m=65536,t=4,p=1$UWk1UElHTHc3N1pGMU1FWQ$6YtOsKP0udMHGZkBeIfTtcL+OYqSqsUo18PQQ4bDXxQ','user7_1738707134.jpg'),
(8, 'user8','$argon2i$v=19$m=65536,t=4,p=1$STRMdDIzM1NxbzkxWGJ3Yg$noCu9C6KiX9TYRAmqtb2hdUoUCZ7no1114MkQiBY4Mk','user8_1738707143.png'),
(9, 'user9','$argon2i$v=19$m=65536,t=4,p=1$Y0JMV055Ymh0cTFZeVFxUw$hhuFZVjZLDiZzh1JdIC9/DtxVlbJYUJp46gGEGAwCyE','user9_1738707156.png'),
(10, 'user10','$argon2i$v=19$m=65536,t=4,p=1$M2F5NUxWcVcwTVBMWGg0ZA$XQSuBAanAG8ZgMqUmIrWebcwAD5PovYjmlk6pHAsjP0','user10_1738707173.png');	 

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `Buildings`
--
ALTER TABLE `Buildings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `Brole_id_fk` (`Brole_id`);

--
-- Indici per le tabelle `Departments`
--
ALTER TABLE `Departments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `Dmap_id_fk` (`Dmap_id`),
  ADD KEY `Duser_id_fk` (`user_id`),
  ADD KEY `Drole_id_fk` (`Drole_id`);

--
-- Indici per le tabelle `MapBuildings`
--
ALTER TABLE `MapBuildings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `MBbuilding_id_fk` (`MBbuilding_id`),
  ADD KEY `MBmap_id_fk` (`MBmap_id`);

--
-- Indici per le tabelle `MapClicks`
--
ALTER TABLE `MapClicks`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `Cmap_id` (`Cmap_id`,`Cuser_id`),
  ADD KEY `Cuser_id_fk` (`Cuser_id`);

--
-- Indici per le tabelle `Maps`
--
ALTER TABLE `Maps`
  ADD PRIMARY KEY (`id`);

--
-- Indici per le tabelle `Messages`
--
ALTER TABLE `Messages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sender_id_fk` (`sender_id`),
  ADD KEY `receiver_id_fk` (`receiver_id`),
  ADD KEY `Mmap_id_fk` (`Mmap_id`);

--
-- Indici per le tabelle `Roles`
--
ALTER TABLE `Roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_role` (`name`);

--
-- Indici per le tabelle `Users`
--
ALTER TABLE `Users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `Buildings`
--
ALTER TABLE `Buildings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT per la tabella `Departments`
--
ALTER TABLE `Departments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT per la tabella `MapBuildings`
--
ALTER TABLE `MapBuildings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=740;

--
-- AUTO_INCREMENT per la tabella `MapClicks`
--
ALTER TABLE `MapClicks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT per la tabella `Maps`
--
ALTER TABLE `Maps`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT per la tabella `Messages`
--
ALTER TABLE `Messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT per la tabella `Roles`
--
ALTER TABLE `Roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT per la tabella `Users`
--
ALTER TABLE `Users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `Buildings`
--
ALTER TABLE `Buildings`
  ADD CONSTRAINT `Brole_id_fk` FOREIGN KEY (`Brole_id`) REFERENCES `Roles` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `Departments`
--
ALTER TABLE `Departments`
  ADD CONSTRAINT `Dmap_id_fk` FOREIGN KEY (`Dmap_id`) REFERENCES `Maps` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `Drole_id_fk` FOREIGN KEY (`Drole_id`) REFERENCES `Roles` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `Duser_id_fk` FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `MapBuildings`
--
ALTER TABLE `MapBuildings`
  ADD CONSTRAINT `MBbuilding_id_fk` FOREIGN KEY (`MBbuilding_id`) REFERENCES `Buildings` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `MBmap_id_fk` FOREIGN KEY (`MBmap_id`) REFERENCES `Maps` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `MapClicks`
--
ALTER TABLE `MapClicks`
  ADD CONSTRAINT `Cmap_id_fk` FOREIGN KEY (`Cmap_id`) REFERENCES `Maps` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `Cuser_id_fk` FOREIGN KEY (`Cuser_id`) REFERENCES `Users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `Messages`
--
ALTER TABLE `Messages`
  ADD CONSTRAINT `Mmap_id_fk` FOREIGN KEY (`Mmap_id`) REFERENCES `Maps` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `receiver_id_fk` FOREIGN KEY (`receiver_id`) REFERENCES `Users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `sender_id_fk` FOREIGN KEY (`sender_id`) REFERENCES `Users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
