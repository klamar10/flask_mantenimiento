-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 29-03-2021 a las 07:24:26
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
-- Estructura de tabla para la tabla `uar_accesos`
--

CREATE TABLE `uar_accesos` (
  `Uid` int(11) NOT NULL,
  `Aid` int(11) NOT NULL,
  `Rid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `uar_accesos`
--

INSERT INTO `uar_accesos` (`Uid`, `Aid`, `Rid`) VALUES
(1, 1, 1),
(1, 2, 1),
(2, 1, 2);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `uar_accesos`
--
ALTER TABLE `uar_accesos`
  ADD PRIMARY KEY (`Uid`,`Aid`,`Rid`);

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `uar_accesos`
--
ALTER TABLE `uar_accesos`
  ADD CONSTRAINT `area_uar` FOREIGN KEY (`Aid`) REFERENCES `area` (`Aid`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `rol_uar` FOREIGN KEY (`Rid`) REFERENCES `roles` (`Rid`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `usuario_uar` FOREIGN KEY (`Uid`) REFERENCES `usuarios` (`Uid`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
