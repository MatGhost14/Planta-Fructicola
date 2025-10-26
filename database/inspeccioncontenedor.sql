-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 26-10-2025 a las 21:42:31
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `inspeccioncontenedor`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('001');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `bitacora_auditoria`
--

CREATE TABLE `bitacora_auditoria` (
  `id_evento` bigint(20) UNSIGNED NOT NULL,
  `id_usuario` bigint(20) UNSIGNED DEFAULT NULL,
  `accion` varchar(120) NOT NULL,
  `detalles` text DEFAULT NULL,
  `creado_en` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `bitacora_auditoria`
--

INSERT INTO `bitacora_auditoria` (`id_evento`, `id_usuario`, `accion`, `detalles`, `creado_en`) VALUES
(1, 2, 'LOGOUT', 'Logout desde aplicación web', '2025-10-21 11:05:37'),
(2, 1, 'LOGIN', 'Login exitoso desde 127.0.0.1', '2025-10-26 14:32:48'),
(3, 1, 'LOGIN', 'Login exitoso desde 127.0.0.1', '2025-10-26 14:36:14'),
(4, 1, 'LOGIN', 'Login exitoso desde 127.0.0.1', '2025-10-26 14:39:06'),
(5, 1, 'LOGIN', 'Login exitoso desde 127.0.0.1', '2025-10-26 14:40:38'),
(6, 1, 'LOGIN', 'Login exitoso desde 127.0.0.1', '2025-10-26 14:41:04'),
(7, 1, 'LOGIN', 'Login exitoso desde 127.0.0.1', '2025-10-26 15:02:31'),
(8, 3, 'LOGIN', 'Login exitoso desde 127.0.0.1', '2025-10-26 15:12:49'),
(9, 3, 'LOGIN', 'Login exitoso desde 127.0.0.1', '2025-10-26 15:13:54'),
(10, 3, 'LOGIN', 'Login exitoso desde 127.0.0.1', '2025-10-26 15:14:56'),
(11, 1, 'LOGOUT', 'Logout desde aplicación web', '2025-10-26 15:25:33'),
(12, 1, 'LOGIN', 'Login exitoso desde 127.0.0.1', '2025-10-26 15:25:42'),
(13, 1, 'LOGOUT', 'Logout desde aplicación web', '2025-10-26 15:25:59'),
(14, 1, 'LOGIN', 'Login exitoso desde 127.0.0.1', '2025-10-26 15:26:07'),
(15, 3, 'LOGIN', 'Login exitoso desde 127.0.0.1', '2025-10-26 15:37:49'),
(16, 3, 'LOGIN', 'Login exitoso desde 127.0.0.1', '2025-10-26 15:44:50'),
(17, 3, 'LOGIN', 'Login exitoso desde 127.0.0.1', '2025-10-26 15:45:04'),
(18, 1, 'LOGIN', 'Login exitoso desde 127.0.0.1', '2025-10-26 15:50:14'),
(19, 1, 'LOGIN', 'Login exitoso desde 127.0.0.1', '2025-10-26 16:56:59'),
(20, 1, 'Inspección creada', 'Contenedor: HAHR756 (INS_1761508699738)', '2025-10-26 16:58:19'),
(21, 1, 'LOGOUT', 'Logout desde aplicación web', '2025-10-26 17:02:29'),
(22, 1, 'LOGOUT', 'Logout desde aplicación web', '2025-10-26 17:06:46'),
(23, 1, 'LOGIN', 'Login exitoso desde 127.0.0.1', '2025-10-26 17:22:15'),
(24, 1, 'Inspección creada', 'Contenedor: HAHR756 (INS_1761510206650)', '2025-10-26 17:23:26'),
(25, 2, 'LOGIN', 'Login exitoso desde 127.0.0.1', '2025-10-26 17:24:41'),
(26, 2, 'LOGIN', 'Login exitoso desde 127.0.0.1', '2025-10-26 17:37:19'),
(27, 2, 'LOGOUT', 'Logout desde aplicación web', '2025-10-26 17:41:26'),
(28, 1, 'LOGIN', 'Login exitoso desde 127.0.0.1', '2025-10-26 17:41:33'),
(29, 1, 'LOGOUT', 'Logout desde aplicación web', '2025-10-26 17:41:39'),
(30, 2, 'LOGIN', 'Login exitoso desde 127.0.0.1', '2025-10-26 17:41:44');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `fotos_inspeccion`
--

CREATE TABLE `fotos_inspeccion` (
  `id_foto` bigint(20) UNSIGNED NOT NULL,
  `id_inspeccion` bigint(20) UNSIGNED NOT NULL,
  `foto_path` varchar(255) NOT NULL,
  `mime_type` varchar(50) NOT NULL DEFAULT 'image/jpeg',
  `hash_hex` varchar(64) DEFAULT NULL,
  `orden` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `tomada_en` datetime DEFAULT NULL,
  `creado_en` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `fotos_inspeccion`
--

INSERT INTO `fotos_inspeccion` (`id_foto`, `id_inspeccion`, `foto_path`, `mime_type`, `hash_hex`, `orden`, `tomada_en`, `creado_en`) VALUES
(2, 2, '/capturas/inspecciones/26-10-2025/2/20251026_172326_722641.jpg', 'image/jpeg', '20e81549ed22c3c97509e88e13fff18886a7aa3f0f7eabbebf87e9076632066e', 0, '2025-10-26 17:23:26', '2025-10-26 17:23:26');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inspecciones`
--

CREATE TABLE `inspecciones` (
  `id_inspeccion` bigint(20) UNSIGNED NOT NULL,
  `codigo` varchar(40) NOT NULL,
  `numero_contenedor` varchar(30) NOT NULL,
  `id_planta` bigint(20) UNSIGNED NOT NULL,
  `id_navieras` bigint(20) UNSIGNED NOT NULL,
  `temperatura_c` decimal(5,2) DEFAULT NULL,
  `observaciones` text DEFAULT NULL,
  `firma_path` varchar(255) DEFAULT NULL,
  `id_inspector` bigint(20) UNSIGNED NOT NULL,
  `estado` enum('pending','approved','rejected') NOT NULL DEFAULT 'pending',
  `inspeccionado_en` datetime NOT NULL DEFAULT current_timestamp(),
  `creado_en` datetime NOT NULL DEFAULT current_timestamp(),
  `actualizado_en` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `inspecciones`
--

INSERT INTO `inspecciones` (`id_inspeccion`, `codigo`, `numero_contenedor`, `id_planta`, `id_navieras`, `temperatura_c`, `observaciones`, `firma_path`, `id_inspector`, `estado`, `inspeccionado_en`, `creado_en`, `actualizado_en`) VALUES
(2, 'INS_1761510206650', 'HAHR756', 3, 3, 18.00, 'de prueba', '/capturas/firmas/2_1761510206.png', 1, 'pending', '2025-10-26 17:23:26', '2025-10-26 17:23:26', '2025-10-26 17:23:26');

--
-- Disparadores `inspecciones`
--
DELIMITER $$
CREATE TRIGGER `trg_inspecciones_ai` AFTER INSERT ON `inspecciones` FOR EACH ROW BEGIN
  INSERT INTO bitacora_auditoria (`id_usuario`,`accion`,`detalles`)
  VALUES (NEW.id_inspector, 'Inspección creada',
          CONCAT('Contenedor: ', NEW.numero_contenedor, ' (', NEW.codigo, ')'));
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trg_inspecciones_au_estado` AFTER UPDATE ON `inspecciones` FOR EACH ROW BEGIN
  IF (OLD.estado <> NEW.estado) THEN
    INSERT INTO bitacora_auditoria (`id_usuario`,`accion`,`detalles`)
    VALUES (NEW.id_inspector, 'Estado actualizado',
            CONCAT('Contenedor: ', NEW.numero_contenedor, ' -> ', NEW.estado));
  END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `navieras`
--

CREATE TABLE `navieras` (
  `id_navieras` bigint(20) UNSIGNED NOT NULL,
  `codigo` varchar(50) NOT NULL,
  `nombre` varchar(120) NOT NULL,
  `creado_en` datetime NOT NULL DEFAULT current_timestamp(),
  `actualizado_en` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `navieras`
--

INSERT INTO `navieras` (`id_navieras`, `codigo`, `nombre`, `creado_en`, `actualizado_en`) VALUES
(1, 'maersk', 'Maersk Line', '2025-10-14 00:44:46', '2025-10-14 00:44:46'),
(2, 'msc', 'MSC', '2025-10-14 00:44:46', '2025-10-14 00:44:46'),
(3, 'cosco', 'COSCO', '2025-10-14 00:44:46', '2025-10-14 00:44:46'),
(4, 'hapag', 'Hapag-Lloyd', '2025-10-14 00:44:46', '2025-10-14 00:44:46'),
(5, 'MAEU', 'Maersk', '2025-10-14 01:34:54', '2025-10-14 01:34:54');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `plantas`
--

CREATE TABLE `plantas` (
  `id_planta` bigint(20) UNSIGNED NOT NULL,
  `codigo` varchar(50) NOT NULL,
  `nombre` varchar(120) NOT NULL,
  `ubicacion` varchar(191) DEFAULT NULL,
  `creado_en` datetime NOT NULL DEFAULT current_timestamp(),
  `actualizado_en` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `plantas`
--

INSERT INTO `plantas` (`id_planta`, `codigo`, `nombre`, `ubicacion`, `creado_en`, `actualizado_en`) VALUES
(1, 'norte', 'Planta Norte', 'Sector Norte', '2025-10-14 00:44:45', '2025-10-14 00:44:45'),
(2, 'sur', 'Planta Sur', 'Sector Sur', '2025-10-14 00:44:45', '2025-10-14 00:44:45'),
(3, 'este', 'Planta Este', 'Sector Este', '2025-10-14 00:44:45', '2025-10-14 00:44:45'),
(4, 'oeste', 'Planta Oeste', 'Sector Oeste', '2025-10-14 00:44:45', '2025-10-14 00:44:45');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `preferencias_usuario`
--

CREATE TABLE `preferencias_usuario` (
  `id_usuario` bigint(20) UNSIGNED NOT NULL,
  `auto_sync` tinyint(1) NOT NULL DEFAULT 1,
  `notificaciones` tinyint(1) NOT NULL DEFAULT 1,
  `geolocalizacion` tinyint(1) NOT NULL DEFAULT 0,
  `actualizado_en` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `preferencias_usuario`
--

INSERT INTO `preferencias_usuario` (`id_usuario`, `auto_sync`, `notificaciones`, `geolocalizacion`, `actualizado_en`) VALUES
(1, 1, 1, 0, '2025-10-14 00:44:46'),
(2, 1, 1, 0, '2025-10-14 00:44:46'),
(3, 1, 1, 0, '2025-10-14 00:44:46');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tokens_api`
--

CREATE TABLE `tokens_api` (
  `id_token` bigint(20) UNSIGNED NOT NULL,
  `id_usuario` bigint(20) UNSIGNED NOT NULL,
  `token_hash` varchar(255) NOT NULL,
  `expira_en` datetime DEFAULT NULL,
  `creado_en` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` bigint(20) UNSIGNED NOT NULL,
  `nombre` varchar(120) NOT NULL,
  `correo` varchar(191) NOT NULL,
  `password_hash` varchar(255) DEFAULT NULL,
  `rol` enum('inspector','supervisor','admin') NOT NULL DEFAULT 'inspector',
  `estado` enum('active','inactive') NOT NULL DEFAULT 'active',
  `ultimo_acceso` datetime DEFAULT NULL,
  `creado_en` datetime NOT NULL DEFAULT current_timestamp(),
  `actualizado_en` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre`, `correo`, `password_hash`, `rol`, `estado`, `ultimo_acceso`, `creado_en`, `actualizado_en`) VALUES
(1, 'Juan Díaz', 'juan.diaz@empresa.com', '$2b$12$1rgcK27AcvHI0J78Zrla5ur1F.nGH0AhwN0RfsKE/kHldnynysncC', 'inspector', 'active', '2025-10-26 17:41:39', '2025-10-14 00:44:46', '2025-10-26 17:41:39'),
(2, 'María López', 'maria.lopez@empresa.com', '$2b$12$1rgcK27AcvHI0J78Zrla5ur1F.nGH0AhwN0RfsKE/kHldnynysncC', 'supervisor', 'active', '2025-10-26 17:41:55', '2025-10-14 00:44:46', '2025-10-26 17:41:55'),
(3, 'Carlos Ruiz', 'carlos.ruiz@empresa.com', '$2b$12$1rgcK27AcvHI0J78Zrla5ur1F.nGH0AhwN0RfsKE/kHldnynysncC', 'admin', 'active', '2025-10-26 15:45:13', '2025-10-14 00:44:46', '2025-10-26 15:45:13');

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `vw_conteo_por_estado`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `vw_conteo_por_estado` (
`estado` enum('pending','approved','rejected')
,`total` bigint(21)
);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `vw_resumen_inspecciones`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `vw_resumen_inspecciones` (
`id_inspeccion` bigint(20) unsigned
,`codigo` varchar(40)
,`numero_contenedor` varchar(30)
,`planta` varchar(120)
,`naviera` varchar(120)
,`temperatura_c` decimal(5,2)
,`inspector` varchar(120)
,`estado` enum('pending','approved','rejected')
,`inspeccionado_en` datetime
,`creado_en` datetime
);

-- --------------------------------------------------------

--
-- Estructura para la vista `vw_conteo_por_estado`
--
DROP TABLE IF EXISTS `vw_conteo_por_estado`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_conteo_por_estado`  AS SELECT `i`.`estado` AS `estado`, count(0) AS `total` FROM `inspecciones` AS `i` GROUP BY `i`.`estado` ;

-- --------------------------------------------------------

--
-- Estructura para la vista `vw_resumen_inspecciones`
--
DROP TABLE IF EXISTS `vw_resumen_inspecciones`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_resumen_inspecciones`  AS SELECT `i`.`id_inspeccion` AS `id_inspeccion`, `i`.`codigo` AS `codigo`, `i`.`numero_contenedor` AS `numero_contenedor`, `p`.`nombre` AS `planta`, `n`.`nombre` AS `naviera`, `i`.`temperatura_c` AS `temperatura_c`, `u`.`nombre` AS `inspector`, `i`.`estado` AS `estado`, `i`.`inspeccionado_en` AS `inspeccionado_en`, `i`.`creado_en` AS `creado_en` FROM (((`inspecciones` `i` join `plantas` `p` on(`p`.`id_planta` = `i`.`id_planta`)) join `navieras` `n` on(`n`.`id_navieras` = `i`.`id_navieras`)) join `usuarios` `u` on(`u`.`id_usuario` = `i`.`id_inspector`)) ;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indices de la tabla `bitacora_auditoria`
--
ALTER TABLE `bitacora_auditoria`
  ADD PRIMARY KEY (`id_evento`),
  ADD KEY `ix_bitacora_usuario_fecha` (`id_usuario`,`creado_en`);

--
-- Indices de la tabla `fotos_inspeccion`
--
ALTER TABLE `fotos_inspeccion`
  ADD PRIMARY KEY (`id_foto`),
  ADD KEY `ix_fotos_inspeccion` (`id_inspeccion`);

--
-- Indices de la tabla `inspecciones`
--
ALTER TABLE `inspecciones`
  ADD PRIMARY KEY (`id_inspeccion`),
  ADD UNIQUE KEY `ux_inspecciones_codigo` (`codigo`),
  ADD KEY `ix_inspecciones_numero` (`numero_contenedor`),
  ADD KEY `ix_inspecciones_estado` (`estado`),
  ADD KEY `ix_inspecciones_fecha` (`inspeccionado_en`),
  ADD KEY `fk_inspecciones_navieras` (`id_navieras`),
  ADD KEY `fk_inspecciones_usuario` (`id_inspector`),
  ADD KEY `ix_inspecciones_planta_estado_fecha` (`id_planta`,`estado`,`inspeccionado_en`);

--
-- Indices de la tabla `navieras`
--
ALTER TABLE `navieras`
  ADD PRIMARY KEY (`id_navieras`),
  ADD UNIQUE KEY `ux_navieras_codigo` (`codigo`),
  ADD UNIQUE KEY `ux_navieras_nombre` (`nombre`);

--
-- Indices de la tabla `plantas`
--
ALTER TABLE `plantas`
  ADD PRIMARY KEY (`id_planta`),
  ADD UNIQUE KEY `ux_plantas_codigo` (`codigo`),
  ADD KEY `ix_plantas_nombre` (`nombre`);

--
-- Indices de la tabla `preferencias_usuario`
--
ALTER TABLE `preferencias_usuario`
  ADD PRIMARY KEY (`id_usuario`);

--
-- Indices de la tabla `tokens_api`
--
ALTER TABLE `tokens_api`
  ADD PRIMARY KEY (`id_token`),
  ADD UNIQUE KEY `ux_token_hash` (`token_hash`),
  ADD KEY `ix_tokens_usuario` (`id_usuario`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `ux_usuarios_correo` (`correo`),
  ADD KEY `ix_usuarios_rol` (`rol`),
  ADD KEY `ix_usuarios_estado` (`estado`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `bitacora_auditoria`
--
ALTER TABLE `bitacora_auditoria`
  MODIFY `id_evento` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT de la tabla `fotos_inspeccion`
--
ALTER TABLE `fotos_inspeccion`
  MODIFY `id_foto` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `inspecciones`
--
ALTER TABLE `inspecciones`
  MODIFY `id_inspeccion` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `navieras`
--
ALTER TABLE `navieras`
  MODIFY `id_navieras` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `plantas`
--
ALTER TABLE `plantas`
  MODIFY `id_planta` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `tokens_api`
--
ALTER TABLE `tokens_api`
  MODIFY `id_token` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `bitacora_auditoria`
--
ALTER TABLE `bitacora_auditoria`
  ADD CONSTRAINT `fk_bitacora_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Filtros para la tabla `fotos_inspeccion`
--
ALTER TABLE `fotos_inspeccion`
  ADD CONSTRAINT `fk_fotos_inspeccion` FOREIGN KEY (`id_inspeccion`) REFERENCES `inspecciones` (`id_inspeccion`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `inspecciones`
--
ALTER TABLE `inspecciones`
  ADD CONSTRAINT `fk_inspecciones_navieras` FOREIGN KEY (`id_navieras`) REFERENCES `navieras` (`id_navieras`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_inspecciones_planta` FOREIGN KEY (`id_planta`) REFERENCES `plantas` (`id_planta`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_inspecciones_usuario` FOREIGN KEY (`id_inspector`) REFERENCES `usuarios` (`id_usuario`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `preferencias_usuario`
--
ALTER TABLE `preferencias_usuario`
  ADD CONSTRAINT `fk_pref_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `tokens_api`
--
ALTER TABLE `tokens_api`
  ADD CONSTRAINT `fk_tokens_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
