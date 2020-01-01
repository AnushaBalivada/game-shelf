# game-shelf
A simple Python program, to play with shelve and Docker.

Uses [shelve](https://docs.python.org/3/library/shelve.html) for object persistence.

## List all games
**Definition**
<pre>`GET /games`</pre>

**Response**
- `200 OK` on success.
```json
[
    {
        "title": "Assassin's Creed IV Black Flag",
        "completed": false,
        "loaned_to": ""
    },
    {
        "title": "inFAMOUS Second Son",
        "completed": true,
        "loaned_to": "Uryū Ishida"
    }
]
```

## List games which have been loaned to others
**Definition**
<pre>`GET /games?loaned=true`</pre>

**Response**
- `200 OK` on success.
```json
[
    {
        "title": "inFAMOUS Second Son",
        "completed": true,
        "loaned_to": "Uryū Ishida"
    }
]
```

## Add new game
**Definition**
<pre>`POST /games`</pre>

**Arguments**
- `"title":string` the title of the game.
- `"completed":boolean` whether you've completed the game.
- `"loaned_to":string` name of the person the game has been loaned to.

**Response**
- `201 Created` on success.
```json
{
    "title": "Assassin's Creed Black Flag",
    "completed": false,
    "loaned_to": ""
}
```

## Get the details of a game
**Definition**
<pre>`GET /game/:title_of_the_game`</pre>

**Response**
- `404 Not Found` if the game does not exist.
- `200 OK` on success.
```json
{
    "title": "Assassin's Creed Black Flag",
    "completed": false,
    "loaned_to": ""
}
```

## Delete a game
###### (Umm...why do you want to remove a game from your library?)
**Definition**
`DELETE /game/:title_of_the_game`

 **Response**
 - `404 Not Found` if the game does not exist.
 - `201 No Content` on success.
