# First run
Install required packages using `pip install -r requirements.txt` <br>
Create database using `python3 manage.py migrate` <br>
To populate database with random records (users, products and disciplines) use `python3 populate/populate_database.py `

Finally, to run server use `python3 manage.py runserver`

## Login

> <span style="background-color: lightgreen;border: 1px lightgreen;font-size: 13px;line-height: 19px;  overflow: auto;padding: 5px 5px;border-radius: 3px;">POST</span>  /api/login/

Endpoint returns user_id if provided data is valid otherwise returns empty dictionary.

| Required parameters |
| ------------------- |
| username            |
| password            |

| Returns |
| --------------|
| user_id or {} |


# API

## User

> <span style="background-color: lightgreen;border: 1px lightgreen;font-size: 13px;line-height: 19px;  overflow: auto;padding: 5px 5px;border-radius: 3px;">POST</span> </span>  /api/user/

Endpoint creates a new user if data is valid and returns user_id otherwise return empty dictionary.

| Required parameters |
| ------------------- |
| username            |
| password            |
| email            |

| Returns |
| --------------|
| user_id or {} |



  > <span style="background-color: YELLOW;
      border: 1px YELLOW;
      font-size: 13px;
      line-height: 19px;
      overflow: auto;
      padding: 5px 5px;
      border-radius: 3px;">PUT</span> /api/user/

This request updates user profile if provided data is valid and returns empty dictionary.

  | Required parameters |
  | ------------------- |
  | id            |


  | Optional parametrs |
  | ------------------- |
  | height           |
  | gender            |
  | daily_carbs |
   |daily_fat |
   |daily_proteins     |

  | Returns |
  | --------------|
  | {} |

  > <span style="background-color: #CC0000 ;
            border: 1px #CC0000   ;
            font-size: 13px;
            line-height: 19px;
            overflow: auto;
            padding: 5px 5px;
            border-radius: 3px;">DELETE</span> /api/user/

This request deletes user record if provided data is valid and returns empty dictionary.

| Required parameters |
| ------------------- |
| id            |
| password            |

| Returns |
| --------------|
| {} |

  > <span style="background-color: lightgreen;border: 1px lightgreen;font-size: 13px;line-height: 19px;  overflow: auto;padding: 5px 5px;border-radius: 3px;">POST</span> </span>  /api/profile/

Endpoint returns information about username if provided data is valid otherwise returns empty dictionary.

  | Required parameters |
  | ------------------- |
  | id            |

  | Returns |
  | --------------|
| { "username": username,<br>&nbsp;&nbsp;"height": height,<br>&nbsp;&nbsp;"gender": gender,<br>&nbsp;&nbsp;"daily_carbs": daily_carbs,<br>&nbsp;&nbsp;"daily_proteins": daily_proteins<br>&nbsp;&nbsp;"daily_fat": daily_fat } |

## Weight

  > <span style="background-color: lightblue;
  border: 1px lightblue;
  font-size: 13px;
  line-height: 19px;
  overflow: auto;
  padding: 5px 5px;
  border-radius: 3px;">GET</span> /api/weights/

Endpoint returns list of dictionares that contains data about previous user weights.

| Required parameters |
| ------------------- |
| user_id            |

| Returns |
| --------------|
| [{<br>&nbsp;&nbsp;&nbsp;&nbsp;"value": value,<br>&nbsp;&nbsp;&nbsp;&nbsp;"date": date <br>}] |

> <span style="background-color: lightblue;
border: 1px lightblue;
font-size: 13px;
line-height: 19px;
overflow: auto;
padding: 5px 5px;
border-radius: 3px;">GET</span> /api/weight/

Endpoint returns weight_id if provided data is valid otherwise returns empty dictionary.

| Required parameters |
| ------------------- |
| user_id            |
| date            |

| Returns |
| --------------|
| weight_id |

> <span style="background-color: lightgreen;border: 1px lightgreen;font-size: 13px;line-height: 19px;  overflow: auto;padding: 5px 5px;border-radius: 3px;">POST</span> /api/weight/

