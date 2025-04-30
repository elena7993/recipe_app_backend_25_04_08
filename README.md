# Recipe App

### User model

- [x] username
- [x] name
- [x] email
- [x] avatar

### Recipe model

- [x] user
- [x] title
- [x] description
- [x] imgs
- [x] video link
- [] like
- [] isLiked

### comment model

- [] user
- [] recipe
- [] payload
- [] rating

### like model

- [] user
- [] recipe


### API
<!-- - [] GET - seeUser -->
- [x] GET - me
- [x] POST - signup
- [x] POST - login
- [x] POST - logout
- [x] PUT - change pw
- [x] POST - editprofile
- [x] POST - delete user
- [x] POST - see user
- [] POST - github login
- [] POST - kakao login

### Recipe
- [x] GET - seeRecipe
- [x] GET - detailRecipe
- [x] POST - createRecipe
- [] PUT - editRecipe
- [] POST - deleteRecipe
- [] GET - isMine
- [] GET - isLiked

### Comment
- [] GET - seeComment
- [] POST - createComment
- [] PUT - editComment
- [] POST - deleteComment
- [] POST - isMine


<!-- {
"username": "test002",
"password": "test654321",
"name": "test"
} -->

<!-- {
"old_password": "test987654",
"new_password": "test654321"
} -->