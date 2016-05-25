#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import random


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute('DELETE from matches;')
    c.execute('DELETE from results;')
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute('DELETE from players;')
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()

    query = """SELECT
            count(*)
        from players;
    """

    c.execute(query)
    data = c.fetchall()

    db.close()

    return data[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """

    db = connect()
    c = db.cursor()

    inputVal = 'INSERT into players (name) values (%s);'

    c.execute(inputVal, (name,))

    db.commit()
    db.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    db = connect()
    c = db.cursor()

    # 

    query = """SELECT
            players.p_id,
            players.name,
            sum(case result when 'win' then 1 else 0 end) as wins,
            count(results.p_id) as matches
        from players
        left join results
            on players.p_id = results.p_id
        group by players.p_id, players.name
        ;
    """

    c.execute(query)
    data = c.fetchall()

    db.close()

    # print data

    return data


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    db = connect()
    c = db.cursor()

    inputMatch = 'INSERT into matches (player_1, player_2) values (%s, %s);'
    matchIdQuery = 'SELECT m_id from matches where player_1 = %s and player_2 = %s'
    inputPlayer = 'INSERT into results (m_id, p_id, result) values (%s, %s, %s)'
    scoreQuery = 'SELECT sum(score) from players where p_id = %s'
    updateScore = 'UPDATE players set score=%s where p_id = %s'

    c.execute(inputMatch, (winner, loser))
    matchId = c.execute(matchIdQuery, (winner, loser))
    c.execute(inputPlayer, (matchId, winner, 'win'))
    c.execute(inputPlayer, (matchId, loser, 'loss'))
    
    c.execute(scoreQuery, (winner,))
    winnerScore = c.fetchall()
    # print winnerScore
    # loserScore = c.execute(scoreQuery, (loser,))
    winnerUpdate = c.execute(updateScore, (winnerScore[0][0] + 1, winner))
    # loserUpdate = c.execute(updateScore, (loserScore + 0, loser))

    db.commit()
    db.close()

def hasMatched(p1, p2):
    """
    Checks if two players have previously been in a match before.

    Returns True or False.

    """

    db = connect()
    c = db.cursor()

    query = """SELECT
            count(*)
        from matches
        where player_1 != player_2
        and player_1 in (p1, p2)
        and player_2 in (p1, p2);
    """

    c.execute(query)

    matchCheck = c.fetchall()

    if matchCheck[0][0] == 0:
        return False
    else:
        return True


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    db = connect()
    c = db.cursor()

    c.execute('SELECT * from players order by score desc')

    playerStatus = c.fetchall()

    outputList = []
    tempTup = ()

    randList = []

    while playerStatus:
        if not randList:
            randList.append(playerStatus.pop(0))
        
        if playerStatus[0][2] == randList[0][2]:
            randList.append(playerStatus.pop(0))
        elif len(randList) == 1:
            randList.append(playerStatus.pop(0))
            tempTup = (randList[0][0], randList[0][1], randList[1][0], randList[1][1])
            outputList.append(tempTup)
            randList = []
            tempTup = ()
        
        while len(randList) >= 2:
            # print 'printing randList', randList
            random.shuffle(randList)
            # print randList
            player1 = randList.pop()
            player2 = randList.pop()
            # print player1, player2
            tempTup = (player1[0], player1[1], player2[0], player2[1])
            # print tempTup
            outputList.append(tempTup)
            # print outputList
            tempTup = ()

    # print outputList
    return outputList

    # Query standings - list of tuples of info for each player.
    # Sort players by wins
    # rand pairing by groups of wins
    # if leftover, shift back into list.
    # if no equals, just pair next two.
    # 