This request creates a new weight record if provided data is valid and returns weight_id otherwise returns empty dictionary.

| Required parameters |
| ------------------- |
| user_id            |
| date            |
| value            |

| Returns |
| --------------|
| weight_id |

> <span style="background-color: #CC0000 ;
            border: 1px #CC0000   ;
            font-size: 13px;
            line-height: 19px;
            overflow: auto;
            padding: 5px 5px;
            border-radius: 3px;">DELETE</span> /api/weight/

This request deletes weight record if provided data is valid and returns empty dictionary.

| Required parameters |
| ------------------- |
| id|

| Returns |
| --------------|
| {}|

## Diary

  > <span style="background-color: lightblue;
  border: 1px lightblue;
  font-size: 13px;
  line-height: 19px;
  overflow: auto;
  padding: 5px 5px;
  border-radius: 3px;">GET</span> /api/diary/

Endpoint returns dairy_id if provided data is valid otherwise returns empty dictionary.

| Required parameters |
| ------------------- |
| user_id            |
| date            |

| Returns |
| --------------|
| diary_id or {} |

  > <span style="background-color: lightgreen;border: 1px lightgreen;font-size: 13px;line-height: 19px;  overflow: auto;padding: 5px 5px;border-radius: 3px;">POST</span> /api/diary/

This request creates a new diary record if provided data is valid and returns diary_id otherwise 	returns empty dictionary.

| Required parameters |
| ------------------- |
| user_id            |
| date            |

| Returns |
| --------------|
| diary_id or {} |

## Meals

  > <span style="background-color: lightblue;
  border: 1px lightblue;
  font-size: 13px;
  line-height: 19px;
  overflow: auto;
  padding: 5px 5px;
  border-radius: 3px;">GET</span> /api/meal/

Endpoint returns information about meal if provided data is valid otherwise return empty dictionary.

  | Required parameters |
  | ------------------- |
  | id            |

  | Returns |
  | --------------|
  | {<br>&nbsp;&nbsp;&nbsp;&nbsp;"total_kcal": total_kcal,<br>&nbsp;&nbsp;&nbsp;&nbsp;"total_carbs": total_carbs,<br>&nbsp;&nbsp;&nbsp;&nbsp;"total_protein": total_protein,<br>&nbsp;&nbsp;&nbsp;&nbsp;"total_fat": total_fat,<br>&nbsp;&nbsp;&nbsp;&nbsp;"ingredients": [<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"ingredient_id": ingredient_id,<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"name": name,<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"amount": amount<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;]<br>} |


> <span style="background-color: lightgreen;border: 1px lightgreen;font-size: 13px;line-height: 19px;  overflow: auto;padding: 5px 5px;border-radius: 3px;">POST</span> /api/meal/

This request create a new meal record if provided data is valid and returns meal_id otherwise 	returns empty dictionary.

| Required parameters |
| ------------------- |
| meal_type_id            |

| Returns |
| --------------|
| meal_id or {} |

> <span style="background-color: YELLOW;
        border: 1px YELLOW;
        font-size: 13px;
        line-height: 19px;
        overflow: auto;
        padding: 5px 5px;
        border-radius: 3px;">PUT</span> /api/meal/

  This request updates meal record if provided data is valid and returns empty	dictionary.

  | Required parameters |
  | ------------------- |
  |id            |
  |total_kcal|
  |total_carbs|
  |total_proteins|
  |total_fat|

  | Returns |
  | --------------|
  | {'meal_id': id} |

> <span style="background-color: #CC0000 ;
            border: 1px #CC0000   ;
            font-size: 13px;
            line-height: 19px;
            overflow: auto;
            padding: 5px 5px;
            border-radius: 3px;">DELETE</span> /api/meal/

This request deletes meal record if provided data is valid and returns empty dictionary 	otherwise return empty dictionary.

| Required parameters |
| ------------------- |
| id            |

| Returns |
| --------------|
| {} |


