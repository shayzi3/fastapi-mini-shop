

Status codes:

Success
205 - Register was success. /api/v1/reg/ 
206 - Auth wass success. /api/v1/auth/
207 - Quit from account. /api/v1/out
208 - User was found. /api/v1/user/ /api/v1/me/
209 - Password changed success! /api/v1/change_password/
210 - Email changed success! /api/v1/change_email/
211 - Name changed success! /api/v1/change_name/

212 - Success add item in storage! /api/v1/add_item/{item_id}
213 - Delete items success. /api/v1/buy_item/{item_id}
214 - Item {item} bought success! /api/v1/buy_item/{item_id}

215 - Account deleted success!  /api/v1/delete_account/


Client errors:
440 - Name already taken. 
441 - In username must be only letters and numbers! 
442 - Invalid name or password!
443 - You dont auth. 
444 - User was not found! /api/v1/user/
445 - Invalid password!
446 - Invalid item! +
447 - Invalid quantity! /api/v1/add_item/{item_id} +
448 - Item was not found in your storage! /api/v1/buy_item/{item_id}
449 - Not enough money! /api/v1/buy_item/{item_id}
450 - The store has less quantity. /api/v1/buy_item/{item_id}
451 - Item was finished... /buy_item/


Global errors:
401 - Invalid refresh token. Need user auth
402 - Scope for token Invalid. (Token not valid)
