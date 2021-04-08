-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 29-03-2021 a las 05:19:47
-- Versión del servidor: 10.4.18-MariaDB
-- Versión de PHP: 8.0.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `dova`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `Uid` int(11) NOT NULL,
  `Unombre` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `Uapellido` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `Ucorreo` varchar(150) COLLATE utf8_unicode_ci NOT NULL,
  `Upassword` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `Ufecha_creacion` datetime NOT NULL,
  `Ufecha_modificacion` datetime NOT NULL,
  `Uestado` int(1) NOT NULL,
  `Eid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`Uid`, `Unombre`, `Uapellido`, `Ucorreo`, `Upassword`, `Ufecha_creacion`, `Ufecha_modificacion`, `Uestado`, `Eid`) VALUES
(1, 'Luis Adrian', 'Morales Zavala', 'lm98adrian@gmail.com', '12345678', '0000-00-00 00:00:00', '2021-03-26 21:48:48', 1, 1),
(2, 'Jose', 'Perez', 'a@gmail.com', '1', '0000-00-00 00:00:00', '2021-03-26 23:12:29', 1, 1),
(6, 'Adrian', 'Morales', 'a2@gmail.com', '123', '0000-00-00 00:00:00', '0000-00-00 00:00:00', 1, 1),
(8, 'x', 'x', 'a3@gmail.com', '1', '0000-00-00 00:00:00', '0000-00-00 00:00:00', 1, 1),
(9, 'x', 'c', 'a4@gmail.com', 'd', '0000-00-00 00:00:00', '0000-00-00 00:00:00', 0, 1),
(14, 'Linda', 'Heredia', 'a5@gmail.com', '12345678', '0000-00-00 00:00:00', '0000-00-00 00:00:00', 1, 1),
(24, 'x', 'x', 'xx@gmail.com', '12345678', '0000-00-00 00:00:00', '0000-00-00 00:00:00', 1, 1),
(25, 'fecha', 'asd', 'asd@gmail.com', '12345678', '0000-00-00 00:00:00', '2021-03-24 00:04:03', 1, 1),
(26, 'prueba', 'fecha', 'fecha@gmail.com', '12345678', '2021-03-24 00:05:20', '2021-03-24 14:30:40', 1, 1),
(27, 'Lindaas', 'Heredia', 'l1@gmail.com', '12345678', '2021-03-24 00:05:20', '2021-03-24 17:43:16', 1, 1),
(30, 'asdasd', 'asdad', 'asdasdsda@gmail.com', '12345678', '2021-03-24 15:10:39', '2021-03-25 17:13:04', 2, 2);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`Uid`),
  ADD UNIQUE KEY `email` (`Ucorreo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `Uid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