## Meal type

> <span style="background-color: lightblue;
  border: 1px lightblue;
  font-size: 13px;
  line-height: 19px;
  overflow: auto;
  padding: 5px 5px;
  border-radius: 3px;">GET</span> /api/meal-types/

Endpoint returns list of dictionaries with information about meal types.

| Required parameters |
| ------------------- |
| diary_id            |

| Returns |
| --------------|
| [{ "meal_type_id": meal_type_id,<br>&nbsp;&nbsp;&nbsp;"name": name, <br>&nbsp;&nbsp;&nbsp;"total_kcal": meal\__total_kcal, <br>&nbsp;&nbsp;&nbsp;"total_carbs": meal\__total_carbs, <br>&nbsp;&nbsp;&nbsp;"total_protein": meal\__total_protein, <br>&nbsp;&nbsp;&nbsp;"total_fat": meal\__total_fat <br>&nbsp;&nbsp;&nbsp;"ingredients": [<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"ingredient_id": ingredient_id,<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"name": name,<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"amount": amount<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;]<br>}] |

> <span style="background-color: lightblue;
  border: 1px lightblue;
  font-size: 13px;
  line-height: 19px;
  overflow: auto;
  padding: 5px 5px;
  border-radius: 3px;">GET</span> /api/meal-type/

Endpoint returns information about meal type.

| Required parameters |
| ------------------- |
| id            |

| Returns |
| --------------|
| { "name": name, <br>&nbsp;&nbsp;&nbsp;"total_kcal": meal\__total_kcal, <br>&nbsp;&nbsp;&nbsp;"total_carbs": meal\__total_carbs, <br>&nbsp;&nbsp;&nbsp;"total_protein": meal\__total_protein, <br>&nbsp;&nbsp;&nbsp;"total_fat": meal\__total_fat <br>&nbsp;&nbsp;&nbsp;"ingredients": [<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"ingredient_id": ingredient_id,<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"name": name,<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"amount": amount<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;]<br>} |

> <span style="background-color: lightgreen;border: 1px lightgreen;font-size: 13px;line-height: 19px;  overflow: auto;padding: 5px 5px;border-radius: 3px;">POST</span> /api/meal-type/

This request creates a new meal type record if provided data is valid and returns meal_type_id
otherwise if given name exist returns its meal_type_id.

| Required parameters |
| ------------------- |
| diary_id |
| name            |

| Returns |
| --------------|
| meal_type_id |

> <span style="background-color: #CC0000 ;
            border: 1px #CC0000   ;
            font-size: 13px;
            line-height: 19px;
            overflow: auto;
            padding: 5px 5px;
            border-radius: 3px;">DELETE</span> /api/meal-type/

This request deletes meal type record if provided data is valid and returns empty dictionary otherwise return empty dictionary.

| Required parameters |
| ------------------- |
| id           |

| Returns |
| --------------|
| {} |

## Ingredients

> <span style="background-color: lightgreen;border: 1px lightgreen;font-size: 13px;line-height: 19px;  overflow: auto;padding: 5px 5px;border-radius: 3px;">POST</span> /api/ingredient/

This request creates a new ingredient record if provided data is valid and returns ingredient id.

| Required parameters |
| ------------------- |
| product_id            |
| meal_id            |
| amount            |

| Returns |
| --------------|
| ingredient_id or {} |

> <span style="background-color: #CC0000 ;
            border: 1px #CC0000   ;
            font-size: 13px;
            line-height: 19px;
            overflow: auto;
            padding: 5px 5px;
            border-radius: 3px;">DELETE</span> /api/ingredient/

This request deletes ingredient record if provided data is valid and return empty dictionary.

| Required parameters |
| ------------------- |
| id            |

| Returns |
| --------------|
| {} |

## Products

> <span style="background-color: lightblue;
  border: 1px lightblue;
  font-size: 13px;
  line-height: 19px;
  overflow: auto;
  padding: 5px 5px;
  border-radius: 3px;">GET</span> /api/products/

