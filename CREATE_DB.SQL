CREATE TABLE if not EXISTS vk_user (
	vk_id int4 PRIMARY KEY,
	vk_city int4 NULL,
	vk_sex int4 NOT NULL,
	vk_age int4 NULL
);

CREATE TABLE pairs (
	id serial4 PRIMARY KEY,
	vk_user_id int8 references vk_user(vk_id),
	vk_pair_id int8 NOT NULL
);

