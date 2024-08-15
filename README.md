

Status codes:

Success
205 - Register was success. /api/reg/ 
206 - Auth wass success. /api/auth/
207 - Quit from account. /api/out
208 - User was found. /api/user/ /api/me/
209 - Password changed success! /api/change_password/
210 - Email changed success! /api/change_email/
211 - Name changed success! /api/change_name/

212 - Success add item in storage! /api/add_item/{item_id}
213 - Delete items success. /api/buy_item/{item_id}
214 - Item {item} bought success! /api/buy_item/{item_id}


Client errors:
440 - Name already taken. 
441 - In username must be only letters and numbers! 
442 - Invalid name or password!
443 - You dont auth. 
444 - User was not found! /api/user/
445 - Invalid password!
446 - Invalid item! +
447 - Invalid quantity! /api/add_item/{item_id} +
448 - Item was not found in your storage! /api/buy_item/{item_id}
449 - Not enough money! /api/buy_item/{item_id}
450 - The store has less quantity. /api/buy_item/{item_id}


Global errors:
401 - Invalid refresh token. Need user auth
402 - Scope for token Invalid. (Token not valid)
