CREATE TABLE auth_user (
  id INTEGER PRIMARY KEY,
  username VARCHAR(150) NOT NULL UNIQUE,
  email VARCHAR(254) NOT NULL,
  password VARCHAR(128) NOT NULL
);

CREATE TABLE portal_profile (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL UNIQUE,
  full_name VARCHAR(150) NOT NULL,
  birth_date DATE NOT NULL,
  phone VARCHAR(30) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES auth_user(id)
);

CREATE TABLE portal_application (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,
  transport VARCHAR(40) NOT NULL CHECK (transport IN ('Катер', 'Круизный лайнер', 'Яхта')),
  start_date DATE NOT NULL,
  payment_method VARCHAR(60) NOT NULL,
  comment TEXT NOT NULL,
  status VARCHAR(40) NOT NULL DEFAULT 'Новая'
    CHECK (status IN ('Новая', 'Идет обучение', 'Обучение завершено')),
  created_at DATE NOT NULL,
  FOREIGN KEY (user_id) REFERENCES auth_user(id)
);

CREATE TABLE portal_review (
  id INTEGER PRIMARY KEY,
  application_id INTEGER NOT NULL UNIQUE,
  user_id INTEGER NOT NULL,
  text TEXT NOT NULL,
  created_at DATE NOT NULL,
  FOREIGN KEY (application_id) REFERENCES portal_application(id),
  FOREIGN KEY (user_id) REFERENCES auth_user(id)
);
