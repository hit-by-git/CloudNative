```mermaid
classDiagram
    %% DATABASE MODELS (SQLModel)
    class UserBase {
        +String email
        +Boolean is_active
        +Boolean is_superuser
        +String full_name
    }
    class ItemBase {
        +String title
        +String description
    }

    class User {
        <<Database Model>>
        +UUID id
        +String hashed_password
        +List[Item] items
    }
    class Item {
        <<Database Model>>
        +UUID id
        +UUID owner_id
    }
    
    %% DATA TRANSFER OBJECTS (Schemas)
    class UserCreate {
        <<Schema>>
        +String password
    }
    class UserUpdate {
        <<Schema>>
        +String email
        +String password
    }
    class UserPublic {
        <<Schema>>
        +UUID id
    }
    
    class ItemCreate {
        <<Schema>>
    }
    class ItemUpdate {
        <<Schema>>
        +String title
        +String description
    }
    class ItemPublic {
        <<Schema>>
        +UUID id
        +UUID owner_id
    }

    class Token {
        <<Schema>>
        +String access_token
        +String token_type
    }

    %% API ROUTERS
    class AuthRouter {
        <<API Endpoint>>
        +login_access_token()
        +reset_password()
    }
    class UsersRouter {
        <<API Endpoint>>
        +create_user()
        +read_user_me()
        +update_user()
        +delete_user()
    }
    class ItemsRouter {
        <<API Endpoint>>
        +read_items()
        +create_item()
        +update_item()
        +delete_item()
    }

    %% INHERITANCE (Base Classes to Specific implementations)
    UserBase <|-- User
    UserBase <|-- UserCreate
    UserBase <|-- UserPublic
    UserBase <|-- UserUpdate
    
    ItemBase <|-- Item
    ItemBase <|-- ItemCreate
    ItemBase <|-- ItemPublic
    ItemBase <|-- ItemUpdate

    %% SEMANTIC RELATIONSHIPS (The Logic)
    User "1" *-- "many" Item : owns
    
    UsersRouter ..> UserCreate : consumes
    UsersRouter ..> UserUpdate : consumes
    UsersRouter ..> UserPublic : returns
    
    ItemsRouter ..> ItemCreate : consumes
    ItemsRouter ..> ItemUpdate : consumes
    ItemsRouter ..> ItemPublic : returns
    
    AuthRouter ..> Token : returns