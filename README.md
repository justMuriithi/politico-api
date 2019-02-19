# politico_api
[![Build Status](https://travis-ci.com/justMuriithi/politico_api.svg?branch=develop)](https://travis-ci.com/justMuriithi/politico_api)           [![Coverage Status](https://coveralls.io/repos/github/justMuriithi/politico_api/badge.svg?branch=develop)](https://coveralls.io/github/justMuriithi/politico_api?branch=develop)        [![Codacy Badge](https://api.codacy.com/project/badge/Grade/f343a0ac1ecd4e9cbba45e2b98631a9d)](https://www.codacy.com/app/justMuriithi/politico_api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=justMuriithi/politico_api&amp;utm_campaign=Badge_Grade)

Politico enables citizens give their mandate to politicians running for different government offices while building trust in the process through transparency.

## API Endpoints
|`/api/v2/auth/signup` | `POST`| `Register a new user` |

|`/api/v2/auth/login` | `POST`| `Login a registered user` |

| `/api/v2/parties` | `POST` | `Create a political party ` | 

| `/api/v2/parties` | `GET` | `Fetch all political parties ` |

| `/api/v2/parties/<int:id>` | `GET` | `Fetch a specific political party` |

| `/api/v2/parties/<int:id>` | `DELETE` | `Delete a specific political party` |

|`/api/v2/parties/<int:id>/name` | `PATCH` | `Edit a political party` |

|`/api/v2/offices` | `POST`| `Create Political office` |

|`/api/v2/offices` | `GET` | `Fetch all political offices` |

|`/api/v2/offices/register` | `POST`| `Vie for office` |

|`/api/v2/candidates` | `GET` | `Fetch all candidates` |

|`/api/v2/candidates/<int:id>` | `GET` | `Fetch a specific candidate` |

|`/api/v2/votes` | `POST`| `Vote` |

|`/api/v2/votes` | `GET`| `Fetch all Votes` |

|`/api/v2/votes/candidate/<int:id>` | `GET`| `Get all votes for a specific candidate` |


## Requirements
- [Python 3](https://www.python.org/)
- [Postman](https://www.getpostman.com/downloads/)
- Code editor of choice preferrably VSCode or Sublime

#### Installation steps
- Clone the git repo
```
$ https://github.com/justMuriithi/politico_api.git
```
- Cd into project folder
```
$ cd politico_api
```
- Create the virtual environment
```
$ virtualenv venv
```
- Activate it
```
$ source venv/bin/activate
```
- Install dependencies
```
$ pip3 install -r requirements.txt
```
- Run the app
``` 
$ flask run 
```
