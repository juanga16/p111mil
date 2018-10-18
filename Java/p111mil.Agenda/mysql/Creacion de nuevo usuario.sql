-- usuario seria el nombre del usuario
-- % significa que puede acceder desde cualquier maquina
-- p111mil seria la contraseña
CREATE USER 'usuario'@'%' IDENTIFIED BY 'p111mil';

-- Significa que solamente puede leer, escirbir y borrar
GRANT SELECT, INSERT, DELETE, UPDATE ON agenda.* TO 'usuario'@'%';

FLUSH PRIVILEGES;
