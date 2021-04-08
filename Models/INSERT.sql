CONFIGURACIONES
INSERT INTO `configuraciones` (`Cid`, `Ccategoria`, `Corden`, `Cdescripcion`, `Cvalor1`) VALUES
(1, 'Estado', 1, 'Habilitado', 1),
(2, 'Estado', 2, 'Deshabilitado', 1);

ROLES
INSERT INTO `roles` (`Rid`, `Rdescripcion`, `Restado`) VALUES
(1, 'Administrador', 1),
(2, 'Trabajador', 1),
(3, 'Profesor', 1);

AREAS
INSERT INTO `area` (`Aid`, `Adescripcion`, `Aestado`) VALUES
(1, 'Mantenimiento', 1),
(2, 'Seguridad', 1);


USUARIOS
INSERT INTO `usuarios` (`Uid`, `Unombre`, `Uapellido`, `Ucorreo`, `Upassword`, `Ufecha_modificacion`, `Ufecha_creacion`, `Uestado`, `Eid`) VALUES
(1, 'Luis Adrian', 'Morales Zavala', 'lm98adrian@gmail.com', '12345678', '0000-00-00 00:00:00', now(), 1, 1)

UAR_accesos
INSERT INTO `uar_accesos` (`Uid`, `Aid`, `Rid`) VALUES
(1, 1, 1)


drop table  mt_funcion_resp;
drop table  mt_asig_funciones;
drop table  mt_asig_et_fn;
drop table  mt_eti_fn;
drop table  mt_funciones;
drop table  mt_etiquetas;
drop table  mt_ambientes;
drop table  `sg_areas`;