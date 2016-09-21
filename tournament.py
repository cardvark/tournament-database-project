#!/usr/bin/env python

# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import random


def connect(database_name='tournament'):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect('dbname={}'.format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print 'Unable to connect to database.'


def deleteMatches():
    """Remove all the match records from the database."""
    db, c = connect()
    c.execute('DELETE from matches;')
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, c = connect()
    c.execute('DELETE from players;')
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, c = connect()

    query = """SELECT
            count(*)
        from players;
    """

    c.execute(query)
    data = c.fetchone()[0]
    db.close()

    return data


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    db, c = connect()

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

    db, c = connect()

    # Calls custom 'playerstandings' view
    # Located in tournament.sql
    query = 'SELECT * from playerstandings;'

    c.execute(query)
    data = c.fetchall()
    db.close()

    return data


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    db, c = connect()

    inputMatch = 'INSERT into matches (winner, loser) values (%s, %s) RETURNING m_id;'

    c.execute(inputMatch, (winner, loser))
    db.commit()
    db.close()


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

    outputList = []
    tempTup = ()
    randList = []
    db, c = connect()

    # # Query and sort players by # of wins
    # c.execute('SELECT * from players order by score desc')
    playersList = playerStandings()

    while playersList:
        currentScore = playersList[0][2]

        # Builds randList with players of the same score until either:
        # 1. player score no longer matches, or
        # 2. run out of players.
        while playersList[0][2] == currentScore:
            randList.append(playersList.pop(0))
            if not playersList:
                break

        # Shuffles and then continues to pair players until
        # insufficient matches in the randList.
        random.shuffle(randList)
        while len(randList) >= 2:
            player1 = randList.pop()
            player2 = randList.pop()
            tempTup = (player1[0], player1[1], player2[0], player2[1])
            outputList.append(tempTup)
            tempTup = ()

    return outputList
