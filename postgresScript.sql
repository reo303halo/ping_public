
CREATE TABLE public.ping_users (
  user_id serial PRIMARY KEY,
  e_mail varchar(45) UNIQUE NOT NULL,
  password varchar(128) NOT NULL,
  firstname varchar(45) NOT NULL,
  lastname varchar(45) NOT NULL,
  role int NOT NULL DEFAULT 0,
  uuid varchar(45) UNIQUE NOT NULL,
  verified int NOT NULL DEFAULT 0,
  active int NOT NULL DEFAULT 0
);

/*
INSERT INTO ping_users (user_id, e_mail, password, firstname, lastname, role, uuid, verified, active)
VALUES
( add user here )
*/

CREATE TABLE public.ping_quiz (
	quiz_id INT PRIMARY KEY,
	user_id INT DEFAULT NULL
);


INSERT INTO ping_quiz (quiz_id, user_id) VALUES
(1111, 1);


ALTER TABLE ping_quiz
  ADD CONSTRAINT quiz_id UNIQUE (quiz_id);

  
ALTER TABLE ping_quiz
  ADD CONSTRAINT owner FOREIGN KEY (user_id) REFERENCES ping_users (user_id) ON DELETE SET NULL ON UPDATE NO ACTION;




CREATE TABLE public.ping_subjects (
  subject_id serial PRIMARY KEY,
  parent_id int DEFAULT NULL,
  subject_name varchar(45) NOT NULL DEFAULT 'Nytt emne'
);


INSERT INTO ping_subjects (subject_id, parent_id, subject_name) VALUES
(0, NULL, 'Default'),
(4, 0, 'IT'),
(5, 0, 'Matte'),
(6, 0, 'Engelsk'),
(7, 4, 'OS'),
(8, 4, 'Web'),
(9, 4, 'Datasikkerhet'),
(10, 4, 'Database'),
(11, 4, 'Programmering'),
(12, 4, 'Sockets'),
(13, 4, 'Programmering 2'),
(14, 4, 'Mobilprogrammering'),
(15, 4, 'Artifical Intelligence');


ALTER TABLE ping_subjects
  ADD CONSTRAINT subject_id_UNIQUE UNIQUE  (subject_id);
  
  
ALTER TABLE ping_subjects
  ADD CONSTRAINT FK_parent FOREIGN KEY (parent_id) REFERENCES ping_subjects (subject_id) ON DELETE CASCADE ON UPDATE NO ACTION;




CREATE TABLE public.ping_questions (
  question_id serial PRIMARY KEY,
  questions varchar(45) NOT NULL,
  subject int NOT NULL,
  options varchar(128) DEFAULT NULL,
  correctAnswer varchar(128) DEFAULT NULL,
  author_id int DEFAULT NULL
);


INSERT INTO ping_questions (question_id, questions, subject, options, correctAnswer, author_id) VALUES
(1, 'Hvilket programmeringsspråk brukes til iOS?', 14, 'Swift,Kotlin,Java,Python', 'Swift', NULL),
(2, 'Hvilken type OS har du på din mobiltelefon?', 14, NULL, NULL, NULL);


ALTER TABLE ping_questions
  ADD CONSTRAINT question_id_UNIQUE UNIQUE (question_id);


ALTER TABLE ping_questions
  ADD CONSTRAINT FK_subject FOREIGN KEY (subject) REFERENCES ping_subjects (subject_id) ON DELETE CASCADE ON UPDATE NO ACTION,
  ADD CONSTRAINT author FOREIGN KEY (author_id) REFERENCES ping_users (user_id) ON DELETE SET NULL ON UPDATE NO ACTION;




CREATE TABLE public.ping_qq_relations (
  answer_id serial PRIMARY KEY,
  quiz_id int DEFAULT NULL,
  question_id int DEFAULT NULL,
  current int NOT NULL DEFAULT 0
);


INSERT INTO ping_qq_relations (answer_id, quiz_id, question_id, current) VALUES
(1, 1111, 1, 1);


ALTER TABLE ping_qq_relations
  ADD CONSTRAINT FK_question_id FOREIGN KEY (question_id) REFERENCES ping_questions (question_id) ON DELETE CASCADE ON UPDATE NO ACTION,
  ADD CONSTRAINT FK_quiz_id FOREIGN KEY (quiz_id) REFERENCES ping_quiz (quiz_id) ON DELETE CASCADE ON UPDATE NO ACTION;




CREATE TABLE public.ping_answers (
  answers_id int DEFAULT NULL,
  answer text NOT NULL
);


INSERT INTO ping_answers (answers_id, answer) VALUES
(1, 'Swift');


ALTER TABLE ping_answers
  ADD CONSTRAINT FK_answer_id FOREIGN KEY (answers_id) REFERENCES ping_qq_relations (answer_id) ON DELETE CASCADE ON UPDATE NO ACTION;
COMMIT;

