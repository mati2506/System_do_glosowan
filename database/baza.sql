CREATE TABLE `answers` (
    `answers_id`                    INTEGER NOT NULL PRIMARY KEY,
    `answer_content`                VARCHAR(255) NOT NULL,
    `question_id`                   INTEGER NULL
);

CREATE TABLE `group` (
    `group_id`     INTEGER NOT NULL PRIMARY KEY,
    `name`         VARCHAR(255) NOT NULL
);

CREATE TABLE `password` (
    `password_id`    INTEGER NOT NULL PRIMARY KEY,
    `value`          VARCHAR(512) NOT NULL,
    `user_id`       INTEGER NULL
);


CREATE TABLE `poll` (
    `poll_id`         INTEGER NOT NULL PRIMARY KEY,
    `title`           VARCHAR(80) NOT NULL,
    `type`            VARCHAR(20) NOT NULL,
    `description`     VARCHAR(500) NOT NULL,
    `group_id`        INTEGER NULL,
    `start_datetime`  DATETIME NOT NULL,
    `end_datetime`    DATETIME NOT NULL,
    `creator`		INTEGER NULL
);


CREATE TABLE `question` (
    `question_id`          INTEGER NOT NULL PRIMARY KEY,
    `content`              VARCHAR(255) NOT NULL,
    `poll_id`              INTEGER NULL
);


CREATE TABLE `results` (
    `results_id`                            INTEGER NOT NULL PRIMARY KEY,
    `sum`                            INTEGER NOT NULL DEFAULT 0,
    `answers_id`                            INTEGER NULL,
    `poll_id`                               INTEGER NULL
);

CREATE TABLE `user_group` (
    `user_group_id`    INTEGER NOT NULL PRIMARY KEY,
    `user_id`         INTEGER NULL,
    `group_id`        INTEGER NULL,
    `if_voted`        CHAR(1) NOT NULL
);

CREATE TABLE `user_role` (
    `user_role_id`      INTEGER NOT NULL PRIMARY KEY,
    `role_name`          VARCHAR(10) NOT NULL,
    `user_id`           INTEGER NULL
);

CREATE TABLE `users` (
    `user_id`               INTEGER NOT NULL PRIMARY KEY,
    `name`                  VARCHAR(50) NULL,
    `surname`               VARCHAR(50) NULL,
    `sex`                   VARCHAR(50) NOT NULL,
    `birth_year`           YEAR NOT NULL,
   `username`              VARCHAR(100) NULL,
    `e-mail`              VARCHAR(100) NULL
);

CREATE TABLE `vote` (
    `vote_id`                      INTEGER NOT NULL PRIMARY KEY,
    `results_id`                   INTEGER NULL,
    `user_id`                      INTEGER NULL
);

CREATE TABLE `inactive_user` (
	`user_id`				INTEGER NOT NULL PRIMARY KEY,
	`active_code`			VARCHAR(20) NOT NULL,
	`register_datetime`		DATETIME NOT NULL
);

ALTER TABLE `inactive_user`
	ADD CONSTRAINT inacrive_user_users_fk FOREIGN KEY (user_id)
	REFERENCES `users` (user_id);

ALTER TABLE `answers`
    ADD CONSTRAINT answers_question_fk FOREIGN KEY ( question_id)
        REFERENCES `question` ( question_id);

ALTER TABLE `password`
    ADD CONSTRAINT password_users_fk FOREIGN KEY ( user_id )
        REFERENCES `users` ( user_id );

ALTER TABLE `poll`
    ADD CONSTRAINT poll_group_fk FOREIGN KEY ( group_id )
        REFERENCES `group` ( `group_id` ),
	ADD CONSTRAINT poll_user_fk FOREIGN KEY ( creator )
	   REFERENCES 	`users` ( `user_id` );

ALTER TABLE `question`
    ADD CONSTRAINT question_poll_fk FOREIGN KEY ( poll_id)
        REFERENCES `poll` ( poll_id);

ALTER TABLE `results`
    ADD CONSTRAINT results_answers_fk FOREIGN KEY ( answers_id)
        REFERENCES `answers` ( answers_id);

ALTER TABLE `results`
    ADD CONSTRAINT results_poll_fk FOREIGN KEY ( poll_id)
        REFERENCES `poll` ( poll_id);

ALTER TABLE `user_group`
  ADD CONSTRAINT `user_group_group_fk` FOREIGN KEY (`group_id`) REFERENCES `group` (`group_id`),
  ADD CONSTRAINT `user_group_user_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

ALTER TABLE `user_role`
    ADD CONSTRAINT user_role_users_fk FOREIGN KEY ( user_id )
        REFERENCES `users` ( user_id );

ALTER TABLE `vote`
    ADD CONSTRAINT vote_results_fk FOREIGN KEY ( results_id)
        REFERENCES `results` ( results_id);

ALTER TABLE `vote`
    ADD CONSTRAINT vote_users_fk FOREIGN KEY ( user_id )
        REFERENCES `users` ( user_id );

INSERT INTO users (user_id, name, surname, sex,birth_year,username,`e-mail`)
VALUES (0,'Administrator', 'Systemu', 'default','0000','admin',"voteplus.info@gmail.com");

INSERT INTO password (password_id, value, user_id)
VALUES (0,"c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd472634dfac71cd34ebc35d16ab7fb8a90c81f975113d6c7538dc69dd8de9077ec",0);

INSERT INTO user_role (user_role_id, role_name, user_id)
VALUES (0,"Admin",0);

INSERT INTO `group` (group_id, name)
VALUES (0,'default');

INSERT INTO poll (`poll_id`,`title`,`type`,`description`,`group_id`,`start_datetime`,`end_datetime`,`creator`)
VALUES (0,'default','default','default',NULL,'0','0',NULL);

INSERT INTO question (`question_id`,`content`,`poll_id`)
VALUES (0,'default',NULL);

INSERT INTO answers (`answers_id`,`answer_content`,`question_id`)
VALUES (0,'default',NULL);

INSERT INTO results (`results_id`,`sum`,`answers_id`,`poll_id`)
VALUES (0,0,NULL,NULL);

INSERT INTO vote (`vote_id`,`results_id`,`user_id`)
VALUES (0,NULL,NULL);

INSERT INTO user_group (user_group_id, user_id, group_id, if_voted) VALUES (0,NULL,NULL,'0')