-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- create database tournament;

create table players (
    p_id serial primary key,
    name text,
    score integer default 0
);

create table matches (
    m_id serial primary key,
    round integer default 0,
    player_1 integer references players (p_id),
    player_2 integer references players (p_id)
);

create table results (
    m_id integer references matches,
    p_id integer references players,
    result text
);

/*

tables:
- players: id (PK), name, score.  what else?
- matches: match ID (PK), round, p id1 (FK), p id2 (FK)
- results: match ID (FK),  p id (FK), result (win, lose, draw)

*/