Endpoint returns a list of products that that have similar names to given data if provided data is valid otherwise return empty list.

| Required parameters |
| ------------------- |
| name            |

| Returns |
| --------------|
| [{ "product_id": product_id,<br>&nbsp;&nbsp;&nbsp;"name": name }] |

> <span style="background-color: lightblue;
  border: 1px lightblue;
  font-size: 13px;
  line-height: 19px;
  overflow: auto;
  padding: 5px 5px;
  border-radius: 3px;">GET</span> /api/product/

Endpoint returns a dictionary that contains product data if provided data is valid otherwise return empty dictionary.

| Required parameters |
| ------------------- |
| id            |

| Returns |
| --------------|
| { "name": name,<br>&nbsp;&nbsp;"kcal": kcal,<br>&nbsp;&nbsp;"carbs": carbs,<br>&nbsp;&nbsp;"proteins": proteins,<br>&nbsp;&nbsp;"fat": fat }  |

> <span style="background-color: lightgreen;border: 1px lightgreen;font-size: 13px;line-height: 19px;  overflow: auto;padding: 5px 5px;border-radius: 3px;">POST</span> /api/product/

This request creates a new product record if provided data is valid and returns product_id otherwise if data is missing or invalid return empty dictionary.

| Required parameters |
| ------------------- |
| name            |
| kcal            |
| carbs            |
| proteins            |
| fat            |

| Returns |
| --------------|
| product_id or {} |

## Activities

> <span style="background-color: lightblue;
  border: 1px lightblue;
  font-size: 13px;
  line-height: 19px;
  overflow: auto;
  padding: 5px 5px;
  border-radius: 3px;">GET</span> /api/activities/

Endpoint returns a list of dictionaries that contains information about activities if provided data is valid otherwise return empty list.

| Required parameters |
| ------------------- |
| diary_id           |

| Returns |
| --------------|
| [{ "name": discipline_\_name,<br>&nbsp;&nbsp;&nbsp;"calories_burn": discipline__calories_burn,<br>&nbsp;&nbsp;&nbsp;"time": time }] |

> <span style="background-color: lightgreen;border: 1px lightgreen;font-size: 13px;line-height: 19px;  overflow: auto;padding: 5px 5px;border-radius: 3px;">POST</span> /api/activity/

This request creates a new acitivity record or update existing one if provided data is valid and returns empty dictionary.

| Required parameters |
| ------------------- |
| diary_id            |
| discipline_id            |
| time            |

| Returns |
| --------------|
| {} |

> <span style="background-color: #CC0000 ;
            border: 1px #CC0000   ;
            font-size: 13px;
            line-height: 19px;
            overflow: auto;
            padding: 5px 5px;
            border-radius: 3px;">DELETE</span> /api/activity/

This request deletes activity record if provided data is valid and return empty dictionary.

| Required parameters |
| ------------------- |
| id            |

| Returns |
| --------------|
| {} |

## Disciplines

> <span style="background-color: lightblue;
  border: 1px lightblue;
  font-size: 13px;
  line-height: 19px;
  overflow: auto;
  padding: 5px 5px;
  border-radius: 3px;">GET</span> /api/disciplines/

Endpoint returns a list of disciplines that that have similar names to given data if provided data is valid otherwise return empty list.

| Required parameters |
| ------------------- |
| name            |

| Returns |
| --------------|
| [{ "discipline_id": discipline_id,<br>&nbsp;&nbsp;&nbsp;"name": name }] |

> <span style="background-color: lightblue;
  border: 1px lightblue;
  font-size: 13px;
  line-height: 19px;
  overflow: auto;
  padding: 5px 5px;
  border-radius: 3px;">GET</span> /api/discipline/

Endpoint returns a dictionary that contains discipline data if provided data is valid otherwise return empty dictionary.

| Required parameters |
| ------------------- |
| id            |

| Returns |
| --------------|
| { "name": name,<br>&nbsp;&nbsp;"calories_burn": calories_burn }  |
