DROP TABLE IF EXISTS `recipe`;
DROP TABLE IF EXISTS `user`;

CREATE TABLE `user`
(
    `id`       INT          NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(255) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `admin`    BOOL         NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE (`username`)
);

CREATE TABLE `recipe`
(
    `id`          INT          NOT NULL AUTO_INCREMENT,
    `category`    VARCHAR(255) NOT NULL,
    `name`        VARCHAR(255) NOT NULL,
    `description` TEXT         NOT NULL,
    `difficulty`  INT          NOT NULL,
    PRIMARY KEY (`id`)
);

INSERT INTO `user`(`username`, `password`, `admin`)
VALUES ('admin', %(password) s, TRUE);