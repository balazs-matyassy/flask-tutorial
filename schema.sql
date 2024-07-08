CREATE TABLE `recipe`
(
    `id`         INT          NOT NULL AUTO_INCREMENT,
    `category`   VARCHAR(255) NOT NULL,
    `name`       VARCHAR(255) NOT NULL,
    `difficulty` INT          NOT NULL,
    PRIMARY KEY (`id`)
);