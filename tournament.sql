-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- create database tournament;

drop database if exists tournament;
create database tournament;
\c tournament;

create table players (
    p_id serial primary key,
    name text
);

create table matches (
    m_id serial primary key,
    winner integer references players (p_id),
    loser integer references players (p_id)
);

create view playerwins as
    select
        players.p_id,
        count(matches.winner) as wins
    from players
    left join matches
        on players.p_id = matches.winner
    group by players.p_id
;

create view playerlosses as
    select
        players.p_id,
        count(matches.loser) as losses
    from players
    left join matches
        on players.p_id = matches.loser
    group by players.p_id
;

-- Combines playerwins and playerlosses queries to generate wins + matches data
create view playerstandings as
    select
        players.p_id,
        players.name,
        playerwins.wins,
        playerwins.wins + playerlosses.losses as matches
    from players
    left join playerwins
         on players.p_id = playerwins.p_id
    left join playerlosses
        on players.p_id = playerlosses.p_id
    order by playerwins.wins desc
;
